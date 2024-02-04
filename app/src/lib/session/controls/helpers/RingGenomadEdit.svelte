<script lang="ts">
	import { plotConfigStore } from "$lib/stores/PlotConfigStore";
	import { changeLineRingSmoothing } from "$lib/stores/RingStore";
	import { GenomadPredictionClass, GenomadRing } from "$lib/types";


    export let ring: GenomadRing;

    let genomadPredictionClasses: GenomadPredictionClass[] = [
        GenomadPredictionClass.PLASMID, GenomadPredictionClass.VIRUS
    ]

    let checked: boolean = ring.lineSmoothing ?? $plotConfigStore.rings.lineSmoothing;

</script>

<div class="grid grid-cols-3 gap-4">
    <div>
        <p class="text-xs opacity-60 mb-2">Select prediction class scores to display</p>
        <select class="select text-xs" multiple bind:value={genomadPredictionClasses}>
            <option value={GenomadPredictionClass.VIRUS}>Viral (Phage)</option>
            <option value={GenomadPredictionClass.PLASMID}>Plasmid (HGT)</option>
        </select>
    </div>    
    <div>
        <label class="text-sm flex mt-6">
            <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={checked} on:change={() => changeLineRingSmoothing(ring.id, checked)}>
            <div class="opacity-40 ml-2">Line smoothing</div>
        </label>
        <p class="text-xs opacity-20 mt-2">Apply natural curve smoothing function - applied to front-end visualisation only</p>
    </div>
</div>