<script lang="ts">

	import Brick from "$lib/brick/Brick.svelte";
	import LandingPage from "$lib/session/LandingPage.svelte";

	import { onMount } from 'svelte';
	import { rings } from "$lib/stores/RingStore";
	import { getDefaultScaleFactor } from "$lib/brick/helpers";	
	import { DEFAULT_RINGS } from "$lib/data";

	
	onMount(() => {
		$rings = DEFAULT_RINGS;
	});
	

</script>

<div class="container mx-auto max-w-[90%] max-h-[90%] h-full">

    <div class="grid sm:grid-cols-1 md:grid-cols-8 h-full">
		<div class="h-full w-ful col-span-4">
			<Brick id="brickPlotLandingPage" scaleFactor={getDefaultScaleFactor() + 0.2}></Brick>
		</div>
		<div class="flex items-center h-full w-full col-span-4">
			<LandingPage></LandingPage>
		</div>
		
	</div>
</div>