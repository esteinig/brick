import { derived, writable } from 'svelte/store';

// A store to keep track of the number of active uploads
const activeUploads = writable(0);

// A derived store to indicate if any upload is in progress
export const uploadInProgress = derived(
    activeUploads,
    $activeUploads => $activeUploads > 0
);

// Functions to increment and decrement the active uploads count
export function startUploadState() {
    activeUploads.update(n => n + 1);
}

export function completeUploadState() {
    activeUploads.update(n => Math.max(0, n - 1)); // Prevents negative values
}