<script lang="ts">

    import RingLabelNew from "../helpers/RingLabelNew.svelte";

    import { startRequestState } from '$lib/stores/RequestInProgressStore';
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
	import { RingType, type LabelRingSchema } from "$lib/types";
    import { createEventDispatcher } from "svelte";
    import { FileType } from "$lib/types";
    
    const dispatch = createEventDispatcher();
    
    let ringConfig: LabelRingSchema = {
        reference: null,
        tsv_id: null,
        labels: []
    }

    async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData()

        ringConfig.reference = $ringReferenceStore;

        data.append('ring_config', JSON.stringify(ringConfig))
        data.append('ring_type', RingType.LABEL)

        ringConfig =  {
            reference: null,
            tsv_id: null,
            labels: []
        }

        startRequestState();

        dispatch('submitAction', { action: event.currentTarget.action, body: data });

	}

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Label Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 text-xs w-full">Label rings consist of text-annotations at the end of lines that point to the feature of interest. 
        Labels are always added to the outer ring and can be added manually or using custom annotation files. If start and end values in the annotation
        file are different, their midpoint is used to draw the annotation line.</p>
    
    {#if $ringReferenceStore}
        <form id="createLabelRingForm" action="?/createRing" method="POST" on:submit|preventDefault={handleSubmit}>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 gap-4 mt-3">
                
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
                    <RingLabelNew index={idx} bind:segment={segment} on:delete={() => {ringConfig.labels.splice(idx, 1); ringConfig.labels = ringConfig.labels}}></RingLabelNew>
                {/each}

            </div>
            
            <div class="mt-6">
                <button class="btn variant-outline-surface mr-2" type="submit" disabled={!(ringConfig.tsv_id || ringConfig.labels.length)}>
                    <div class="flex items-center align-center">    
                        <span>Construct</span>
                    </div>
                </button>
                <button class="btn variant-outline-surface" type="button" on:click={() => ringConfig.labels = [...ringConfig.labels, { start: 0, end: 0, text: ""}]}>
                    <div class="flex items-center align-center">
                        <span>New label</span>
                    </div>
                </button>
            </div>
            
        </form>
    {/if}
</div>