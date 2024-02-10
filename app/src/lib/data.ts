import { type BlastRing, type AnnotationRing, type ReferenceRing, RingType, LabelRing, type Palette, type RingReference, Ring } from "$lib/types";
import type { Session } from "$lib/types";


/** DEFAULT DATA */ 

export const DEFAULT_COLOR: string = "#d3d3d3"

/** FALLBACK DATA */ 

export const FALLBACK_REFERENCE: RingReference = {
    session_id: "DEFAULT", 
    reference_id: "DEFAULT", 
    sequence: { 
        id: "SOLO", 
        length: 5983947 
    }
}

let innerRingData: Array<ReferenceRing | AnnotationRing> = [

    {   
        id: 'drgaetyq346',
        index: 0,
        visible: true,
        color: '#b4b87f',
        height: 20,
        type: RingType.ANNOTATION,
        title: "Open reading frames from Bakta v1.9.3",
        reference: FALLBACK_REFERENCE,
        data: [
            {
                "meta": null,
                "end": 4012712,
                "start": 0,
                "text": ""
            }
        ]
    },
];

let blastRingData: Array<BlastRing> = [
    {   
        id: '346q345q5yq',
        index: 1,
        visible: true,
        color: '#6ea8ab',
        height: 20,
        type: RingType.BLAST,
        title: "Mycobacterium sp. SMC-2",
        reference: FALLBACK_REFERENCE,
        data: [
            {
                "meta": null,
                "end": 5012712,
                "start": 0,
                "text": ""
            }
        ]
    },
    {   
        id: 'wsetrweryt246t36',
        index: 2,
        visible: true,
        color: '#8f5715',
        height: 20,
        type: RingType.BLAST,
        title: "Mycobacterium nebraskense",
        reference: FALLBACK_REFERENCE,
        data: [
            {
                "meta": null,
                "end": 5012712,
                "start": 0,
                "text": ""
            }

        ]
    },
];

let outerRingData: Array<AnnotationRing | LabelRing> = [
    {   
        id: '3dfgaerty25',
        index: 3,
        visible: true,
        color: '#d3d3d3',
        height: 20,
        type: RingType.LABEL,
        title: "Custom feature labels",
        reference: FALLBACK_REFERENCE,
        data: [
            {
                "meta": null,
                "end": 747778,
                "start": 742382,
                "text": "Phage-associated"
            },
            {
                "meta": null,
                "end": 2247778,
                "start": 2242382,
                "text": "Penicillin resistance"
            },
            {
                "meta": null,
                "end": 3747778,
                "start": 3742382,
                "text": "Mobile element integration"
            },
        ]
    },
];

export const FALLBACK_RINGS: Array<ReferenceRing | AnnotationRing | BlastRing> = [...innerRingData, ...blastRingData, ...outerRingData];

export const FALLBACK_SESSION: Session = {
    id: 'FALLBACK',
    date: '2024-01-23T02:47:28.686146',
    files: [],
    rings: FALLBACK_RINGS
}

/** PALETTES */ 

// MoMA

const DALI = [
    "#b4b87f", "#9c913f", "#585b33", "#6ea8ab", "#397893", "#31333f", "#8f5715", "#ba9a44", "#cfbb83"
];

const PANTON = [
    "#e84a00", "#bb1d2c", "#9b0c43", "#661f66", "#2c1f62", "#006289", "#004759"
];

const RATTNER = [
    "#de8e69", "#f1be99", "#c1bd38", "#7a9132", "#4c849a", "#184363", "#5d5686", "#a39fc9"
];

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

// Manu New Zealand

const HOIHO = [
    "#CABEE9", "#7C7189", "#FAE093", "#D04E59", "#BC8E7D", "#2F3D70"
];

const KAKAPO = [
    "#7D9D33", "#CED38C", "#DCC949", "#BCA888", "#CD8862", "#775B24"
];

const KAKARIKI = [
    "#44781E", "#A1B654", "#2C3B75", "#B8321A", "#565052"
];

