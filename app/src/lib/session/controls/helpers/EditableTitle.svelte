<script lang="ts">
    import { createEventDispatcher, tick } from 'svelte';

    export let title = '';
    export let titleColor = '';

    let inputElement: HTMLInputElement;
    let editing = false;

    const dispatch = createEventDispatcher();

    function updateTitle(event: any) {
        dispatch('update', { newTitle: title });
        editing = false; 
    }

    function updateTitleWithEnter(event: any) {
        if (event.key === 'Enter'){
            dispatch('update', { newTitle: title });
            editing = false;
        }
    }

    async function startEditing() {
        editing = true;
        await tick();
        inputElement.focus();
        inputElement.select()
    }
</script>

<div class="flex items-center align-center w-full pr-4 truncate">
    {#if editing}
        <input bind:this={inputElement} class="input p-1 pl-2 w-full truncate" style="color: {titleColor}" type="text" bind:value={title} on:keypress={updateTitleWithEnter} on:blur={updateTitle}  />
    {:else}
        <span role="none" class='cursor-text p-1 truncate' style="color: {titleColor}" on:click={startEditing}>{title}</span>
    {/if}
</div>