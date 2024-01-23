<script lang="ts">
	import { RingDirection, type RingUpdateSchema } from '$lib/types';
    import { createEventDispatcher } from 'svelte';
	import { page } from "$app/stores";
	import { startRequestState } from "$lib/stores/RequestInProgressStore";
    

    type RingId = string;

    // Ring identifier used for element identifier and database update 
    export let id: RingId; 
    export let direction: RingDirection;
    export let currentIndex: number;
    export let indexGroup: RingId[];

    export let placeholder: boolean = false;

    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    let formElement: HTMLFormElement;
    let newIndex: number;
    
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

    function updateIndex() {
        newIndex = direction === RingDirection.IN ? currentIndex-1 : currentIndex+1
        dispatch('update', { index: newIndex });

        if (updateDatabase) formElement.requestSubmit();
    }

    // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        let data = new FormData();

        if (updateVerbose) startRequestState();
                
        sessionRingUpdateSchema.id = id;
        sessionRingUpdateSchema.index = newIndex;
        sessionRingUpdateSchema.index_group = indexGroup;

        data.append('session_id', $page.params.session);
        data.append('ring_update', JSON.stringify(sessionRingUpdateSchema));

        sessionRingUpdateSchema.index = null;
        sessionRingUpdateSchema.index_group = null;
        sessionRingUpdateSchema.id = "";

        dispatch('submitAction', { action: event.currentTarget.action, body: data, updateVerbose: updateVerbose, updateDatabase: updateDatabase });

	}


</script>

<div id="updateRingIndex-{id}" class="{placeholder ? 'invisible' : ''}">
    <div class="flex items-center align-center w-full pr-4 truncate">
        <form id="updateRingIndexForm-{id}" bind:this={formElement} action="?/updateSessionRing" method="POST" on:submit|preventDefault={handleSubmit}>
           {#if direction === RingDirection.IN}
                <button class="btn btn-icon h-4 w-4" type="button" on:click={updateIndex} disabled={placeholder}>
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>
            {:else}
                <button class="btn btn-icon h-4 w-4" type="button" on:click={updateIndex} disabled={placeholder}>
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>
            {/if}
        </form>
    
    </div>
</div>