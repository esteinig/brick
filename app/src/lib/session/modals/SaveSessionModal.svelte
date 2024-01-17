<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { completeRequestState, startRequestState } from '$lib/stores/RequestInProgressStore';
	import { ToastType, triggerToast } from '$lib/helpers';
	import { type Ring, type SessionUpdateSchema } from '$lib/types';
	import { sessionFiles } from '$lib/stores/SessionFileStore';
	import { rings } from '$lib/stores/RingStore';
	import { invalidate } from '$app/navigation';

	/** Exposes parent props to this component. */
	export let parent: SvelteComponent;

	const modalStore = getModalStore();
	const toastStore = getToastStore();

    let loading: boolean = false;

    let sessionUpdateSchema: SessionUpdateSchema = {
        id: $page.params.session,
        files: $sessionFiles,
        ring_updates: $rings.map((ring: Ring) => {
            return { 
                id: ring.id, 
                index: ring.index, 
                color: ring.color, 
                height: ring.height, 
                title: ring.title, 
                visible: ring.visible 
            }
        })
    }
    
    const defaultTitle: string = `Save session`


</script>


{#if $modalStore[0]}
	<div id="saveSessionModal" class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">{$modalStore[0].title ?? defaultTitle}</header>
		<article>
            <p class="opacity-80">Sessions are stored in our database for one week and accessible on this page, with the unique identifier: 
                <span id="saveSessionLink" class="code"><a href="{$page.url.href}">{$page.params.session}</a></span> <br><br> 
                If you want to revisit your session after its expiration, submitting this prompt will download the ring data, which can be uploaded into a new session. <br><br>
                Please note that uploaded files will not be available after one week or in the restored session due to storage limitations.<p>
        </article>

        <form class='p-4 space-y-4 rounded-container-token' id="saveSessionModalForm" action="?/updateSession" method="POST" use:enhance={({ formData }) => {
            
            loading = true;

            // We cannot easily update the entire session due to size, therefore only
            // the user modifications of ring indices and colors (others to be added)
            // are put into the already stored ring data from the task runners when
            // rings are created.

            formData.append('session_id', $page.params.session)
            formData.append('session_update', JSON.stringify(sessionUpdateSchema))

            // Tracks the common request state from multiple components 
            startRequestState();
        
            return async ({ result }) => {
                await applyAction(result);

                loading = false;
                completeRequestState();

                    
                if (result.type === "success"){
                    triggerToast("Session saved sucessfully", ToastType.SUCCESS, toastStore);
                } else {
                    // Validation errors from pydantic schemes are an array of validation objects:
                    if ($page.form.detail instanceof Array){
                        for (const error of $page.form.detail) {
                            triggerToast(
                                error.msg ?? `Error ${result.status}: an unknown error occurred`, 
                                ToastType.ERROR, 
                                toastStore
                            );
                        }
                    } else {
                        triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
                    }
                }
                // When the request has completed, return any response data from modal and close
                // if ($modalStore[0].response) $modalStore[0].response(responseData);
		        modalStore.close(); 
            };
        }}>
		<footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
			<button class="btn {parent.buttonPositive}" type="submit">Submit</button>
		</footer>
	</div>
{/if}