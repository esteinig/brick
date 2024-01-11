// store.ts
import { writable } from 'svelte/store';
import { type PlotConfig, type TitleConfig, type ReferenceConfig, type AnnotationConfig, type RingConfig, TitleStyle } from '$lib/types';

const initialPlotConfig: PlotConfig = {
    reference: { 
        size: 5983947
    },
    svg: {
        backgroundOpacity: 100,
        backgroundColor: "#d3d3d3"
    },
    title: {
      text: "BRICK v0.1.0",
      subtext: "",
      color: "#d3d3d3",
      opacity: 100,
      styles: [TitleStyle.ITALIC],
      size: 120
    },
    rings: { 
        radius: 200, 
        height: 20, 
        gap: 5 
    },
    annotation: {
      lineLength: 70,
      lineStyle: "stroke: #d3d3d3; stroke-width: 0.07rem",
      textGap: 5,
      textStyle: "fill: #d3d3d3; opacity: 0.8; font-size: 90%"
    }
};

export const plotConfigStore = writable<PlotConfig>(initialPlotConfig);

// Functions to update store attributes
export const updateTitle = (newTitle: TitleConfig) => {
    plotConfigStore.update(currentConfig => {
        return { ...currentConfig, title: newTitle };
    });
};

export const updateReference = (newReference: ReferenceConfig) => {
    plotConfigStore.update(currentConfig => {
        return { ...currentConfig, reference: newReference };
    });
};

export const updateAnnotation = (newAnnotation: AnnotationConfig) => {
    plotConfigStore.update(currentConfig => {
        return { ...currentConfig, annotation: newAnnotation };
    });
};

export const updateRings = (newRings: RingConfig) => {
    plotConfigStore.update(currentConfig => {
        return { ...currentConfig, rings: newRings };
    });
};