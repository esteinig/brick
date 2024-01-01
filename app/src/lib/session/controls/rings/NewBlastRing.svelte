<script lang="ts">
	import { type BlastRingSchema, BlastMethod } from "$lib/types";
	import { ToastType, triggerToast } from "$lib/helpers";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { addRing } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
    
    const toastStore = getToastStore();

    export let selectedReference: SessionFile;
    
    let ringConfig: BlastRingSchema = {
        session_id: $page.params.session,
        reference_id: selectedReference.id,
        genome_id: "",
        blast_method: BlastMethod.BLASTN,
        min_alignment: 0,
        min_identity: 0
    }

    let loading: boolean = false;


</script>

<div class="border border-gray-300 rounded-lg border-opacity-10 p-4">
    <p class="opacity-60 mb-2">BLAST Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">BLAST rings consist of segments representing the alignment of a genome
        against the selected reference. Computation of alignments may take a second depending on server load</p>
    
    {#if selectedReference}
    <form id="createBlastRingForm" action="?/createBlastRing" method="POST" use:enhance={({ formData }) => {
                
        loading = true;
        formData.append('ring_config', JSON.stringify(ringConfig))
    
        return async ({ result }) => {
            await applyAction(result);
            loading = false;
                
            if (result.type === "success"){
                addRing($page.form.result)
                triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
            } else {
                triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
            }
        };
    }}>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3 items-center">
            <div>
                <label class="label text-xs">
                    <p class="opacity-40">Reference</p>
                    <input id="blastReferenceFileName" class="input text-xs" disabled value={selectedReference.name_original}/>
                </label>
            </div>
            <div>
                {#if sessionFileTypeAvailable(FileType.GENOME)}
                    <label class="label text-xs">
                        <p class="opacity-40">Genome for comparison</p>
                        <select class="select text-xs" bind:value={ringConfig.genome_id}>
                            {#each $sessionFiles as file}
                                {#if file.type === FileType.GENOME}
                                    <option value={file.id}>{file.name_original}</option>
                                {/if}
                            {/each}
                        </select>
                    </label>
                {:else}
                    <div class="text-xs text-error-500 text-center">Please upload a genome file in the data panel</div>
                {/if}
            </div>
        </div>
        
        {#if ringConfig.genome_id}

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