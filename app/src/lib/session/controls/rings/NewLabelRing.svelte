<script lang="ts">
	import { RingType, type RingSegment, type LabelRingSchema, type PydanticValidationError } from "$lib/types";
	import { ToastType, triggerToast } from "$lib/helpers";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { addRing, isRingTypePresent } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
	import EditableRingSegment from "../helpers/EditableRingSegment.svelte";
    
    const toastStore = getToastStore();

    export let selectedReference: SessionFile;
    
    let ringConfig: LabelRingSchema = {
        session_id: $page.params.session,
        tsv_id: null,
        labels: []
    }

    let loading: boolean = false;

    let labelRingPresent: boolean = isRingTypePresent(RingType.LABEL);

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Label Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Label rings consist of text-annotations at the end of lines that point to the feature of interest. 
        Labels are always added to the outer ring and can be added manually or using custom annotation files. If start and end values in the annotation
        file are different, their midpoint is used to draw the annotation line.</p>
    
    {#if selectedReference}
        <form id="createLabelRingForm" action="?/createRing" method="POST" use:enhance={({ formData }) => {
            
            loading = true;
            formData.append('ring_config', JSON.stringify(ringConfig))
            formData.append('ring_type', RingType.LABEL)

            // Clear the data in this component
            ringConfig =  {
                session_id: $page.params.session,
                tsv_id: null,
                labels: []
            }

            return async ({ result }) => {
                await applyAction(result);
                loading = false;
                    
                if (result.type === "success"){
                    addRing($page.form.result)
                    if ($page.form.result.data.length) {
                        triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
                    } else {
                        triggerToast("Ring created, requested labels not found", ToastType.WARNING, toastStore);
                    }   
                } else {
                    // Validation errors from pydantic schemes are an array of validation objects:
                    if ($page.form.detail instanceof Array){
                        for (const error of $page.form.detail) {
                            triggerToast(
                                error.msg ?? `Error ${result.status}: an unknown error occurred`, 
                                ToastType.ERROR, 
                                toastStore
                            );
                        }
                    } else {
                        triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
                    }
                    
                }
            };
        }}>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 gap-4 my-3">
                
                <label class="label text-xs mt-3 lg:w-1/2">
                    <p class="opacity-40">Custom labels</p>
                    <select class="select text-xs" bind:value={ringConfig.tsv_id} disabled={!sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}>
                        {#each $sessionFiles as file}
                            {#if file.type === FileType.ANNOTATION_CUSTOM}
                                <option value={file.id}>{file.name_original}</option>
                            {/if}
                        {/each}
                    </select>
                </label>

                {#each ringConfig.labels as segment, idx}
                    <EditableRingSegment index={idx} bind:segment={segment} on:delete={() => {ringConfig.labels.splice(idx, 1); ringConfig.labels = ringConfig.labels}}></EditableRingSegment>
                {/each}

            </div>
            
            

            <div class="mt-12">
                <button class="btn variant-outline-surface mr-2" type="submit" disabled={loading || !(ringConfig.tsv_id || ringConfig.labels.length)}>
                    <div class="flex items-center align-center">
                        {#if labelRingPresent}
                            <span>Add to ring</span>
                        {:else}                            
                            <span>Create ring</span>
                        {/if}
                        
                    </div>
                </button>
                <button class="btn variant-outline-surface" type="button" disabled={loading} on:click={() => ringConfig.labels = [...ringConfig.labels, { start: 0, end: 0, text: "", color: "#d3d3d3"}]}>
                    <div class="flex items-center align-center">
                        <span>New label</span>
                    </div>
                </button>
            </div>
            
        </form>
    {/if}
</div>