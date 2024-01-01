<script lang="ts">
	import Brick from "$lib/brick/Brick.svelte";
	import LandingPage from "$lib/session/LandingPage.svelte";
	import { DEFAULT_RINGS, DEFAULT_CONFIG } from "$lib/data";
	import { rings } from "$lib/stores/RingStore";

	$rings = DEFAULT_RINGS;

</script>

<div class="container mx-auto max-w-[90%] max-h-[90%] h-full">

    <div class="grid sm:grid-cols-1 md:grid-cols-2 gap-4 h-full">
		<div class="h-full w-full">
			<Brick config={DEFAULT_CONFIG}></Brick>
		</div>
		<div class="flex items-center h-full w-full">
			<LandingPage></LandingPage>
		</div>
		
	</div>
</div>
