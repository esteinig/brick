<script lang="ts">
	import { goto } from '$app/navigation';
	import { navigating } from '$app/stores';
	import { AppShell, AppBar, type ModalSettings} from '@skeletonlabs/skeleton';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { PUBLIC_BRICK_VERSION } from '$env/static/public';
	import { createSessionId } from '$lib/session/helpers';
 
	const modalStore = getModalStore();

	const newSessionPrompt: ModalSettings = {
		type: 'confirm',
		// Data
		title: 'Please Confirm',
		body: 'Are you sure you wish to create a new session? We do not store user data on our servers; all current data will be lost.',
		// TRUE if confirm pressed, FALSE if cancel pressed
		response: (r: boolean) => {
			if (r) {
				goto('/brick/'+createSessionId())
			}
		},
	};
	
	const saveSessionPrompt: ModalSettings = {
		type: 'confirm',
		// Data
		title: 'Please Confirm',
		body: 'Are you sure you wish to create a new session? We do not store user data on our servers; all current data will be lost.',
		// TRUE if confirm pressed, FALSE if cancel pressed
		response: (r: boolean) => {
			if (r) {
				goto('/brick/'+createSessionId())
			}
		},
	};

</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<a href="/brick"><code class="text-xl">BRICK {PUBLIC_BRICK_VERSION}</code></a>
			</svelte:fragment>
			<svelte:fragment slot="trail">

				<button
				class="btn btn-sm variant-ghost-surface"
				on:click={() => modalStore.trigger(newSessionPrompt)}
				>
					New Session
				</button>
				
				<button
					class="btn btn-sm variant-ghost-surface"
					on:click={() => modalStore.trigger(saveSessionPrompt)}
				>
					Save Session
				</button>

				<a
					class="btn btn-sm variant-ghost-surface"
					href="https://github.com/esteinig/brick"
					target="_blank"
					rel="noreferrer"
				>
					GitHub
				</a>
			</svelte:fragment>
		</AppBar>

		{#if $navigating}
			<ProgressBar height="h-1"/>
		{/if}
	</svelte:fragment>
	<slot />
</AppShell>