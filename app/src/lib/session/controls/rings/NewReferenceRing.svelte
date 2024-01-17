<script lang="ts">
	import { ReferenceRing } from "$lib/types";
    import { addRing } from "$lib/stores/RingStore";
    import { ringReferenceStore } from '$lib/stores/RingReferenceStore';
    
</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Reference Ring</p>
    <p class="opacity-20 mb-2 text-xs w-full">
        Reference rings are simple continuous segments representing the 
        reference genome against which other genomes or sequences are compared.
        Reference rings are usually shown on the inner track and can be omitted entirely.
    </p>
    <div class="flex justify-right mt-12">
        <button class="btn variant-outline-surface" type="button" on:click={() => addRing(new ReferenceRing($ringReferenceStore, -1, $ringReferenceStore.sequence.length))} disabled={!$ringReferenceStore}>
            <div class="flex items-center align-center">
                <span>Construct</span>
            </div>
        </button>
    </div>
</div>