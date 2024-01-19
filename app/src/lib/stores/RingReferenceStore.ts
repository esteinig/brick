import { writable } from 'svelte/store';
import type { RingReference } from '$lib/types';

// Define the type for the store
type RingReferenceStore = RingReference | null;

export function clearRingReference() {
    ringReferenceStore.update(_ => null)
}


// Create the store
export const ringReferenceStore = writable<RingReferenceStore>(null);
