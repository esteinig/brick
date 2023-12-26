<script lang="ts">
	import Brick from "$lib/brick/Brick.svelte";
	import { createSessionId } from "$lib/brick/helpers";
	
	
</script>

<div class="container h-full mx-auto mb-10 flex justify-center items-center">
	<Brick width={900} height={800}></Brick>
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
			<a><code class="text-xs opacity-100">Steinig et al. (2024) - BRICK: bacterial genome annotation and identity visualisation - Microbial Genomics</code></a>
		</div>
	</div>
</div>

<style lang="postcss">
	figure {
		@apply flex relative flex-col;
	}
	figure svg,
	.img-bg {
		@apply w-64 h-64 md:w-80 md:h-80;
	}
	.img-bg {
		@apply absolute z-[-1] rounded-full blur-[50px] transition-all;
		animation: pulse 5s cubic-bezier(0, 0, 0, 0.5) infinite,
			glow 5s linear infinite;
	}
	@keyframes glow {
		0% {
			@apply bg-primary-400/50;
		}
		33% {
			@apply bg-secondary-400/50;
		}
		66% {
			@apply bg-tertiary-400/50;
		}
		100% {
			@apply bg-primary-400/50;
		}
	}
	@keyframes pulse {
		50% {
			transform: scale(1.5);
		}
	}
</style>
