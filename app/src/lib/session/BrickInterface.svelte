 
<script lang="ts">
    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import DataControlPanel from "$lib/session/controls/panels/DataControlPanel.svelte";
	import RingControlPanel from "$lib/session/controls/panels/RingControlPanel.svelte";
    import PlotControlPanel from '$lib/session/controls/panels/PlotControlPanel.svelte';
	import PaletteControlPanel from './controls/panels/PaletteControlPanel.svelte';
	import AboutPanel from './controls/panels/AboutPanel.svelte';

    import { type TaskStatusResponse, TaskResultType, BlastRing, type ErrorResponse, LabelRing, AnnotationRing, ReferenceRing, Ring, type SessionFile, type Session, type ActionRequestData, type ActionRequestDataUpdate } from "$lib/types";
	import { ToastType, handleEndpointErrorResponse, triggerToast } from "$lib/helpers";
    import { completeRequestState } from '$lib/stores/RequestInProgressStore';
	import { tabIndexStore } from '$lib/stores/TabIndexStore';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, deserialize } from "$app/forms";
	import type { ActionResult } from "@sveltejs/kit";
    import { addRing, rings } from "$lib/stores/RingStore";
	import { goto } from "$app/navigation";

    import { addSessionFile, sessionFiles } from '$lib/stores/SessionFileStore';
	import { ringReferenceStore } from '$lib/stores/RingReferenceStore';
	import { completeDropzoneLoading } from '$lib/stores/FileDropzoneStateStore';

    const toastStore = getToastStore();
    
    const ringResultTypes: TaskResultType[] = [
        TaskResultType.REFERENCE_RING,
        TaskResultType.BLAST_RING,
        TaskResultType.LABEL_RING,
        TaskResultType.ANNOTATION_RING,
        TaskResultType.GENOMAD_RING,
    ]

    function handleRingActionResult(taskResultType: TaskResultType, ringResponse: TaskStatusResponse) {

        // Adding ring data with their explicit types
        if (taskResultType === TaskResultType.BLAST_RING){
            addRing(ringResponse.result as BlastRing)
        } else if (taskResultType === TaskResultType.REFERENCE_RING) {
            addRing(ringResponse.result as ReferenceRing)
        } else if (taskResultType === TaskResultType.ANNOTATION_RING) {
            addRing(ringResponse.result as AnnotationRing)
        } else if (taskResultType === TaskResultType.LABEL_RING) {
            addRing(ringResponse.result as LabelRing)
        } else if (taskResultType === TaskResultType.GENOMAD_RING) {
            addRing(ringResponse.result as LabelRing)
        }

        // Ring type specific warnings if no data was added
        if (ringResponse.result instanceof Ring && !ringResponse.result.data.length){
            let warningMessage = "Ring created, but no segments found";

            if (taskResultType === TaskResultType.ANNOTATION_RING) {
                warningMessage = "Ring created, but requested annotations not found"
            } else if (taskResultType === TaskResultType.LABEL_RING) {
                warningMessage = "Ring created, but requested labels not found"
            } else if (taskResultType === TaskResultType.BLAST_RING) {
                warningMessage = "Ring created, but comparison did not produce alignments"
            } 

            triggerToast(warningMessage, ToastType.WARNING, toastStore);
        } else {
            triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
        }
    }

    function handleSessionFileActionResult(taskResponse: TaskStatusResponse) {
        triggerToast("File uploaded sucessfully", ToastType.SUCCESS, toastStore);
        addSessionFile(taskResponse.result as SessionFile)
    }

    function handleSessionRehydrationActionResult(taskResponse: TaskStatusResponse) {
        triggerToast("Session re-hydrated sucessfully", ToastType.SUCCESS, toastStore);
        
        // Update the entire session data manually - would prefer invalidation
        // and running the reload function but there are issues for this kind of
        // visualiztion, for more details see comments in: /brick/+layout.svelte

        let hydratedSession: Session = taskResponse.result as Session;
        
        $sessionFiles = hydratedSession.files;
        $rings = hydratedSession.rings;
        $rings.length ? $ringReferenceStore = $rings[0].reference : $ringReferenceStore = null;
    }

    function handleActionResult(result: ActionResult) {

        if (result.type === "success"){
            let taskResponse = result.data as TaskStatusResponse;
            let taskResultType = taskResponse.result_type; // we expect ring creation actions

            if (ringResultTypes.includes(taskResultType)){
                handleRingActionResult(taskResultType, taskResponse)
            } else if (taskResultType === TaskResultType.SESSION_FILE) {
                handleSessionFileActionResult(taskResponse)
            } else if (taskResultType === TaskResultType.SESSION) {
                handleSessionRehydrationActionResult(taskResponse)
            } else {
                triggerToast("An unexpected task response type was returned :(", ToastType.ERROR, toastStore)
            }            
        } else if (result.type === 'failure') {
            let ringResponse = result.data as ErrorResponse;
            handleEndpointErrorResponse(ringResponse.detail ?? `Error ${result.status}: an unknown error occurred`, toastStore)
        } else if (result.type === 'error') {
            throw result.error
        } else {
            goto(result.location)
        }
    }

    function handleActionUpdateResult(result: ActionResult, updateVerbose: boolean, successMessage: string) {

        if (result.type === "success"){
            if (updateVerbose) triggerToast(successMessage, ToastType.SUCCESS, toastStore);         
        } else if (result.type === 'failure') {
            let updateResponse = result.data as ErrorResponse;
            handleEndpointErrorResponse(updateResponse.detail ?? `Error ${result.status}: an unknown error occurred`, toastStore)
        } else if (result.type === 'error') {
            throw result.error
        } else {
            goto(result.location)
        }
    }

    /**
     * Handler for ring construction action requests
     * @param data
     */
    async function handleCreateRingAction(data: ActionRequestData): Promise<void> {

        // Action request
		const response = await fetch(data.action, {
			method: 'POST',
			body: data.body,
            headers: {
                'x-sveltekit-action': 'true'
            }
		})

        // Results from the server action function must
        // be deserialized manually in this case
		const result: ActionResult = deserialize(
            await response.text()
        );


		await applyAction(result);

        completeRequestState();
        handleActionResult(result);
    }

    /**
     * Multipart form data body for upload request to Sveltekit and FastAPI servers
     * @param fromData
     * @param boundary 
     */
    async function generateFormDataBody(formData: FormData, boundary: string): Promise<Blob> {
        const parts: Uint8Array[] = [];

        async function appendFilePart(key: string, file: File): Promise<void> {
            parts.push(new TextEncoder().encode(`--${boundary}\r\n`));
            parts.push(new TextEncoder().encode(`Content-Disposition: form-data; name="${key}"; filename="${file.name}"\r\n`));
            parts.push(new TextEncoder().encode(`Content-Type: ${file.type || 'application/octet-stream'}\r\n\r\n`));

            const fileData = await file.arrayBuffer();
            parts.push(new Uint8Array(fileData));

            parts.push(new TextEncoder().encode('\r\n'));
        }

        for (const [key, value] of formData.entries()) {
            if (value instanceof File) {
                await appendFilePart(key, value);
            } else {
                parts.push(new TextEncoder().encode(`--${boundary}\r\n`));
                parts.push(new TextEncoder().encode(`Content-Disposition: form-data; name="${key}"\r\n\r\n`));
                parts.push(new TextEncoder().encode(value));
                parts.push(new TextEncoder().encode('\r\n'));
            }
        }

        // Add the closing boundary
        parts.push(new TextEncoder().encode(`--${boundary}--`));

        // Concatenate all parts into a single Uint8Array
        const body = new Uint8Array(parts.reduce((acc, part) => acc + part.length, 0));
        let offset = 0;
        parts.forEach(part => {
            body.set(part, offset);
            offset += part.length;
        });

        return new Blob([body], { type: `multipart/form-data; boundary=${boundary}` });
    }

    /**
     * Handler for form upload action requests
     * @param data
     */
    async function handleUploadFileAction(data: ActionRequestData, id: string) {
        const boundary = '--------------------------' + Date.now().toString(16);

        const response = await fetch(data.action, {
            method: 'POST',
            body: await generateFormDataBody(data.body, boundary),
            headers: {
                'x-sveltekit-action': 'true',
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
            },
        });

        // Results from the server action function must
        // be deserialized manually in this case
        const result: ActionResult = deserialize(await response.text());

        await applyAction(result);

        completeDropzoneLoading(id);
        handleActionResult(result);
    }

    /**
     * Handler for ring (style) updates
     * @param data
     */
     async function handleUpdateRingAction(data: ActionRequestDataUpdate) {
        
        if (data.updateDatabase) {
            const response = await fetch(data.action, {
                method: 'POST',
                body: data.body,
                headers: {
                    'x-sveltekit-action': 'true'
                }
            });

            // Results from the server action function must
            // be deserialized manually in this case
            const result: ActionResult = deserialize(await response.text());

            await applyAction(result);

            if (data.updateVerbose) completeRequestState();
            handleActionUpdateResult(result, data.updateVerbose, "Ring updated sucessfully");
        }
        
    }

    /**
     * Handler for ring deletion
     * @param data
     */
     async function handleDeleteRingAction(data: ActionRequestDataUpdate) {
        
        if (data.updateDatabase) {
            const response = await fetch(data.action, {
                method: 'POST',
                body: data.body,
                headers: {
                    'x-sveltekit-action': 'true'
                }
            });

            // Results from the server action function must
            // be deserialized manually in this case
            const result: ActionResult = deserialize(await response.text());

            await applyAction(result);

            if (data.updateVerbose) completeRequestState();
            handleActionUpdateResult(result, data.updateVerbose, "Ring deleted successfully");
        }
    }

    /**
     * Handler for file deletion
     * @param data
     */
     async function handleDeleteFileAction(data: ActionRequestDataUpdate) {
        
        if (data.updateDatabase) {
            const response = await fetch(data.action, {
                method: 'POST',
                body: data.body,
                headers: {
                    'x-sveltekit-action': 'true'
                }
            });

            // Results from the server action function must
            // be deserialized manually in this case
            const result: ActionResult = deserialize(await response.text());

            await applyAction(result);

            if (data.updateVerbose) completeRequestState();
            handleActionUpdateResult(result, data.updateVerbose, "File deleted successfully");
        }
    }

    let showEditRingMenu: boolean = false;
    let showNewRingMenu: boolean = false;

