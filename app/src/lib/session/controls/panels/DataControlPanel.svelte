<script lang="ts">
    import FileUpload from "$lib/session/controls/upload/FileUpload.svelte";
	import FileTable from "$lib/session/controls/upload/FileTable.svelte";

    import { SlideToggle } from "@skeletonlabs/skeleton";

    import { FileFormat, FileType } from "$lib/types";
	import { type UploadConfig } from "$lib/types";
	import { sessionFiles } from "$lib/stores/SessionFileStore";
    
    export const config: UploadConfig[] = [
        {
            title: 'Reference genome',
            message: 'Reference genome sequences',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.REFERENCE
        },
        {
            title: 'Comparison genomes',
            message: 'BLAST genome sequences',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.GENOME
        },
        {
            title: 'Reference annotation',
            message: 'Reference genome annotations',
            meta: '.gbk',
            single: false,
            format: FileFormat.GENBANK,
            type: FileType.ANNOTATION_GENBANK
        },
        {
            title: 'Custom annotations',
            message: 'Custom annotation table',
            meta: '.tsv',
            single: false,
            format: FileFormat.TSV,
            type: FileType.ANNOTATION_CUSTOM
        },
    ]

    let showFileTable: boolean = false;
    let referenceAvailable: boolean = false;

    let infoText: string = "";

    $: referenceAvailable = $sessionFiles.some(file => file.type === FileType.REFERENCE)
    
    function handleInfoMouseover(event: any){
        infoText = event.detail
    }
    function handleInfoMouseout(){
        infoText = "";
    }
 </script>

<div id="brickRingControlPanel" class="p-2 text-base">

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-x-8 gap-y-4">
            <div class="my-2">
                <p class="opacity-60 mb-2">{config[0].title}</p>
                <FileUpload message={config[0].message} meta={config[0].meta} format={config[0].format} type={config[0].type} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}  information="Ideally one or multiple chromosome-level assemblies">
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
                <p class="opacity-60 mb-2">{config[2].title}</p>
                <FileUpload message={config[2].message} meta={config[2].meta} format={config[2].format} type={config[2].type} disabled={!referenceAvailable} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}  information="Custom annotations file is tab-delimited with header: start  end  text  color">
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
                <p class="opacity-60 mb-2">{config[1].title}</p>
                <FileUpload message={config[1].message} meta={config[1].meta} format={config[1].format} type={config[1].type} disabled={!referenceAvailable} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}  information="One or multiple genome sequences (contigs or complete)">
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
                <p class="opacity-60 mb-2">{config[3].title}</p>
                <FileUpload message={config[3].message} meta={config[3].meta} format={config[3].format} type={config[3].type} disabled={!referenceAvailable} on:mouseover={handleInfoMouseover}  on:mouseout={handleInfoMouseout}  information="Custom labels file is tab-delimited with header: start  end  text  color">
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
            <SlideToggle name="sliderFileTable" active="bg-secondary-500" size="sm" bind:checked={showFileTable}>File Table</SlideToggle>
        </div>
    </div>


    {#if showFileTable}
        <div class="mt-8">
            <FileTable></FileTable>
        </div>
    {/if}
</div>