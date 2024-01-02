<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let title = '';
    export let titleColor = '';

    let editing = false;

    const dispatch = createEventDispatcher();

    function updateTitle(event: any) {
        dispatch('update', { newTitle: title });
        editing = false; 
    }

    function updateTitleWithEnter(event: any) {
        if (event.keyCode === 13){
            dispatch('update', { newTitle: title });
            editing = false;
        }
    }

    function startEditing() {
        editing = true; // Start editing when the text is 
    }
</script>

<div class="flex items-center align-center truncate w-full pr-4">
    {#if editing}
        <input class="input p-1 pl-2 w-full" style="color: {titleColor}" type="text" bind:value={title} on:keypress={updateTitleWithEnter} on:blur={updateTitle}  />
    {:else}
        <span role="none" class='cursor-text p-1' style="color: {titleColor}" on:click={startEditing}>{title}</span>
    {/if}
</div>