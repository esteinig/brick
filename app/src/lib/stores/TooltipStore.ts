import { writable} from 'svelte/store';
import type { RingSegment } from '$lib/types';

// Define the type for the store
type TooltipStore = RingSegment | undefined;

// Create the store
const tooltip = writable<TooltipStore>(undefined);

// Function to add a new session file
function setTooltip(ringSegment: RingSegment) {
    tooltip.update(_ => ringSegment);
}

// Function to remove a session file by id
function removeTooltip() {
    tooltip.update(_ => undefined);
}


function clearTooltip() {
    tooltip.update(_ => undefined)
}
// Export the store and functions
export { tooltip, setTooltip, removeTooltip};