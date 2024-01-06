<script lang="ts">
	import ColorPalette from "$lib/session/palette/ColorPalette.svelte";
	import PalettePopup from "$lib/session/palette/PalettePopup.svelte";
	import { paletteStore, type Palette } from "$lib/stores/PaletteStore";
	import { Accordion, AccordionItem } from "@skeletonlabs/skeleton";

    const DALI = [
        "#b4b87f", 
        "#9c913f", 
        "#585b33", 
        "#6ea8ab", 
        "#397893", 
        "#31333f",
        "#8f5715", 
        "#ba9a44", 
        "#cfbb83"
    ]

    const PANTON = [
        "#e84a00",
        "#bb1d2c",
        "#9b0c43",
        "#661f66",
        "#2c1f62",
        "#006289",
        "#004759"
    ]

    const RATTNER = [
        "#de8e69", 
        "#f1be99", 
        "#c1bd38", 
        "#7a9132",  
        "#4c849a", 
        "#184363", 
        "#5d5686",
        "#a39fc9"
    ]

    const ALKALAY = [
        "#241d1d", "#5b2125", "#8d3431", "#bf542e", "#e9a800"
    ]
    const CLAY = [
        "#c48329", "#8b3b36", "#a2b4b7", "#514a2e", "#cf9860", "#8E4115"
    ]
    const CONNORS = [
        "#d92a05", "#f35d36", "#fc9073", "#ffba1b", "#60cfa1"
    ]
    const DOUGHTON = [
        "#155b51", "#216f63", "#2d8277", "#3a9387", "#45a395", "#c468b2","#af509c", "#803777", "#5d2155", "#45113f"
    ]
    const ERNST = [
        "#e8e79a", "#c2d89a", "#8cbf9a", "#5fa2a4", "#477b95", "#315b88", "#24396b", "#191f40"
    ]
    const KLEIN = [
        "#ff4d6f", "#579ea4", "#df7713", "#f9c000","#86ad34", "#5d7298","#81b28d", "#7e1a2f", "#2d2651", "#c8350d", "#bd777a"
    ]
    const LEVINE = [
        "#E0D9B2", "#818053", "#6B3848", "#8B3E50", "#D5BB6C", "#3F3A4B", "#474C66", "#A5806F"
    ]
    const OKEEFFE = [
        "#f3d567", "#ee9b43", "#e74b47", "#b80422", "#172767", "#19798b"
    ]
    const SIDHU = [
        "#af4646", "#762b35", "#005187", "#251c4a", "#78adb7", "#4c9a77", "#1b7975"
    ]
    const VANGOGH = [
        "#c3a016", "#c3d878", "#58a787", "#8ebacd", "#246893", "#163274", "#0C1F4b"
    ]

    // NZ 

    const HOIHO = [
        "#CABEE9",
        "#7C7189", 
        "#FAE093", 
        "#D04E59", 
        "#BC8E7D", 
        "#2F3D70"
    ]

    const KAKAPO = [
        "#7D9D33", 
        "#CED38C", 
        "#DCC949", 
        "#BCA888", 
        "#CD8862", 
        "#775B24"
    ]
    const KAKARIKI = [
        "#44781E", 
        "#A1B654", 
        "#2C3B75", 
        "#B8321A", 
        "#565052"
    ]
    const KERERU = [
        "#325756", 
        "#7d9fc2", 
        "#C582B2", 
        "#51806a", 
        "#4d5f8e",
        "#A092B7"
    ]
    const TAMBJA = [
        "#3399ff", 
        "#666600", 
        "#003399", 
        "#999900", 
        "#000000"
    ]
    const MOMA_PALETTES = [
        { name: 'Salvador Dalí', artwork: "The Persistence of Memory (1931)", colors: DALI, link: "https://www.moma.org/collection/works/79018" },
        { name: 'Verner Panton', artwork: "Spectrum textile (1974", colors: PANTON, link: "https://www.moma.org/collection/works/292747?artist_id=4485&page=1&sov_referrer=artist" },
        { name: "Vincent van Gogh", artwork: "The Starry Night (Saint Rémy, June 1889)", colors: VANGOGH, link: "https://www.moma.org/collection/works/79802?sov_referrer=theme&theme_id=5134" },
        { name: 'Abraham Rattner', artwork: "Mother and Child (1938)", colors: RATTNER, link: "https://www.moma.org/collection/works/78474?classifications=9&date_begin=Pre-1850&date_end=2023&direction=fwd&include_uncataloged_works=1&page=37&q=&utf8=%E2%9C%93" },
        { name: 'Shay Alkalay', artwork: "Stack (2008)", colors: ALKALAY, link: "https://www.moma.org/collection/works/126820?classifications=3&date_begin=Pre-1850&date_end=2023&direction=fwd&page=5&q=&utf8=%E2%9C%93&with_images=1" },
        { name: 'Maude Schuyler Clay', artwork: "Sarah Cross (1980)", colors: CLAY, link: "https://www.moma.org/collection/works/49695?artist_id=1139&page=1&sov_referrer=artist" },
        { name: 'Matt Connors', artwork: "Egypt, Hard G (2015)", colors: CONNORS, link: "https://www.moma.org/collection/works/202454?artist_id=36363&page=1&sov_referrer=artist" },
        { name: 'Steve Doughton', artwork: "Ferrum 5000 (1995)", colors: DOUGHTON, link: "https://www.moma.org/collection/works/314423" },
        { name: 'Max Ernst', artwork: "Two Children Are Threatened by a Nightingale (1924)", colors: ERNST, link: "https://www.moma.org/collection/works/79293" },
        { name: 'David Klein', artwork: "New York Fly TWA (1956)", colors: KLEIN, link: "https://www.moma.org/collection/works/6291?artist_id=3134&page=1&sov_referrer=artist" },
        { name: 'Sherrie Levine', artwork: "After Mondrian from Meltdown (1989)", colors: LEVINE, link: "https://www.moma.org/collection/works/65715" },
        { name: "Georgia O'Keeffe", artwork: "Abstraction Blue (1927)", colors: OKEEFFE, link: "https://www.moma.org/collection/works/78677?sov_referrer=theme&theme_id=5264" },
        { name: "Zorawar Sidhu, Rob Swainston", artwork: "May 24 from the series Doomscrolling (2020-21)", colors: SIDHU, link: "https://www.moma.org/collection/works/431041?artist_id=134546&page=1&sov_referrer=artist" },
        
    


    ]
    const NZ_PALETTES = [
        { name: 'Hoiho', species: "Megadyptes antipodes", colors: HOIHO },
        { name: 'Kākāpō', species: "Strigops habroptilus", colors: KAKAPO },
        { name: 'Kākāriki', species: "Cyanoramphus spp.",colors: KAKARIKI },
        { name: 'Kererū', species: "Hemiphaga novaeseelandiae", colors: KERERU },
        { name: 'Gloomy nudibranch', species: "Tambja kushimotoensis", colors: TAMBJA },
    ]


    function handlePaletteClick(colors: string[], name: string) {
        
        let paletteInStore: boolean = $paletteStore.some(p => p.name === name);

        if (paletteInStore){
            paletteStore.removePalette(name)
        } else {
            const samplePalette: Palette = {
                name: name,
                colors: colors
            };
            paletteStore.addPalette(samplePalette);
        }
    }

