<script lang="ts">
	import { Accordion } from "@skeletonlabs/skeleton";
    import { type PaletteItem, PaletteName } from '$lib/types';
    import { NZ_PALETTES, MOMA_PALETTES, NATIONAL_PARK_PALETTES } from "$lib/data";

    import PaletteDisplay from '$lib/session/palette/PaletteDisplay.svelte';

    let paletteItems: PaletteItem[] = [
        { 
            name: PaletteName.NP,
            link: "https://github.com/kevinsblake/NatParksPalettes/",
            palettes: NATIONAL_PARK_PALETTES,
            author: " Kevin S. Blake"
        },
        { 
            name: PaletteName.MOMA,
            link: "https://github.com/BlakeRMills/MoMAColors",
            palettes: MOMA_PALETTES,
            author: "Blake R. Mills"
        },{
            name: PaletteName.NZ,
            link: "https://g-thomson.github.io/Manu/",
            palettes: NZ_PALETTES,
            author:  "George Thompson"
        },
    ]

</script>

<div class="">
    <div class="opacity-60 my-8 flex items-center">
        Select any number of palettes for ring color selections
    </div>
    <Accordion>
        {#each paletteItems as paletteItem}
            <PaletteDisplay palette={paletteItem}></PaletteDisplay>
        {/each}
    </Accordion>
      


    
</div>