<script lang="ts">
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

    // Current visibility
    export let visible: boolean = false;

    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    function toggleVisibility(visibility: boolean) {
        
        // When a color is selected from the palette, dispatch
        // it as an event for use in the parent which changes
        // color in the ring store
        visible = visibility;
        dispatch('toggleVisibility', { visibility: visibility });

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

</script>

<div id={`ringVisibilityToggle-${id}`}>

    <form id="updateRingColorPaletteForm" bind:this={formElement} action="?/updateSessionRing" method="POST" use:enhance={({ formData }) => {
                    
        if (updateVerbose) startRequestState();
            
        sessionRingUpdateSchema.id = id;
        sessionRingUpdateSchema.visible = visible;

        formData.append('session_id', $page.params.session);
        formData.append('ring_update', JSON.stringify(sessionRingUpdateSchema));
            
        sessionRingUpdateSchema.id = "";
        sessionRingUpdateSchema.visible = null;

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
        {#if visible}
            <button class="btn btn-icon h-4 w-4 mr-4" on:click={() => toggleVisibility(false)}>
                <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" stroke-linecap="round" stroke-linejoin="round"></path>
                    <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </button>
        {:else}
            <button class="btn btn-icon h-4 w-4 mr-4" on:click={() => toggleVisibility(true)}>
                <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </button>
        {/if}
    </form>
</div>