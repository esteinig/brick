 
<script lang="ts">
    import { TabGroup, Tab } from '@skeletonlabs/skeleton';

	import DataControlPanel from "$lib/session/controls/panels/DataControlPanel.svelte";
	import RingControlPanel from "$lib/session/controls/panels/RingControlPanel.svelte";
    import PlotControlPanel from '$lib/session/controls/panels/PlotControlPanel.svelte';
	import PaletteControlPanel from './controls/panels/PaletteControlPanel.svelte';
	import AboutPanel from './controls/panels/AboutPanel.svelte';

	import { uploadInProgress } from '$lib/stores/UploadInProgressStore';
	import { tabIndexStore } from '$lib/stores/TabIndexStore';
    
</script>

<div class="h-full w-full p-2">
    
    <TabGroup>
        <Tab bind:group={$tabIndexStore} name="tab1" value={0}>
            <span>Data<span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab2" value={1} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Rings</span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab3" value={2} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}>Plot</span>
        </Tab>

        <Tab bind:group={$tabIndexStore} name="tab4" value={3} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-60">Palettes</span></span>
        </Tab>
        <Tab bind:group={$tabIndexStore} name="tab4" value={4} disabled={$uploadInProgress}>
            <span class={$uploadInProgress ? 'opacity-30 cursor-not-allowed' : ''}><span class="opacity-60">About</span></span>
        </Tab>


        <!-- Tab Panels --->
        <svelte:fragment slot="panel">
            {#if $tabIndexStore === 0}
                <DataControlPanel></DataControlPanel>
            {:else if $tabIndexStore === 1}
                <RingControlPanel></RingControlPanel>
            {:else if $tabIndexStore === 2}
                <PlotControlPanel></PlotControlPanel>
            {:else if $tabIndexStore === 3}
                <PaletteControlPanel></PaletteControlPanel>
            {:else if $tabIndexStore === 4}
                <AboutPanel />
            {/if}
        </svelte:fragment>
    </TabGroup>
</div>

