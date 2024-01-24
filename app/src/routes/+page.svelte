<script lang="ts">

	import Brick from "$lib/brick/Brick.svelte";
	import LandingPage from "$lib/session/LandingPage.svelte";

	import { onMount } from 'svelte';
	import { rings } from "$lib/stores/RingStore";
	import { getDefaultScaleFactor } from "$lib/brick/helpers";	
	import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
	import { page } from "$app/stores";
	import { plotConfigStore } from "$lib/stores/PlotConfigStore";

	
	function setDefaultTitles() {
		$plotConfigStore.title.text = "Mycobacterium sp. nov."
		$plotConfigStore.title.style.italic = true;
		$plotConfigStore.subtitle.text = "Genome annotation and comparison with non-tuberculous mycobacteria";
	}

	onMount(() => {
		setDefaultTitles();
		$ringReferenceStore = $page.data.reference;
		$rings = $page.data.rings;
		console.log("Landing page", $plotConfigStore)
	});
	

</script>

<div class="container mx-auto max-w-[90%] max-h-[90%] h-full">

    <div class="grid sm:grid-cols-1 md:grid-cols-8 h-full">
		<div class="h-full w-ful col-span-5">
			<Brick id="brickPlotLandingPage" scaleFactor={getDefaultScaleFactor() + 0.2}></Brick>
		</div>
		<div class="flex items-center h-full w-full col-span-3">
			<LandingPage></LandingPage>
		</div>	
	</div>
</div>