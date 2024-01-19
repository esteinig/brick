<script lang="ts">
	import { type BlastRingSchema, BlastMethod, RingType } from "$lib/types";
	import { ToastType, triggerToast } from "$lib/helpers";
	import { FileType } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable, getSessionFileById } from "$lib/stores/SessionFileStore";
    import { addRing } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";

    import { startRequestState, completeRequestState } from '$lib/stores/RequestInProgressStore';
    
    const toastStore = getToastStore();
    
    let ringConfig: BlastRingSchema = {
        reference: null,
        genome_id: "",
        blast_method: BlastMethod.BLASTN,
        min_alignment: 0,
        min_identity: 0
    }

    let loading: boolean = false

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">BLAST Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">BLAST rings consist of segments representing the alignment of a genome
        against the selected reference.</p>
    
    {#if $ringReferenceStore}
        <form id="createBlastRingForm" action="?/createRing" method="POST" use:enhance={({ formData }) => {
            
            // Important to do here, otherwise not set
            // correctly on re-hydration because the
            // selection of the reference is not done
            ringConfig.reference = $ringReferenceStore;

            loading = true;
            formData.append('ring_config', JSON.stringify(ringConfig))
            formData.append('ring_type', RingType.BLAST)


            // Reset data for the component
            ringConfig = {
                reference: $ringReferenceStore,
                genome_id: "",
                blast_method: BlastMethod.BLASTN,
                min_alignment: 0,
                min_identity: 0
            }


            // Tracks the common request state from multiple components 
            startRequestState();
        
            return async ({ result }) => {
                await applyAction(result);
                loading = false;
                completeRequestState();
                    
                if (result.type === "success"){
                    // invalidate("app:session")
                    addRing($page.form.result)
                    triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
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
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3 items-center">
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Reference</p>
                        <input id="blastReferenceFileName" class="input text-xs" disabled value={getSessionFileById($ringReferenceStore.reference_id)?.name_original}/>
                    </label>
                </div>
                <div>
                    {#if sessionFileTypeAvailable(FileType.GENOME)}
                        <label class="label text-xs">
                            <p class="opacity-40">Comparison</p>
                            <select class="select text-xs" bind:value={ringConfig.genome_id}>
                                {#each $sessionFiles as file}
                                    {#if file.type === FileType.GENOME}
                                        <option value={file.id}>{file.name_original}</option>
                                    {/if}
                                {/each}
                            </select>
                        </label>
                    {:else}
                        <div class="text-xs text-tertiary-500 text-center mt-4">Please upload a genome sequence file</div>
                    {/if}
                </div>
            </div>
            

            <div class="flex justify-right mt-12">
                <button class="btn variant-outline-surface" type="submit" disabled={loading || !ringConfig.genome_id}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
            </div>
        </form>
    {/if}
</div>