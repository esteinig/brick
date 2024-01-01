
/*  ===========
 *  BRICK RINGS
 *  ===========
*/



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

export class Ring {
    index: number;
    visible: boolean;
    color: string;
    height: number;
    type: RingType;
    title: string;
    data: RingSegment[]

    constructor(
        index: number, 
        visible: boolean = true,
        type: RingType = RingType.GENERIC, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "Ring"
    ) {
        
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
        index: number,
        size: number,
        visible: boolean = true,
        type: RingType = RingType.REFERENCE, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "ReferenceRing"
    ) {
        super(index, visible, type, color, height, title)
        this.size = size;
        this.data = [
            {start: 0, end: size, color: color, text: title}
        ]
    }

}

export class AnnotationRing extends Ring {
    constructor(
        index: number,
        visible: boolean = true,
        type: RingType = RingType.ANNOTATION, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "AnnotationRing"
    ) {
        super(index, visible, type, color, height, title)
    }
}

export class BlastRing extends Ring {
    constructor(
        index: number,
        visible: boolean = true,
        type: RingType = RingType.BLAST, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "BlastRing"
    ) {
        super(index, visible, type, color, height, title)
    }
}

export class LabelRing extends Ring {
    constructor(
        index: number,
        visible: boolean = true,
        type: RingType = RingType.LABEL, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: string = "LabelRing"
    ) {
        super(index, visible, type, color, height, title)
    }
}


/*  =============
 *  SESSION FILES
 *  =============
*/

export type SessionFile = {
    session_id: string
    id: string       
    type: string
    format: string
    records: number
    length: number
    name_original: string
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

/*  ===============
 *  API RING SCHEMAS
 *  ================
*/

export enum BlastMethod {
    BLASTN = "blastn"
}

export type BlastRingSchema = {
    session_id: string
    reference_id: string
    genome_id: string
    blast_method: BlastMethod,
    min_identity: number
    min_alignment: number
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

export type BlastRingResponse = {
    task_id: string
} & ErrorResponse

export type TaskStatusResponse = {
    status: TaskStatus
    task_id: string
    result: SessionFile
} & ErrorResponse


/*  ==================
 *  PLOT CONFIGURATION
 *  ==================
*/

export type PlotConfig = {
    reference: ReferenceConfig
    title: TitleConfig
    rings: RingConfig
    annotation: AnnotationConfig
}
export type ReferenceConfig = {
    size: number
}

export type TitleConfig = {
    text: string
    color: string
    opacity: number
    fontStyle: string,
    size: string
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