<script lang="ts">
    import Brick from "$lib/brick/Brick.svelte";
    import BrickInterface from "$lib/session/BrickInterface.svelte";

	import { DEFAULT_CONFIG, DEFAULT_RINGS } from "$lib/data";

	import type { Ring } from "$lib/types";
	import type { PlotConfig } from "$lib/types";

    export let rings: Ring[] = DEFAULT_RINGS;
    export let config: PlotConfig = DEFAULT_CONFIG;

</script>



<div class="container mt-[2.5%] mx-auto max-w-[90%] max-h-[90%] h-full">

    <div class="grid sm:grid-cols-1 md:grid-cols-8 gap-8 h-full">
		<div class="col-span-5 h-full w-full">
            <Brick bind:rings={rings} bind:config={config}></Brick>
		</div>
		<div class="col-span-3 h-full w-full">
            <BrickInterface bind:rings={rings} bind:config={config}></BrickInterface>
		</div>
	</div>
</div>
