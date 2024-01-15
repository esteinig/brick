<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  import { downloadJSON, downloadSVG, getDefaultScaleFactor } from './helpers';
	import { RingType, type Ring, type RingSegment, TitleStyle } from '$lib/types';
	import { plotConfigStore } from '$lib/stores/PlotConfigStore';
	import { fade } from 'svelte/transition';
  import { createFilteredRingsStore } from '$lib/stores/RingStore';
  import { ringReferenceStore } from '$lib/stores/RingReferenceStore';
  import { createEventDispatcher } from 'svelte';
	import { removeTooltip, setTooltip } from '$lib/stores/TooltipStore';

  $: rings = createFilteredRingsStore($ringReferenceStore) // reactive so it updates on changes to reference sequence

  const dispatch = createEventDispatcher();
  let segmentClicked: boolean = false;

  function handleMouseover(ringSegment: RingSegment) {
      dispatch('hover', ringSegment);
      setTooltip(ringSegment)
  }

  function handleMouseout() {
      dispatch('hover', undefined);
      removeTooltip()
  }

  function handleClick(ringSegment: RingSegment) {
      if (segmentClicked){
        dispatch('click', undefined);
        segmentClicked = false;
      } else {
        dispatch('click', ringSegment);
        segmentClicked = true;
      }
  }
   

  export let id: string = "brickRingPlot";
  export let width: number = 1024;
  export let height: number = 768;
  
  export let border: boolean = false;
  export let borderClass: string = "border border-gray-300 rounded-2xl border-opacity-5";

  export let scaleFactor: number = getDefaultScaleFactor();

  export let enableZoom: boolean = true;
  export let zoomRange: [number, number] = [0.5, 20];

  export let enableControls: boolean = false;

  export let responsive: boolean = true;
  export let visible: boolean = !responsive;

  // Fade transitions allows for SVF resizing of the window if the component
  // is responsive to avoid a resize-glitch before the figure becomes visible
  
  export let fadeDelay: number = 0;
  export let fadeDuration: number = 1200;

  // Arc segment annotations otherwise start at 3 pm
  const annotationSegmentRotation: number = 90;  

  // Events

  let container: HTMLElement;
  let svg: any;
  let g: any;
  
  onMount(() => {
    
    if (responsive) {
      width = container.offsetWidth;
      height = container.offsetHeight;

      const resizeObserver = new ResizeObserver(entries => {
          for (let entry of entries) {
            const { width: newWidth, height: newHeight } = entry.contentRect;
            width = newWidth;
            height = newHeight;

          }
      })
      resizeObserver.observe(container);

      visible = true;

      return () => {
        resizeObserver.disconnect();
      };
    }
  });

  // Center and scale figure
  let scaledTransform: string;

  // Circular data scaling
  $: degreeScale = d3.scaleLinear(
    [0, $ringReferenceStore.sequence.length], [0,360] // TODO: What if you just go linear or implement the ST93 paper again with a couple changes ah 0 to 1; apply this to each of multiple input sequences to align in circle as e.g. Genome 1 0-10, Genome2 10-20
  );

  
  // Reactive for controls to change `scaleFactor`
  $: scaledTransform = `translate(${width / 2},${height / 2}) scale(${scaleFactor})`;


  // Reactive statement instead of onMount to allow 
  // for conditional visibility with fade transtion
  $: if (svg && g) {

    // Calculate the center of the SVG element
    const centerX = svg.clientWidth / 2;
    const centerY = svg.clientHeight / 2;

    // Define the initial transform to center the content
    const initialTransform = d3.zoomIdentity.translate(centerX, centerY);

    // Set up the zoom behavior
    const zoomBehavior = d3.zoom()
      .scaleExtent(zoomRange)
      .on('zoom', (event: any) => {
        g.setAttribute('transform', event.transform);
      });

    // Apply the zoom behavior and set the initial transform
    d3.select(svg)
      .call(zoomBehavior)
      .call(zoomBehavior.transform, initialTransform);
  }

  // All ring data is fed through this generator which will calculate the start
  // and end angles on the circle for each segment and adjust inner and outer
  // heights based on radius, ring height and gap size
  function arcGenerator(d: RingSegment, index: number, height: number, radius: number, gap: number): string {
    
    const ringHeight = getRingHeight($rings, 0, index);
    return d3.arc()
      .innerRadius(radius+(index*gap)+ringHeight)
      .outerRadius(radius+(index*gap)+ringHeight+height)
      .startAngle((d: RingSegment) => (degreeScale(d.start)) * (Math.PI / 180))
      .endAngle((d: RingSegment) => (degreeScale(d.end)) * (Math.PI / 180))
      (d);
  }

  function getRingHeight(rings: Ring[], start_index: number, end_index: number): number {
    return rings.slice(start_index, end_index+1).map(ring => ring.height).reduce((a, b) => a+b)
  }

  function getOuterRingHeight(rings: Ring[], gap: number): number {
    return rings.map(ring => ring.height+gap).reduce((a, b) => a+b)+$plotConfigStore.rings.radius
  }

  // Function to calculate the midpoint of an arc segment
  function calculateMidpoint(d: RingSegment): number {
      return (degreeScale((d.start + d.end) / 2)-annotationSegmentRotation) * (Math.PI / 180);
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointX1(d: RingSegment, gap: number): number {
      return Math.cos(calculateMidpoint(d)) * getOuterRingHeight($rings, gap)
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointY1(d: RingSegment, gap: number): number {
      return Math.sin(calculateMidpoint(d)) * getOuterRingHeight($rings, gap);
  }

  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointX2(d: RingSegment, lineLength: number, gap: number): number {
      return calculateOuterArcPointX1(d, gap) + lineLength * Math.cos(calculateMidpoint(d))
  }
  // Function to calculate the coordinates of the point on the outer edge of the arc
  function calculateOuterArcPointY2(d: RingSegment, lineLength: number, gap: number): number {
      return calculateOuterArcPointY1(d, gap) + lineLength * Math.sin(calculateMidpoint(d))
  }

  function addAlphaToHexColor(hex: string, opacity: number) {
    const alpha = Math.round(opacity * 255).toString(16).padStart(2, '0');
    return hex + alpha;
}
  // TODO: implement reset zoom and zoom in/out button

</script>

<div id="{id}" bind:this={container} class="w-full h-full {border ? borderClass : ''}" >
  
    {#if visible}
      <svg bind:this={svg} class="w-full h-full {enableZoom ? 'cursor-grab' : ''}" style={`background-color: ${addAlphaToHexColor($plotConfigStore.svg.backgroundColor, $plotConfigStore.svg.backgroundOpacity)}`} transition:fade={{duration: fadeDuration, delay: fadeDelay}}>
        <g bind:this={g} transform={scaledTransform}>
            <g text-anchor="middle">
              <text class="title {$plotConfigStore.title.styles.includes(TitleStyle.CODE) ? 'code': ''}" style="{$plotConfigStore.title.styles.includes(TitleStyle.BOLD) ? 'font-weight: bold': ''}; fill: {$plotConfigStore.title.color}; opacity: {$plotConfigStore.title.opacity}; {$plotConfigStore.title.styles.includes(TitleStyle.ITALIC) ? 'font-style: italic': ''}; transform: scale({$plotConfigStore.title.size / 100})">{$plotConfigStore.title.text}</text>
              <text class="subtitle" dy="{1.35*$plotConfigStore.subtitle.height}em" style="fill: {$plotConfigStore.subtitle.color}; opacity: {$plotConfigStore.subtitle.opacity}; {$plotConfigStore.subtitle.styles.includes(TitleStyle.ITALIC) ? 'font-style: italic': ''}; transform: scale({$plotConfigStore.subtitle.size / 135})">{$plotConfigStore.subtitle.text}</text>
          </g>


          <!-- <text class="title {$plotConfigStore.title.styles.includes(TitleStyle.CODE) ? 'code': ''}" style="{$plotConfigStore.title.styles.includes(TitleStyle.BOLD) ? 'font-weight: bold': ''}; fill: {$plotConfigStore.title.color}; opacity: {$plotConfigStore.title.opacity}; {$plotConfigStore.title.styles.includes(TitleStyle.ITALIC) ? 'font-style: italic': ''}; transform: scale({$plotConfigStore.title.size / 100}); text-anchor: middle">{$plotConfigStore.title.text}</text>
          <text class="subtitle" style="fill: {$plotConfigStore.title.color}; opacity: {$plotConfigStore.title.opacity}; {$plotConfigStore.title.styles.includes(TitleStyle.ITALIC) ? 'font-style: italic': ''}; transform: scale({$plotConfigStore.title.size / 100}); text-anchor: middle">{$plotConfigStore.title.subtext}</text> -->
          
          {#each $rings as ring}
            {#if ring.type === RingType.LABEL}
              {#each ring.data as ringAnnotation}
              <line 
                x1={calculateOuterArcPointX1(ringAnnotation, $plotConfigStore.rings.gap)} 
                y1={calculateOuterArcPointY1(ringAnnotation, $plotConfigStore.rings.gap)} 
                x2={calculateOuterArcPointX2(ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap)} 
                y2={calculateOuterArcPointY2(ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap)}
                style="{$plotConfigStore.annotation.lineStyle}"
                class="brickAnnotationLine"
                visibility={ring.visible ? 'visible': 'hidden'}
              />
            {/each}
            {#each ring.data as ringAnnotation}
              <text 
                x={calculateOuterArcPointX2(ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap)} 
                y={calculateOuterArcPointY2(ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap)}
                style="{$plotConfigStore.annotation.textStyle}"
                text-anchor={degreeScale(ringAnnotation.start) > 180 ? 'end' : 'start' }
                dominant-baseline={degreeScale(ringAnnotation.start) > 180 ? 'middle': 'middle'}
                class="brickAnnotationText"
                visibility={ring.visible ? 'visible': 'hidden'}
              >
              <tspan x={
              degreeScale(ringAnnotation.start) > 180 ? calculateOuterArcPointX2(
                  ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap
                )-$plotConfigStore.annotation.textGap : calculateOuterArcPointX2(
                  ringAnnotation, $plotConfigStore.annotation.lineLength, $plotConfigStore.rings.gap
                )+$plotConfigStore.annotation.textGap
              }>{ringAnnotation.text}</tspan>
              </text>
            {/each}
          {:else}
            {#each ring.data as ringSegment}
              <path 
                class="brickRingSegment" 
                d={arcGenerator(ringSegment, ring.index, $plotConfigStore.rings.height, $plotConfigStore.rings.radius, $plotConfigStore.rings.gap)} 
                style="fill: {ring.color}; opacity: 1; cursor: pointer" 
                visibility={ring.visible ? 'visible': 'hidden'} 
                on:mouseover={() => handleMouseover(ringSegment)} 
                on:focus={() => handleMouseover(ringSegment)} 
                on:mouseout={handleMouseout} 
                on:blur={handleMouseout}
                on:click={() => handleClick(ringSegment)}
                role="tooltip"
              ></path>
            {/each}
          {/if}
        {/each}
        </g>
      </svg>

      {#if enableControls}
        <div class="flex justify-center mb-5">
          <button class="btn border border-primary-500 text-xs mr-2" on:click={() => downloadSVG(id)}>
            <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            SVG
          </button>
          <button class="btn border border-primary-500 text-xs" on:click={() => downloadJSON($rings)}>
            <svg class="w-4 h-4 mr-2" data-slot="icon" aria-hidden="true" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            JSON
          </button>
        </div>
      {/if}
    {/if}
</div>