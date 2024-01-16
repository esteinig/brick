<script lang="ts">
	import { downloadJSON, downloadSVG } from "$lib/brick/helpers";
    import { plotConfigStore } from "$lib/stores/PlotConfigStore";
    import { rings } from "$lib/stores/RingStore";
	import { TitleStyle } from "$lib/types";
    
    import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';


    let titleOpacity: number = 80;
    $: $plotConfigStore.title.opacity = titleOpacity/100;


    let subtitleOpacity: number = 80;
    let subtitleHeight: number = 100;
    
    $: $plotConfigStore.subtitle.opacity = subtitleOpacity/100;
    $: $plotConfigStore.subtitle.height = subtitleHeight/100;

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

    function toggleFontStyle(styleKey: TitleStyle, subtitle: boolean = false): void {
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

        if (subtitle){
            $plotConfigStore.subtitle.styles = updatedStyles; 
        } else {
            $plotConfigStore.title.styles = updatedStyles; 
        }
        
    }

    let selectedConfig: string = "";

</script>

<div id="brickPlotControlPanel" class="p-2 text-base">



   
    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-8">
        <div id="brickPlotBackground" class="mt-8 mb-16">
           <div id="brickPlotExports">
            
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8">
                <label class="label text-xs col-span-3">
                    <p class="opacity-40 mb-2">Background opacity</p>
                    <input type="range" bind:value={svgOpacity} min="0" max="100" />
                </label>
                <label class="label text-xs col-span-2">
                    <p class="opacity-40 mb-2">Color</p>
                    <input class="input" type="color" style="height: 2rem; width: 2rem;" bind:value={svgColor} />
                </label>
            </div>
            <div class="flex justify-start mb-5 mt-4">
                <button class="btn border border-primary-500 text-base mr-3 truncate" on:click={() => downloadSVG("brickPlotSession")}>
                  <svg class="w-6 h-6 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  SVG
                </button>
                <button class="btn border border-secondary-500 text-base truncate" on:click={() => downloadJSON($rings)}>
                  <svg class="w-6 h-6 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  JSON
                </button>
            </div>
        </div>
            
        </div>
        <div id="brickPlotZoom" class="mt-8 mb-16">
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8 ">
                <div class="col-span-2">
                    <label class="text-sm flex items-center">
                        <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={$plotConfigStore.svg.zoomEnabled} />
                        <div class="opacity-40 ml-2">Enable Zoom</div>
                    </label>
                    <p class="text-xs opacity-20 mt-4">Use the mousewheel or buttons below the plot</p>
                </div>
                
                <div class="flex-1 col-span-3">
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Zoom-out limit ({$plotConfigStore.svg.zoomLowerLimit})</p>
                        <input type="range" bind:value={$plotConfigStore.svg.zoomLowerLimit} min="0" max="10" step="0.1" />
                    </label>
                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Zoom-in limit ({$plotConfigStore.svg.zoomUpperLimit})</p>
                        <input type="range" bind:value={$plotConfigStore.svg.zoomUpperLimit} min="0" max="100" step="1" />
                    </label>
                </div>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-1 gap-8">
        <div id="brickPlotSettings">
            <p class="opacity-60 mb-4">Settings</p>
            <ListBox class="text-sm opacity-80">
                <ListBoxItem bind:group={selectedConfig} name="medium" value="title">Title styles</ListBoxItem>
                <ListBoxItem bind:group={selectedConfig} name="medium" value="labels">Label styles</ListBoxItem>
                <ListBoxItem bind:group={selectedConfig} name="medium" value="rings">Ring spacing</ListBoxItem>
            </ListBox>
        </div>
        
    </div>
    
    <div class="p-4 my-8">
        {#if selectedConfig === "title"}
            <div id="brickPlotConfigTitle" class="mb-8">
                <p class="opacity-60 mb-4">Title</p>

                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">

                    <label class="label text-xs">
                        <p class="opacity-40">Text</p>
                        <input class="input" type="text" bind:value={$plotConfigStore.title.text} />
                    </label>
                    <div class="flex gap-x-8 align-center">
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
                        <label class="label text-xs">
                            <p class="opacity-40">Color</p>
                            <input class="input" type="color" style="height: 2rem; width: 2rem;" bind:value={$plotConfigStore.title.color} />
                        </label>
                        <label class="label text-xs">
                                <p class="opacity-40">Font styles</p>
                                <div class="grid grid-cols-1">
                                    {#each Array.from(styles.keys()) as f}
                                        <button
                                            class="chip {styles.get(f) ? 'variant-filled': 'variant-soft'} m-1"
                                            on:click={() => toggleFontStyle(f)}
                                            on:keypress={() => toggleFontStyle(f)}
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
                                </div>
                        </label>
                    </div>
                </div>
            </div>
            <div id="brickPlotConfigSubtitle" class="">
                <p class="opacity-60 mb-4">Subtitle</p>
        
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">
        
                    <label class="label text-xs">
                        <p class="opacity-40">Text</p>
                        <input class="input" type="text" bind:value={$plotConfigStore.subtitle.text} />
                    </label>
                    <div class="flex gap-x-8 align-center">
                        <div class="flex-1">
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Opacity (%)</p>
                                <input type="range" bind:value={subtitleOpacity} min="0" max="100" />
                            </label>
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Size (%)</p>
                                <input type="range" bind:value={$plotConfigStore.subtitle.size} min="0" max="200" />
                            </label>
                            <label class="label text-xs">
                                <p class="opacity-40">Height (%)</p>
                                <input type="range" bind:value={subtitleHeight} min="0" max="200" />
                            </label>
                        </div>
                        <label class="label text-xs">
                            <p class="opacity-40">Color</p>
                            <input class="input" type="color" style="height: 2rem; width: 2rem;" bind:value={$plotConfigStore.subtitle.color} />
                        </label>
                        <label class="label text-xs">
                                <p class="opacity-40">Font styles</p>
                                <div class="grid grid-cols-1">
                                    {#each Array.from(styles.keys()) as f}
                                        <button
                                            class="chip {styles.get(f) ? 'variant-filled': 'variant-soft'} m-1"
                                            on:click={() => toggleFontStyle(f, true)}
                                            on:keypress={() => toggleFontStyle(f, true)}
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
                                </div>
                        </label>
                    </div>
                </div>
            </div>
        {:else if selectedConfig === "rings"}
            
            <div id="brickPlotConfigRings" class="">
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
        {:else if selectedConfig === "labels"}
            <div id="brickPlotConfigLabels" class="mb-8">
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
                            <p class="opacity-40">Color</p>
                            <input class="input" type="color" style="height: 2rem; width: 2rem;" bind:value={lineColor} />
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
                            <p class="opacity-40">Color</p>
                            <input class="input" type="color" style="height: 2rem; width: 2rem;" bind:value={textColor} />
                        </label>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    
</div>

<style lang="postcss">
    .checkbox:checked, .checkbox:indeterminate {
        background-color: rgb(var(--color-secondary-500) / var(--tw-bg-opacity));
    }

    /* .checkbox:checked:focus, .checkbox:indeterminate:focus {
        --tw-bg-opacity: 1;
        background-color: rgb(var(--color-secondary-500) / var(--tw-bg-opacity));
        --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
        --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(0px + var(--tw-ring-offset-width)) var(--tw-ring-color);
        box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
    }
    .checkbox:focus {
        --tw-bg-opacity: 1;
        background-color: rgb(var(--color-secondary-500) / var(--tw-bg-opacity));
        --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
        --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(0px + var(--tw-ring-offset-width)) var(--tw-ring-color);
        box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
    } */
</style>