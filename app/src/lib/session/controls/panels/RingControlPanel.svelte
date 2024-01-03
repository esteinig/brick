<script lang="ts">
    import { RingType } from "$lib/types";
    import ColorPicker from 'svelte-awesome-color-picker';
	import type { PlotConfig } from "$lib/types";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles } from "$lib/stores/SessionFileStore";
    import { changeRingTitle, moveRingInside, moveRingOutside, removeRing, rings } from "$lib/stores/RingStore";

	import NewReferenceRing from "$lib/session/controls/rings/NewReferenceRing.svelte";
	import NewBlastRing from "$lib/session/controls/rings/NewBlastRing.svelte";
	import NewAnnotationRing from "../rings/NewAnnotationRing.svelte";

    import { tooltip } from "$lib/stores/TooltipStore";
	import NewLabelRing from "../rings/NewLabelRing.svelte";
	import EditableTitle from "../helpers/EditableTitle.svelte";

    export let config: PlotConfig;

    let newRing: RingType;

    let selectedReference: SessionFile;
    let showNewRingMenu: boolean = false;

    function handleTitleUpdate(event: any, index: number) {
        changeRingTitle(index, event.detail.newTitle)
    }

</script>

<div id="brickRingControlPanel" class="p-2 text-base">
    <div class="mb-8">
        <p class="opacity-60 mb-2">Reference</p>

        {#if $sessionFiles.length}
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3">
                <div>
                    <label class="label text-xs">
                        <p class="opacity-40">Select a reference genome</p>
                        <select class="select text-xs" bind:value={selectedReference}>
                            {#each $sessionFiles as file}
                                {#if file.type === FileType.REFERENCE}
                                    <option value={file}>{file.name_original}</option>
                                {/if}
                            {/each}
                        </select>
                    </label>
                </div>
                {#if selectedReference}
                    <div>
                        <label class="label text-xs">
                            <p class="opacity-40">Genome size (bp)</p>
                            <input class="input text-xs" disabled value={selectedReference.length ?? 0}/>
                        </label>
                    </div>            
                {/if}
            </div>
        {:else}
            <p class="opacity-100 p-4 text-sm text-error-500">No reference genomes have been uploaded</p>
        {/if}
    </div>  
    

    {#if showNewRingMenu}
        <div>
            <p class="opacity-60 mb-2">Basic rings</p>
            <div class="p-2">
                <div class="">
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center">
                            <span>Reference</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true}  on:click={() => newRing = RingType.ANNOTATION}>
                        <div class="flex items-center align-center">
                            <span>Annotations</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true}  on:click={() => newRing = RingType.BLAST}>
                        <div class="flex items-center align-center">
                            <span>BLAST</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true}  on:click={() => newRing = RingType.LABEL}>
                        <div class="flex items-center align-center">
                            <span>Labels</span>
                        </div>
                    </button>
                </div>                
            </div>
            <p class="opacity-60 mt-4 mb-2">Specialty rings</p>
            <div class="p-2">
                <div class="">
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center">
                            <span>LLM Annotation</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface mr-2" disabled={selectedReference ? false : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center">
                            <span>geNomad</span>
                        </div>
                    </button>
                </div>                
            </div>
        </div>
        
        <div class="mt-8">
            {#if newRing == RingType.REFERENCE}
                <NewReferenceRing selectedReference={selectedReference}></NewReferenceRing>
            {:else if newRing == RingType.BLAST}
                <NewBlastRing selectedReference={selectedReference}></NewBlastRing>
            {:else if newRing == RingType.ANNOTATION}
                <NewAnnotationRing selectedReference={selectedReference}></NewAnnotationRing>
            {:else if newRing == RingType.LABEL}
                <NewLabelRing selectedReference={selectedReference}></NewLabelRing>
            {/if}
        </div>

    {:else}
        {#if $rings.length}
            <div>
                <p class="opacity-60 mb-2">Rings</p>
                    {#each $rings as ring}
                            <div class="grid grid-cols-8 gap-x-2 items-center align-center p-2 rounded-token hover:variant-soft hover:cursor-pointer">
                                <div class="flex items-center gap-x-2 col-span-7">
                                    {#if ring.visible}
                                        <button class="btn btn-icon h-4 w-4 ml-4" on:click={() => ring.visible ? ring.visible = false : ring.visible = true}>
                                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" stroke-linecap="round" stroke-linejoin="round"></path>
                                                <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                                            </svg>
                                        </button>
                                    {:else}
                                        <button class="btn btn-icon h-4 w-4 ml-4" on:click={() => ring.visible ? ring.visible = false : ring.visible = true}>
                                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" stroke-linecap="round" stroke-linejoin="round"></path>
                                            </svg>
                                        </button>
                                    {/if}
                                    <button class="btn btn-icon h-4 w-4" style="color: {ring.color};">
                                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
                                            </svg>
                                    </button>
                                    <span class="text-black -ml-1 mr-4"><ColorPicker --input-size="0.75rem" label="" bind:hex={ring.color}></ColorPicker></span>
                                    <EditableTitle title={ring.title} titleColor={ring.color} on:update={(event) => handleTitleUpdate(event, ring.index)} />
                                </div>
                                <div class="flex justify-end gap-x-2 col-span-1">
                                    <button class="btn btn-icon h-4 w-4" on:click={() => moveRingInside(ring.index)}>
                                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" stroke-linecap="round" stroke-linejoin="round"></path>
                                        </svg>
                                    </button>
                                    <button class="btn btn-icon h-4 w-4" on:click={() => moveRingOutside(ring.index)}>
                                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" stroke-linecap="round" stroke-linejoin="round"></path>
                                        </svg>
                                    </button>
                                    <button class="btn btn-icon h-4 w-4 ml-4 mr-4" on:click={() => removeRing(ring.index)}>
                                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" stroke-linecap="round" stroke-linejoin="round"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                    {/each}
            </div>
        {:else}
            <p class="opacity-80 pl-4 text-sm"></p>
        {/if}
    {/if}
    
    <div class="mt-12 flex justify-start items-center">
        {#if showNewRingMenu}
            <div class="text-sm opacity-100">
                <button class="btn p-1" on:click={() => showNewRingMenu = false}>
                    <div class="flex items-center align-center">
                        <div class="w-8 h-8">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">Rings</span>
                    </div>
                </button>
            </div>
        {:else}
            <div class="text-sm opacity-100">
                <button class="btn p-1" on:click={() => showNewRingMenu = true}>
                    <div class="flex items-center align-center">
                        <div class="w-8 h-8">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">New Ring</span>
                    </div>
                </button>
            </div>
        {/if}
    </div>

    {#if $tooltip}
        <div class="mt-12">
            <p class="mt-2">
                <span class="opacity-40 mr-1">{$tooltip?.start.toLocaleString()} - {$tooltip?.end.toLocaleString()} bp{#if $tooltip?.text}: {/if}</span>
                
                <span class="opacity-60">{$tooltip?.text}</span>
                
            </p>
        </div>
    {/if}
</div>