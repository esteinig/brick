<script lang="ts">
	import { ReferenceRing } from "$lib/types";
	import { type SessionFile } from "$lib/types";
    import { addRing } from "$lib/stores/RingStore";

    export let selectedReference: SessionFile;
    
</script>

<div class="border border-gray-300 rounded-lg border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Reference Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        Reference rings are simple continuous segments representing the 
        reference genome against which other genomes or sequences are compared.
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Reference rings are usually shown on the inner track and can be omitted entirely.</p>
    
    {#if selectedReference}
        <div class="flex justify-right mt-4">
            <button class="btn variant-outline-surface" on:click={() => addRing(new ReferenceRing(-1, selectedReference.length))}>
                <div class="flex items-center align-center">
                    <span>Submit</span>
                </div>
            </button>
        </div>
    {/if}
</div>