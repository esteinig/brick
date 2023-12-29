export type BrickRingTitle = {
    text: string
    italic: boolean
    code: boolean
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
    type: string;
    title: BrickRingTitle;
    data: RingSegment[]

    constructor(
        index: number, 
        visible: boolean = true,
        type: string = "Ring", 
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
        type: string = "ReferenceRing", 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: BrickRingTitle | null = null
    ) {
        super(index, visible, type, color, height, title)
        this.size = size;
    }

}

export class AnnotationRing extends Ring {
    constructor(
        index: number,
        visible: boolean = true,
        type: string = "AnnotationRing", 
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
        type: string = "BlastRing", 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: BrickRingTitle | null = null
    ) {
        super(index, visible, type, color, height, title)
    }
}

export class TextAnnotation extends Ring {
    constructor(
        index: number,
        visible: boolean = true,
        type: string = "TextAnnotation", 
        color: string = "#d3d3d3", 
        height: number = 20, 
        title: BrickRingTitle | null = null
    ) {
        super(index, visible, type, color, height, title)
    }
}