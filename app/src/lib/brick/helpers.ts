import type { Ring } from "$lib/types";

export function downloadSVG(id: string) {
    const svg = document.querySelector(`#${id} svg`);

    if (!svg) {
      console.error(`SVG element not found: ${id} svg`);
      return;
    }

    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);

    const a = document.createElement('a');
    a.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source);
    a.download = 'brick.svg';
    a.click();

}

export function downloadPNG(id: String) {
    const svg = document.querySelector(`#${id} svg`);

    if (!svg) {
        console.error(`SVG element not found: ${id} svg`);
        return;
    }

    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);

    const img = new Image();
    const svgBlob = new Blob([source], {type: 'image/svg+xml;charset=utf-8'});
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const context = canvas.getContext('2d');

        if (!context) {
            console.error('2D context element not found');
            return;
        }

        context.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);

        const canvasData = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = canvasData;
        a.download = 'brick.png';
        a.click();
    };

    img.src = url;
}

export function downloadJSON(ringData: Ring[]) {
    // Convert data to JSON string with 2-space indent
    const jsonString = JSON.stringify(ringData, null, 2);

    // Create a Blob from the JSON string
    const blob = new Blob([jsonString], { type: 'application/json' });

    // Create a URL for the Blob
    const url = URL.createObjectURL(blob);

    // Create a temporary anchor element and trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = 'brick.json'; // Name of the downloaded file
    document.body.appendChild(a); // Append the anchor to the document
    a.click(); // Trigger a click on the element to start download

    // Clean up: remove the anchor element and revoke the Blob URL
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

export function getDefaultScaleFactor() {

      const windowWidth = window.innerWidth;

      // Tailwind breakpoints for window sizes
      const breakpoints = {
        xs: 480,    // Extra small devices (portrait phones)
        sm: 640,    // Small devices (landscape phones)
        md: 768,    // Medium devices (tablets)
        lg: 1024,   // Large devices (laptops/desktops)
        xl: 1280,   // Extra large devices (large laptops and desktops)
        xxl: 1536,  // Bigger desktops
        xxxl: 1920, // Full HD and larger screens
        uhd: 2560,  // 2K, QHD, and some larger screens
        uhd4k: 3840 // 4K UHD screens
      };

      // Determine scaleFactor based on breakpoints
      // used by Tailwind for standard devices
      if (windowWidth < breakpoints.sm) {
          return 0.6;
      } else if (windowWidth < breakpoints.md) {
          return 0.8;
      } else if (windowWidth < breakpoints.lg) {
          return 0.8;
      } else if (windowWidth < breakpoints.lg) {
          return 0.8;
      } else if (windowWidth < breakpoints.xl) {
          return 0.8;
      } else if (windowWidth < breakpoints.xxl) {
          return 0.8;
      } else if (windowWidth < breakpoints.xxxl) {
          return 0.8;
      } else if (windowWidth < breakpoints.uhd) {
          return 0.8;
      } else if (windowWidth < breakpoints.uhd4k) {
          return 0.8;
      } else {
          return 0.9;
      }
}