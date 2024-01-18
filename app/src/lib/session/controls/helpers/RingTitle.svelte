<script lang="ts">
	import type { RingUpdateSchema } from '$lib/types';
    import { createEventDispatcher, tick } from 'svelte';
	import { applyAction, enhance } from "$app/forms";
	import { page } from "$app/stores";
    import { ToastType, triggerToast } from "$lib/helpers";
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { completeRequestState, startRequestState } from "$lib/stores/RequestInProgressStore";
    
    const toastStore = getToastStore();

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

</script>

<div id="editableRingTitle-{id}">
    <div class="flex items-center align-center w-full pr-4 truncate">
        {#if editing}
            <form id="updateRingTitleForm-{id}" bind:this={formElement} action="?/updateSessionRing" method="POST" use:enhance={({ formData }) => {
                    
                if (updateVerbose) startRequestState();
                
                sessionRingUpdateSchema.id = id;
                sessionRingUpdateSchema.title = title;

                formData.append('session_id', $page.params.session);
                formData.append('ring_update', JSON.stringify(sessionRingUpdateSchema));

                sessionRingUpdateSchema.color = null;
                sessionRingUpdateSchema.id = "";

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
                <input bind:this={inputElement} class="input p-1 pl-2 w-full truncate" style="color: {titleColor}" type="text" bind:value={title} on:keypress={updateTitleWithEnter} on:blur={updateTitle}  />
            </form>
        {:else}
            <span role="none" class='cursor-text p-1 truncate' style="color: {titleColor}" on:click={startEditing}>{title}</span>
        {/if}
    </div>
</div>