<script lang="ts">
	import ColorPicker from "$lib/session/palette/ColorPicker.svelte";
	import PalettePopup from "$lib/session/palette/PalettePopup.svelte";
	import { changeRingColor, changeRingTitle, isRingTypePresent, moveRingInside, moveRingOutside, removeRing, toggleRingVisibility } from "$lib/stores/RingStore";
	import { RingDirection, type ActionRequestDataUpdate, type Ring, RingType } from "$lib/types";
	import DeleteRing from "./DeleteRing.svelte";
	import RingIndex from "./RingIndex.svelte";
	import RingTitle from "./RingTitle.svelte";
	import RingVisibility from "./RingVisibility.svelte";

    import { createEventDispatcher } from 'svelte';

    type RingId = string;

    export let ring: Ring;
    export let indexGroup: RingId[];
    export let ringData: Ring[]


    const dispatch = createEventDispatcher();

    // Bubble up sub-component action requests for ring updates

    function handleSubmitAction(requestData: ActionRequestDataUpdate) {
        dispatch('submitAction', { requestData });
    }

    // Bubble up store actions for real-time updates to ring

    function handleSelectColor(color: string) {
        dispatch('selectColor', { color });
    }
    function handleToggleVisibility() {
        dispatch('toggleVisibility', { });
    }
    function handleUpdateTitle(title: string) {
        dispatch('updateTitle', { title });
    }
    function handleMoveRingOutside() {
        dispatch('moveRingOutside', { });
    }
    function handleMoveRingInside() {
        dispatch('moveRingInside', { });
    }

    function handleDeleteRing() {
        dispatch('delete', { });
    }


</script>

<div class="grid grid-cols-8 gap-x-2 items-center align-center">
    <div class="flex items-center gap-x-2 col-span-7">
        <span class="text-black ml-2">
            <ColorPicker id={ring.id} color={ring.color} on:submitAction={(event) => handleSubmitAction(event.detail) } on:selectColor={(event) => handleSelectColor(event.detail.color)}></ColorPicker>
        </span>
        <div class="mt-0.5">
            <PalettePopup id={ring.id} color={ring.color} on:submitAction={(event) => handleSubmitAction(event.detail) } on:selectColor={(event) => handleSelectColor(event.detail.color)}></PalettePopup>
        </div>
        <RingVisibility id={ring.id} visible={ring.visible} on:submitAction={(event) => handleSubmitAction(event.detail) } on:toggleVisibility={handleToggleVisibility}></RingVisibility>
        <RingTitle id={ring.id} title={ring.title} titleColor={ring.color} on:submitAction={(event) => handleSubmitAction(event.detail) } on:updateTitle={(event) => handleUpdateTitle(event.detail.title)} />
    </div>
    <div class="flex justify-end gap-x-2 col-span-1">
        {#if ring.type !== RingType.LABEL}
            {#if ring.index !== 0}
                <RingIndex id={ring.id} direction={RingDirection.IN} currentIndex={ring.index} on:submitAction={(event) => handleSubmitAction(event.detail) } on:update={handleMoveRingInside} indexGroup={indexGroup}></RingIndex>
            {:else}
                <RingIndex placeholder id={ring.id} direction={RingDirection.IN} currentIndex={ring.index} indexGroup={indexGroup}></RingIndex>
            {/if}
            {#if !((isRingTypePresent(RingType.LABEL) && ring.index === ringData.length-2) || ring.index === ringData.length-1)}
                <RingIndex id={ring.id} direction={RingDirection.OUT} currentIndex={ring.index} on:submitAction={(event) => handleSubmitAction(event.detail) } on:update={handleMoveRingOutside} indexGroup={indexGroup}></RingIndex>
            {:else}
                <RingIndex placeholder id={ring.id} direction={RingDirection.OUT} currentIndex={ring.index} indexGroup={indexGroup}></RingIndex>
            {/if}
        {/if}
        <DeleteRing id={ring.id} indexGroup={indexGroup} on:submitAction={(event) => handleSubmitAction(event.detail)} on:delete={handleDeleteRing}></DeleteRing>
    </div>
</div>