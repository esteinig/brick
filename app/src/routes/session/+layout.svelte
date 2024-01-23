<script lang="ts">
	import { navigating } from '$app/stores';
	import { AppShell, AppBar, type ModalSettings} from '@skeletonlabs/skeleton';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { env } from '$env/dynamic/public';
	import { requestInProgress } from '$lib/stores/RequestInProgressStore';
	import { page } from '$app/stores';
	import type { Session } from '$lib/types';
	import { sessionFiles } from '$lib/stores/SessionFileStore';
	import { rings } from '$lib/stores/RingStore';
	import { downloadJSON } from '$lib/brick/helpers';

	const modalStore = getModalStore();
	
	const newSessionPrompt: ModalSettings = {
		type: 'component',
		component: 'newSessionModal'
	};
	

	function downloadSession() {
		
		/** Recreate the session model data from stores. */
		const modelData: Session = {
			id: $page.params.session,
			date: $page.data.session.date,
			files: $sessionFiles,
			rings: $rings
		}

		downloadJSON(modelData);
	}

	const INFOBANNER: string = "BRICK is under active development - persistence of session data and backwards compatibility are not guaranteed until major version release"

</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<a href="/"><code class="text-xl">BRICK {env.PUBLIC_BRICK_VERSION}</code></a>
				{#if INFOBANNER}
					<div class="ml-16 text-xs opacity-40">{INFOBANNER}</div>
				{/if}
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<button class="btn btn-sm variant-ghost-surface" on:click={() => modalStore.trigger(newSessionPrompt)}>
					<svg class="w-4 h-4" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
						<path d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" stroke-linecap="round" stroke-linejoin="round"></path>
					  </svg>
					<div class="opacity-90 ml-2">New Session</div>
				</button>
				<button class="btn btn-sm variant-ghost-surface" on:click={downloadSession}>
					<svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
					<div class="opacity-90 ml-2">Download</div>
				</button>
				<!-- <button class="btn btn-sm variant-ghost-surface" on:click={() => modalStore.trigger(newSessionPrompt)}>
					<svg class="w-4 h-4" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
						<path d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" stroke-linecap="round" stroke-linejoin="round"></path>
					  </svg>
					<div class="opacity-90 ml-2">Share</div>
				</button> -->
			</svelte:fragment>
		</AppBar>
		{#if $navigating || $requestInProgress}
			<ProgressBar height="h-1"/>
		{:else}
			<!-- Placeholder to not respond to screen size adjustment -->
			<div class="h-1"></div>
		{/if}
	</svelte:fragment>

    <slot />
</AppShell>
