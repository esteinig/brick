<script lang="ts">
    import { RingType, type Sequence, Ring, type ActionRequestData, type ActionRequestDataUpdate } from "$lib/types";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles } from "$lib/stores/SessionFileStore";
    import { ringReferenceStore } from "$lib/stores/RingReferenceStore";
    import { changeRingTitle, moveRingInside, moveRingOutside, removeRing, toggleRingVisibility, changeRingColor, getRingById, changeLabelText, changeLabelLineLength, changeLabelTextSize, changeLabelPosition, changeLabelTextColor, changeLabelLineWidth, changeLabelLineColor, changeLabelLineAngle, removeLabel} from "$lib/stores/RingStore";

	import NewReferenceRing from "$lib/session/controls/rings/NewReferenceRing.svelte";
	import NewBlastRing from "$lib/session/controls/rings/NewBlastRing.svelte";
	import NewAnnotationRing from "../rings/NewAnnotationRing.svelte";

    import { tooltip } from "$lib/stores/TooltipStore";
	import NewLabelRing from "../rings/NewLabelRing.svelte";

    import { createFilteredRingsStore } from '$lib/stores/RingStore';
    import { requestInProgress } from '$lib/stores/RequestInProgressStore';
	import { createEventDispatcher } from "svelte";
	import NewGenomadRing from "../rings/NewGenomadRing.svelte";
	import { ListBox, ListBoxItem } from "@skeletonlabs/skeleton";
	import RingLabelEdit from "../helpers/RingLabelEdit.svelte";
	import RingSettings from "../helpers/RingSettings.svelte";
    
    export let showNewRingMenu: boolean = false;
    export let showEditRingMenu: boolean = false;


    const dispatch = createEventDispatcher();

    $: ringData = createFilteredRingsStore($ringReferenceStore) // reactive so it updates on changes to reference sequence

    let newRing: RingType;
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

    async function handleUpdateLabelRequest(data: ActionRequestDataUpdate) {
        dispatch("updateLabelAction", data)
    }

    const editableRingTypes: RingType[] = [
        RingType.LABEL
    ]

    let selectedRingId: string = "";

    let selectedRing: Ring | null = null;
    let editButtonDisabled: boolean = true;

    $: selectedRing = getRingById(selectedRingId);
    $: editButtonDisabled = selectedRing ? !editableRingTypes.includes(selectedRing.type) : true;


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
                    <button class="btn {newRing === RingType.REFERENCE ? 'variant-ghost-primary' : 'variant-ringed-primary'}" disabled={!selectedReference} on:click={() => newRing = RingType.REFERENCE}>
                        <div class="flex items-center align-center truncate">
                            <span>Reference</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.ANNOTATION ? 'variant-ghost-primary' : 'variant-ringed-primary'}" disabled={!selectedReference}  on:click={() => newRing = RingType.ANNOTATION}>
                        <div class="flex items-center align-center truncate">
                            <span>Annotations</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.BLAST ? 'variant-ghost-secondary' : 'variant-ringed-secondary'}" disabled={!selectedReference || $requestInProgress ? true : false}  on:click={() => newRing = RingType.BLAST}>
                        <div class="flex items-center align-center truncate">
                            <span>BLAST</span>
                        </div>
                    </button>
                    <button class="btn {newRing === RingType.LABEL ? 'variant-ghost-secondary' : 'variant-ringed-secondary'}" disabled={!selectedReference}  on:click={() => newRing = RingType.LABEL}>
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
                    <button class="btn {newRing === RingType.GENOMAD ? 'variant-ghost-primary' : 'variant-ringed-primary'}" disabled={!selectedReference || $requestInProgress ? true : false} on:click={() => newRing = RingType.GENOMAD}>
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
            {:else if newRing == RingType.GENOMAD}
                <NewGenomadRing on:submitAction={(event) => handleCreateRingRequest(event.detail)}></NewGenomadRing>
            {/if}
        </div>
    
    {:else if showEditRingMenu}
        
        {#if selectedRing && selectedRing.type === RingType.LABEL}
            {#each selectedRing.data.sort((a, b) => a.start - b.start) as labelSegment, idx}
                <RingLabelEdit 
                    bind:segment={labelSegment} 
                    ringIdentifier={selectedRing.id}
                    labelIndex={idx}
                    labelEditOpacity={idx === 0 ? 100 : 40}
                    on:submitAction={(event) => handleUpdateLabelRequest(event.detail)}
                    on:delete={(_) => { removeLabel(selectedRingId, idx); selectedRing = getRingById(selectedRingId)}}
                    on:changePosition={(event) => changeLabelPosition(selectedRingId, event.detail.position, idx)}
                    on:changeText={(event) => changeLabelText(selectedRingId, event.detail.text, idx)}
                    on:changeTextSize={(event) => changeLabelTextSize(selectedRingId, event.detail.textSize, idx)}
                    on:changeTextColor={(event) => changeLabelTextColor(selectedRingId, event.detail.textColor, idx)}
                    on:changeLineAngle={(event) => changeLabelLineAngle(selectedRingId, event.detail.lineAngle, idx)}
                    on:changeLineLength={(event) => changeLabelLineLength(selectedRingId, event.detail.lineLength, idx)}
                    on:changeLineWidth={(event) => changeLabelLineWidth(selectedRingId, event.detail.lineWidth, idx)}
                    on:changeLineColor={(event) => changeLabelLineColor(selectedRingId, event.detail.lineColor, idx)}
                />
            {/each}
        {/if}


    {:else}

        {#if $ringData.length}
            <div>
                <p class="opacity-60 mb-2">Rings</p>
                <ListBox>
                    {#each $ringData as ring}
                        <ListBoxItem bind:group={selectedRingId} name="rings" value="{ring.id}" active="variant-soft">
                            <RingSettings 
                                ring={ring}
                                ringData={$ringData}
                                indexGroup={indexGroup}
                                on:submitAction={(event) => handleUpdateRingRequest(event.detail.requestData)} 
                                on:selectColor={(event) => changeRingColor(ring.id, event.detail.color)}
                                on:toggleVisibility={(_) => toggleRingVisibility(ring.id)}
                                on:updateTitle={(event) => changeRingTitle(ring.id, event.detail.title)}
                                on:moveRingInside={(_) => moveRingInside(ring.id)}
                                on:moveRingOutside={(_) => moveRingOutside(ring.id, $ringData.length-1)}
                                on:delete={() => removeRing(ring.id, indexGroup)}
                            />
                        </ListBoxItem>
                    {/each}
                </ListBox>
            </div>
        {:else}
            <p class="opacity-80 pl-4 text-sm"></p>
        {/if}
    {/if}
    
    <div class="mt-12 flex justify-start items-center">
        {#if showNewRingMenu || showEditRingMenu}
            <div class="text-sm opacity-90">
                <button class="btn p-1" on:click={() => {showNewRingMenu = false; showEditRingMenu = false}}>
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
                        <div class="w-7 h-7 text-primary-500">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">New ring</span>
                    </div>
                </button>
                <button class="btn p-1 ml-4" on:click={() => showEditRingMenu = true} disabled={editButtonDisabled}>
                    <div class="flex items-center align-center">
                        <div class="w-7 h-7 text-secondary-500">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>
                        </div>
                        <span class="ml-2 text-base">Edit ring</span>
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