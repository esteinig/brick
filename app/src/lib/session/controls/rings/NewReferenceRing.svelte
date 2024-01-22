<script lang="ts">
	import { type ReferenceRingSchema, RingType } from "$lib/types";
	import { ToastType, handleEndpointErrorResponse, triggerToast } from "$lib/helpers";
    import { addRing } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
    import { startRequestState, completeRequestState } from '$lib/stores/RequestInProgressStore';
    
    const toastStore = getToastStore();
    
    let ringConfig: ReferenceRingSchema = {
        reference: null
    }

    let loading: boolean = false

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Reference Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">
        Reference rings are simple continuous segments representing the 
        reference genome against which other sequences are compared.
        Reference rings are usually shown on the inner track and can be omitted entirely.
    </p>
    
    {#if $ringReferenceStore}
        <form id="createBlastRingForm" action="?/createRing" method="POST" use:enhance={({ formData }) => {
            
            ringConfig.reference = $ringReferenceStore;

            formData.append('ring_config', JSON.stringify(ringConfig))
            formData.append('ring_type', RingType.REFERENCE)

            ringConfig = { reference: null }
            
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
            
            <div class="flex justify-right mt-4">
                <button class="btn variant-outline-surface" type="submit"  disabled={loading || !$ringReferenceStore}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
            </div>
        </form>
    {/if}
</div>