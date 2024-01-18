<script lang="ts">
	import { RingDirection, type RingUpdateSchema } from '$lib/types';
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
    export let direction: RingDirection;
    export let currentIndex: number;
    export let indexGroup: RingId[];

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


</script>

<div id="updateRingIndex-{id}">
    <div class="flex items-center align-center w-full pr-4 truncate">
        <form id="updateRingIndexForm-{id}" bind:this={formElement} action="?/updateSessionRing" method="POST" use:enhance={({ formData }) => {
                
            if (updateVerbose) startRequestState();
            
            sessionRingUpdateSchema.id = id;
            sessionRingUpdateSchema.index = newIndex;
            sessionRingUpdateSchema.index_group = indexGroup;

            formData.append('session_id', $page.params.session);
            formData.append('ring_update', JSON.stringify(sessionRingUpdateSchema));

            sessionRingUpdateSchema.index = null;
            sessionRingUpdateSchema.index_group = null;
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
           {#if direction === RingDirection.IN}
                <button class="btn btn-icon h-4 w-4" type="button" on:click={updateIndex}>
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>
            {:else}
                <button class="btn btn-icon h-4 w-4" type="button" on:click={updateIndex}>
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </button>
            {/if}
        </form>
    
    </div>
</div>