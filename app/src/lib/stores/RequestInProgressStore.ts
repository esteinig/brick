import { derived, writable } from 'svelte/store';

// A store to keep track of the number of active requests
const activeRequests = writable(0);

// A derived store to indicate if any upload is in progress
export const requestInProgress = derived(
    activeRequests,
    $activeRequests => $activeRequests > 0
);

// Functions to increment and decrement the active uploads count
export function startRequestState() {
    activeRequests.update(n => n + 1);
}

export function completeRequestState() {
    activeRequests.update(n => Math.max(0, n - 1)); // Prevents negative values
}