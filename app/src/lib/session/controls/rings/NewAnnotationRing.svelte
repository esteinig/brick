<script lang="ts">
	import { type AnnotationRingSchema } from "$lib/types";
	import { ToastType, triggerToast } from "$lib/helpers";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { addRing } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
    
    const toastStore = getToastStore();

    export let selectedReference: SessionFile;
    
    let ringConfig: AnnotationRingSchema = {
        session_id: $page.params.session,
        genbank_id: null,
        tsv_id: null,
        genbank_features: [],
        genbank_qualifiers: []
    }

    let loading: boolean = false;
    let selectedGenbankFile: SessionFile;
    
    $: ringConfig.genbank_id = selectedGenbankFile?.id ?? null; // bit of fuckery due to listing of selections below

</script>

<div class="border border-gray-300 rounded-lg border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Annotation Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Annotation rings consist of segments representing features along the 
        selected reference genome. Annotations can be extracted from Genbank or custom table files.</p>
    
    {#if selectedReference}
        <form id="createAnnotationRingForm" action="?/createAnnotationRing" method="POST" use:enhance={({ formData }) => {
                    
            loading = true;
            formData.append('ring_config', JSON.stringify(ringConfig))
        
            return async ({ result }) => {
                await applyAction(result);
                loading = false;
                    
                if (result.type === "success"){
                    addRing($page.form.result)
                    if ($page.form.result.data.length) {
                        triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
                    } else {
                        triggerToast("Ring created, requested annotations not found", ToastType.WARNING, toastStore);
                    }
                    
                } else {
                    triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
                }
            };
        }}>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3">
                
                {#if sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK)}
                    <div>
                        <label class="label text-xs">
                            <p class="opacity-40">Genbank annotations</p>
                            <select class="select text-xs" bind:value={selectedGenbankFile}>
                                {#each $sessionFiles as file}
                                    {#if file.type === FileType.ANNOTATION_GENBANK}
                                        <option value={file}>{file.name_original}</option>
                                    {/if}
                                {/each}
                            </select>
                        </label>
                         {#if sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}
                            <label class="label text-xs mt-3">
                                <p class="opacity-40">Custom annotations</p>
                                <select class="select text-xs" bind:value={ringConfig.tsv_id}>
                                    {#each $sessionFiles as file}
                                        {#if file.type === FileType.ANNOTATION_CUSTOM}
                                            <option value={file.id}>{file.name_original}</option>
                                        {/if}
                                    {/each}
                                </select>
                            </label>
                        {/if}
                    </div>
                {/if}

                {#if ringConfig.genbank_id}
                    <div>
                        <label class="label text-xs">
                            <p class="opacity-40">Genbank features</p>
                            <select class="select text-xs" bind:value={ringConfig.genbank_features} multiple>
                                {#if selectedGenbankFile}
                                    {#each selectedGenbankFile.selections.features.sort() as feature}
                                        <option value={feature}>{feature}</option>
                                    {/each}
                                {/if}
                            </select>
                        </label>
                    </div>
                {/if}

                {#if !sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK) && !sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}
                    <div class="text-xs text-error-500 text-center">Please upload a reference annotation file</div>
                {/if}
            </div>
            
            {#if ringConfig.genbank_id || ringConfig.tsv_id}

                <div class="flex justify-right mt-4">
                    <button class="btn variant-outline-surface" type="submit">
                        <div class="flex items-center align-center">
                            <span>Compute</span>
                        </div>
                    </button>
                </div>
            {/if}
        </form>
    {/if}
</div>