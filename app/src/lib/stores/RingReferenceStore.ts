import { writable } from 'svelte/store';
import type { RingReference } from '$lib/types';
import { DEFAULT_RING_REFERENCE } from '$lib/data';

// Define the type for the store
type RingReferenceStore = RingReference;

export function clearRingReference() {
    ringReferenceStore.update(_ => DEFAULT_RING_REFERENCE)
}


// Create the store
export const ringReferenceStore = writable<RingReferenceStore>(DEFAULT_RING_REFERENCE);
