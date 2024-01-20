import { browser } from "$app/environment";
import { getTransitionDurationTotal } from "$lib/stores/PlotConfigStore";
import type { Ring, Session } from "$lib/types";

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

export async function downloadPNG(id: string) {
    
    // await waitForTransition();

    const svgElement = document.getElementById(id)?.querySelector('svg');
    if (!svgElement) {
        console.error(`SVG element not found: ${id} > svg`);
        return;
    }

    const viewBox = svgElement.getAttribute('viewBox');
    const [x, y, width, height] = viewBox ? viewBox.split(' ').map(Number) : [0, 0, svgElement.clientWidth, svgElement.clientHeight];

    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgElement);

    const img = new Image();
    const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        if (!ctx) {
            console.error('2D context not found for canvas');
            return;
        }

        ctx.drawImage(img, -x, -y, width, height);
        URL.revokeObjectURL(url);

        const pngData = canvas.toDataURL('image/png');
        const downloadLink = document.createElement('a');
        downloadLink.href = pngData;
        downloadLink.download = 'brick.png';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    };

    img.src = url;
}


// Helper function to wait for transitions to complete - might not be needed 
function waitForTransition() {
    return new Promise(resolve => {
        // Assuming a fixed duration for the transition
        const transitionDuration = getTransitionDurationTotal(); // Adjust as needed
        setTimeout(resolve, transitionDuration);
    });
}

export function downloadJSON(data: Ring[] | Session) {

    // Convert data to JSON string with 2-space indent
    const jsonString = JSON.stringify(data, null, 2);

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
    
    if (browser){
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
            return 0.5;
        } else if (windowWidth < breakpoints.md) {
            return 0.5;
        } else if (windowWidth < breakpoints.lg) {
            return 0.5;
        } else if (windowWidth < breakpoints.lg) {
            return 0.6;
        } else if (windowWidth < breakpoints.xl) {
            return 0.7;
        } else if (windowWidth < breakpoints.xxl) {
            return 0.8;
        } else if (windowWidth < breakpoints.xxxl) {
            return 0.9;
        } else if (windowWidth < breakpoints.uhd) {
            return 1.0;
        } else if (windowWidth < breakpoints.uhd4k) {
            return 1.3;
        } else {
            return 1.4;
        }
    } else {
        return 1.0
    }
    
}