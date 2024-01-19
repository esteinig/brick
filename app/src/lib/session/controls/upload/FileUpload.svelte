<script lang="ts">
  import { addSessionFile, sessionFiles } from '$lib/stores/SessionFileStore';
  import { FileFormat, FileType, TaskResultType, type Session } from '$lib/types';
  import { ToastType, createUuid, triggerToast } from '$lib/helpers';

  import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';    
  import { page } from '$app/stores';
  import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from '$app/forms';
	import { completeUploadState, startUploadState } from '$lib/stores/UploadInProgressStore';
	import { createEventDispatcher } from 'svelte';
	import { rings } from '$lib/stores/RingStore';
	import { ringReferenceStore } from '$lib/stores/RingReferenceStore';

  const toastStore = getToastStore();
  
  // Determine server-side processing of uploaded files
  export let format: FileFormat;
  export let type: FileType;

  export let id: string = `brickFileUpload-${createUuid(true)}`;
  export let message: string = "Please upload a file"
  export let meta: string = "";
  export let information: string = ""

  export let disabled: boolean = false;

  let formElement: HTMLFormElement; // neded for drop zone handler
  let files: FileList;

  let loading: boolean = false;

  const dispatch = createEventDispatcher();

  function handleMouseover() {
      dispatch('mouseover', information);
  }
  function handleMouseout() {
      dispatch('mouseout', information);
  }
  function handleSessionHydration() {

    // Update the entire session data manually - would prefer invalidation
    // and running the reload function but there are issues for this kind of
    // visualiztion, for more details see comments in: /brick/+layout.svelte

    let hydratedSession: Session = $page.form.result;
    
    $sessionFiles = hydratedSession.files;
    $rings = hydratedSession.rings;

    if ($rings.length) $ringReferenceStore = $rings[0].reference;

  }
  
</script>
  
<form 
  on:mouseover={handleMouseover} 
  on:mouseout={handleMouseout} 
  on:focus={handleMouseover} 
  on:blur={handleMouseout}
  id="form-{id}" bind:this={formElement} action="?/uploadFile" method="POST" enctype="multipart/form-data" use:enhance={({ formData }) => {
  
  // TODO: Multiple Files

  const config = JSON.stringify({ 
      session_id: $page.params.session,
      file_format: format,
      file_type: type,
      original_filename: files[0].name 
  });

  // Modify form data by deleting file with unique
  // dropzone identifiers and replacing it with a
  // simple `file` entry
  
  formData.delete(id); 
  formData.append('file', files[0]);
  formData.append('config', config);

  // Upload state for this component instance
  loading = true;

  // Tracks the common upload state from multiple components 
  startUploadState();

  return async ({ result }) => {
    
    await applyAction(result);

    loading = false;
    completeUploadState();

    if (result.type === "success"){
      if ($page.form.result_type === TaskResultType.SESSION_FILE) {
        triggerToast("File uploaded sucessfully", ToastType.SUCCESS, toastStore);
        addSessionFile($page.form.result)
      } else if ($page.form.result_type === TaskResultType.SESSION) {
        triggerToast("Session rehydrated sucessfully", ToastType.SUCCESS, toastStore);
        handleSessionHydration();
      } else {  
        triggerToast("An unknown type was returned from file upload", ToastType.ERROR, toastStore);
      }
      
    } else {
      triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
    }
  };
}}>
  <div id="{id}">
      <FileDropzone name="{id}" bind:files={files} on:change={() => formElement.requestSubmit()} disabled={disabled}>
          <svelte:fragment slot="lead">
            <div class="flex justify-center items-center"><slot name="icon"></slot></div>
          </svelte:fragment>
          <svelte:fragment slot="message">
            <span class="text-xs">{message}</span>
          </svelte:fragment>
          <svelte:fragment slot="meta">
            <span class="text-xs">{meta}</span>
          </svelte:fragment>
      </FileDropzone>
      {#if loading}
        <div class="mt-1"><ProgressBar/></div>
      {:else}
        <div class="mt-3"></div>
      {/if}
  </div>
</form>
