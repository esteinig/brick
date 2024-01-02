<script lang="ts">
	import { type AnnotationRingSchema, type LabelRingSchema } from "$lib/types";
	import { ToastType, triggerToast } from "$lib/helpers";
	import { FileType, type SessionFile } from "$lib/types";
    import { sessionFiles, sessionFileTypeAvailable } from "$lib/stores/SessionFileStore";
    import { addRing } from "$lib/stores/RingStore";
	import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from "$app/forms";
    
    const toastStore = getToastStore();

    export let selectedReference: SessionFile;
    
    let ringConfig: LabelRingSchema = {
        session_id: $page.params.session,
        tsv_id: ""
    }

    let loading: boolean = false;

</script>

<div class="border border-gray-300 rounded-lg border-opacity-10 p-4">
    <p class="opacity-60 mb-2">Label Ring</p>
    <p class="opacity-40 mb-2 text-sm w-full">
        
    </p>
    <p class="opacity-20 mb-2 text-xs w-full">Label rings consist of text-annotations that are always added to the outer ring.
        Labels can be added manually or using custom annotation files. If start and end values in the annotation
        file are different, their midpoint is used to draw the annotation line.</p>
    
    {#if selectedReference}
        <form id="createLabelRingForm" action="?/createLabelRing" method="POST" use:enhance={({ formData }) => {
                    
            loading = true;
            formData.append('ring_config', JSON.stringify(ringConfig))
        
            return async ({ result }) => {
                await applyAction(result);
                loading = false;
                    
                if (result.type === "success"){
                    addRing($page.form.result)
                    if ($page.form.result.data.length) {
                        triggerToast("Ring created sucessfully", ToastType.SUCCESS, toastStore);
                    } else {
                        triggerToast("Ring created, requested annotations not found", ToastType.WARNING, toastStore);
                    }   
                } else {
                    triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
                }
            };
        }}>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4 my-3">
                
                
                {#if sessionFileTypeAvailable(FileType.ANNOTATION_CUSTOM)}
                    <label class="label text-xs mt-3">
                        <p class="opacity-40">Custom labels</p>
                        <select class="select text-xs" bind:value={ringConfig.tsv_id}>
                            {#each $sessionFiles as file}
                                {#if file.type === FileType.ANNOTATION_CUSTOM}
                                    <option value={file.id}>{file.name_original}</option>
                                {/if}
                            {/each}
                        </select>
                    </label>
                {/if}

            </div>
            
            {#if ringConfig.tsv_id}

                <div class="flex justify-right mt-4">
                    <button class="btn variant-outline-surface" type="submit">
                        <div class="flex items-center align-center">
                            <span>Create</span>
                        </div>
                    </button>
                </div>
            {/if}
        </form>
    {/if}
</div>