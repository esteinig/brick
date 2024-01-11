<script lang="ts">
	import { downloadJSON, downloadPNG, downloadSVG } from "$lib/brick/helpers";
    import { plotConfigStore } from "$lib/stores/PlotConfigStore";
    import { rings } from "$lib/stores/RingStore";
	import { TitleStyle } from "$lib/types";

    let titleOpacity: number = 80;
    $: $plotConfigStore.title.opacity = titleOpacity/100;

    let lineColor: string = "#d3d3d3";
    let lineOpacity: number = 80;
    let lineWidth: number = 7;

    $: $plotConfigStore.annotation.lineStyle = `stroke: ${lineColor}; stroke-width: ${lineWidth/100}rem; opacity: ${lineOpacity/100};`

    let textColor: string = "#d3d3d3";
    let textSize: number = 80;
    let textOpacity: number = 80;

    $: $plotConfigStore.annotation.textStyle = `fill: ${textColor}; opacity: ${textOpacity/100}; font-size: ${textSize}%` 

    let svgColor: string = "#d3d3d3";
    let svgOpacity: number = 0;

    $: $plotConfigStore.svg.backgroundOpacity = svgOpacity/100;
    $: $plotConfigStore.svg.backgroundColor = svgColor;
    

    let styles: Map<TitleStyle, boolean> = new Map([
        [TitleStyle.ITALIC, false],
        [TitleStyle.BOLD, false],
        [TitleStyle.CODE, false]
    ]);

    function toggleFontStyle(styleKey: TitleStyle): void {
        // Toggle the style
        styles.set(
            styleKey, 
            !styles.get(styleKey)
        );


            // Update the styles array in the store
        let updatedStyles: TitleStyle[] = [];
        styles.forEach((value, key) => {
            if (value) {
                updatedStyles.push(key);
            }
        });

        console.log(updatedStyles)

        $plotConfigStore.title.styles = updatedStyles;  // {'variant-filled' : 'variant-soft'}
    }
</script>

<div id="brickPlotControlPanel" class="p-2 text-base">
    <div id="brickPlotConfigTitle" class="mb-16">
        <p class="opacity-60 mb-4">Title</p>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">

            <label class="label text-xs">
                <p class="opacity-40">Text</p>
                <input class="input" type="text" bind:value={$plotConfigStore.title.text} />
            </label>
            <label class="label text-xs">
                <p class="opacity-40">Subtext</p>
                <input class="input" type="text" bind:value={$plotConfigStore.title.subtext} />
            </label>
            <div class="flex gap-x-8 align-center">
                <label class="label text-xs">
                    <p class="opacity-40">Color</p>
                    <input class="input" type="color" style="height: 2.3rem; width: 2.3rem;" bind:value={$plotConfigStore.title.color} />
                </label>
               <label class="label text-xs">
                    <p class="opacity-40">Font styles</p>
                    {#each Array.from(styles.keys()) as f}
                        <button
                            class="chip {styles.get(f) ? 'variant-filled': 'variant-soft'} m-1"
                            on:click={() => toggleFontStyle(f)}
                            on:keypress={/* Keypress handler if necessary */ () => {} }
                        >
                            {#if styles.get(f)}
                                <span>
                                    <svg class="w-2 h-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="m4.5 12.75 6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                    </svg>
                                </span>
                            {/if}
                            <span class="capitalize">{f}</span>
                        </button>
                    {/each}
                </label>
            </div>

            <div class="flex-1">
                <label class="label text-xs mb-4">
                    <p class="opacity-40">Opacity (%)</p>
                    <input type="range" bind:value={titleOpacity} min="0" max="100" />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Size (%)</p>
                    <input type="range" bind:value={$plotConfigStore.title.size} min="0" max="200" />
                </label>
            </div>

        </div>
    </div>
    <div id="brickPlotConfigRings" class="mb-16">
        <p class="opacity-60 mb-4">Rings</p>

        <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 gap-8">

            <label class="label text-xs">
                <p class="opacity-40">Radius</p>
                <input type="range" bind:value={$plotConfigStore.rings.radius} min="0" max="1000" />
            </label>
            <label class="label text-xs mb-4">
                <p class="opacity-40">Height</p>
                <input type="range" bind:value={$plotConfigStore.rings.height} min="0" max="100" />
            </label>
            <label class="label text-xs">
                <p class="opacity-40">Gap</p>
                <input type="range" bind:value={$plotConfigStore.rings.gap} min="0" max="100" />
            </label>

        </div>
    </div>
    <div id="brickPlotConfigRings" class="mb-8">
        <p class="opacity-60 mb-4">Labels</p>
        <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-8">
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8">

                <div class="flex-1 col-span-3">
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Line length</p>
                        <input type="range" bind:value={$plotConfigStore.annotation.lineLength} min="0" max="100" />
                    </label>
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Line opacity</p>
                        <input type="range" bind:value={lineOpacity} min="0" max="100" />
                    </label>
                    <label class="label text-xs">
                        <p class="opacity-40">Line width</p>
                        <input type="range" bind:value={lineWidth} min="0" max="25" />
                    </label>
                </div>
            
                <label class="label text-xs col-span-2">
                    <p class="opacity-40">Line color</p>
                    <input class="input" type="color" style="height: 2.3rem; width: 2.3rem;" bind:value={lineColor} />
                </label>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8">

                <div class="flex-1 col-span-3">
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Text gap</p>
                        <input type="range" bind:value={$plotConfigStore.annotation.textGap} min="0" max="100" />
                    </label>
        
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Text opacity</p>
                        <input type="range" bind:value={textOpacity} min="0" max="100" />
                    </label>
                    <label class="label text-xs">
                        <p class="opacity-40">Text size</p>
                        <input type="range" bind:value={textSize} min="0" max="200" />
                    </label>
                </div>
            
                <label class="label text-xs col-span-2">
                    <p class="opacity-40">Text color</p>
                    <input class="input" type="color" style="height: 2.3rem; width: 2.3rem;" bind:value={textColor} />
                </label>
            </div>
        </div>
    </div>
    <div id="brickPlotConfigExport" class="my-16">
        <p class="opacity-60 mb-4">Export</p>
        <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-8">
            <div class="flex justify-start mb-5">
                <button class="btn border border-primary-500 text-xs mr-2" on:click={() => downloadSVG("brickPlotSession")}>
                  <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  SVG
                </button>
                <!-- <button class="btn border border-primary-500 text-xs mr-2" on:click={() => downloadPNG("brickPlotSession")}>
                  <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  PNG
                </button> -->
                <button class="btn border border-secondary-500 text-xs" on:click={() => downloadJSON($rings)}>
                  <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  JSON
                </button>
            </div>
            <div id="brickPlotConfigExport" class="flex gap-x-8">
                <label class="label text-xs">
                    <p class="opacity-40 mb-2">Background opacity</p>
                    <input type="range" bind:value={svgOpacity} min="0" max="100" />
                </label>
                <label class="label text-xs col-span-2">
                    <p class="opacity-40 mb-2">Background color</p>
                    <input class="input" type="color" style="height: 2.3rem; width: 2.3rem;" bind:value={svgColor} />
                </label>
            </div>
        </div>
    </div>
</div>