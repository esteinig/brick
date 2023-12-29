 
<script lang="ts">
    import Brick from "$lib/brick/Brick.svelte";
	import RingControlPanel from "./RingControlPanel.svelte";

    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import { BRICK_INTERFACE_CONFIG_DEFAULT, type BrickInterfaceConfiguration } from "./types";
    import { DEFAULT_CONFIG, DEFAULT_RINGS } from "$lib/data";
	import type { Ring } from "$lib/types";
	import type { PlotConfig } from "$lib/brick/types";
	import DataControlPanel from "./DataControlPanel.svelte";

    export let rings: Ring[] = DEFAULT_RINGS;
    export let config: PlotConfig = DEFAULT_CONFIG;

    export let interfaceConfiguration: BrickInterfaceConfiguration = BRICK_INTERFACE_CONFIG_DEFAULT;

    let tab: number = 0;

</script>

<div class="container mt-[2.5%] mx-auto max-w-[90%] max-h-[90%] h-full">
    
    <div class="grid sm:grid-cols-1 md:grid-cols-8 gap-8 h-full">
        <div class="md:col-span-5">
            <div class="grid grid-rows-1 md:grid-rows-1 gap-y-8 h-full">
                <div class="row-span-1">
                    <div class="border-primary-500 h-full w-full">
                        <Brick bind:rings={rings} bind:config={config} width={interfaceConfiguration.svg_window_width} height={interfaceConfiguration.svg_window_height}></Brick>
                    </div>
                </div>
            </div>
        </div>

        <div class="md:col-span-3">
            <div class="grid grid-rows-1 md:grid-rows-2 gap-y-8 h-full">
                <div class="row-span-1">
                    <div class="border-primary-500 h-full w-full p-2">
                        
                        <TabGroup>
                            <Tab bind:group={tab} name="tab1" value={0}>
                                <span>Data<span>
                            </Tab>
                            <Tab bind:group={tab} name="tab2" value={1}>
                                <span>Rings</span>
                            </Tab>
                            <Tab bind:group={tab} name="tab3" value={2}>
                                <span>Plot</span>
                            </Tab>

                            <Tab bind:group={tab} name="tab4" value={3}>
                                <span>Export</span>
                            </Tab>
                            <Tab bind:group={tab} name="tab4" value={4}>
                                <span>About</span>
                            </Tab>
                            <!-- Tab Panels --->
                            <svelte:fragment slot="panel">
                                {#if tab === 0}
                                    <DataControlPanel></DataControlPanel>
                                {:else if tab === 1}
                                    <RingControlPanel bind:rings={rings} bind:config={config}></RingControlPanel>
                                {:else if tab === 2}
                                <span></span>
                                {:else if tab === 3}
                                <span></span>
                                {:else if tab === 4}
                                <span></span>
                                {/if}
                            </svelte:fragment>
                        </TabGroup>
                    </div>
                </div>
                <div class="row-span-1">
                    <div class="border-primary-500 h-full w-full">
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

