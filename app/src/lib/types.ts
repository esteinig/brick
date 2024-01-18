
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
    LABEL = "label"
}


export type RingSegment = {
    start: number
    end: number
    color: string
    text: string
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
        this.id = createUuid()
        this.size = size;
        this.data = [
            {start: 0, end: size, color: color, text: title}
        ]
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
        this.id = createUuid()
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
        this.id = createUuid()
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
        this.id = createUuid()
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
    name_original: string,
    selections: Selections
}

export type FileConfig = {
    session_id: string
    file_format: FileFormat
    file_type: FileType
    original_filename: string
}

export type UploadConfig = {
    title: string
    message: string
    meta: string
    single: boolean
    format: FileFormat
    type: FileType
}

export enum FileFormat {
    FASTA = "fasta",
    GENBANK = "genbank",
    TSV = "tsv"
}

export enum FileType {
    REFERENCE = "reference",
    GENOME = "genome",
    ANNOTATION_GENBANK = "annotation_genbank",
    ANNOTATION_CUSTOM = "annotation_custom"
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

export type RingSchema = {
    reference: RingReference
}

export type BlastRingSchema = {
    genome_id: string
    blast_method: BlastMethod,
    min_identity: number
    min_alignment: number
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

export type TaskStatusResponse = {
    status: TaskStatus
    task_id: string
    result: SessionFile
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

export enum TitleStyle {
    ITALIC = "italic",
    BOLD = "bold",
    CODE = "code",
    NORMAL = "normal"
}

export type PlotConfig = {
    title: TitleConfig
    subtitle: SubtitleConfig
    rings: RingConfig
    svg: SvgConfig
    annotation: AnnotationConfig
}

export type SvgConfig = {
    backgroundOpacity: number
    backgroundColor: string
    zoomEnabled: boolean
    zoomLowerLimit: number
    zoomUpperLimit: number
}

export type TitleConfig = {
    text: string
    color: string
    opacity: number
    styles: TitleStyle[]
    size: number
}


export type SubtitleConfig = {
    text: string
    color: string
    opacity: number
    styles: TitleStyle[]
    size: number
    height: number
}

export type AnnotationConfig = {
    lineLength: number
    lineStyle: string
    textGap: number
    textStyle: string
}

export type RingConfig = {
    radius: number
    height: number
    gap: number
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