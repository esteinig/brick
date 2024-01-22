<script lang="ts">
    import { createEventDispatcher } from 'svelte';
	import { applyAction, enhance } from "$app/forms";
	import { page } from "$app/stores";
    import { ToastType, triggerToast } from "$lib/helpers";
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { completeRequestState, startRequestState } from "$lib/stores/RequestInProgressStore";
	import type { RingUpdateSchema } from '$lib/types';
    
    const toastStore = getToastStore();

    type RingId = string;

    // Ring identifier used for element identifier and database update 
    export let id: RingId; 
    export let indexGroup: RingId[];
    
    // Whether to update the color in the database session
    export let updateDatabase: boolean = true;
    // Show status of request loading and success toasts
    export let updateVerbose: boolean = false;

    let formElement: HTMLFormElement;
    
    // Events dispatched
    const dispatch = createEventDispatcher();

    function deleteRing() {
        dispatch('delete', { updateVerbose: updateVerbose, updateDatabase: updateDatabase });
        if (updateDatabase) formElement.requestSubmit();
    }

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

<div id={`deleteRing-${id}`}>
    <div class="flex items-center align-center w-full pr-4 truncate">

            <form id="deleteRingForm-{id}" bind:this={formElement} action="?/deleteSessionRing" method="POST" use:enhance={({ formData }) => {
                    
                if (updateVerbose) startRequestState();
                
                sessionRingUpdateSchema.id = id;
                sessionRingUpdateSchema.index_group = indexGroup;

                formData.append('session_id', $page.params.session);
                formData.append('ring_update', JSON.stringify(sessionRingUpdateSchema));

                sessionRingUpdateSchema.index_group = null;
                sessionRingUpdateSchema.id = "";

                return async ({ result }) => {
                    await applyAction(result);

                    if (updateVerbose) completeRequestState();

                        
                    if (result.type === "success"){
                        if (updateVerbose) triggerToast("Ring deleted sucessfully", ToastType.SUCCESS, toastStore);
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
            <button class="btn btn-icon h-4 w-4 ml-4 mr-4" type="button" on:click={deleteRing}>
                <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </button>
            
        </form>
    </div>
</div>