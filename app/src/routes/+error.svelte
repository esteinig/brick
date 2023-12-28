<!-- src/routes/+error.svelte -->
<script lang="ts">
    import { page } from '$app/stores';
</script>

<div class="h-full flex justify-center items-center">
    <div class="text-center space-y-4">
        <h3 class="h3 my-2" style="color: red">Error</h3>
        <span class="">{$page.error?.message || "Look, it's a mystery error!"}</span>
    </div>
</div>