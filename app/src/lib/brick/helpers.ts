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