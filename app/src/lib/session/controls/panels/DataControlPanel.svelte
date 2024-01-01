<script lang="ts">
    import FileUpload from "$lib/session/controls/upload/FileUpload.svelte";
	import FileTable from "$lib/session/controls/upload/FileTable.svelte";

    import { SlideToggle } from "@skeletonlabs/skeleton";

    import { FileFormat, FileType } from "$lib/types";
	import { type SessionFile, type UploadConfig } from "$lib/types";
    
    export const config: UploadConfig[] = [
        {
            title: 'Reference genome',
            message: 'Upload one or multiple chromosome-level assemblies as reference genomes',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.REFERENCE
        },
        {
            title: 'Comparison genomes',
            message: 'Upload one or multiple genome sequences for comparison with BLAST',
            meta: '.fasta',
            single: false,
            format: FileFormat.FASTA,
            type: FileType.GENOME
        },
        {
            title: 'Reference annotation',
            message: 'Upload annotations in Genbank format',
            meta: '.gbk',
            single: false,
            format: FileFormat.GENBANK,
            type: FileType.ANNOTATION_GENBANK
        },
        {
            title: 'Custom annotations',
            message: 'Upload custom annotations as table ',
            meta: '.tsv',
            single: false,
            format: FileFormat.TSV,
            type: FileType.ANNOTATION_CUSTOM
        },
    ]

    let showFileTable: boolean = false;

</script>

<div id="brickRingControlPanel" class="p-2 text-base">
    
    {#if showFileTable}
        <FileTable></FileTable>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-x-8 gap-y-4">
            {#each config as uploadConfig}
                <div class="my-2">
                    <p class="opacity-60 mb-2">{uploadConfig.title}</p>
                    <FileUpload message={uploadConfig.message} meta={uploadConfig.meta} format={uploadConfig.format} type={uploadConfig.type}>
                        <svelte:fragment slot="icon">
                        <div class="sm:w-6 md:w-12">
                            <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9 8.25H7.5a2.25 2.25 0 0 0-2.25 2.25v9a2.25 2.25 0 0 0 2.25 2.25h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25H15m0-3-3-3m0 0-3 3m3-3V15" stroke-linecap="round" stroke-linejoin="round"></path>
                            </svg>                    
                        </div>    
                        </svelte:fragment>
                    </FileUpload>
                </div>
            {/each}
        </div>
    {/if}

    <div class="mt-4 mb-8 flex justify-between items-center">
        <p>Information</p>
        <div class="text-sm opacity-40">
            <SlideToggle name="sliderFileTable" active="bg-secondary-500" size="sm" bind:checked={showFileTable}>File Table</SlideToggle>
        </div>
    </div>

</div>