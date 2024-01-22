<script lang="ts">
  import { type UploadConfig } from '$lib/types';
  import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';    
  import { page } from '$app/stores';
	import { createEventDispatcher } from 'svelte';
	import { fileDropzoneStateStore, startDropzoneLoading } from '$lib/stores/FileDropzoneStateStore';

  
  export let config: UploadConfig;
  export let disabled: boolean = false;

  let formElement: HTMLFormElement; // neded for drop zone handler
  let files: FileList;

  const dispatch = createEventDispatcher();

  function handleMouseover() {
      dispatch('mouseover', config.info);
  }
  function handleMouseout() {
      dispatch('mouseout',  config.info);
  }
  

  function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {

    // TODO: multiple file submission?
    
    let data = new FormData();

    const fileConfig = JSON.stringify({ 
        session_id: $page.params.session,
        file_format: config.format,
        file_type: config.type,
        original_filename: files[0].name 
    });
    
    data.append('file', files[0]);
    data.append('config', fileConfig);

    // Upload state for this component instance
    startDropzoneLoading(config.id);

    dispatch('submitAction', { action: event.currentTarget.action, body: data });

  }



</script>
  
<form 
  
  id="form-{config.id}" 
  bind:this={formElement} 
  action="?/uploadFile" 
  method="POST" 
  enctype="multipart/form-data"
  on:submit|preventDefault={handleSubmit}
  on:mouseover={handleMouseover} 
  on:mouseout={handleMouseout} 
  on:focus={handleMouseover} 
  on:blur={handleMouseout}
>
  <div id="{config.id}">
      <FileDropzone name="{config.id}" bind:files={files} on:change={() => formElement.requestSubmit()} disabled={disabled}>
          <svelte:fragment slot="lead">
            <div class="flex justify-center items-center"><slot name="icon"></slot></div>
          </svelte:fragment>
          <svelte:fragment slot="message">
            <span class="text-xs">{config.message}</span>
          </svelte:fragment>
          <svelte:fragment slot="meta">
            <span class="text-xs">{config.meta}</span>
          </svelte:fragment>
      </FileDropzone>
      {#if $fileDropzoneStateStore.get(config.id)}
        <div class="mt-1"><ProgressBar/></div>
      {:else}
        <div class="mt-3"></div>
      {/if}
  </div>
</form>
