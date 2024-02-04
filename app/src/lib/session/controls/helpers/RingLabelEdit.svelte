<script lang="ts">
	import { page } from '$app/stores';
	import { createUuid } from '$lib/helpers';
    import ColorPicker from '$lib/session/palette/ColorPicker.svelte';
	import PalettePopup from '$lib/session/palette/PalettePopup.svelte';
    import { plotConfigStore } from '$lib/stores/PlotConfigStore';
	import { startRequestState } from '$lib/stores/RequestInProgressStore';
	import type { ActionRequestDataUpdate, LabelUpdateSchema, RingSegment } from '$lib/types';
    import { createEventDispatcher } from 'svelte';

    type RingId = string;
    type LabelId = string;

    export let segment: RingSegment;
    export let labelIdentifier: LabelId;
    export let ringIdentifier: RingId;
    export let labelEditOpacity: number = 20;


    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    const dispatch = createEventDispatcher();


    function handleDelete() {
        dispatch('delete', { segment: segment });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handlePosition() {
        dispatch('changePosition', { position: position });
        if (updateDatabase) formElement.requestSubmit();
        
    }

    function handleLineAngle() {
        dispatch('changeLineAngle', { lineAngle: lineAngle });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleText() {
        dispatch('changeText', { text: segment.text });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleTextColor(color: string) {
        dispatch('changeTextColor', { textColor: color });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleTextSize() {
        dispatch('changeTextSize', { textSize: textSize });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleLineLength() {
        dispatch('changeLineLength', { lineLength: lineLength });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleLineWidth() {
        dispatch('changeLineWidth', { lineWidth: lineWidth });
        if (updateDatabase) formElement.requestSubmit();
    }

    function handleLineColor(color: string) {
        dispatch('changeLineColor', { lineColor: color });
        if (updateDatabase) formElement.requestSubmit();
    }

    let position: number = segment.start === segment.end ? segment.start : segment.start + ((segment.end - segment.start) / 2);

    let lineAngle: number = segment.lineAngle ?? 0;
    let lineLength: number = segment.lineLength ?? $plotConfigStore.labels.lineLength;
    let lineWidth: number = segment.lineWidth ?? $plotConfigStore.labels.lineWidth;
    let lineColor: string =  segment.lineColor ?? $plotConfigStore.labels.lineColor;

    let textSize: number = segment.textSize ?? $plotConfigStore.labels.textSize;
    let textColor: string = segment.textColor ?? $plotConfigStore.labels.textColor;
    
    let labelUuid: string = createUuid();
    let lineUuid: string = createUuid();

    const DEFAULT_NON_HOVER_OPACITY: number = 40;
    const DEFAULT_HOVER_OPACITY: number = 100;

    let formElement: HTMLFormElement;

    let labelUpdateSchema: LabelUpdateSchema = {
        ring_id: ringIdentifier,
        label_id: labelIdentifier,
        lineAngle: null,
        lineWidth: null,
        lineLength: null,
        lineColor: null,
        text: null,
        textSize: null,
        textColor: null
    }

    // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData();

        labelUpdateSchema = {
            ...labelUpdateSchema,
            lineAngle: lineAngle,
            lineWidth: lineWidth,
            lineLength: lineLength,
            lineColor: lineColor,
            text: segment.text,
            textSize: textSize,
            textColor: textColor
        }

        if (updateVerbose) startRequestState();
                
        data.append('session_id', $page.params.session);
        data.append('label_update', JSON.stringify(labelUpdateSchema));

        labelUpdateSchema = {
            ...labelUpdateSchema,
            lineAngle: null,
            lineWidth: null,
            lineLength: null,
            lineColor: null,
            text: null,
            textSize: null,
            textColor: null
        }

        dispatch('submitAction', { action: event.currentTarget.action, body: data, updateVerbose: updateVerbose, updateDatabase: updateDatabase } as ActionRequestDataUpdate);

	}

</script>

<form id="updateRingLabel-{labelUuid}" bind:this={formElement} action="?/updateLabel" method="POST" on:submit|preventDefault={handleSubmit}>
    <div 
        role="form" 
        class="grid grid-rows-2 gap-2 items-center align-center p-1 opacity-{labelEditOpacity}" 
        on:mouseover={() => labelEditOpacity = DEFAULT_HOVER_OPACITY} 
        on:mouseout={() => labelEditOpacity = DEFAULT_NON_HOVER_OPACITY} 
        on:focus={() => labelEditOpacity = DEFAULT_HOVER_OPACITY} 
        on:blur={() => labelEditOpacity = DEFAULT_NON_HOVER_OPACITY}
    >
        <div class="grid grid-cols-4 gap-2">

            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Label text</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={segment.text} on:change={handleText}/>
                </label>
            </div>
            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Position (bp)</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={position} on:change={handlePosition}/>
                </label>
            </div>

            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Label size (%)</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={textSize} on:change={handleTextSize}/>
                </label>
            </div>

            <div class="col-span-1 flex items-center mt-4">
                <span class="text-black ml-2 mt-1">
                    <ColorPicker id={labelUuid} size={1.0} bind:color={textColor} on:selectColor={(event) => handleTextColor(event.detail.color)}></ColorPicker>
                </span>
                <div class="mt-1 ml-2">
                    <PalettePopup id={labelUuid} size={5} bind:color={textColor} on:selectColor={(event) => handleTextColor(event.detail.color)}></PalettePopup>
                </div>
                <button class="btn btn-icon h-5 w-5 ml-4 mr-4" type="button" on:click={handleDelete}>
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>
            </div>
        </div>
        <div class="grid grid-cols-4 gap-2">
            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Line angle</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={lineAngle} on:change={handleLineAngle}/>
                </label>
            </div>
            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Line length</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={lineLength} on:change={handleLineLength} />
                </label>
            </div>
            <div class="col-span-1">
                <label class="label text-xs">
                    <p class="opacity-40">Line width</p>
                    <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={lineWidth} on:change={handleLineWidth} />
                </label>
            </div>
            <div class="col-span-1 flex items-center mt-4">
                <span class="text-black ml-2 mt-1">
                    <ColorPicker id={lineUuid} size={1.0} bind:color={lineColor} on:selectColor={(event) => handleLineColor(event.detail.color)}></ColorPicker>
                </span>
                <div class="mt-1 ml-2">
                    <PalettePopup id={lineUuid} size={5} bind:color={lineColor} on:selectColor={(event) => handleLineColor(event.detail.color)}></PalettePopup>
                </div>
            </div>
        </div>
    </div>
</form>