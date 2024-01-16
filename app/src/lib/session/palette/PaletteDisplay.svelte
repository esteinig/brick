<script lang="ts">
    import ColorPalette from "$lib/session/palette/ColorPalette.svelte";
	import { paletteStore, type Palette as PaletteStorePalette } from "$lib/stores/PaletteStore";
	import { AccordionItem } from "@skeletonlabs/skeleton";
	import type { PaletteItem } from "$lib/types";

    export let palette: PaletteItem;

    function handlePaletteClick(colors: string[], name: string) {
        
        let paletteInStore: boolean = $paletteStore.some(p => p.name === name);

        if (paletteInStore){
            paletteStore.removePalette(name)
        } else {
            const samplePalette: PaletteStorePalette = {
                name: name,
                colors: colors
            };
            paletteStore.addPalette(samplePalette);
        }
    }


</script>


<AccordionItem>
    <svelte:fragment slot="lead"> <a href="{palette.link}"  target="_blank" rel="noreferrer">
        <svg class="h-4 w-4" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
    </a></svelte:fragment>
    <svelte:fragment slot="summary">
        <p class="opacity-80 text-lg">{palette.name}<span class="opacity-60 text-base ml-1.5">by {palette.author}</span></p>

    </svelte:fragment>
    <svelte:fragment slot="content">
        <div class="my-6">
            {#each palette.palettes as subpalette, i }
                <div role="button" tabindex="{i}" class="flex items-center justify-between my-4 rounded-token hover:variant-soft hover:cursor-pointer p-4"  on:click={() => handlePaletteClick(subpalette.colors, subpalette.name)} on:keydown={() => handlePaletteClick(subpalette.colors, subpalette.name) }>   
                   
                    <ColorPalette title={subpalette.name} subtitle={subpalette.subtitle} colors={subpalette.colors} subtitleClass="opacity-80 ml-2 text-sm truncate"></ColorPalette>
                    
                    {#if $paletteStore.some(p => p.name === subpalette.name)}
                        <div class="h-7 w-7 text-secondary-500">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor"   viewBox="0 0 46.991 46.99"   xmlns="http://www.w3.org/2000/svg">
                                <!-- viewBox="0 0 24 24" <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path> -->
                                <path d="M22.082,2.61c-3.74,0-7.598,0.592-11.465,1.76C9.503,4.706,6.115,5.73,4.877,9.082c-1.222,3.312,0.536,6.051,1.819,8.052   c0.732,1.142,1.563,2.436,1.563,3.337c0,1.522-2.301,4.68-3.824,6.77c-2.771,3.804-5.914,8.113-3.672,12.523   c2.081,4.092,7.132,4.615,11.299,4.615c18.282,0,34.928-11.048,34.928-23.179C46.99,12.261,37.469,2.61,22.082,2.61z M16.5,34.109   c-0.027,2.194-1.809,3.967-4.01,3.967c-2.217,0-4.014-1.798-4.014-4.015c0-2.219,1.797-4.017,4.014-4.017   c0.682,0,1.314,0.188,1.877,0.486c1.266,0.675,2.137,1.991,2.137,3.526C16.503,34.078,16.5,34.095,16.5,34.109z M17.01,15.082   c-0.848-0.736-1.395-1.809-1.395-3.02c0-2.218,1.798-4.015,4.015-4.015c2.218,0,4.015,1.797,4.015,4.015   c0,0.205-0.031,0.401-0.061,0.599c-0.291,1.931-1.941,3.416-3.954,3.416C18.623,16.077,17.715,15.693,17.01,15.082z M24.63,35.076   c-1.424,0-2.668-0.746-3.381-1.864c-0.396-0.623-0.635-1.357-0.635-2.15c0-2.217,1.799-4.015,4.018-4.015   c1.975,0,3.607,1.431,3.941,3.31c0.041,0.23,0.07,0.466,0.07,0.705C28.644,33.278,26.849,35.076,24.63,35.076z M27.486,13.244   c-0.021-0.171-0.052-0.339-0.052-0.516c0-1.855,1.265-3.401,2.975-3.861c0.333-0.09,0.678-0.153,1.04-0.153   c1.575,0,2.925,0.916,3.582,2.237c0.27,0.538,0.432,1.136,0.432,1.777c0,1.387-0.701,2.609-1.771,3.33   c-0.641,0.433-1.412,0.685-2.242,0.685C29.408,16.743,27.742,15.215,27.486,13.244z M33.74,28.743   c-0.676,0-1.305-0.184-1.863-0.479c-1.271-0.675-2.148-1.996-2.148-3.535c0-2.218,1.797-4.017,4.014-4.017   c1.258,0,2.366,0.59,3.104,1.494c0.562,0.69,0.914,1.562,0.914,2.521C37.755,26.945,35.958,28.743,33.74,28.743z"/>
                                
                            </svg>
                        </div>
                    {/if}
                </div>

               
            {/each}
        </div>
    </svelte:fragment>
</AccordionItem>