</script>

<div class="h-full w-full p-2">
    
    <TabGroup>
        <Tab bind:group={$tabIndexStore} name="tab1" value={0}>
            <span>Data<span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab2" value={1} on:click={() => { showEditRingMenu = false; showNewRingMenu = false }}>
            <span>Rings</span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab3" value={2}>
            <span>Plot</span>
        </Tab>

        <Tab bind:group={$tabIndexStore} name="tab4" value={3}>
            <span class="opacity-65">Palettes</span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab4" value={4}>
            <span class="opacity-65">About</span>
        </Tab>


        <!-- Tab Panels --->
        <svelte:fragment slot="panel">
            {#if $tabIndexStore === 0}
                <DataControlPanel 
                    on:fileUploadAction={(event) => handleUploadFileAction(event.detail.data, event.detail.id)}
                    on:fileDeleteAction={(event) => handleDeleteFileAction(event.detail.data)}
                ></DataControlPanel>
            {:else if $tabIndexStore === 1}
                <RingControlPanel 
                    bind:showNewRingMenu={showNewRingMenu}
                    bind:showEditRingMenu={showEditRingMenu}
                    on:createRingAction={(event) => handleCreateRingAction(event.detail)} 
                    on:updateRingAction={(event) => handleUpdateRingAction(event.detail)}
                    on:deleteRingAction={(event) => handleDeleteRingAction(event.detail)}
                    
                ></RingControlPanel>
            {:else if $tabIndexStore === 2}
                <PlotControlPanel></PlotControlPanel>
            {:else if $tabIndexStore === 3}
                <PaletteControlPanel></PaletteControlPanel>
            {:else if $tabIndexStore === 4}
                <AboutPanel />
            {/if}
        </svelte:fragment>
    </TabGroup>
</div>