const KERERU = [
    "#325756", "#7d9fc2", "#C582B2", "#51806a", "#4d5f8e", "#A092B7"
];

const TAMBJA = [
    "#3399ff", "#666600", "#003399", "#999900", "#000000"
];


// National Parks

const Acadia = [
    "#212E52", "#444E7E", "#8087AA", "#B7ABBC", "#F9ECE8", "#FCC893", "#FEB424", "#FD8700", "#D8511D"
];
const Arches = [
    "#1A3D82", "#0C62AF", "#4499F5", "#8FCAFD", "#F2F2F2", "#F0AC7D", "#CD622E", "#B14311", "#832B0F"
];
const Arches2 = [
    "#3A1F46", "#7F4B89", "#B46DB3", "#E3A5D6", "#F3DAE4"
];
const Banff = [
    "#006475", "#00A1B7", "#55CFD8", "#586028", "#898928", "#616571", "#9DA7BF"
];
const BryceCanyon = [
    "#882314", "#C0532B", "#CF932C", "#674D53", "#8C86A0", "#724438", "#D5AB85"
];
const CapitolReef = [
    "#291919", "#532A34", "#7C5467", "#878195", "#AEB2B7", "#D4D9DD"
];
const Charmonix = [
    "#008FF8", "#B6AA0D", "#E2C2A2", "#E23B0E", "#F2C621", "#196689"
];
const CraterLake = [
    "#1D4A79", "#794C23", "#6B7444", "#6089B5", "#BF9785", "#275E4D", "#807B7F"
];
const Cuyahoga = [
    "#E07529", "#FAAE32", "#7F7991", "#A84A00", "#5D4F36", "#B39085"
];
const DeathValley = [
    "#8C2B0E", "#C5692D", "#FEB359", "#132F5B", "#435F90", "#68434E", "#B47E83"
];
const Denali = [
    "#20223E", "#3F3F7B", "#278192", "#00B089", "#2EEA8C", "#8FF7BD"
];
const Everglades = [
    "#345023", "#596C0B", "#83A102", "#003B68", "#426F86", "#7A712F"
];
const Glacier = [
    "#01353D", "#088096", "#58B3C7", "#7AD4E4", "#B8FCFC"
];
const GrandCanyon = [
    "#521E0F", "#9C593E", "#DDA569", "#3F4330", "#8E7E3C", "#2A4866", "#6592B0"
];
const Halekala = [
    "#722710", "#A3844D", "#675243", "#A85017", "#838BAA"
];
const IguazuFalls = [
    "#415521", "#97AD3D", "#4C3425", "#7F6552", "#5A8093", "#9FBAD3"
];
const KingsCanyon = [
    "#613921", "#A77652", "#F2C27B", "#AAC9ED", "#44637D", "#8E949F"
];
const LakeNakuru = [
    "#D76E9A", "#A1ACC8", "#AD3C36", "#332627", "#EACACF", "#AA6B77"
];
const Olympic = [
    "#3A4330", "#426737", "#75871B", "#BAB97D", "#FAF3CE", "#FDE16A", "#F9B40E", "#E88C23", "#A25933"
];
const Redwood = [
    "#5E3B49", "#9B5F6B", "#BA817D", "#325731", "#6A9741", "#5F4E2F"
];
const RockyMtn = [
    "#274C31", "#A3AEB5", "#2F4B6A", "#8F8081", "#3F7156", "#6F89A7", "#5B5443"
];
const Saguaro = [
    "#127088", "#C85729", "#92874B", "#CD8A39", "#AC3414", "#57643C"
];
const SmokyMtns = [
    "#42511A", "#889D35", "#D3D175", "#B50200", "#DA6C41", "#7C6E66", "#BCAFA6"
];
const SouthDowns = [
    "#948D2A", "#D5B44D", "#89A4BF", "#F1D6B6", "#9B8358", "#577291"
];
const Torres = [
    "#2F397A", "#7391BD", "#894846", "#E9988C", "#535260", "#B7A7A6", "#785838", "#C68D61", "#4F6008", "#93995C"
];
const Triglav = [
    "#386EC2", "#B5B5B2", "#990006", "#625D0A", "#B9741F", "#213958"
];
const WindCave = [
    "#2F100E", "#6C3322", "#B07159", "#C9A197", "#E0CDCD"
];
const Volcanoes = [
    "#082544", "#1E547D", "#79668C", "#DE3C37", "#F2DC7E"
];
const Yellowstone = [
    "#0067A2", "#DFCB91", "#CB7223", "#289A84", "#7FA4C2", "#AF7E56"
];
const Yosemite = [
    "#293633", "#3D5051", "#6B7F7F", "#87A1C7", "#516B95", "#304F7D"
];


