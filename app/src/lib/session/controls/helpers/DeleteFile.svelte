<script lang="ts">
    import { createEventDispatcher } from 'svelte';
	import { page } from "$app/stores";
	import { startRequestState } from "$lib/stores/RequestInProgressStore";
    
    type FileId = string;

    // Ring identifier used for element identifier and database update 
    export let id: FileId; 
    
    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    let formElement: HTMLFormElement;
    
    // Events dispatched
    const dispatch = createEventDispatcher();

    function deleteFile() {
        dispatch('delete', { delete: true });
        if (updateDatabase) formElement.requestSubmit();
    }

    // Manual form action, dispatches the action request fetch function after populating 
    // it with this components value to interface, so it can run in the background - 
	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		
        if (updateVerbose) startRequestState();
        
        let data = new FormData();
                
        data.append('session_id', $page.params.session);
        data.append('file_id', id);

        dispatch('submitAction', { action: event.currentTarget.action, body: data, updateVerbose: updateVerbose, updateDatabase: updateDatabase });
	}

    // Do reload the session data, so that the files 
    // are not reconstituded when empty 
    // invalidate("app:session")

</script>

<div id={`deleteRing-${id}`}>
    <div class="flex items-center align-center w-full pr-4 truncate">

            <form id="deleteFileForm-{id}" bind:this={formElement} action="?/deleteSessionFile" method="POST" on:submit|preventDefault={handleSubmit}>
            <button class="btn btn-icon h-4 w-4 ml-4 mr-4" type="button" on:click={deleteFile}>
                <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </button>
            
        </form>
    </div>
</div>