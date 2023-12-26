<script lang="ts">
    import BrickInterface from "$lib/session/BrickInterface.svelte";
	import type { BrickInterfaceConfiguration } from "$lib/session/types";
    
    let brickInterfaceConfiguration: BrickInterfaceConfiguration;

    export let data;

    console.log(data)

</script>

<BrickInterface config={brickInterfaceConfiguration}/>