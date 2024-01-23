<script lang="ts">
	import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function dispatchFontChange() {
        
        dispatch('change', { 
            italic: italic,
            bold: bold,
            code: code
        });


    }
    export let italic: boolean = false;
    export let bold: boolean = false;
    export let code: boolean = false;

</script>

<div>
    <button class="chip {italic ? 'variant-filled': 'variant-soft'} m-1" on:click={() => { italic = !italic; dispatchFontChange()}} on:keypress={() => { italic = !italic; dispatchFontChange() }}>
        {#if italic}
            <span>
                <svg class="w-2 h-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m4.5 12.75 6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </span>
        {/if}
        <span class="">Italic</span>
    </button>
    <button class="chip {bold ? 'variant-filled': 'variant-soft'} m-1" on:click={() => { bold = !bold; dispatchFontChange() }} on:keypress={() =>  { bold = !bold; dispatchFontChange() } }>
        {#if bold}
            <span>
                <svg class="w-2 h-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m4.5 12.75 6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </span>
        {/if}
        <span class="">Bold</span>
    </button>
    <button class="chip {code ? 'variant-filled': 'variant-soft'} m-1" on:click={() => { code = !code; dispatchFontChange() }} on:keypress={() => { code = !code; dispatchFontChange() }}>
        {#if code}
            <span>
                <svg class="w-2 h-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="m4.5 12.75 6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </span>
        {/if}
        <span class="">Code</span>
    </button>

</div>