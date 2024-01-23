<script lang="ts">
    import { RingType, type Sequence, RingDirection, Ring, FileFormat, type ActionRequestData, type ActionRequestDataUpdate } from "$lib/types";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles } from "$lib/stores/SessionFileStore";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
    import { changeRingTitle, moveRingInside, moveRingOutside, removeRing, isRingTypePresent, toggleRingVisibility, changeRingColor, rings} from "$lib/stores/RingStore";

	import NewReferenceRing from "$lib/session/controls/rings/NewReferenceRing.svelte";
	import NewBlastRing from "$lib/session/controls/rings/NewBlastRing.svelte";
	import NewAnnotationRing from "../rings/NewAnnotationRing.svelte";

    import { tooltip } from "$lib/stores/TooltipStore";
	import NewLabelRing from "../rings/NewLabelRing.svelte";
	import RingTitle from "../helpers/RingTitle.svelte";
	import PalettePopup from "$lib/session/palette/PalettePopup.svelte";

    import { createFilteredRingsStore } from '$lib/stores/RingStore';
    import { requestInProgress } from '$lib/stores/RequestInProgressStore';
	import ColorPicker from "$lib/session/palette/ColorPicker.svelte";
	import RingVisibility from "$lib/session/controls/helpers/RingVisibility.svelte";
	import DeleteRing from "../helpers/DeleteRing.svelte";
	import RingIndex from "../helpers/RingIndex.svelte";

	import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    $: ringData = createFilteredRingsStore($ringReferenceStore) // reactive so it updates on changes to reference sequence

    let newRing: RingType;
    let showNewRingMenu: boolean = false;

    let selectedReference: SessionFile | null;
    let selectedSequence: Sequence | null;
    
    let previousReference: SessionFile | null = null;
    
    // Automatically select the first sequence if it exists
    $: if (selectedReference !== previousReference) {
        previousReference = selectedReference; // update previous

        if (selectedReference && selectedReference.selections && selectedReference.selections.sequences.length > 0) {
            selectedSequence = selectedReference.selections.sequences[0];
        } else {
            selectedSequence = null;
        }
    }

    // Not very nice, needs refactoring
    $: if (selectedSequence) {

        $ringReferenceStore = {
            session_id: selectedReference?.session_id ?? "", 
            reference_id: selectedReference?.id ?? "", 
            sequence: { 
                id: selectedSequence?.id ?? "", 
                length: selectedSequence?.length ?? 0 
            }
        }
    }

    // Get the ring identifiers from the other rings
    // in the current filtered ring store to update
    // their indices if the index / position of a 
    // ring is changed
    $: indexGroup = $ringData.map(ring => ring.id);


    async function handleCreateRingRequest(data: ActionRequestData) {
        dispatch("createRingAction", data)
    }

    async function handleUpdateRingRequest(data: ActionRequestDataUpdate) {
        dispatch("updateRingAction", data)
    }
    
    async function handleDeleteRingRequest(data: ActionRequestDataUpdate) {
        dispatch("deleteRingAction", data)
    }

</script>


    
    

