<script lang="ts">
    import { env } from '$env/dynamic/public';
    import { TaskStatus, type FileConfig, type FileUploadResponse, type SessionFile, type TaskStatusResponse } from '../types';
    import { FileFormat, FileType } from '../types';
    import { createUuid } from '../helpers';

	  import { FileDropzone, ProgressBar, type ToastSettings } from '@skeletonlabs/skeleton';    
	  import { page } from '$app/stores';
    import { getToastStore } from '@skeletonlabs/skeleton';

    const toastStore = getToastStore();

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
    const timeout = 30000; 
    const pollingInterval = 2000; 
    const errorToastTimeout: number = 10000

    let isLoading: boolean = false;
    let files: FileList;

    
    
    // Function to handle file drop
    async function handleDrop(_: Event): Promise<void> {
      if (files.length > 0) single ? await uploadFile(files[0]) : await Promise.resolve([...files].map(file => uploadFile(file)));
    }

    async function uploadFile(file: File): Promise<void> {

      isLoading = true;

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

        const data: FileUploadResponse = await response.json();

        if (response.ok) {
          await checkResults(data.task_id);
        } else {
          toastStore.trigger({
            message: `${data.detail ?? 'Unknown error occurred during upload'}`,
            background: 'variant-filled-error',
            timeout: errorToastTimeout
          } satisfies ToastSettings)
        }
        isLoading = false;
      } catch (error) {
        toastStore.trigger({
          message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          background: 'variant-filled-error',
          timeout: errorToastTimeout
        } satisfies ToastSettings)
        isLoading = false;
      }

    }


    async function checkResults(taskId: string): Promise<void> {

      const startTime = new Date().getTime();

      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Operation timed out')), timeout)
      );
  
      const statusCheck = async () => {
        while (true) {
          const currentTime = new Date().getTime();
          if (currentTime - startTime > timeout) {
            throw new Error('Processing checks timed out');
          }
  
          const response = await fetch(`${env.PUBLIC_API_URL}/files/result/${taskId}`);

          if (!response.ok) {
            const data = await response.json();
            throw new Error(`${data.detail ? data.detail : `${response.status}`}`);
          }

          const data: TaskStatusResponse = await response.json();
          
          if (data.status === TaskStatus.SUCCESS) {

            toastStore.trigger({
              message: `File uploaded successfully`,
              background: 'variant-filled-success',
              timeout: 3000
            } satisfies ToastSettings)

            sessionFiles = [...sessionFiles, data.result]  // updates the uploaded files array for parent access
            return;
          }
          await new Promise(resolve => setTimeout(resolve, pollingInterval));
        }
      };
  
      try {
        await Promise.race([statusCheck(), timeoutPromise]);
        isLoading = false;
      } catch (error) {
        isLoading = false;
        toastStore.trigger({
          message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          background: 'variant-filled-error',
          timeout: errorToastTimeout,
        } satisfies ToastSettings)
      }
    }
  </script>
  
  
<div id="{id}">
    <FileDropzone name="{id}-{dropzoneIdentifier}" bind:files={files} on:change={handleDrop}>
        <svelte:fragment slot="lead"><div class="flex justify-center items-center"><slot name="icon"></slot></div></svelte:fragment>
        <svelte:fragment slot="message"><span class="text-xs">{message}</span></svelte:fragment>
        <svelte:fragment slot="meta"><span class="text-xs">{meta}</span></svelte:fragment>
    </FileDropzone>
    {#if isLoading}
      <div class="mt-1"><ProgressBar/> </div>
    {/if}
</div>
