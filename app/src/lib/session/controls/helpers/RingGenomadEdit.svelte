<script lang="ts">
	import { plotConfigStore } from "$lib/stores/PlotConfigStore";
	import { changeLineRingGenomadDisplay, changeLineRingSmoothing } from "$lib/stores/RingStore";
	import { GenomadRing } from "$lib/types";
	import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";

    export let ring: GenomadRing;

    let displayClass: number = 2;
    let lineSmoothingEnabled: boolean = ring.lineSmoothing ?? $plotConfigStore.rings.lineSmoothing;

    $: if (displayClass >= 0) {
        changeLineRingGenomadDisplay(ring.id, displayClass)
    }

</script>

<div class="grid grid-cols-1 gap-8">
    
    <div class="justify-center">
        <p class="text-xs opacity-60">Prediction class scores</p>
        <RadioGroup>
            <RadioItem bind:group={displayClass} name="justify" value={0}>Plasmid</RadioItem>
            <RadioItem bind:group={displayClass} name="justify" value={1}>Virus</RadioItem>
            <RadioItem bind:group={displayClass} name="justify" value={2}>Both</RadioItem>
        </RadioGroup>
    </div>    
    <div class="justify-center">
        <label class="text-sm flex mt-2">
            <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={lineSmoothingEnabled} on:change={() => changeLineRingSmoothing(ring.id, lineSmoothingEnabled)}>
            <div class="opacity-40 ml-2">Line smoothing</div>
        </label>
        <p class="text-xs opacity-20 mt-1">Apply natural curve smoothing function (front-end visualisation only)</p>
    </div>
</div>