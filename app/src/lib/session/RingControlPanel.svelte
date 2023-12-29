<script lang="ts">
    import type { Ring } from "$lib/types";
    import ColorPicker from 'svelte-awesome-color-picker';
	import { ListBox, ListBoxItem } from "@skeletonlabs/skeleton";
	import type { PlotConfig } from "$lib/brick/types";

    export let rings: Ring[];
    export let config: PlotConfig;

    let selectedRingIndex: string = "";

</script>

<div id="brickRingControlPanel" class="p-2 text-base">

    <ListBox class="my-5" active="variant-soft">
        {#each rings as ring}
            <ListBoxItem bind:group={selectedRingIndex} name="medium" value={ring.index}>
                <div class="flex items-center align-center gap-x-2">
                    {#if ring.visible}
                        <button class="btn btn-icon h-4 w-4" on:click={() => ring.visible ? ring.visible = false : ring.visible = true}>
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </button>
                    {:else}
                        <button class="btn btn-icon h-4 w-4" on:click={() => ring.visible ? ring.visible = false : ring.visible = true}>
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </button>
                    {/if}
                    <span style="color: {ring.color}" class="mr-3 ml-1">Ring {ring.index}</span>
                    
                    <button class="btn btn-icon h-4 w-4" style="color: {ring.color};">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                    </button>
                    <span class="text-black -ml-1 mr-2"><ColorPicker --input-size="0.75rem" label="" bind:hex={ring.color}></ColorPicker></span>
                    
                    <span class="ml-2 {ring.title.italic ? 'italic':''} {ring.title.code ? 'code': ''}">{ring.title.text}</span>
                    
                </div>
            </ListBoxItem>
        {/each}
    </ListBox>
    <div class="flex">
        <button class="btn variant-outline-surface ml-2">

            <div class="flex items-center align-center">
                <div class="w-5 h-5 mr-2 ">
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </div>
                <span>Reference</span>
             </div>
        </button>
        <button class="btn variant-outline-surface ml-2">
            <div class="flex items-center align-center">
                <div class="w-5 h-5 mr-1.5">
                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 4.5v15m7.5-7.5h-15" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                </div>
                <span>Annotation</span>
            </div>
        </button>
    </div>
</div>