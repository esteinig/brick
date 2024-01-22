 
<script lang="ts">
    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import DataControlPanel from "$lib/session/controls/panels/DataControlPanel.svelte";
	import RingControlPanel from "$lib/session/controls/panels/RingControlPanel.svelte";
    import PlotControlPanel from '$lib/session/controls/panels/PlotControlPanel.svelte';
	import PaletteControlPanel from './controls/panels/PaletteControlPanel.svelte';
	import AboutPanel from './controls/panels/AboutPanel.svelte';

    import { type TaskStatusResponse, TaskResultType, BlastRing, type ErrorResponse } from "$lib/types";
	import { ToastType, handleEndpointErrorResponse, triggerToast } from "$lib/helpers";
    import { completeRequestState } from '$lib/stores/RequestInProgressStore';
	import { uploadInProgress } from '$lib/stores/UploadInProgressStore';
	import { tabIndexStore } from '$lib/stores/TabIndexStore';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, deserialize } from "$app/forms";
	import type { ActionResult } from "@sveltejs/kit";
    import { addRing } from "$lib/stores/RingStore";
	import { goto } from "$app/navigation";

    const toastStore = getToastStore();

    interface RingRequestData {
        action: string,
        body: FormData
    }
    
    async function handleCreateRingAction(data: RingRequestData): Promise<void> {

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
            
        if (result.type === "success"){
            let ringResponse = result.data as TaskStatusResponse;

            if (ringResponse.result_type === TaskResultType.BLAST_RING){
                addRing(ringResponse.result as BlastRing)
                triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
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

</script>

<div class="h-full w-full p-2">
    
    <TabGroup>
        <Tab bind:group={$tabIndexStore} name="tab1" value={0}>
            <span>Data<span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab2" value={1} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Rings</span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab3" value={2} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Plot</span>
        </Tab>

        <Tab bind:group={$tabIndexStore} name="tab4" value={3} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-60">Palettes</span></span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab4" value={4} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-60">About</span></span>
        </Tab>


        <!-- Tab Panels --->
        <svelte:fragment slot="panel">
            {#if $tabIndexStore === 0}
                <DataControlPanel></DataControlPanel>
            {:else if $tabIndexStore === 1}
                <RingControlPanel on:createRingAction={(event) => handleCreateRingAction(event.detail)}></RingControlPanel>
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

