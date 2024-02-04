
/*  ===========
 *  BRICK RINGS
 *  ===========
*/

import { createUuid } from "./helpers"


export enum RingType {
    GENERIC = "generic",
    REFERENCE = "reference",
    BLAST = "blast",
    ANNOTATION = "annotation",
    LABEL = "label",
    GENOMAD = "genomad"
}

export type SegmentMeta = {
    plasmid: number
    chromosome: number
    virus: number
}

export type RingSegment = {
    start: number
    end: number
    text: string
    labelIdentifier?: string
    lineLength?: number
    lineWidth?: number
    lineOpacity?: number
    lineColor?: string
    textSize?: number
    textColor?: string
    textOpacity?: number
    lineAngle?: number
    plasmid?: number
    chromosome?: number
    virus?: number
}

export type RingReference = {
    session_id: string
    reference_id: string
    sequence: Sequence
}

export class Ring {
    id: string;
    reference: RingReference;
    index: number;
    visible: boolean;
    color: string;
    height: number;
    type: RingType;
    title: string;
    data: RingSegment[]

    // Special fields for subclasses
    size?: number;
    lineSmoothing?: boolean;
    lineHeight?: number;

    constructor(
        reference: RingReference,
        index: number, 
        visible: boolean = true,
        type: RingType = RingType.GENERIC, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Ring"
    ) { 
        this.id = createUuid()
        this.reference = reference
        this.index = index;
        this.visible = visible;
        this.color = color;
        this.height = height;
        this.type = type;
        this.title = title;
        this.data = [];
    }
}

export class ReferenceRing extends Ring {
    size: number;

    constructor(
        reference: RingReference,
        index: number,
        size: number,
        visible: boolean = true,
        type: RingType = RingType.REFERENCE, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Reference Ring"
    ) {
        super(reference, index, visible, type, color, height, title)
        this.id = createUuid();
        this.size = size;
        this.data = [
            {start: 0, end: size, text: title}
        ];
    }

}

export class AnnotationRing extends Ring {
    constructor(
        reference: RingReference,
        index: number,
        visible: boolean = true,
        type: RingType = RingType.ANNOTATION, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Annotation Ring"
    ) {
        super(reference, index, visible, type, color, height, title)
        this.id = createUuid();
    }
}

export class BlastRing extends Ring {
    constructor(
        reference: RingReference,
        index: number,
        visible: boolean = true,
        type: RingType = RingType.BLAST, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Blast Ring"
    ) {
        super(reference, index, visible, type, color, height, title)
        this.id = createUuid();
    }
}


export class GenomadRing extends Ring {

    constructor(
        reference: RingReference,
        index: number,
        visible: boolean = true,
        type: RingType = RingType.GENOMAD, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "geNomad Ring",
        lineSmoothing: boolean = false,
    ) {
        super(reference, index, visible, type, color, height, title)
        this.id = createUuid();
        this.lineSmoothing = lineSmoothing;
        this.lineHeight = height;
    }
}

export class LabelRing extends Ring {

    constructor(
        reference: RingReference,
        index: number,
        visible: boolean = true,
        type: RingType = RingType.LABEL, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Label Ring"
    ) {
        super(reference, index, visible, type, color, height, title)
        this.id = createUuid();
    }
}


/*  =============
 *  SESSION FILES
 *  =============
*/


export type Sequence = {
    id: string
    length: number
}

export type Selections = {
    sequences: Sequence[]
    features: string[]
    qualifiers: string[]
}

export type SessionFile = {
    session_id: string
    id: string       
    type: string
    format: string
    records: number
    total_length: number
    name_original: string
    selections: Selections
}

export type FileConfig = {
    session_id: string
    file_format: FileFormat
    file_type: FileType
    original_filename: string
}

export type UploadConfig = {
    id: string
    title: string
    message: string
    meta: string
    single: boolean
    format: FileFormat
    type: FileType
    info: string
}

export enum FileFormat {
    FASTA = "fasta",
    GENBANK = "genbank",
    TSV = "tsv",
    JSON = "json"
}

export enum FileType {
    REFERENCE = "reference",
    GENOME = "genome",
    ANNOTATION_GENBANK = "annotation_genbank",
    ANNOTATION_CUSTOM = "annotation_custom",
    SESSION = "session"
}

export enum TaskStatus {
    PENDING = "PENDING",
    STARTED = "STARTED",
    SUCCESS = "SUCCESS",
    FAILURE = "FAILURE",
    PROCESSING = "PROCESSING"
}

/*  ================
 *  API RING SCHEMAS
 *  ================
*/

export enum BlastMethod {
    BLASTN = "blastn"
}


export enum GenomadPredictionClass {
    CHROMOSOME = "chromosome",
    PLASMID = "plasmid",
    VIRUS = "virus"
}

