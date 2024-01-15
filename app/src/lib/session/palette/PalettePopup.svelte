<script lang="ts">
    import { popup, type PopupSettings } from "@skeletonlabs/skeleton";
    import { paletteStore } from "$lib/stores/PaletteStore";
	import ColorPalette from "./ColorPalette.svelte";
    import { createEventDispatcher, tick } from 'svelte';

    const dispatch = createEventDispatcher();

    function selectColor(event: any) {
        color = event.detail.color
        dispatch('selectColor', { color: event.detail.color });
    }
    
    export let id: string = "";
    export let color: string = "#d3d3d3";

    const popupPalette: PopupSettings = {
        // Represents the type of event that opens/closed the popup
        event: 'click',
        // Matches the data-popup value on your popup element
        target: `popupPalette-${id}`,
        // Defines which side of your trigger the popup will appear
        placement: 'left',
        closeQuery: '#will-close'
    };


</script>

<div class="palettePopup-{id}">
    <button class="btn btn-icon h-4 w-4" style="color: {color};" use:popup={popupPalette}>
        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
    </button>

    <div class="card p-4 shadow-xl border border-opacity-80 border-surface-500 bg-surface-300 z-50" data-popup={`popupPalette-${id}`}>
        <div class="head mb-4 flex justify-between items-center align-mddle">
            <p class="opacity-80">Palette selections</p>
            
		    <button id="will-close" class="btn">
                <svg class="w-6 h-6" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
            </button>

        </div>
        <div class="body">
            {#each $paletteStore as palette}
                <div class="my-4">
                    <ColorPalette colors={palette.colors} title={palette.name} on:selectColor={selectColor}/>
                </div>
            {/each}
        </div>
    </div>
</div>