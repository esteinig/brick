<script lang="ts">
    import { popup, type PopupSettings } from "@skeletonlabs/skeleton";
    import { paletteStore } from "$lib/stores/PaletteStore";
	import ColorPalette from "./ColorPalette.svelte";
    import { createEventDispatcher } from 'svelte';
	import { applyAction, enhance } from "$app/forms";
	import { page } from "$app/stores";
    import { ToastType, triggerToast } from "$lib/helpers";
    import { getToastStore } from '@skeletonlabs/skeleton';
	import type { RingUpdateSchema } from "$lib/types";
	import { completeRequestState, startRequestState } from "$lib/stores/RequestInProgressStore";
    
    const dispatch = createEventDispatcher();
    const toastStore = getToastStore();

    type RingId = string;

    // Ring identifier used for element identifier and database update 
    export let id: RingId; 

    // Color of ring - reactive to selection from palette
    // dispatches color as event accessible `on:selectColor`
    export let color: string = "#d3d3d3";

    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    function selectColor(event: any) {
        
        // When a color is selected from the palette, dispatch
        // it as an event for use in the parent which changes
        // color in the ring store
        
        color = event.detail.color;
        dispatch('selectColor', { color: event.detail.color });

        // If the component allows for updating the value in the
        // database (atomic singular update of color on this
        // specific ring) trigger the form action

        if (updateDatabase) formElement.requestSubmit();

    }
    
    const popupPalette: PopupSettings = {
        // Represents the type of event that opens/closed the popup
        event: 'click',
        // Matches the data-popup value on your popup element
        target: `popupPalette-${id}`,
        // Defines which side of your trigger the popup will appear
        placement: 'left',
        closeQuery: '#will-close'
    };

    let formElement: HTMLFormElement;

    let sessionRingUpdateSchema: RingUpdateSchema = {
        id: "",
        index: null,
        color: null,
        height: null,
        title: null,
        visible: null,
        index_group: null
    }

</script>

<div id="palettePopup-{id}">
    
    <button class="btn btn-icon h-4 w-4" style="color: {color};" use:popup={popupPalette} type="button">
        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
    </button>

    <div class="card p-4  shadow-xl border border-opacity-80 border-surface-500 bg-surface-300 z-50" data-popup={`popupPalette-${id}`}>

        <form id="updateRingColorPaletteForm" bind:this={formElement} action="?/updateSessionRing" method="POST" use:enhance={({ formData }) => {
            
            if (updateVerbose) startRequestState();
            
            sessionRingUpdateSchema.id = id;
            sessionRingUpdateSchema.color = color;

            formData.append('session_id', $page.params.session);
            formData.append('ring_update', JSON.stringify(sessionRingUpdateSchema));
            
            sessionRingUpdateSchema.id = "";
            sessionRingUpdateSchema.color = null;

            return async ({ result }) => {
                await applyAction(result);

                if (updateVerbose) completeRequestState();

                if (result.type === "success"){
                    if (updateVerbose) triggerToast("Ring updated sucessfully", ToastType.SUCCESS, toastStore);
                } else {
                    // Validation errors from pydantic schemes are an array of validation objects:
                    if ($page.form.detail instanceof Array){
                        for (const error of $page.form.detail) {
                            triggerToast(
                                error.msg ?? `Error ${result.status}: an unknown error occurred`, 
                                ToastType.ERROR, 
                                toastStore
                            );
                        }
                    } else {
                        triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
                    }
                }
            };

        }}>
            <div class="head mb-4 flex justify-between items-center align-middle">
                <p class="opacity-80 text-lg">Palette selections</p>
                
                <button id="will-close" class="btn" type="button">
                    <svg class="w-6 h-6" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>

            </div>
            <div class="body">
                {#each $paletteStore as palette}
                    <div class="my-4">
                        <ColorPalette colors={palette.colors} title={palette.name} subtitle={palette.subtitle} hoverDisplay={false} on:selectColor={selectColor}/>
                    </div>
                {/each}
            </div>
        </form>
    </div>
</div>