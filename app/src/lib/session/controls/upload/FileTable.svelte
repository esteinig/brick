<script lang="ts">
	import { removeSessionFile, sessionFiles } from "$lib/stores/SessionFileStore";
    import DeleteFile from "../helpers/DeleteFile.svelte";
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
                        <td><DeleteFile id={sessionFile.id} updateVerbose on:delete={() => removeSessionFile(sessionFile.id)}></DeleteFile></td>
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
