<script lang="ts">
	import { BlastRing, Ring } from "$lib/types";
	import { addNewRing } from "./helpers";
	import { FileType, type SessionFile } from "./types";

    export let rings: Ring[];
    export let sessionFiles: SessionFile[];
    export let selectedReference: SessionFile;
    
    let selectedGenome: SessionFile

    async function getBlastRing() {



        rings = addNewRing(rings, new BlastRing(-1));
    }

</script>

<div class="border border-gray-300 rounded-lg border-opacity-10 p-4">
    <p class="opacity-60 mb-2">BLAST Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">BLAST rings consist of segments representing the alignment of a genome
        against the selected reference. Computation of alignments may take a second depending on server load</p>
    
    {#if selectedReference}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3">
            <div>
                <label class="label text-xs">
                    <p class="opacity-40">Reference</p>
                    <input class="input text-xs" disabled value={selectedReference.name_original}/>
                </label>
            </div>
            <div>
                <label class="label text-xs">
                    <p class="opacity-40">Select a genome for alignment</p>
                    <select class="select text-xs" bind:value={selectedGenome}>
                        {#each sessionFiles as file}
                            {#if file.type === FileType.GENOME}
                                <option value={file}>{file.name_original}</option>
                            {/if}
                        {/each}
                    </select>
                </label>
            </div>
        </div>
        
        {#if selectedGenome}
            <div class="flex justify-right mt-4">
                <button class="btn variant-outline-surface" on:click={getBlastRing}>
                    <div class="flex items-center align-center">
                        <span>Submit</span>
                    </div>
                </button>
            </div>
        {/if}
    {/if}
</div>