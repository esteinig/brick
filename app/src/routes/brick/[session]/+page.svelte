<script lang="ts">
    import Brick from "$lib/brick/Brick.svelte";
    import BrickInterface from "$lib/session/BrickInterface.svelte";
	import { getDefaultScaleFactor } from "$lib/brick/helpers";
	import { page } from "$app/stores";
	import { sessionFiles } from "$lib/stores/SessionFileStore";
	
	
	// Events from the figure to display in control interface
	function handleClick(event: any)  {
        console.log(`Clicked: ${ event.detail}`);
    }

	$: console.log($page.data)

	
</script>	



<div class="container mt-[2.5%] mx-auto max-w-[90%] max-h-[90%] h-full">

    <div class="grid sm:grid-cols-1 md:grid-cols-8 gap-8 h-full">
		<div class="col-span-5 h-screen w-full">
            <Brick id="brickPlotSession" scaleFactor={getDefaultScaleFactor() + 0.4} on:click={handleClick} border></Brick>
		</div>
		<div class="col-span-3 h-full w-full">
            <BrickInterface></BrickInterface>
		</div>
	</div>
</div>
