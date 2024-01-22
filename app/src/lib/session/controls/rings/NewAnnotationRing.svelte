<script lang="ts">
	import { RingType, type AnnotationRingSchema } from "$lib/types";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
    import { startRequestState } from '$lib/stores/RequestInProgressStore';
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    
    let ringConfig: AnnotationRingSchema = {
        reference: null,
        genbank_id: null,
        tsv_id: null,
        genbank_features: [],
        genbank_qualifiers: []
    }

    let selectedGenbankFile: SessionFile;
    
    $: ringConfig.genbank_id = selectedGenbankFile?.id ?? null; // bit of fuckery due to listing of selections below
    
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData()

        ringConfig.reference = $ringReferenceStore

        data.append('ring_config', JSON.stringify(ringConfig))
        data.append('ring_type', RingType.ANNOTATION)

        ringConfig = {
            reference: null,
            genbank_id: null,
            tsv_id: null,
            genbank_features: [],
            genbank_qualifiers: []
        }

        startRequestState();

        dispatch('submitAction', { action: event.currentTarget.action, body: data });

	}
    
</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Annotation Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Annotation rings consist of segments representing features along the 
        selected reference genome. Annotations can be extracted from Genbank or custom table files.</p>
    
    {#if $ringReferenceStore}
        <form id="createAnnotationRingForm" action="?/createRing" method="POST" on:submit|preventDefault={handleSubmit}>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3">
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Genbank annotations</p>
                        <select class="select text-xs" bind:value={selectedGenbankFile} disabled={!sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK)}>
                            {#each $sessionFiles as file}
                                {#if file.type === FileType.ANNOTATION_GENBANK}
                                    <option value={file}>{file.name_original}</option>
                                {/if}
                            {/each}
                        </select>
                    </label>
                </div>
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Genbank features</p>
                        <select class="select text-xs" multiple bind:value={ringConfig.genbank_features} disabled={!sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK)}>
                            {#if selectedGenbankFile}
                                {#each selectedGenbankFile.selections.features.sort() as feature}
                                    <option value={feature}>{feature}</option>
                                {/each}
                            {/if}
                        </select>
                    </label>
                </div>
                <div>
                    <label class="label text-xs mt-3">
                        <p class="opacity-40">Custom annotations</p>
                        <select class="select text-xs " bind:value={ringConfig.tsv_id} disabled={!sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}>
                            {#each $sessionFiles as file}
                                {#if file.type === FileType.ANNOTATION_CUSTOM}
                                    <option value={file.id}>{file.name_original}</option>
                                {/if}
                            {/each}
                        </select>
                    </label>

                </div>
            </div>
            
            <div class="flex items-center mt-12">
                <button class="btn variant-outline-surface" type="submit" disabled={!(ringConfig.genbank_id || ringConfig.tsv_id)}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
                 
                {#if !sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK) && !sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}
                    <div class="text-xs text-tertiary-500 ml-3">Please upload a reference annotation file</div>
                {/if}
            </div>
        </form>
    {/if}
</div>