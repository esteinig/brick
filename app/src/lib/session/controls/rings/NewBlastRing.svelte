<script lang="ts">
	import { type BlastRingSchema, BlastMethod, RingType } from "$lib/types";
	import { ToastType, handleEndpointErrorResponse, triggerToast } from "$lib/helpers";
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
        min_identity: 0,
        min_evalue: 0.000001
    }

    let loading: boolean = false

    function isNumberInRange(value: string | number): boolean {
        const num = typeof value === 'string' ? parseFloat(value) : value;
        return !isNaN(num) && num >= 0 && num <= 100;
    }

    function isNumberValid(value: string | number): boolean {
        const num = typeof value === 'string' ? parseFloat(value) : value;
        return !isNaN(num) && num >= 0;
    }

    let identityInputValidationClass: string = "";
    let alignmentInputValidationClass: string = "";
    let evalueInputValidationClass: string = "";

    $: identityInputValidationClass = isNumberInRange(ringConfig.min_identity) ? ringConfig.min_identity === 0 ? '' : 'input-success' : 'input-error';
    $: alignmentInputValidationClass = isNumberValid(ringConfig.min_alignment) ? ringConfig.min_alignment === 0 ? '' : 'input-success' : 'input-error';
    $: evalueInputValidationClass = isNumberValid(ringConfig.min_evalue) ? ringConfig.min_evalue === 0.000001 ? '' : 'input-success' : 'input-error';

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">BLAST Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">BLAST rings consist of segments representing the alignment of a genome
        against the selected reference.</p>
    
    {#if $ringReferenceStore}
        <form id="createBlastRingForm" action="?/createRing" method="POST" use:enhance={({ formData }) => {
            
            ringConfig.reference = $ringReferenceStore;

            formData.append('ring_config', JSON.stringify(ringConfig))
            formData.append('ring_type', RingType.BLAST)

            ringConfig = {
                reference: null,
                genome_id: "",
                blast_method: BlastMethod.BLASTN,
                min_alignment: 0,
                min_identity: 0,
                min_evalue:  0.000001
            }

            loading = true;
            startRequestState();
        
            return async ({ result }) => {
                await applyAction(result);

                loading = false;
                completeRequestState();
                    
                if (result.type === "success"){
                    addRing($page.form.result)
                    triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
                } else {
                    handleEndpointErrorResponse($page.form?.detail ?? `Error ${result.status}: an unknown error occurred`, toastStore)
                }
            };
        }}>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-4 my-3 items-center">
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
                            <select class="select text-xs" bind:value={ringConfig.genome_id} disabled={loading}>
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
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 gap-4 my-3 items-center">
                <label class="label text-xs">
                    <p class="opacity-40">Minimum identity (%)</p>
                    <input id="blastMinIdentity" class="input text-xs {identityInputValidationClass}" type="text" bind:value={ringConfig.min_identity} />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Minimum alignment length</p>
                    <input id="blastMinIdentity" class="input text-xs {alignmentInputValidationClass}" type="text" bind:value={ringConfig.min_alignment} />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Minimum e-value</p>
                    <input id="blastMinIdentity" class="input text-xs {evalueInputValidationClass}" type="text" bind:value={ringConfig.min_evalue} />
                </label>
            </div>
            

            <div class="flex justify-right mt-6">
                <button class="btn variant-outline-surface" type="submit" disabled={loading || !ringConfig.genome_id}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
            </div>
        </form>
    {/if}
</div>