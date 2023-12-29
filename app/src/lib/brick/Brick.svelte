<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  import type { PlotConfig } from './types';
  import { downloadJSON, downloadPNG, downloadSVG } from './helpers';
	import type { Ring, RingSegment } from '$lib/types';
	import { DEFAULT_CONFIG } from '$lib/data';

  const TEXT_ROTATION: number = 90;  // arc segment annotations otherwise start at 3 pm
  
  export let rings: Ring[];

  export let id: string = "brickRingPlot";
  export let width: number = 600;
  export let height: number = 600;

  export let zoom: boolean = true;
  export let buttons: boolean = false;

  export let config: PlotConfig = DEFAULT_CONFIG;

  onMount(() => {
    if (zoom) {
      let svgGroup = d3.select('#brickRingPlot g');
      d3.select('#brickRingPlot svg')
        .call(
          d3.zoom()
            .scaleExtent([0.5, 5])
            .on('zoom', (event: any) => {
                svgGroup.attr('transform', event.transform);
            })
        );
    }
  });

  let degreeScale = d3.scaleLinear([0, config.reference.size], [0,360]);

  // All ring data is fed through this generator which will calculate the start
  // and end angles on the circle for each segment and adjust inner and outer
  // heights based on radius, ring height and gap size
  function arcGenerator(d: RingSegment, index: number, height: number): string {
    
    const ringHeight = getRingHeight(rings, 0, index);

    return d3.arc()
      .innerRadius(config.rings.radius+(index*config.rings.gap)+ringHeight)
      .outerRadius(config.rings.radius+(index*config.rings.gap)+ringHeight+height)
      .startAngle((d: RingSegment) => (degreeScale(d.start)) * (Math.PI / 180))
      .endAngle((d: RingSegment) => (degreeScale(d.end)) * (Math.PI / 180))
      (d);
  }

  function getRingHeight(rings: Ring[], start_index: number, end_index: number): number {
    return rings.slice(start_index, end_index+1).map(ring => ring.height).reduce((a, b) => a+b)
  }

  function getOuterRingHeight(rings: Ring[]): number {
    return rings.map(ring => ring.height+config.rings.gap).reduce((a, b) => a+b)+config.rings.radius
  }

  // Function to calculate the midpoint of an arc segment
  function calculateMidpoint(d: RingSegment): number {
      return (degreeScale((d.start + d.end) / 2)-TEXT_ROTATION) * (Math.PI / 180);
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointX1(d: RingSegment): number {
      return Math.cos(calculateMidpoint(d)) * getOuterRingHeight(rings)
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointY1(d: RingSegment): number {
      return Math.sin(calculateMidpoint(d)) * getOuterRingHeight(rings);
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointX2(d: RingSegment): number {
      return calculateOuterArcPointX1(d) + config.annotation.lineLength * Math.cos(calculateMidpoint(d))
  }
  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointY2(d: RingSegment): number {
      return calculateOuterArcPointY1(d) + config.annotation.lineLength * Math.sin(calculateMidpoint(d))
  }


  // function resetZoom() {
  //     svg.transition()
  //         .duration(750)
  //         .call(zoomBehaviour.transform, d3.zoomIdentity)
  //         .select('g').attr('transform', `translate(${width / 2},${height / 2})`)
  // }

</script>

<div>
  <div id="{id}" class="mb-5">
    <svg width={width} height={height}>
      <g transform='translate({width / 2},{height / 2})'>
        <text class="title" style="fill: {config.title.color}; opacity: {config.title.opacity}; font-style: {config.title.fontStyle}; text-anchor: middle">{config.title.text}</text>
        
        {#each rings as ring}
          {#if ring.type === "TextAnnotation"}
            {#each ring.data as ringAnnotation}
            <line 
              x1={calculateOuterArcPointX1(ringAnnotation)} 
              y1={calculateOuterArcPointY1(ringAnnotation)} 
              x2={calculateOuterArcPointX2(ringAnnotation)} 
              y2={calculateOuterArcPointY2(ringAnnotation)}
              style="{config.annotation.lineStyle}"
              class="brickAnnotationLine"
              visibility={ring.visible ? 'visible': 'hidden'}
            />
          {/each}
          {#each ring.data as ringAnnotation}
            <text 
              x={calculateOuterArcPointX2(ringAnnotation)} 
              y={calculateOuterArcPointY2(ringAnnotation)}
              style="{config.annotation.textStyle}; fill: {ring.color}"
              text-anchor={degreeScale(ringAnnotation.start) > 180 ? 'end' : 'start' }
              dominant-baseline={degreeScale(ringAnnotation.start) > 180 ? 'middle': 'middle'}
              class="brickAnnotationText"
              visibility={ring.visible ? 'visible': 'hidden'}
            >
            <tspan x={degreeScale(ringAnnotation.start) > 180 ? calculateOuterArcPointX2(ringAnnotation)-config.annotation.textGap : calculateOuterArcPointX2(ringAnnotation)+config.annotation.textGap}>{ringAnnotation.text}</tspan>
            </text>
          {/each}
        {:else}
          {#each ring.data as ringSegment}
            <path class="brickRingSegment" d={arcGenerator(ringSegment, ring.index, ring.height)} style="fill: {ring.color}; opacity: 0.8" visibility={ring.visible ? 'visible': 'hidden'}></path>
          {/each}
        {/if}
      {/each}
      </g>
    </svg>

      {#if buttons}
      <div class="flex justify-center mb-5">
        <button class="btn border border-primary-500 text-xs mr-2" on:click={() => downloadSVG(id)}>
          <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          SVG
        </button>
        <button class="btn border border-primary-500 text-xs mr-2" on:click={() => downloadPNG(id)}>
          <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          PNG
        </button>
        <button class="btn border border-primary-500 text-xs" on:click={() => downloadJSON(rings)}>
          <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          JSON
        </button>
      </div>
    {/if}
  </div>
</div>
