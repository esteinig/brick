// store.ts
import { writable } from 'svelte/store';
import { type PlotConfig, TitleStyle } from '$lib/types';

const initialPlotConfig: PlotConfig = {
    svg: {
        backgroundOpacity: 100,
        backgroundColor: "#d3d3d3",
        zoomEnabled: false,
        zoomLowerLimit: 0.5,
        zoomUpperLimit: 10
    },
    title: {
      text: "BRICK v0.1.0",
      color: "#d3d3d3",
      opacity: 100,
      styles: [TitleStyle.ITALIC],
      size: 120
    },
    subtitle: {
        text: "",
        color: "#d3d3d3",
        opacity: 100,
        styles: [TitleStyle.ITALIC],
        size: 100,
        height: 100
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
