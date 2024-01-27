<script lang="ts">
	import { type ReferenceRingSchema, RingType } from "$lib/types";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
    import { startRequestState } from '$lib/stores/RequestInProgressStore';
    import { createEventDispatcher } from "svelte";
    
    const dispatch = createEventDispatcher();
    
    let ringConfig: ReferenceRingSchema = {
        reference: null
    }
 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData()

        ringConfig.reference = $ringReferenceStore;

        data.append('ring_config', JSON.stringify(ringConfig))
        data.append('ring_type', RingType.REFERENCE)

        ringConfig = { reference: null }

        startRequestState();

        dispatch('submitAction', { action: event.currentTarget.action, body: data});

	}

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Reference Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">
        Reference rings are simple continuous segments representing the reference genome against which other sequences are compared.
        Reference rings are usually shown on the inner track and can be omitted entirely.
    </p>
    
    {#if $ringReferenceStore}
        <form id="createReferenceRingForm" action="?/createRing" method="POST" on:submit|preventDefault={handleSubmit}>
            
            <div class="flex justify-right mt-4">
                <button class="btn variant-outline-surface" type="submit" disabled={!$ringReferenceStore}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
            </div>
        </form>
    {/if}
</div>