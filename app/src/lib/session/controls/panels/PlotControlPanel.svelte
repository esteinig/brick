<script lang="ts">
	import { downloadPNG, downloadSVG } from "$lib/brick/helpers";
	import { createUuid } from "$lib/helpers";
	import PalettePopup from "$lib/session/palette/PalettePopup.svelte";
    import { plotConfigStore } from "$lib/stores/PlotConfigStore";
    
    import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import FontStyles from "../helpers/FontStyles.svelte";

    let selectedConfig: string = "title";

</script>

<div id="brickPlotControlPanel" class="p-2 text-base">

    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-8">
        <div id="brickPlotBackground" class="mt-8 mb-16">
           <div id="brickPlotExports">
            
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8">
                <label class="label text-xs col-span-3">
                    <p class="opacity-40 mb-2">Background opacity</p>
                    <input type="range" bind:value={$plotConfigStore.svg.backgroundOpacity} min="0" max="100" />
                </label>
                
                <div class="flex gap-2 col-span-2 mt-4">
                    <input class="input" type="color" style="height: 1.5rem; width: 1.5rem;" bind:value={$plotConfigStore.svg.backgroundColor} />
                    <PalettePopup id={createUuid()} size={6} updateDatabase={false} bind:color={$plotConfigStore.svg.backgroundColor}></PalettePopup>
                </div>
            </div>
            <div class="flex justify-start mb-5 mt-4">
                <button class="btn border border-primary-500 text-base mr-3 truncate" on:click={() => downloadSVG("brickPlotSession")}>
                  <svg class="w-6 h-6 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  SVG
                </button>
                <button class="btn border border-primary-500 text-base truncate" on:click={() => downloadPNG("brickPlotSession")}>
                  <svg class="w-6 h-6 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                  PNG
                </button>
            </div>
        </div>
    </div>

    <div id="brickPlotZoom" class="mt-12 mb-16">
        <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8 ">
            <div class="col-span-2">
                <label class="text-sm flex items-center">
                    <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={$plotConfigStore.svg.zoomEnabled} />
                    <div class="opacity-40 ml-2">Enable zoom</div>
                </label>
                <p class="text-xs opacity-20 mt-4">Use mousewheel or buttons to zoom, click and drag to move</p>
                <label class="text-sm flex items-center mt-4">
                    <input class="checkbox focus:ring-offset-surface-500 focus:checked:ring-offset-secondary-500" type="checkbox" bind:checked={$plotConfigStore.svg.positionEnabled} />
                    <div class="opacity-40 ml-2">Enable position</div>
                </label>
                <p class="text-xs opacity-20 mt-4">Hover anywhere to display position on central reference</p>
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

    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-8">
        <div id="brickPlotSettings">
            <p class="opacity-60 mb-4">Settings</p>
            <ListBox class="text-sm opacity-80" active="variant-outline-secondary">
                <ListBoxItem bind:group={selectedConfig} name="medium" value="title" active="variant-ghost-secondary">Title styles</ListBoxItem>
                <ListBoxItem bind:group={selectedConfig} name="medium" value="labels" active="variant-ghost-secondary">Label styles</ListBoxItem>
                <ListBoxItem bind:group={selectedConfig} name="medium" value="rings" active="variant-ghost-secondary">Ring spacing</ListBoxItem>
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
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-x-4">
                        <div class="flex-1 col-span-3">
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Opacity (%)</p>
                                <input type="range" bind:value={$plotConfigStore.title.opacity} min="0" max="500" />
                            </label>
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Size (%)</p>
                                <input type="range" bind:value={$plotConfigStore.title.size} min="0" max="500" />
                            </label>
                        </div>
                        <div class="flex gap-2 mt-4">
                            <input class="input" type="color" style="height: 1.5rem; width: 1.5rem;" bind:value={$plotConfigStore.title.color} />
                            <PalettePopup id={createUuid()} size={6} updateDatabase={false} bind:color={$plotConfigStore.title.color}></PalettePopup>
                        </div>
                        <div class="flex-1 mt-2 text-xs">
                            <FontStyles on:change={(event) => $plotConfigStore.title.style = event.detail}></FontStyles>
                        </div>
                    </div>
                </div>
            </div>
            <div id="brickPlotConfigSubtitle" class="">
                <p class="opacity-60 mb-4">Subtitle</p>
        
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">
                    
                    <div>
                        <label class="label text-xs">
                            <p class="opacity-40">Text</p>
                            <input class="input" type="text" bind:value={$plotConfigStore.subtitle.text} />
                        </label>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-x-4">

                        <div class="flex-1 col-span-3">
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Opacity (%)</p>
                                <input type="range" bind:value={$plotConfigStore.subtitle.opacity} min="0" max="100" />
                            </label>
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Size (%)</p>
                                <input type="range" bind:value={$plotConfigStore.subtitle.size} min="0" max="200" />
                            </label>
                            <label class="label text-xs">
                                <p class="opacity-40">Height (%)</p>
                                <input type="range" bind:value={$plotConfigStore.subtitle.height} min="0" max="500" />
                            </label>
                        </div>

                        <div class="flex gap-2 mt-4">
                            <input class="input" type="color" style="height: 1.5rem; width: 1.5rem;" bind:value={$plotConfigStore.subtitle.color} />
                            <PalettePopup id={createUuid()} size={6} updateDatabase={false} bind:color={$plotConfigStore.subtitle.color}></PalettePopup>
                        </div>

                        <div class="flex-1 mt-2 text-xs">
                            <FontStyles on:change={(event) => $plotConfigStore.subtitle.style = event.detail}></FontStyles>
                        </div>
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
                        <p class="opacity-40">Inner ring height</p>
                        <input type="range" bind:value={$plotConfigStore.rings.height} min="0" max="100" />
                    </label>

                    <label class="label text-xs mb-4">
                        <p class="opacity-40">Outer ring height</p>
                        <input type="range" bind:value={$plotConfigStore.rings.outerHeight} min="0" max="100" />
                    </label>

                    <label class="label text-xs">
                        <p class="opacity-40">Inner ring gap</p>
                        <input type="range" bind:value={$plotConfigStore.rings.gap} min="0" max="100" />
                    </label>
                    <label class="label text-xs">
                        <p class="opacity-40">Label ring gap</p>
                        <input type="range" bind:value={$plotConfigStore.rings.labelGap} min="0" max="100" />
                    </label>
                    <label class="label text-xs">
                        <p class="opacity-40">Line ring width</p>
                        <input type="range" bind:value={$plotConfigStore.rings.lineWidth} min="0" max="10" step="0.2"/>
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
                                <input type="range" bind:value={$plotConfigStore.labels.lineLength} min="0" max="100" />
                            </label>
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Line opacity (%)</p>
                                <input type="range" bind:value={$plotConfigStore.labels.lineOpacity} min="0" max="100" />
                            </label>
                            <label class="label text-xs">
                                <p class="opacity-40">Line width (%)</p>
                                <input type="range" bind:value={$plotConfigStore.labels.lineWidth} min="0" max="25" />
                            </label>
                        </div>
                        
                        <div class="flex gap-2 col-span-2 mt-4">
                            <input class="input" type="color" style="height: 1.5rem; width: 1.5rem;" bind:value={$plotConfigStore.labels.lineColor} />
                            <PalettePopup id={createUuid()} size={6} updateDatabase={false} bind:color={$plotConfigStore.labels.lineColor}></PalettePopup>
                        </div>
                        
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-5 gap-8">
        
                        <div class="flex-1 col-span-3">
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Text gap</p>
                                <input type="range" bind:value={$plotConfigStore.labels.textGap} min="0" max="25" />
                            </label>
                
                            <label class="label text-xs mb-4">
                                <p class="opacity-40">Text opacity (%)</p>
                                <input type="range" bind:value={$plotConfigStore.labels.textOpacity} min="0" max="100" />
                            </label>
                            <label class="label text-xs">
                                <p class="opacity-40">Text size (%)</p>
                                <input type="range" bind:value={$plotConfigStore.labels.textSize} min="0" max="200" />
                            </label>
                        </div>
                    
                        <div class="flex gap-2 col-span-2 mt-4">
                            <input class="input" type="color" style="height: 1.5rem; width: 1.5rem;" bind:value={$plotConfigStore.labels.textColor} />
                            <PalettePopup id={createUuid()} size={6} updateDatabase={false} bind:color={$plotConfigStore.labels.textColor}></PalettePopup>
                        </div>
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