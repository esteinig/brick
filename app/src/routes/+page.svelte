<script lang="ts">
	
	import Brick from "$lib/brick/Brick.svelte";
	import { createSessionId } from "$lib/session/helpers";

	import { DEFAULT_RINGS } from "$lib/data";
	
	
</script>

<div class="container h-full mx-auto mb-10 flex justify-center items-center">
	<Brick rings={DEFAULT_RINGS} width={900} height={800}></Brick>
	<div class="space-y-10 text-center flex flex-col items-center">

		<div class="gap-y-0">
			<h2 class="h2 mb-1"><code>BRICK</code></h2>
			<p><code>BRIG</code><sup>*</sup> - like interactive data visualization for</p>
			<p>bacterial whole genome comparison and annotation</p>

			<div class="w-full mt-3">
				<div class="opacity-70" style="font-size: 0.6rem"><sup>*</sup>BLAST Ring Image Generator (<a target="_blank" rel="noreferrer" href="https://github.com/happykhan/BRIG">Alikhan et al. 2011)</a></div>
			</div>
		</div>
		<!-- / -->
		<div class="flex justify-center space-x-2">
			<a
				class="btn border border-primary-500"
				href="/brick/{createSessionId()}"
			>
				Create Figure
			</a>
			<button
				class="btn border border-secondary-500"
			>
				Documentation
        </button>
		</div>
		<div class="gap-y-0 text-center flex flex-col items-center">
			<div class="text-sm opacity-70 mb-2">Please consider citing our publication if you explore data or create figures for publication.</div>	
			<a href="https://github.com/esteinig/brick" target="_blank" rel="noreferrer"><code class="text-xs opacity-100">Steinig et al. (2024) - BRICK: bacterial genome annotation and identity visualisation - Microbial Genomics</code></a>
		</div>
	</div>
</div>
