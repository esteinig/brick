 
<script lang="ts">
    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import DataControlPanel from "$lib/session/controls/panels/DataControlPanel.svelte";
	import RingControlPanel from "$lib/session/controls/panels/RingControlPanel.svelte";
    import PlotControlPanel from '$lib/session/controls/panels/PlotControlPanel.svelte';

	import { uploadInProgress } from '$lib/stores/UploadInProgressStore';
	import PaletteControlPanel from './controls/panels/PaletteControlPanel.svelte';

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
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-80 text-surface-500">Palettes</span></span>
        </Tab>
        <Tab bind:group={tab} name="tab4" value={4} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-80 text-surface-500">About</span></span>
        </Tab>


        <!-- Tab Panels --->
        <svelte:fragment slot="panel">
            {#if tab === 0}
                <DataControlPanel></DataControlPanel>
            {:else if tab === 1}
                <RingControlPanel></RingControlPanel>
            {:else if tab === 2}
                <PlotControlPanel></PlotControlPanel>
            {:else if tab === 3}
                <PaletteControlPanel></PaletteControlPanel>
            {:else if tab === 4}
                <span></span>
            {/if}
        </svelte:fragment>
    </TabGroup>
</div>

