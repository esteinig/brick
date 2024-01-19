<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
    import { tick } from 'svelte';

	import { goto } from '$app/navigation';
	import { createSessionId } from '$lib/helpers';
	import { clearSessionFiles } from '$lib/stores/SessionFileStore';
	import { clearRings } from '$lib/stores/RingStore';
	import { clearRingReference } from '$lib/stores/RingReferenceStore';
	import { resetTabs } from '$lib/stores/TabIndexStore';

	/** Exposes parent props to this component. */
	export let parent: SvelteComponent;

	const modalStore = getModalStore();
    const defaultTitle: string = `New session`

    async function handleNewSession() {

        clearSessionFiles();
        clearRings();
        clearRingReference();
        resetTabs();

        // Important to ensure that all
        // stores have been cleared 
        await tick();

        modalStore.close()

        goto(`/session/${createSessionId()}`)
    }

</script>


{#if $modalStore[0]}
	<div id="saveSessionModal" class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">{$modalStore[0].title ?? defaultTitle}</header>
		<article>
            <p class="opacity-80">Sessions and files are stored in our database for one week and are accessible on this page, with the unique identifier: 
                <span id="saveSessionLink" class="code"><a href="{$page.url.href}">{$page.params.session}</a></span> <br><br> 
                If you want to revisit your session after its expiration, you can download the model data and upload the file into a new session (re-hydration). <br><br>
                Please note that uploaded files that have expired will not be available in restored sessions.
                </p>
        </article>
		
        <footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
			<button class="btn {parent.buttonPositive}" type="button" on:click={handleNewSession}>New Session</button>
		</footer>
	</div>
{/if}