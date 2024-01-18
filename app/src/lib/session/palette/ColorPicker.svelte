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

    // Color of ring - reactive to selection from picker
    // dispatches color as event accessible `on:selectColor`
    export let color: string = "#d3d3d3";

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


</script>

<div id="colorPicker-{id}">
    <div class="grid grid-cols-[auto_1fr] gap- align-center items-center">
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
            <input id="colorPickerInput-{id}" class="input" style="height: 0.9rem; width: 0.9rem;" type="color" value={color} on:change={(event) => selectColor(event)}/>
        </form>
    </div>
</div>