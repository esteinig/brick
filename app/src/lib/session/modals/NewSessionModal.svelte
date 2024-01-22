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

    let clipboardValue: string = $page.url.href;
    let clipboardCopy: boolean = false;

    async function copyToClipboard() {
        try {
            await navigator.clipboard.writeText(clipboardValue);
            clipboardCopy = true;

            setTimeout(() => {
                clipboardCopy = false;
            }, 1000);

        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }
    // <br><br> 
    //             If you want to revisit your session after it has expired, download the session data (.json) and upload into a new session (re-hydration). 
    //             Please note that uploaded files that have expired will not be available in re-hydrated sessions.
    //             <br><br>

</script>


{#if $modalStore[0]}
	<div id="saveSessionModal" class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">{$modalStore[0].title ?? defaultTitle}</header>
		<article>
            <p class="opacity-80">Sessions and files are available on the current page for one week:</p>
            <div class="flex mt-2 pb-4">
                <input class="input" type="text" placeholder="{$page.url.href}"readonly tabindex="-1" />
                {#if clipboardCopy}
                    
                    <button class='btn-icon btn-icon-sm ml-1' type='button' tabindex="-1">
                        <svg class="h-8 w-8 text-success-500" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="m4.5 12.75 6 6 9-13.5" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>
                    </button>
                {:else}
                    <button class='btn-icon btn-icon-sm ml-1' type='button' on:click={copyToClipboard} tabindex="-1">
                        <svg class="h-8 w-8" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8.25 7.5V6.108c0-1.135.845-2.098 1.976-2.192.373-.03.748-.057 1.123-.08M15.75 18H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08M15.75 18.75v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5A3.375 3.375 0 0 0 6.375 7.5H5.25m11.9-3.664A2.251 2.251 0 0 0 15 2.25h-1.5a2.251 2.251 0 0 0-2.15 1.586m5.8 0c.065.21.1.433.1.664v.75h-6V4.5c0-.231.035-.454.1-.664M6.75 7.5H4.875c-.621 0-1.125.504-1.125 1.125v12c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V16.5a9 9 0 0 0-9-9Z" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>
                    </button>
                {/if}
            </div>
        </article>
		
        <footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonNeutral}" on:click={parent.onClose} tabindex="-1">{parent.buttonTextCancel}</button>
			<button class="btn {parent.buttonPositive}" type="button" on:click={handleNewSession} tabindex="-1">New Session</button>
		</footer>
	</div>
{/if}