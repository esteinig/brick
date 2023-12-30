<script lang="ts">
  import { env } from '$env/dynamic/public';
  import { type FileConfig, type FileUploadResponse, type SessionFile, type TaskStatusResponse } from '../types';
  import { FileFormat, FileType } from '../types';
  import { checkCeleryResults, createUuid } from '../helpers';

  import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';    
  import { page } from '$app/stores';
  import { getToastStore } from '@skeletonlabs/skeleton';

  const toastStore = getToastStore();


  let errorToastMessage: string = "Unknown error";
  const errorToast = {
      message: errorToastMessage,
      background: 'variant-filled-error',
      timeout: 10000,
    }

  // Required as these determine server-side processing of uploaded files
  export let format: FileFormat;
  export let type: FileType;

  export let id: string = "brickFileUpload";
  export let url: string = `${env.PUBLIC_API_URL}/files/upload`;

  export let message: string = "Please upload a file (.tsv, .fasta, .gbk)"
  export let meta: string = ""

  export let single: boolean = false;

  export let sessionFiles: SessionFile[] = [];

  const dropzoneIdentifier: string = createUuid(true);

  let loading: boolean = false;
  let files: FileList;

  // Function to handle file drop
  async function handleDrop(_: Event): Promise<void> {
    if (files.length > 0) single ? 
      await uploadFile(files[0]) : 
      await Promise.resolve([...files].map(
        file => uploadFile(file)
      ));
  }

  async function uploadFile(file: File): Promise<void> {

    loading = true;

    let config = JSON.stringify({ 
      session_id: $page.params.session,
      file_format: format,
      file_type: type,
      original_filename: file.name
    } satisfies FileConfig);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('config', config);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });

      const fileUploadResponseData: FileUploadResponse = await response.json();

      if (response.ok) {
        try {
          let taskStatusResponseData: TaskStatusResponse = await checkCeleryResults(
            `${env.PUBLIC_API_URL}/files/result/${fileUploadResponseData.task_id}`, toastStore
          );
          sessionFiles = [...sessionFiles, taskStatusResponseData.result];
        } catch (error) {
          errorToastMessage = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
          toastStore.trigger(errorToast);
        }
      } else {
        errorToastMessage =  `${fileUploadResponseData.detail ?? 'Unknown error occurred during upload'}`;
        toastStore.trigger(errorToast);
      }
    } catch (error) {
      errorToastMessage = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
      toastStore.trigger(errorToast);
    }

    loading = false;
  }
</script>
  
  
<div id="{id}">
    <FileDropzone name="{id}-{dropzoneIdentifier}" bind:files={files} on:change={handleDrop}>
        <svelte:fragment slot="lead"><div class="flex justify-center items-center"><slot name="icon"></slot></div></svelte:fragment>
        <svelte:fragment slot="message"><span class="text-xs">{message}</span></svelte:fragment>
        <svelte:fragment slot="meta"><span class="text-xs">{meta}</span></svelte:fragment>
    </FileDropzone>
    {#if loading}
      <div class="mt-1"><ProgressBar/> </div>
    {/if}
</div>
