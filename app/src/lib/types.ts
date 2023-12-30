export type BrickRingTitle = {
    text: string
    italic: boolean
    code: boolean
}


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
    title: BrickRingTitle;
    data: RingSegment[]

    constructor(
        index: number, 
        visible: boolean = true,
        type: RingType = RingType.GENERIC, 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: BrickRingTitle | null = null
    ) {
        
        this.index = index;
        this.visible = visible;
        this.color = color;
        this.height = height;
        this.type = type;
        
        this.title = title ?? {
            text: `Ring ${index}`,
            italic: false,
            code: false
        } satisfies BrickRingTitle;

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
        title: BrickRingTitle | null = null
    ) {
        super(index, visible, type, color, height, title)
        this.size = size;
        this.data = [
            {start: 0, end: size, color: color, text: title ? title.text: "Reference"}
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
        title: BrickRingTitle | null = null
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
        title: BrickRingTitle | null = null
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
        title: BrickRingTitle | null = null
    ) {
        super(index, visible, type, color, height, title)
    }
}