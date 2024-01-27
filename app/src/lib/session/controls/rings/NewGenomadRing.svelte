<script lang="ts">
    import { getSessionFileById } from "$lib/stores/SessionFileStore";
    import { requestInProgress, startRequestState } from '$lib/stores/RequestInProgressStore';
	import { type GenomadRingSchema, GenomadPredictionClass, RingType } from "$lib/types";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
	import { createEventDispatcher } from "svelte";
	import { capitalize } from "$lib/helpers";
    
    const dispatch = createEventDispatcher();

    
    let ringConfig: GenomadRingSchema = {
        reference: null,
        window_size: 10000,
        min_window_score: 0.5,
        min_segment_score: 0.7,
        min_segment_length: 10000,
        prediction_classes: [GenomadPredictionClass.PLASMID, GenomadPredictionClass.VIRUS],
        ring_type: RingType.LABEL
    }

    function isNumberInRange(value: string | number): boolean {
        const num = typeof value === 'string' ? parseFloat(value) : value;
        return !isNaN(num) && num >= 0 && num <= $ringReferenceStore.sequence.length;
    }

    function isNumberValidProbability(value: string | number): boolean {
        const num = typeof value === 'string' ? parseFloat(value) : value;
        return !isNaN(num) && num >= 0 && num <= 1.0;
    }

    function isNumberRecommendedSegmentLength(value: string | number): boolean {
        const num = typeof value === 'string' ? parseFloat(value) : value;
        return !isNaN(num) && num % ringConfig.window_size === 0;
    }



    $: windowInputValidationClass = isNumberInRange(ringConfig.window_size) ? ringConfig.window_size === 10000 ? '' : 'input-success' : 'input-error';
    $: windowScoreInputValidationClass = isNumberValidProbability(ringConfig.min_window_score) ? ringConfig.min_window_score === 0.5 ? '' : 'input-success' : 'input-error';
    $: segmentScoreInputValidationClass = isNumberValidProbability(ringConfig.min_segment_score) ? ringConfig.min_segment_score === 0.7 ? '' : 'input-success' : 'input-error';
    $: segmentLengthInputValidationClass = isNumberRecommendedSegmentLength(ringConfig.min_segment_length) ? ringConfig.min_segment_length === 10000 ? '' : 'input-success' : 'input-warning';


    // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData()

        ringConfig.reference = $ringReferenceStore;

        data.append('ring_config', JSON.stringify(ringConfig))
        data.append('ring_type', RingType.GENOMAD)

        ringConfig = {
            reference: null,
            window_size: 10000,
            min_window_score: 0.5,
            min_segment_score: 0.7,
            min_segment_length: 10000,
            prediction_classes: [GenomadPredictionClass.PLASMID, GenomadPredictionClass.VIRUS],
            ring_type: RingType.LABEL
        } // reset

        startRequestState();

        // Instead of executing the action request we dispatch the
        // data to the parent component (RingControlPanel) and from
        // there to the overall Interface component, so that the 
        // form action results can be handled while the user is 
        // navigating or doing other things - this allows also for
        // long running requests in the background!

        dispatch('submitAction', { action: event.currentTarget.action, body: data});

	}

</script>

<div class="border border-gray-300 rounded-2xl border-opacity-10 p-4">
    <p class="opacity-60 mb-2">geNomad Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">
        geNomad rings visualize predictions for chromsomal, plasmid or viral origin on non-overlapping windows along a reference sequence. 
        Scores between 0 and 1 are computed for each origin prediction and can be added as a label, annotation or probability ring.
    </p>
    
    {#if $ringReferenceStore}
        
        <form id="createGenomadRing" action="?/createRing" method="POST" on:submit|preventDefault={handleSubmit}>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-4 my-3 items-center">
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Reference</p>
                        <input id="genomadReferenceFile" class="input text-xs" disabled value={getSessionFileById($ringReferenceStore.reference_id)?.name_original}/>
                    </label>
                </div>
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Ring type</p>
                        <select id="genomadRingType" class="select text-xs" bind:value={ringConfig.ring_type}>
                            <option value={RingType.ANNOTATION}>{capitalize(RingType.ANNOTATION)}</option>
                            <option value={RingType.LABEL}>{capitalize(RingType.LABEL)}</option>
                            <option value={RingType.GENOMAD}>Probability</option>
                        </select>
                    </label>
                </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-4 my-3 items-center">
                <label class="label text-xs">
                    <p class="opacity-40">Window size (bp)</p>
                    <input id="genomadWindowSize" class="input text-xs {windowInputValidationClass}" type="text" bind:value={ringConfig.window_size} />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Minimum window score</p>
                    <input id="genomadProbability" class="input text-xs {windowScoreInputValidationClass}" type="text" bind:value={ringConfig.min_window_score} />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Minimum total segment length (bp)</p>
                    <input id="genomadSegmentLength" class="input text-xs {segmentLengthInputValidationClass}" type="text" bind:value={ringConfig.min_segment_length} />
                </label>
                <label class="label text-xs">
                    <p class="opacity-40">Minimum average segment score</p>
                    <input id="genomadProbability" class="input text-xs {segmentScoreInputValidationClass}" type="text" bind:value={ringConfig.min_segment_score} />
                </label>
            </div>
            
            <div class="flex justify-right mt-6">
                <button class="btn variant-outline-surface" type="submit" disabled={!$ringReferenceStore}>
                    <div class="flex items-center align-center">
                        <span>Construct</span>
                    </div>
                </button>
            </div>
        </form>
    {/if}
</div>