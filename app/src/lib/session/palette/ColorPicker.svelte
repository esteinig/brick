<script lang="ts">
    import { createEventDispatcher } from 'svelte';
	import { page } from "$app/stores";
	import type { RingUpdateSchema } from "$lib/types";
	import { startRequestState } from "$lib/stores/RequestInProgressStore";
    
    const dispatch = createEventDispatcher();

    type RingId = string;

    // Ring identifier used for element identifier and database update 
    export let id: RingId; 

    // Color of ring - reactive to selection from picker
    // dispatches color as event accessible `on:selectColor`
    export let color: string = "#d3d3d3";

    export let size: number = 0.9;

    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;


    function selectColor(event: any) {
        
        // When a color is selected from the picker, dispatch
        // it as an event for use in the parent which changes
        // color in the ring store
        const target = event.target as HTMLInputElement;

        color = target.value;
        dispatch('selectColor', { color: target.value });

        // If the component allows for updating the value in the
        // database (atomic singular update of color on this
        // specific ring) trigger the form action

        if (updateDatabase) formElement.requestSubmit();

    }

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

     // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData();

        if (updateVerbose) startRequestState();
                
        sessionRingUpdateSchema.id = id;
        sessionRingUpdateSchema.color = color;

        data.append('session_id', $page.params.session);
        data.append('ring_update', JSON.stringify(sessionRingUpdateSchema));
        
        sessionRingUpdateSchema.id = "";
        sessionRingUpdateSchema.color = null;

        dispatch('submitAction', { action: event.currentTarget.action, body: data, updateVerbose: updateVerbose, updateDatabase: updateDatabase });

	}


</script>

<div id="colorPicker-{id}">
    <div class="grid grid-cols-[auto_1fr] gap- align-center items-center">
        <form id="updateRingColorPaletteForm" bind:this={formElement} action="?/updateSessionRing" method="POST" on:submit|preventDefault={handleSubmit}>
            <input id="colorPickerInput-{id}" class="input" style="height: {size}rem; width: {size}rem;" type="color" value={color} on:change={(event) => selectColor(event)}/>
        </form>
    </div>
</div>