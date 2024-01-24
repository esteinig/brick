<script lang="ts">
	import { createSessionId } from "$lib/helpers";
	import { plotConfigStore } from "$lib/stores/PlotConfigStore";

    function resetPlotConfig() {
        // On the landing page we set values that overwrite the ones
        // from the DEFAULT_CONFIGSTORE - this should be improved for 
        // the next release
        $plotConfigStore.title.text = "BRICK";
        $plotConfigStore.title.style.italic = false;
        $plotConfigStore.subtitle.text = "BRIG-like Interactive Circular Knowledgebase";
    }

    const published: boolean = false;
</script>

<div class="container">
    <div class="text-center flex flex-col items-center">

        <div class="gap-y-0 mb-6">
            <h2 class="h2 mb-1"><code>BRICK</code></h2>
            <p><code>BRIG</code><sup>*</sup> - like interactive data visualization for bacterial genome annotation and comparison</p>

            <div class="w-full mt-1">
                <div class="opacity-70" style="font-size: 0.6rem"><sup>*</sup><a target="_blank" rel="noreferrer" href="https://github.com/happykhan/BRIG">BLAST Ring Image Generator (Alikhan et al. 2011)</a></div>
            </div>
        </div>
        <div class="flex justify-center space-x-2 mb-10">
            <a
                class="btn border border-primary-500"
                href="/session/{createSessionId()}"
                on:click={resetPlotConfig}
            >
                Create Figure
            </a>
            <button
                class="btn border border-secondary-500"
                disabled
            >
                Documentation
        </button>
        </div>
        <div class="gap-y-1 text-center flex flex-col items-center">
            {#if published}
                <div class="text-sm opacity-70 mb-2">Please consider citing our publication in research outputs</div>	
                <a href="https://github.com/esteinig/brick" target="_blank" rel="noreferrer"><code class="text-xs opacity-100">Steinig et al. (2024) - BRICK: bacterial genome annotation and identity visualisation - Microbial Genomics (or similar)</code></a>
            {:else}
                <a href="https://github.com/esteinig/brick" target="_blank" rel="noreferrer"><code class="text-xs opacity-100">https://github.com/esteinig/brick</code></a>
            {/if}
        </div>    
    </div>
</div>