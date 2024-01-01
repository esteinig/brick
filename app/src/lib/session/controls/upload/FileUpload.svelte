<script lang="ts">
  import { addSessionFile } from '$lib/stores/SessionFileStore';
  import { FileFormat, FileType } from '$lib/types';
  import { ToastType, createUuid, triggerToast } from '$lib/helpers';

  import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';    
  import { page } from '$app/stores';
  import { getToastStore } from '@skeletonlabs/skeleton';
	import { applyAction, enhance } from '$app/forms';

  const toastStore = getToastStore();
  
  // Determine server-side processing of uploaded files
  export let format: FileFormat;
  export let type: FileType;

  export let id: string = `brickFileUpload-${createUuid(true)}`;
  export let message: string = "Please upload a file"
  export let meta: string = ""

  let formElement: HTMLFormElement; // neded for drop zone handler
  let files: FileList;

  let loading: boolean = false;

</script>
  
<form id="form-{id}" bind:this={formElement} action="?/uploadFile" method="POST" enctype="multipart/form-data" use:enhance={({ formElement, formData, action, cancel, submitter }) => {
  
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

  loading = true;

  return async ({ result }) => {
    
    await applyAction(result);
    loading = false;

    // TODO: Handle session file updates

    if (result.type === "success"){
      triggerToast("File uploaded sucessfully", ToastType.SUCCESS, toastStore);
      addSessionFile($page.form.result)
    } else {
      triggerToast($page.form.detail ?? `Error ${result.status}: an unknown error occurred`, ToastType.ERROR, toastStore);
    }
  };
}}>
  <div id="{id}">
      <FileDropzone name="{id}" bind:files={files} on:change={() => formElement.requestSubmit()}>
          <svelte:fragment slot="lead"><div class="flex justify-center items-center"><slot name="icon"></slot></div></svelte:fragment>
          <svelte:fragment slot="message"><span class="text-xs">{message}</span></svelte:fragment>
          <svelte:fragment slot="meta"><span class="text-xs">{meta}</span></svelte:fragment>
      </FileDropzone>
      {#if loading}
        <div class="mt-1"><ProgressBar/></div>
      {/if}
  </div>
</form>
