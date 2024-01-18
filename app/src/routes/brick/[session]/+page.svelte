<script lang="ts">
    import Brick from "$lib/brick/Brick.svelte";
    import BrickInterface from "$lib/session/BrickInterface.svelte";
	import { getDefaultScaleFactor } from "$lib/brick/helpers";
	import { page } from "$app/stores";
	import { sessionFiles } from "$lib/stores/SessionFileStore";
	import { rings } from "$lib/stores/RingStore";
	import { invalidate } from "$app/navigation";
	import { browser } from "$app/environment";

	// Events from the figure to display in control interface
	function handleClick(event: any)  {
        console.log(`Clicked: ${ event.detail}`);
    }

	// Update session files store when data has changed
	$: if (!$page.data.session) {
		if (browser) invalidate('app:session')
	} else {
		// Without the length guards the stores are overwritten
		// with not-updated data (e.g. after adding a ring) since
		// we are not invalidating session data after each creation
		// but add rings to the store directly in the form action return

		// Maybe it's better to invalidate, since this is quite fucky

		if (!$rings.length){
			$rings = $page.data.session.rings
		}
		if (!$sessionFiles.length){
			$sessionFiles = $page.data.session.files
		}
	}

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
