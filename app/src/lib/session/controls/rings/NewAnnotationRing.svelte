<script lang="ts">
	import { RingType, type AnnotationRingSchema } from "$lib/types";
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

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Annotation Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Annotation rings consist of segments representing features along the 
        selected reference genome. Annotations can be extracted from Genbank or custom table files.</p>
    
    {#if selectedReference}
        <form id="createAnnotationRingForm" action="?/createRing" method="POST" use:enhance={({ formData }) => {
                    
            loading = true;
            formData.append('ring_config', JSON.stringify(ringConfig))
            formData.append('ring_type', RingType.ANNOTATION)

            // Clear data in this component
            ringConfig = {
                session_id: $page.params.session,
                genbank_id: null,
                tsv_id: null,
                genbank_features: [],
                genbank_qualifiers: []
            }
        
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
                <button class="btn variant-outline-surface" type="submit" disabled={loading || !(ringConfig.genbank_id || ringConfig.tsv_id)}>
                    <div class="flex items-center align-center">
                        <span>Create ring</span>
                    </div>
                </button>
                 
                {#if !sessionFileTypeAvailable(FileType.ANNOTATION_GENBANK) && !sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}
                    <div class="text-xs text-tertiary-500 ml-3">Please upload a reference annotation file</div>
                {/if}
            </div>
        </form>
    {/if}
</div>