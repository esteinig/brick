<script lang="ts">
    import { FileFormat, FileType, type ActionRequestData } from "$lib/types";
    import FileUpload from "$lib/session/controls/upload/FileUpload.svelte";
	import { sessionFiles, removeSessionFile } from "$lib/stores/SessionFileStore";
    import { SlideToggle } from "@skeletonlabs/skeleton";
	import { type UploadConfig } from "$lib/types";
	import { createEventDispatcher } from "svelte";
    import DeleteFile from "../helpers/DeleteFile.svelte";

    const dispatch = createEventDispatcher();
    
    export const configs: UploadConfig[] = [
        {   
            id: 'referenceDropzone',
            title: 'Reference genome',
            message: 'Reference genome sequences',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.REFERENCE,
            info: 'Chromosome- or scaffold-level assemblyies as reference genome'
        },
        {
            id: 'blastDropzone',
            title: 'Comparison genomes',
            message: 'BLAST genome sequences',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.GENOME,
            info: 'Custom annotations file with ring segments, tab-delimited with header (start  end  text  color)'
        },
        {
            id: 'genbankDropzone',
            title: 'Reference annotation',
            message: 'Reference genome annotations',
            meta: '.gbk',
            single: false,
            format: FileFormat.GENBANK,
            type: FileType.ANNOTATION_GENBANK,
            info: 'Complete or contig-level sequences for comparison against reference'
        },
        {
            id: 'customDropzone',
            title: 'Custom annotations',
            message: 'Custom annotation table',
            meta: '.tsv',
            single: false,
            format: FileFormat.TSV,
            type: FileType.ANNOTATION_CUSTOM,
            info: "Custom labels file with ring segments, tab-delimited with header (start  end  text  color)"
        },
        {
            id: 'sessionDropzone',
            title: 'Session re-hydration',
            message: 'Session data',
            meta: '.json',
            single: false,
            format: FileFormat.JSON,
            type: FileType.SESSION,
            info: 'Re-hydration will overwrite all current data in this session!'
        },
    ]

    let showFileTable: boolean = false;
    let infoText: string = "";

    $: referenceAvailable = $sessionFiles.some(file => file.type === FileType.REFERENCE);
    
    function handleInfoMouseover(event: any){ 
        infoText = event.detail 
    }
    function handleInfoMouseout() { 
        infoText = ""; 
    }
    function handleFileUploadAction(data: ActionRequestData, id: string) {
        dispatch("fileUploadAction", {data: data, id: id})
    }
    function handleFileDeleteAction(data: ActionRequestData, id: string) {
        dispatch("fileDeleteAction", {data: data, id: id})
    }

 </script>

<div id="brickRingControlPanel" class="p-2 text-base">

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-x-8 gap-y-4">
            <div class="my-2">
                <p class="opacity-60 mb-2">{configs[0].title}</p>
                <FileUpload config={configs[0]} on:mouseover={handleInfoMouseover} on:submitAction={(event) => handleFileUploadAction(event.detail, configs[0].id)} on:mouseout={handleInfoMouseout}>
                    <svelte:fragment slot="icon">
                    <div class="md:w-12 text-primary-500">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>                    
                    </div>    
                    </svelte:fragment>
                </FileUpload>
            </div>
            <div class="my-2">
                <p class="opacity-60 mb-2">{configs[2].title}</p>
                <FileUpload config={configs[2]} disabled={!referenceAvailable} on:submitAction={(event) => handleFileUploadAction(event.detail, configs[2].id)} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}>
                    <svelte:fragment slot="icon">
                    <div class="md:w-12 text-primary-500">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>                    
                    </div>    
                    </svelte:fragment>
                </FileUpload>
            </div>
            <div class="my-2">
                <p class="opacity-60 mb-2">{configs[1].title}</p>
                <FileUpload config={configs[1]} disabled={!referenceAvailable} on:submitAction={(event) => handleFileUploadAction(event.detail, configs[1].id)} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}>
                    <svelte:fragment slot="icon">
                    <div class="md:w-12 text-secondary-500">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>                    
                    </div>    
                    </svelte:fragment>
                </FileUpload>
            </div>
            <div class="my-2">
                <p class="opacity-60 mb-2">{configs[3].title}</p>
                <FileUpload config={configs[3]} disabled={!referenceAvailable} on:submitAction={(event) => handleFileUploadAction(event.detail, configs[3].id)} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}>
                    <svelte:fragment slot="icon">
                    <div class="md:w-12 text-secondary-500">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>                    
                    </div>    
                    </svelte:fragment>
                </FileUpload>
            </div>
        </div>

    <div class="mt-4 mb-8 flex justify-between items-center">
        <p class="text-xs opacity-60">{infoText}</p>
        <div class="text-sm opacity-80">
            <SlideToggle name="sliderFileTable" active="bg-secondary-500" size="sm" bind:checked={showFileTable}>File table</SlideToggle>
        </div> 
    </div>
 
    {#if showFileTable}
        <div class="mt-8">
            
            {#if $sessionFiles.length}
                <div class="table-container">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>File</th>
                                <th>Type</th>
                                <th>Format</th>
                                <th>Records</th>
                                <th>Length</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each $sessionFiles as sessionFile}
                                <tr>
                                    <td class="truncate">{sessionFile.name_original}</td>
                                    <td>{sessionFile.type}</td>
                                    <td>{sessionFile.format}</td>
                                    <td>{sessionFile.records}</td>
                                    <td>{sessionFile.total_length}</td>
                                    <td><DeleteFile id={sessionFile.id} updateVerbose on:submitAction={(event) => handleFileDeleteAction(event.detail, sessionFile.id)} on:delete={() => removeSessionFile(sessionFile.id)}></DeleteFile></td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {:else}
                <div class="p-4 text-center">
                    <p class="text-secondary-500">No files have been uploaded to this session</p>
                </div>
            {/if}
        </div>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-x-8 gap-y-4">
            <div class="my-2">
                <p class="opacity-60 mb-2">{configs[4].title}</p>
                <FileUpload config={configs[4]} on:submitAction={(event) => handleFileUploadAction(event.detail, configs[4].id)} on:mouseover={handleInfoMouseover} on:mouseout={handleInfoMouseout} >
                    <svelte:fragment slot="icon">
                    <div class="md:w-12 text-primary-500">
                        <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                        </svg>                    
                    </div>    
                    </svelte:fragment>
                </FileUpload>
            </div>
        </div>
    {/if}
</div>