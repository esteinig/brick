<script lang="ts">
  import { addSessionFile } from '$lib/stores/SessionFileStore';
  import { FileFormat, FileType } from '$lib/types';
  import { ToastType, createUuid, triggerToast } from '$lib/helpers';

  import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';    
  import { page } from '$app/stores';
  import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from '$app/forms';
	import { completeUploadState, startUploadState } from '$lib/stores/UploadInProgressStore';
	import { createEventDispatcher } from 'svelte';

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
  
  

</script>
  
<form on:mouseover={handleMouseover} on:mouseout={handleMouseout} id="form-{id}" bind:this={formElement} action="?/uploadFile" method="POST" enctype="multipart/form-data" use:enhance={({ formData }) => {
  
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
  
  formData.delete(id); formData.append('file', files[0]);
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
      triggerToast("File uploaded sucessfully", ToastType.SUCCESS, toastStore);
      addSessionFile($page.form.result)
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
