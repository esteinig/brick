<script lang="ts">
    import Brick from "$lib/brick/Brick.svelte";
    import BrickInterface from "$lib/session/BrickInterface.svelte";
	import { getDefaultScaleFactor } from "$lib/brick/helpers";
	import { page } from "$app/stores";
	import { sessionFiles } from "$lib/stores/SessionFileStore";
	import { rings } from "$lib/stores/RingStore";
	import { onMount } from "svelte";
	import { ringReferenceStore } from "$lib/stores/RingReferenceStore";

	// Events from the figure to display in control interface
	function handleClick(event: any)  {
        console.log(`Clicked: ${ event.detail}`);
    }


	onMount(() => {
		$rings = $page.data.session.rings;
		if ($rings.length) $ringReferenceStore = $rings[0].reference;
		$sessionFiles = $page.data.session.files;

		console.log($page.data.session)
	})

</script>	



<div class="container mt-[2.5%] mx-auto max-w-[95%] max-h-[90%]">

    <div class="grid sm:grid-cols-1 md:grid-cols-8 gap-8 h-screen overflow-hidden">
		<div class="col-span-5 w-full max-h-[85%]">
            <Brick id="brickPlotSession" scaleFactor={getDefaultScaleFactor() + 0.4} on:click={handleClick} border></Brick>
		</div>
		<div class="col-span-3 h-full w-full overflow-auto">
            <BrickInterface></BrickInterface>
		</div>
	</div>
</div>
