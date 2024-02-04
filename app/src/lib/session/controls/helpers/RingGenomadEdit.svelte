<script lang="ts">
	import { plotConfigStore } from "$lib/stores/PlotConfigStore";
	import { changeLineRingSmoothing } from "$lib/stores/RingStore";
	import { GenomadRing } from "$lib/types";
	import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";


    export let ring: GenomadRing;

    let genomadPredictionClasses: number = 2;

    let checked: boolean = ring.lineSmoothing ?? $plotConfigStore.rings.lineSmoothing;


</script>

<div class="grid grid-cols-3 gap-8">
    
    <div>
        <p class="text-xs opacity-60">Prediction class scores</p>
        <RadioGroup>
            <RadioItem bind:group={genomadPredictionClasses} name="justify" value={0}>Plasmid</RadioItem>
            <RadioItem bind:group={genomadPredictionClasses} name="justify" value={1}>Virus</RadioItem>
            <RadioItem bind:group={genomadPredictionClasses} name="justify" value={2}>Both</RadioItem>
        </RadioGroup>
    </div>    
    <div>
        <label class="text-sm flex mt-2">
            <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={checked} on:change={() => changeLineRingSmoothing(ring.id, checked)}>
            <div class="opacity-40 ml-2">Line smoothing</div>
        </label>
        <p class="text-xs opacity-20 mt-1">Apply natural curve smoothing function - applied to front-end visualisation only</p>
    </div>
</div>