</script>

<div class="">
    <Accordion>
        <AccordionItem open>
            <svelte:fragment slot="lead"><a href="https://g-thomson.github.io/Manu/"  target="_blank" rel="noreferrer">
                <!-- <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"></svg> -->
                <div class="h-6 w-6 fill-white">
                    <svg data-slot="icon" aria-hidden="true" stroke-width="1.5" stroke="currentColor" viewBox="0 0 199.944 199.944" xml:space="preserve">
                        <path d="M166.598,174.271h-16.692c-4.357,0-8.663-1.983-11.461-3.608c-0.181,0.682-0.479,1.358-0.956,1.949  c-0.609,0.757-1.747,1.659-3.702,1.659h-8.302c-1.104,0-2-0.896-2-2s0.896-2,2-2h8.302c0.451,0,0.55-0.122,0.587-0.168  c0.289-0.358,0.343-1.202,0.297-1.908l-18.866-12.024c-1.321,0.408-2.751,0.379-4.069-0.099c-1.696-0.616-3.048-1.926-3.706-3.595  l-0.05-0.127c-0.771-1.982-0.973-4.065-0.996-5.559c-2.245-0.164-6.356-0.473-11.867-0.923c-7.813-0.638-28.922-0.843-32.398-0.873  l-47.875,24.315c-2.516,1.279-5.368,1.465-8.025,0.523c-2.658-0.938-4.758-2.871-5.914-5.442c0-0.001-0.001-0.002-0.001-0.003  c-0.002-0.005-0.005-0.01-0.007-0.015c-1.112-2.489-1.19-5.262-0.218-7.81c0.973-2.55,2.881-4.568,5.373-5.683l52.17-23.323  c3.358-3.709,35.444-39.088,49.458-52.433c13.03-12.41,24.313-21.002,26.865-22.909c0.626-2.004,2.454-7.717,3.577-9.801  c0.094-0.174,0.201-0.396,0.327-0.653c1.601-3.282,5.853-12.001,20.768-15.449c14.717-3.401,24.178,7.717,26.053,10.166  c1.364,0.676,5.318,2.758,7.653,5.254c2.96,3.164,3.671,8.037,3.699,8.243c0.099,0.703-0.184,1.406-0.741,1.847  c-0.557,0.44-1.305,0.554-1.968,0.293c-0.005-0.002-0.073-0.028-0.195-0.073c-1.047,1.146-2.819,2.849-4.735,3.67  c-1.411,0.605-2.644,0.871-3.559,0.982l-1.543,4.697c-0.199,1.46-1.547,11.489-1.547,15.182c0,0.437,0.066,1.183,0.144,2.046  c0.57,6.411,2.085,23.44-12.002,43.052c-4.993,6.951-11.396,11.881-17.882,15.376c0.047,2.818-0.056,8.634-1.57,11.03  c-0.161,0.255-0.342,0.515-0.541,0.773l18.339,10c0.056,0.03,0.11,0.063,0.163,0.099c0.186,0.121,6.407,4.166,12.268,4.166h16.693  c1.104,0,2,0.896,2,2s-0.896,2-2,2H181.25c-4.389,0-8.739-1.751-11.513-3.147c-0.159,0.495-0.396,0.984-0.744,1.432  c-0.608,0.782-1.772,1.716-3.861,1.716h-8.303c-1.104,0-2-0.896-2-2s0.896-2,2-2h8.303c0.134,0,0.58-0.013,0.703-0.171  c0.152-0.196,0.204-0.632,0.192-1.06l-18.685-10.188c-1.006,0.615-2.104,1.044-3.219,1.137c-1.589,0.137-3.037-0.445-4.09-1.622  c-1.778-1.985-2.175-5.655-2.203-8.313c-6.816,1.887-12.319,2.428-14.364,2.572c-0.34,0.379-0.874,1.015-1.585,1.977  c-0.271,0.366-0.797,1.298-1.282,3.434c-0.231,1.019-0.675,1.964-1.29,2.779l18.281,11.651c0.059,0.037,0.115,0.077,0.17,0.12  c0.243,0.187,6.394,4.838,12.145,4.838h16.692c1.104,0,2,0.896,2,2S167.702,174.271,166.598,174.271z M5.659,164.432  c0.674,0.729,1.521,1.289,2.489,1.631c1.617,0.571,3.352,0.459,4.883-0.318l48.31-24.536c0.284-0.145,0.583-0.222,0.92-0.217  c0.998,0.007,24.551,0.186,33.181,0.891c8.541,0.696,13.702,1.054,13.753,1.058c0.549,0.038,1.057,0.3,1.406,0.724  c0.35,0.425,0.509,0.974,0.44,1.52c-0.003,0.025-0.354,3.093,0.675,5.74c0.274,0.697,0.754,1.16,1.383,1.388  c0.629,0.229,1.323,0.183,1.915-0.121c0.027-0.016,0.055-0.03,0.083-0.045c0.812-0.455,1.396-1.236,1.603-2.148  c0.494-2.172,1.155-3.829,1.966-4.926c1.579-2.136,2.478-2.957,2.575-3.043c0.345-0.307,0.785-0.484,1.246-0.504  c0.297-0.013,29.875-1.493,44.739-22.186c13.22-18.403,11.85-33.792,11.266-40.363c-0.089-0.998-0.159-1.786-0.159-2.4  c0-4.24,1.543-15.433,1.608-15.907c0.017-0.119,0.044-0.236,0.081-0.35l1.673-5.09l-4.183-4.704  c-0.152-0.172-0.271-0.365-0.355-0.57c-0.001-0.002-0.001-0.004-0.002-0.005c0,0,0,0,0-0.001c-0.078-0.19-0.125-0.391-0.142-0.595  v-0.001c0-0.002,0-0.005,0-0.005c0-0.002,0-0.004,0-0.006c-0.002,0-0.001-0.002-0.001-0.004c0-0.001,0-0.001,0-0.001  c0-0.002,0-0.003,0-0.004c0,0,0-0.002,0-0.004c0-0.001,0-0.001,0-0.001c-0.001-0.001-0.001-0.003-0.001-0.004l0,0  c0-0.002,0-0.003,0-0.005l0,0c-0.018-0.279,0.023-0.563,0.126-0.834l0,0c0.001-0.001,0.001-0.002,0.002-0.004l0,0  c0-0.002,0.002-0.003,0.002-0.005c0-0.001,0-0.002,0.001-0.003c0.001,0,0.001-0.002,0.001-0.004c0.001,0,0.001-0.001,0.001-0.001  c0-0.002,0-0.004,0.002-0.004c0-0.001,0.001-0.002,0.001-0.005c0.001-0.001,0.001-0.002,0.001-0.002  c0.002-0.002,0.002-0.003,0.002-0.005l0.001-0.001c0-0.001,0-0.002,0.001-0.003c0,0-0.002,0,0.002-0.004  c0-0.003,0.001-0.004,0.001-0.004c0-0.001,0.001-0.002,0.001-0.002c0-0.001,0.001-0.002,0.001-0.003c0,0-0.002-0.001,0.002-0.004  c0-0.001,0.001-0.001,0.001-0.004c0.001-0.001,0.001-0.002,0.001-0.002c0.001-0.001,0.001-0.002,0.001-0.002  c0.001-0.001,0.001-0.002,0.001-0.002c0-0.001,0.001-0.002,0.001-0.003c0,0,0.002-0.002,0.002-0.004s-0.001-0.001,0.002-0.004  c0-0.002,0.001-0.005,0.001-0.004c0.001-0.002,0.002-0.002,0.002-0.005c0.002,0,0.001-0.002,0.002-0.004  c0-0.001,0.001-0.004,0.002-0.004c0-0.002,0.002-0.004,0.002-0.004c0-0.001,0.001-0.003,0.001-0.004h0.001  c0-0.002,0.001-0.003,0.002-0.005l4.469-10.056c-2.201-2.741-9.832-10.82-21.533-8.116c-13.057,3.02-16.571,10.228-18.072,13.306  c-0.154,0.315-0.286,0.584-0.401,0.798c-0.938,1.74-2.822,7.597-3.47,9.707c-0.127,0.413-0.385,0.774-0.734,1.029  c-0.123,0.09-12.441,9.105-27.002,22.973c-14.613,13.918-49.185,52.146-49.532,52.531c-0.186,0.206-0.413,0.371-0.667,0.485  L7.683,154.535c-1.517,0.678-2.677,1.905-3.27,3.457c-0.345,0.903-0.472,1.853-0.385,2.788l55.055-24.901  c-0.393-2.24,0.71-4.391,2.848-5.519c0.979-0.517,2.188-0.141,2.702,0.835c0.516,0.978,0.142,2.187-0.835,2.702  c-0.627,0.331-0.884,0.781-0.766,1.338c0.032,0.152,0.097,0.307,0.187,0.44c0.021,0.028,0.043,0.057,0.063,0.086  c0.133,0.161,0.308,0.276,0.51,0.29c1.172,0.061,8.171-0.991,14.354-1.932c6.594-1.003,14.067-2.141,19.047-2.655  c1.799-0.187,3.71-0.346,5.704-0.512c9.483-0.789,20.232-1.684,29.675-6.193c11.601-5.54,20.803-19.04,23.444-34.393  c2.532-14.724-7.046-19.164-7.144-19.208c-1.009-0.448-1.464-1.63-1.015-2.64c0.448-1.01,1.629-1.465,2.64-1.015  c0.125,0.056,12.515,5.783,9.46,23.54c-2.854,16.592-12.927,31.242-25.661,37.324c-10.104,4.826-21.728,5.793-31.067,6.57  c-1.966,0.164-3.852,0.32-5.624,0.504c-4.885,0.505-12.308,1.635-18.856,2.631c-8.709,1.326-13.718,2.079-15.222,1.968  c-0.814-0.054-1.582-0.327-2.247-0.767L5.659,164.432z M141.85,141.671c-0.072,2.538,0.211,5.808,1.165,6.874  c0.224,0.251,0.442,0.337,0.776,0.303c1.152-0.096,2.915-1.427,3.849-2.906c0.576-0.911,0.893-3.867,0.95-6.915  C146.301,140.065,144.033,140.938,141.85,141.671z M182.858,50.517l1.974,2.22c0.583-0.063,1.49-0.235,2.573-0.699  c0.646-0.276,1.337-0.782,1.972-1.337c-0.744-0.178-1.5-0.324-2.199-0.402C185.986,50.166,184.351,50.305,182.858,50.517z   M186.148,46.249c0.513,0,1.008,0.022,1.471,0.073c1.331,0.148,2.779,0.486,4.061,0.848c-0.4-0.941-0.946-1.92-1.68-2.704  c-1.287-1.377-3.439-2.738-5.079-3.651l-2.548,5.731C183.574,46.38,184.909,46.249,186.148,46.249z M166.033,48.448  c-3.635,0-6.593-2.957-6.593-6.593c0-3.635,2.958-6.592,6.593-6.592c3.636,0,6.593,2.957,6.593,6.592  C172.626,45.491,169.669,48.448,166.033,48.448z M166.033,39.263c-1.43,0-2.593,1.163-2.593,2.592c0,1.43,1.163,2.593,2.593,2.593  s2.593-1.163,2.593-2.593C168.626,40.426,167.463,39.263,166.033,39.263z"/>
                    </svg>
                </div>         
            </a></svelte:fragment>
            <svelte:fragment slot="summary">
                <p class="opacity-60 text-lg"> Manu - New Zealand Native Species - Geoffrey Thomson</p>
            </svelte:fragment>
            <svelte:fragment slot="content">
                <div class="my-6">
                    {#each NZ_PALETTES as palette }
                        <div class="flex items-center justify-between my-4 rounded-token hover:variant-soft hover:cursor-pointer p-4 rounded-2xl"  on:click={() => handlePaletteClick(palette.colors, palette.name) }>     
                            <div class="">
                                <ColorPalette title={palette.name} colors={palette.colors} subtitle={palette.species} subtitleClass="opacity-80 ml-2 text-sm italic"></ColorPalette>
                            </div>
                            
                            {#if $paletteStore.some(p => p.name === palette.name)}
                                <div class="h-7 w-7 text-secondary-500">
                                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
                                      </svg>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </svelte:fragment>
        </AccordionItem>
        <AccordionItem>
            <svelte:fragment slot="lead"> <a href="https://github.com/BlakeRMills/MoMAColors"  target="_blank" rel="noreferrer">
                <svg class="h-5 w-5" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
            </a></svelte:fragment>
            <svelte:fragment slot="summary">
                <p class="opacity-60 text-lg">Museum of Modern Art - Blake R. Mills</p>
  
            </svelte:fragment>
            <svelte:fragment slot="content">
                <div class="my-6">
                    {#each MOMA_PALETTES as palette }
                        <div class="flex items-center justify-between my-4 rounded-token hover:variant-soft hover:cursor-pointer p-4 rounded-2xl"  on:click={() => handlePaletteClick(palette.colors, palette.name) }>   
                            <div>
                                <ColorPalette title={palette.name} subtitle={palette.artwork} colors={palette.colors} subtitleClass="opacity-80 ml-2 text-sm truncate"></ColorPalette>
                            </div>
                            {#if $paletteStore.some(p => p.name === palette.name)}
                                <div class="h-7 w-7 text-secondary-500">
                                    <svg data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" stroke-linecap="round" stroke-linejoin="round"></path>
                                    </svg>
                                </div>
                            {/if}
                        </div>

                       
                    {/each}
                </div>
            </svelte:fragment>
        </AccordionItem>
        <!-- ... -->
    </Accordion>
      


    
</div>