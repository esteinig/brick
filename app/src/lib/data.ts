import { type BlastRing, type AnnotationRing, type ReferenceRing, type BrickRingTitle, RingType, LabelRing } from "$lib/types";
import type { AnnotationConfig, PlotConfig, ReferenceConfig, RingConfig, TitleConfig } from "./brick/types";


let innerRingData: Array<ReferenceRing | AnnotationRing> = [

    {
        index: 0,
        visible: true,
        color: '#b4b87f',
        height: 20,
        type: RingType.ANNOTATION,
        title: {
            italic: false,
            code: true,
            text: 'Bakta v1.9.3',
        } satisfies BrickRingTitle,
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
        title: {
            italic: true,
            code: false,
            text: "Mycobacterium sp. SMC-2",
        },
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
        title: {
            italic: true,
            code: false,
            text: "Mycobacterium nebraskense",
        } satisfies BrickRingTitle,
        data: [
            {
                "color": "#8f5715",
                "end": 5012712,
                "start": 0,
                "text": ""
            }

        ]
    } satisfies BlastRing,
];

let outerRingData: Array<AnnotationRing | LabelRing> = [
    {
        index: 3,
        visible: true,
        color: '#d3d3d3',
        height: 20,
        type: RingType.LABEL,
        title: {
            italic: false,
            code: false,
            text: "Custom feature annotations",
        } satisfies BrickRingTitle,
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
    } satisfies AnnotationRing,
];

export const DEFAULT_CONFIG: PlotConfig = {
    reference: {
      size: 5983947
    } satisfies ReferenceConfig,
    title: {
      text: "Mycobacterium sp. nov. (SOLO)",
      color: "#d3d3d3",
      opacity: 0.8,
      fontStyle: 'italic',
      size: '100%'
    } satisfies TitleConfig, 
    rings: {
      radius: 200, 
      height: 20, 
      gap: 5
    } satisfies RingConfig,
    annotation: {
      lineLength: 42,
      lineStyle: "stroke: #d3d3d3; stroke-width: 0.07rem",
      textGap: 5,
      textStyle: "fill: #d3d3d3; opacity: 0.8; font-size: 90%"

    } satisfies AnnotationConfig
  }

export const DEFAULT_RINGS: Array<ReferenceRing | AnnotationRing | BlastRing> = [...innerRingData, ...blastRingData, ...outerRingData];