 
<script lang="ts">

    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import type { Ring } from "$lib/types";
	import type { PlotConfig } from "$lib/brick/types";
    import { DEFAULT_CONFIG, DEFAULT_RINGS } from "$lib/data";

	import DataControlPanel from "./DataControlPanel.svelte";
	import RingControlPanel from "./RingControlPanel.svelte";

    export let rings: Ring[] = DEFAULT_RINGS;
    export let config: PlotConfig = DEFAULT_CONFIG;

    let tab: number = 0;

</script>




<div class="h-full w-full p-2">
    
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

