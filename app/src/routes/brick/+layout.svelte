<script lang="ts">
	import { goto } from '$app/navigation';
	import { navigating } from '$app/stores';
	import { AppShell, AppBar, type ModalSettings} from '@skeletonlabs/skeleton';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { env } from '$env/dynamic/public';
	import { createSessionId } from '$lib/helpers';
	import { clearSessionFiles } from '$lib/stores/SessionFileStore';
	import { clearRings } from '$lib/stores/RingStore';
	import { requestInProgress } from '$lib/stores/RequestInProgressStore';
    import { page } from '$app/stores';

	const modalStore = getModalStore();	

	const newSessionPrompt: ModalSettings = {
		type: 'confirm',
		title: 'New session',
		body: 'Are you sure you wish to create a new session? All current data will be lost.',
		// TRUE if confirm pressed, FALSE if cancel pressed
		response: (r: boolean) => {
			if (r) {
				clearSessionFiles(); 
				clearRings();
				goto('/brick/'+createSessionId())
			}
		},
	};
	
	const saveSessionPrompt: ModalSettings = {
		type: 'confirm',
		title: 'Download session',
		body: `Sessions are stored in our database for one week and accessible with the unique identifier <span class="code"><a href="${$page.url.href}">${$page.params.session}</a></span> on this page <br><br> 
		If you want to revisit your session, confirming this prompt will download the raw data model as JSON. You can then upload the data in a new session. <br><br>
		Please note that uploaded files will not be available after one week due to storage limitations.`,
		response: (r: boolean) => {
			if (r) {
				goto('/brick/'+createSessionId())
			}
		},
	};

</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<a href="/"><code class="text-xl">BRICK {env.PUBLIC_BRICK_VERSION}</code></a>
			</svelte:fragment>
			<svelte:fragment slot="trail">

				<button
				class="btn btn-sm variant-ghost-surface"
				on:click={() => modalStore.trigger(newSessionPrompt)}
				>
					New
				</button>
				
				<button
					class="btn btn-sm variant-ghost-surface"
					on:click={() => modalStore.trigger(saveSessionPrompt)}
				>
					Save
				</button>

				<button
					class="btn btn-sm variant-ghost-surface"
					on:click={() => modalStore.trigger(saveSessionPrompt)}
				>
					Share
				</button>
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

<style lang="postcss">

</style>