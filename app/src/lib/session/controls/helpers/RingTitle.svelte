<script lang="ts">
	import type { RingUpdateSchema } from '$lib/types';
    import { createEventDispatcher, tick } from 'svelte';
	import { page } from "$app/stores";
	import { startRequestState } from "$lib/stores/RequestInProgressStore";
    

    type RingId = string;

    // Ring identifier used for element identifier and database update 
    export let id: RingId; 
    export let title: string;
    export let titleColor: string = '#d3d3d3';

    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    let inputElement: HTMLInputElement;
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

    // Events dispatched
    const dispatch = createEventDispatcher();

    function updateTitle() {
        dispatch('update', { title: title });
        editing = false; 
        if (updateDatabase) formElement.requestSubmit();
    }

    function updateTitleWithEnter(event: any) {
        if (event.key === 'Enter'){
            dispatch('update', { title: title });
            editing = false;
            if (updateDatabase) formElement.requestSubmit();
        }
    }

    // State changes

    let editing = false;

    async function startEditing() {
        editing = true;
        await tick();
        inputElement.focus();
        inputElement.select();
    }

    // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData();

        if (updateVerbose) startRequestState();
                
        sessionRingUpdateSchema.id = id;
        sessionRingUpdateSchema.title = title;

        data.append('session_id', $page.params.session);
        data.append('ring_update', JSON.stringify(sessionRingUpdateSchema));

        sessionRingUpdateSchema.color = null;
        sessionRingUpdateSchema.id = "";

        dispatch('submitAction', { action: event.currentTarget.action, body: data, updateVerbose: updateVerbose, updateDatabase: updateDatabase });

	}

</script>

<div id="editableRingTitle-{id}">
    <div class="flex items-center align-center w-full pr-4 truncate">
        {#if editing}
            <form id="updateRingTitleForm-{id}" bind:this={formElement} action="?/updateSessionRing" method="POST" on:submit|preventDefault={handleSubmit}>
                <input bind:this={inputElement} class="input p-1 pl-2 w-full truncate" style="color: {titleColor}" type="text" bind:value={title} on:keypress={updateTitleWithEnter} on:blur={updateTitle}  />
            </form>
        {:else}
            <span role="none" class='cursor-text p-1 truncate' style="color: {titleColor}" on:click={startEditing}>{title}</span>
        {/if}
    </div>
</div>