export const NATIONAL_PARK_PALETTES: Palette[] = [
        { name: 'Acadia', subtitle: "Acadia National Park", colors: Acadia, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Acadia.png" },
        { name: 'Arches', subtitle: "Arches National Park", colors: Arches, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Arches.png" },
        { name: 'Arches #2', subtitle: "Arches National Park (Variant)", colors: Arches2, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Arches2.png" },
        { name: 'Banff', subtitle: "Banff National Park", colors: Banff, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Banff.png" },
        { name: 'Bryce Canyon', subtitle: "Bryce Canyon National Park", colors: BryceCanyon, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/BryceCanyon.png" },
        { name: 'Capitol Reef', subtitle: "Capitol Reef National Park", colors: CapitolReef, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/CapitolReef.png" },
        { name: 'Charmonix', subtitle: "Charmonix", colors: Charmonix, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Charmonix.png" },
        { name: 'Crater Lake', subtitle: "Crater Lake National Park", colors: CraterLake, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/CraterLake.png" },
        { name: 'Cuyahoga', subtitle: "Cuyahoga Valley National Park", colors: Cuyahoga, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Cuyahoga.png" },
        { name: 'Death Valley', subtitle: "Death Valley National Park", colors: DeathValley, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/DeathValley.png" },
        { name: 'Denali', subtitle: "Denali National Park", colors: Denali, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Denali.png" },
        { name: 'Everglades', subtitle: "Everglades National Park", colors: Everglades, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Everglades.png" },
        { name: 'Glacier', subtitle: "Glacier National Park", colors: Glacier, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Glacier.png" },
        { name: 'Grand Canyon', subtitle: "Grand Canyon National Park", colors: GrandCanyon, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/GrandCanyon.png" },
        { name: 'Halekala', subtitle: "Haleakalā National Park", colors: Halekala, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Halekala.png" },
        { name: 'Iguazu Falls', subtitle: "Iguazu Falls", colors: IguazuFalls, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/IguazuFalls.png" },
        { name: 'Kings Canyon', subtitle: "Kings Canyon National Park", colors: KingsCanyon, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/KingsCanyon.png" },
        { name: 'Lake Nakuru', subtitle: "Lake Nakuru", colors: LakeNakuru, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/LakeNakuru.png" },
        { name: 'Olympic', subtitle: "Olympic National Park", colors: Olympic, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Olympic.png" },
        { name: 'Redwood', subtitle: "Redwood National and State Parks", colors: Redwood, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Redwood.png" },
        { name: 'Rocky Mountains', subtitle: "Rocky Mountains National Park", colors: RockyMtn, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/RockyMtn.png" },
        { name: 'Saguaro', subtitle: "Saguaro National Park", colors: Saguaro, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Saguaro.png" },
        { name: 'Smoky Mountains', subtitle: "Great Smoky Mountains National Park", colors: SmokyMtns, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/SmokyMtns.png" },
        { name: 'South Downs', subtitle: "South Downs", colors: SouthDowns, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/SouthDowns.png" },
        { name: 'Torres', subtitle: "Torres del Paine National Park", colors: Torres, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Torres.png" },
        { name: 'Triglav', subtitle: "Triglav National Park", colors: Triglav, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Triglav.png" },
        { name: 'Wind Cave', subtitle: "Wind Cave National Park", colors: WindCave, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/WindCave.png" },
        { name: 'Volcanoes', subtitle: "Hawaiʻi Volcanoes National Park", colors: Volcanoes, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Volcanoes.png" },
        { name: 'Yellowstone', subtitle: "Yellowstone National Park", colors: Yellowstone, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Yellowstone.png" },
        { name: 'Yosemite', subtitle: "Yosemite National Park", colors: Yosemite, link: "https://github.com/kevinsblake/NatParksPalettes/blob/main/photos/Yosemite.png" }
];

export const MOMA_PALETTES: Palette[] = [
    { name: 'Salvador Dalí', subtitle: "The Persistence of Memory (1931)", colors: DALI, link: "https://www.moma.org/collection/works/79018" },
    { name: 'Verner Panton', subtitle: "Spectrum textile (1974)", colors: PANTON, link: "https://www.moma.org/collection/works/292747?artist_id=4485&page=1&sov_referrer=artist" },
    { name: "Vincent van Gogh", subtitle: "The Starry Night (Saint Rémy, June 1889)", colors: VANGOGH, link: "https://www.moma.org/collection/works/79802?sov_referrer=theme&theme_id=5134" },
    { name: 'Abraham Rattner', subtitle: "Mother and Child (1938)", colors: RATTNER, link: "https://www.moma.org/collection/works/78474?classifications=9&date_begin=Pre-1850&date_end=2023&direction=fwd&include_uncataloged_works=1&page=37&q=&utf8=%E2%9C%93" },
    { name: 'Shay Alkalay', subtitle: "Stack (2008)", colors: ALKALAY, link: "https://www.moma.org/collection/works/126820?classifications=3&date_begin=Pre-1850&date_end=2023&direction=fwd&page=5&q=&utf8=%E2%9C%93&with_images=1" },
    { name: 'Maude Schuyler Clay', subtitle: "Sarah Cross (1980)", colors: CLAY, link: "https://www.moma.org/collection/works/49695?artist_id=1139&page=1&sov_referrer=artist" },
    { name: 'Matt Connors', subtitle: "Egypt, Hard G (2015)", colors: CONNORS, link: "https://www.moma.org/collection/works/202454?artist_id=36363&page=1&sov_referrer=artist" },
    { name: 'Steve Doughton', subtitle: "Ferrum 5000 (1995)", colors: DOUGHTON, link: "https://www.moma.org/collection/works/314423" },
    { name: 'Max Ernst', subtitle: "Two Children Are Threatened by a Nightingale (1924)", colors: ERNST, link: "https://www.moma.org/collection/works/79293" },
    { name: 'David Klein', subtitle: "New York Fly TWA (1956)", colors: KLEIN, link: "https://www.moma.org/collection/works/6291?artist_id=3134&page=1&sov_referrer=artist" },
    { name: 'Sherrie Levine', subtitle: "After Mondrian from Meltdown (1989)", colors: LEVINE, link: "https://www.moma.org/collection/works/65715" },
    { name: "Georgia O'Keeffe", subtitle: "Abstraction Blue (1927)", colors: OKEEFFE, link: "https://www.moma.org/collection/works/78677?sov_referrer=theme&theme_id=5264" },
    { name: "Zorawar Sidhu, Rob Swainston", subtitle: "May 24 from the series Doomscrolling (2020-21)", colors: SIDHU, link: "https://www.moma.org/collection/works/431041?artist_id=134546&page=1&sov_referrer=artist" },
];

export const NZ_PALETTES: Palette[] = [
    { name: 'Hoiho', subtitle: "Megadyptes antipodes", colors: HOIHO, link: "" },
    { name: 'Kākāpō', subtitle: "Strigops habroptilus", colors: KAKAPO, link: "" },
    { name: 'Kākāriki', subtitle: "Cyanoramphus spp.",colors: KAKARIKI, link: "" },
    { name: 'Kererū', subtitle: "Hemiphaga novaeseelandiae", colors: KERERU, link: "" },
    { name: 'Gloomy nudibranch', subtitle: "Tambja kushimotoensis", colors: TAMBJA, link: "" },
];