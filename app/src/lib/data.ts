import { type BlastRing, type AnnotationRing, type ReferenceRing, RingType, LabelRing } from "$lib/types";

let innerRingData: Array<ReferenceRing | AnnotationRing> = [

    {
        index: 0,
        visible: true,
        color: '#b4b87f',
        height: 20,
        type: RingType.ANNOTATION,
        title: "Open reading frames from Bakta v1.9.3",
        data: [
            {
                "color": "#b4b87f",
                "end": 4012712,
                "start": 0,
                "text": ""
            }
        ]
    } satisfies AnnotationRing,
];

let blastRingData: Array<BlastRing> = [
    {
        index: 1,
        visible: true,
        color: '#6ea8ab',
        height: 20,
        type: RingType.BLAST,
        title: "Mycobacterium sp. SMC-2",
        data: [
            {
                "color": "#6ea8ab",
                "end": 5012712,
                "start": 0,
                "text": ""
            }
        ]
    },
    {
        index: 2,
        visible: true,
        color: '#8f5715',
        height: 20,
        type: RingType.BLAST,
        title: "Mycobacterium nebraskense",
        data: [
            {
                "color": "#8f5715",
                "end": 5012712,
                "start": 0,
                "text": ""
            }

        ]
    },
];

let outerRingData: Array<AnnotationRing | LabelRing> = [
    {
        index: 3,
        visible: true,
        color: '#d3d3d3',
        height: 20,
        type: RingType.LABEL,
        title: "Custom feature labels",
        data: [
            {
                "color": "#8f5715",
                "end": 747778,
                "start": 742382,
                "text": "Phage-associated"
            },
            {
                "color": "#8f5715",
                "end": 2247778,
                "start": 2242382,
                "text": "Penicillin resistance"
            },
            {
                "color": "#8f5715",
                "end": 3747778,
                "start": 3742382,
                "text": "Mobile element integration"
            },
        ]
    },
];

export const DEFAULT_RINGS: Array<ReferenceRing | AnnotationRing | BlastRing> = [...innerRingData, ...blastRingData, ...outerRingData];


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

export const MOMA_PALETTES = [
    { name: 'Salvador Dalí', artwork: "The Persistence of Memory (1931)", colors: DALI, link: "https://www.moma.org/collection/works/79018" },
    { name: 'Verner Panton', artwork: "Spectrum textile (1974)", colors: PANTON, link: "https://www.moma.org/collection/works/292747?artist_id=4485&page=1&sov_referrer=artist" },
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
];
export const NZ_PALETTES = [
    { name: 'Hoiho', species: "Megadyptes antipodes", colors: HOIHO },
    { name: 'Kākāpō', species: "Strigops habroptilus", colors: KAKAPO },
    { name: 'Kākāriki', species: "Cyanoramphus spp.",colors: KAKARIKI },
    { name: 'Kererū', species: "Hemiphaga novaeseelandiae", colors: KERERU },
    { name: 'Gloomy nudibranch', species: "Tambja kushimotoensis", colors: TAMBJA },
];