// Ring reference can be null in this schema
// but is required at endpoint, this is so
// that the $ringReferenceStore can be null
// when no reference or sequence is available
// or selected by user in application
export type RingSchema = {
    reference: RingReference | null  
}

export type ReferenceRingSchema = {} & RingSchema

export type BlastRingSchema = {
    genome_id: string
    blast_method: BlastMethod
    min_identity: number
    min_alignment: number
    min_evalue: number
} & RingSchema


export type GenomadRingSchema = {
    window_size: number
    min_window_score: number
    min_segment_score: number
    min_segment_length: number
    prediction_classes: GenomadPredictionClass[]
    ring_type: RingType.LABEL | RingType.ANNOTATION | RingType.GENOMAD
} & RingSchema

export type AnnotationRingSchema = {
    genbank_id: string | null
    tsv_id: string | null
    genbank_features: string[]
    genbank_qualifiers: string[]
} & RingSchema


export type LabelRingSchema = {
    tsv_id: string | null
    labels: RingSegment[]
} & RingSchema

export type RingUpdateSchema = {
    id: string
    index: number | null
    color: string | null
    height: number | null
    title: string | null
    visible: boolean | null
    index_group: string[] | null
}

export type LabelUpdateSchema = {
    ring_id: string
    label_id: string
    lineLength: number | null
    lineWidth: number | null 
    lineAngle: number | null 
    lineColor: string | null 
    text: string | null
    textSize: number | null 
    textColor: string | null 
}


/*  =============
 *  FORM ACTIONS
 *  =============
*/

export type ActionRequestData = {
    action: string
    body: FormData
}

export type ActionRequestDataUpdate = {
    updateDatabase: boolean
    updateVerbose: boolean
} & ActionRequestData

/*  =============
 *  API RESPONSES
 *  =============
*/

export type ErrorResponse = {
    detail: string
}

export type FileUploadResponse = {
    task_id: string
} & ErrorResponse

export type CreateRingResponse = {
    task_id: string
} & ErrorResponse

export enum TaskResultType {
    SESSION = 'SESSION',
    SESSION_FILE = 'SESSION_FILE',
    BLAST_RING = 'BLAST_RING',
    ANNOTATION_RING = 'ANNOTATION_RING',
    LABEL_RING = 'LABEL_RING',
    REFERENCE_RING = 'REFERENCE_RING',
    GENOMAD_RING = 'GENOMAD_RING'
}

export type TaskStatusResponse = {
    status: TaskStatus
    task_id: string
    result: Session | SessionFile | BlastRing | AnnotationRing | LabelRing
    result_type: TaskResultType 
} & ErrorResponse

export type PydanticValidationError = {
    ctx: any,
    input: any,
    loc: string[]
    msg: string
    type: string
    url: string
}

export type Session = {
    id: string
    date: string
    files: SessionFile[]
    rings: Ring[]
}


export type SessionResponse = Session & ErrorResponse;


/*  ==================
 *  PLOT CONFIGURATION
 *  ==================
*/


export type TitleStyle = {
    italic: boolean
    bold: boolean
    code: boolean
}

export type PlotConfig = {
    title: TitleConfig
    transition: TransitionConfig
    subtitle: SubtitleConfig
    rings: RingConfig
    svg: SvgConfig
    labels: LabelConfig
}

export type TransitionConfig = {
    enabled: boolean
    fadeDuration: number
    fadeDelay: number
}

export type SvgConfig = {
    backgroundOpacity: number
    backgroundColor: string
    zoomEnabled: boolean
    zoomLowerLimit: number
    zoomUpperLimit: number
    positionEnabled: boolean
    tooltipEnabled: boolean
}

export type TitleConfig = {
    text: string
    color: string
    opacity: number
    style: TitleStyle
    size: number
}


export type SubtitleConfig = {
    text: string
    color: string
    opacity: number
    style: TitleStyle
    size: number
    height: number
}

export type LabelConfig = {
    lineColor: string
    lineWidth: number
    lineOpacity: number
    lineLength: number
    textColor: string
    textSize: number
    textOpacity: number
    textGap: number
}

export type RingConfig = {
    radius: number
    height: number
    outerHeight: number
    gap: number
    labelGap: number
    lineWidth: number
    lineSmoothing: boolean
}


/*  ==================
 *  COLOR PALETTES
 *  ==================
*/

export interface Color {
    title: string;
    subtitle: string;
    color: string; // HEX color code
    url: string;
  }


export type Palette = {
    name: string
    subtitle: string
    colors: string[]
    link: string
}

export type PaletteItem = {
    name: PaletteName
    palettes: Palette[]
    link: string
    author: string
}

export enum PaletteName {
    NZ = "Manu New Zealand",
    NP = "National Parks Palettes",
    MOMA = "Museum of Modern Art"
}


export enum RingDirection {
    IN = "in",
    OUT = "out"
}