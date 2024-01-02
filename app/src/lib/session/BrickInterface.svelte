 
<script lang="ts">
    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import type { PlotConfig } from "$lib/types";

    import { DEFAULT_CONFIG } from "$lib/data";

	import DataControlPanel from "$lib/session/controls/panels/DataControlPanel.svelte";
	import RingControlPanel from "$lib/session/controls/panels/RingControlPanel.svelte";

	import { uploadInProgress } from '$lib/stores/UploadInProgressStore';


    export let config: PlotConfig = DEFAULT_CONFIG;

    let tab: number = 0;

</script>

<div class="h-full w-full p-2">
    
    <TabGroup>
        <Tab bind:group={tab} name="tab1" value={0}>
            <span>Data<span>
        </Tab>
        <Tab bind:group={tab} name="tab2" value={1} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Rings</span>
        </Tab>
        <Tab bind:group={tab} name="tab3" value={2} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Plot</span>
        </Tab>

        <Tab bind:group={tab} name="tab4" value={3} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Export</span>
        </Tab>
        <Tab bind:group={tab} name="tab4" value={4} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>About</span>
        </Tab>
        <!-- Tab Panels --->
        <svelte:fragment slot="panel">
            {#if tab === 0}
                <DataControlPanel></DataControlPanel>
            {:else if tab === 1}
                <RingControlPanel bind:config={config}></RingControlPanel>
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

