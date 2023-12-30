<script lang="ts">
	import { createSessionId } from "$lib/session/helpers";
</script>

<div class="container">
    <div class="text-center flex flex-col items-center">

        <div class="gap-y-0 mb-6">
            <h2 class="h2 mb-1"><code>BRICK</code></h2>
            <p><code>BRIG</code><sup>*</sup> - like interactive data visualization for</p>
            <p>bacterial whole genome comparison and annotation</p>

            <div class="w-full mt-3">
                <div class="opacity-70" style="font-size: 0.6rem"><sup>*</sup>BLAST Ring Image Generator (<a target="_blank" rel="noreferrer" href="https://github.com/happykhan/BRIG">Alikhan et al. 2011)</a></div>
            </div>
        </div>
        <div class="flex justify-center space-x-2 mb-10">
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
        <div class="gap-y-1 text-center flex flex-col items-center">
            <div class="text-sm opacity-70 mb-2">Please consider citing our publication in research outputs</div>	
            <a href="https://github.com/esteinig/brick" target="_blank" rel="noreferrer"><code class="text-xs opacity-100">Steinig et al. (2024) - BRICK: bacterial genome annotation and identity visualisation - Microbial Genomics</code></a>
        </div>
    </div>
</div>