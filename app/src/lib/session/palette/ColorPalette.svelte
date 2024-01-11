<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let colors: string[];
    export let title: string = "";
    export let subtitle: string = "";
    export let colorFields: number = 12;

    export let titleClass: string = "opacity-80 mb-2";
    export let subtitleClass: string = "opacity-80 ml-2 text-sm";
    export let displayValueClass: string = "opacity-40 ml-1 text-xs";

    let displayValue: string = "";


    const dispatch = createEventDispatcher();


    function colorClickHandler(color: string) {
        dispatch('selectColor', { color: color });
    }
</script>

<div id="colorPalette">
    <p class={titleClass}>{title} <span class={subtitleClass}>{subtitle}</span><span class={displayValueClass}>{displayValue}</span></p>
    <div class="grid grid-cols-12 gap-1">
        {#each colors as color}
            <div class="p-4 rounded shadow-lg" style="background-color: {color};" on:mouseover={() => displayValue = color} on:mouseout={() => displayValue = ""} on:click={() => colorClickHandler(color)}></div>
        {/each}
    </div>
</div>