<div id="brickRingControlPanel" class="p-2 text-base">

    <div class="mb-8">
        <p class="opacity-60 mb-2">Reference</p>

        {#if $sessionFiles.length}
            <div class="grid grid-cols-4 sm:grid-cols-4 md:grid-cols-4 gap-4 my-3">
                <div class="col-span-2">
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
                    <div class="col-span-2">
                        <label class="label text-xs">
                            <p class="opacity-40">Select a reference sequence</p>
                            <select class="select text-xs" bind:value={selectedSequence}>
                                {#each selectedReference.selections.sequences as seq}
                                    <option value={seq}>{seq.id}</option>
                                {/each}
                            </select>
                        </label>
                    </div>        
                {/if}
            </div>
        {:else}
            <p class="opacity-90 p-4 text-sm">No reference genomes have been uploaded</p>
        {/if}
    </div>  
    

    {#if showNewRingMenu}
        <div>
            <p class="opacity-60 mb-2">Basic rings</p>
            <div class="p-2">
                <div class="grid grid-cols-4 sm:grid-cols-4 md:grid-cols-4 gap-4 my-3">
                    <button class="btn {newRing === RingType.REFERENCE ? 'variant-ghost-primary' : 'variant-ringed-primary'}" disabled={!selectedReference || $requestInProgress ? true : false} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center truncate">
                            <span>Reference</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.ANNOTATION ? 'variant-ghost-primary' : 'variant-ringed-primary'}" disabled={!selectedReference || $requestInProgress ? true : false}  on:click={() => newRing = RingType.ANNOTATION}>
                        <div class="flex items-center align-center truncate">
                            <span>Annotations</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.BLAST ? 'variant-ghost-secondary' : 'variant-ringed-secondary'}" disabled={!selectedReference || $requestInProgress ? true : false}  on:click={() => newRing = RingType.BLAST}>
                        <div class="flex items-center align-center truncate">
                            <span>BLAST</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.LABEL ? 'variant-ghost-secondary' : 'variant-ringed-secondary'}" disabled={!selectedReference || $requestInProgress ? true : false}  on:click={() => newRing = RingType.LABEL}>
                        <div class="flex items-center align-center truncate">
                            <span>Labels</span>
                        </div>
                    </button>
                </div>                
            </div>
            <p class="opacity-60 mt-4 mb-2">Specialty rings</p>
            <div class="p-2">
                <div class="grid grid-cols-4 sm:grid-cols-4 md:grid-cols-4 gap-4 my-3">
                    <button class="btn variant-outline-surface" disabled={selectedReference ? true : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center truncate">
                            <span>abritAMR</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface" disabled={selectedReference ? true : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center truncate">
                            <span>geNomad</span>
                        </div>
                    </button>
                    <button class="btn variant-outline-surface" disabled={selectedReference ? true : true} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center truncate">
                            <span>LLM</span>
                        </div>
                    </button>
                </div>                
            </div>
        </div>
        
        <div class="mt-8">
            {#if newRing == RingType.REFERENCE}
                <NewReferenceRing on:submitAction={(event) => handleCreateRingRequest(event.detail)}></NewReferenceRing>
            {:else if newRing == RingType.BLAST}
                <NewBlastRing on:submitAction={(event) => handleCreateRingRequest(event.detail)}></NewBlastRing>
            {:else if newRing == RingType.ANNOTATION}
                <NewAnnotationRing on:submitAction={(event) => handleCreateRingRequest(event.detail)}></NewAnnotationRing>
            {:else if newRing == RingType.LABEL}
                <NewLabelRing on:submitAction={(event) => handleCreateRingRequest(event.detail)}></NewLabelRing>
            {/if}
        </div>

    {:else}

        {#if $ringData.length}
            <div>
                <p class="opacity-60 mb-2">Rings</p>
                    {#each $ringData as ring}
                        <div class="grid grid-cols-8 gap-x-2 items-center align-center p-2 rounded-token hover:variant-soft hover:cursor-pointer">
                            <div class="flex items-center gap-x-2 col-span-7">
                                <span class="text-black ml-2">
                                    <ColorPicker id={ring.id} color={ring.color} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:selectColor={(event) => changeRingColor(ring.id, event.detail.color)}></ColorPicker>
                                </span>
                                <div class="mt-0.5">
                                    <PalettePopup id={ring.id} color={ring.color} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:selectColor={(event) => changeRingColor(ring.id, event.detail.color)}></PalettePopup>
                                </div>
                                <RingVisibility id={ring.id} visible={ring.visible} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:toggleVisibility={(_) => toggleRingVisibility(ring.id)}></RingVisibility>
                                <RingTitle id={ring.id} title={ring.title} titleColor={ring.color} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:update={(event) => changeRingTitle(ring.id, event.detail.title)} />
                            </div>
                            <div class="flex justify-end gap-x-2 col-span-1">
                                {#if ring.type !== RingType.LABEL}
                                    {#if ring.index !== 0}
                                        <RingIndex id={ring.id} direction={RingDirection.IN} currentIndex={ring.index} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:update={(_) => moveRingInside(ring.id)} indexGroup={indexGroup}></RingIndex>
                                    {:else}
                                        <RingIndex placeholder id={ring.id} direction={RingDirection.IN} currentIndex={ring.index} indexGroup={indexGroup}></RingIndex>
                                    {/if}
                                    {#if !((isRingTypePresent(RingType.LABEL) && ring.index === $ringData.length-2) || ring.index === $ringData.length-1)}
                                        <RingIndex id={ring.id} direction={RingDirection.OUT} currentIndex={ring.index} on:submitAction={(event) => handleUpdateRingRequest(event.detail) } on:update={(_) => moveRingOutside(ring.id, $ringData.length-1)} indexGroup={indexGroup}></RingIndex>
                                    {:else}
                                        <RingIndex placeholder id={ring.id} direction={RingDirection.OUT} currentIndex={ring.index} indexGroup={indexGroup}></RingIndex>
                                    {/if}
                                {/if}
                                <DeleteRing id={ring.id} indexGroup={indexGroup} on:submitAction={(event) => handleDeleteRingRequest(event.detail)} on:delete={() => removeRing(ring.id, indexGroup)}></DeleteRing>
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
            <div class="text-sm opacity-90">
                <button class="btn p-1" on:click={() => showNewRingMenu = false}>
                    <div class="flex items-center align-center">
                        <div class="w-7 h-7">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">Rings</span>
                    </div>
                </button>
            </div>
        {:else}
            <div class="text-sm opacity-90">
                <button class="btn p-1" on:click={() => showNewRingMenu = true}>
                    <div class="flex items-center align-center">
                        <div class="w-7 h-7">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">New ring</span>
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