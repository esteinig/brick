// store.ts
import { writable, get } from 'svelte/store';
import { type PlotConfig } from '$lib/types';

const initialPlotConfig: PlotConfig = {
    svg: {
        backgroundOpacity: 0,
        backgroundColor: "#d3d3d3",
        zoomEnabled: false,
        zoomLowerLimit: 0.5,
        zoomUpperLimit: 10
    },
    transition: {
      enabled: true,
      fadeDelay: 0,
      fadeDuration: 800
    },
    title: {
      text: "BRICK",
      color: "#d3d3d3",
      opacity: 80,
      style: {
        italic: false,
        bold: false,
        code: false
      },
      size: 120
    },
    subtitle: {
        text: "BRIG-like Interactive Circular Knowledgebase",
        color: "#d3d3d3",
        opacity: 80,
        style: {
          italic: false,
          bold: false,
          code: false
        },
        size: 90,
        height: 120
    },
    rings: { 
        radius: 200, 
        height: 20, 
        gap: 5 
    },
    labels: {
      lineColor: "#d3d3d3",
      lineWidth: 7,
      lineOpacity: 80,
      lineLength: 50,
      textColor: "#d3d3d3",
      textSize: 90,
      textOpacity: 80,
      textGap: 5
    }
};

export function getTransitionDurationTotal() {
  const plotConfig = get(plotConfigStore);
  return plotConfig.transition.fadeDelay + plotConfig.transition.fadeDuration;
}
export const plotConfigStore = writable<PlotConfig>(initialPlotConfig);
