<script lang="ts">
	import type { RingSegment } from '$lib/types';

    export let index: number;
    export let segment: RingSegment;

    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function handleDelete() {
        dispatch('delete', { index: index });
    }

    $: segment.end = segment.start;
    
</script>

<div class="grid grid-cols-4 gap-x-2 items-center align-center p-1 rounded-token">
    <div class="col-span-1">
        <label class="label text-xs">
            <p class="opacity-40">Position</p>
            <input class="input p-1 pl-2 w-full truncate" type="number" bind:value={segment.start}/>
        </label>
    </div>
    <div class="col-span-2">
        <label class="label text-xs">
            <p class="opacity-40">Label</p>
            <input class="input p-1 pl-2 w-full truncate" type="text" bind:value={segment.text} />
        </label>
    </div>

    <div class="col-span-1 flex items-center mt-4">
        <button class="btn btn-icon h-5 w-5 ml-4 mr-4" type="button" on:click={handleDelete}>
            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
        </button>
    </div>
</div>