
export type ReferenceData = {
    name: string     // ref name title
    italic: boolean  // ref name title italic?
    size: number     // total ref ring arc size
}

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

export type RingSegment = {
    color: string  // color value
    start: number  // start end on arc seg
    end: number
    text: string   // html text span tooltip
}