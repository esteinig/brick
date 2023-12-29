export type BrickInterfaceConfiguration = {
    svg_window_width: number
    svg_window_height: number
}

export const BRICK_INTERFACE_CONFIG_DEFAULT: BrickInterfaceConfiguration = {
    svg_window_width: 1024,
    svg_window_height: 768
}

export type SessionFile = {
    session_id: string
    id: string            
    name: string     
    name_original: string
    type: string
    format: string
    records: number
    length: number
}

export type FileConfig = {
    session_id: string
    file_format: FileFormat
    file_type: FileType
    original_filename: string
}

export type UploadConfig = {
    title: string
    url: string
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

export type ErrorResponse = {
    detail: string
}

export type FileUploadResponse = {
    task_id: string
} & ErrorResponse


export type TaskStatusResponse = {
    status: TaskStatus
    task_id: string
    result: SessionFile
} & ErrorResponse
