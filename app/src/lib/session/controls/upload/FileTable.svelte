<script lang="ts">
	import { sessionFiles } from "$lib/stores/SessionFileStore";

</script>

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
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{:else}
    <div class="p-4 text-center">
        <p class="text-primary-500">No files have been uploaded</p>
    </div>
{/if}
