import { writable } from 'svelte/store';

// Define the type for the store
type TabIndexStore = number;

export function resetTabs() {
    tabIndexStore.update(_ => 0)
}

// Create the store
export const tabIndexStore = writable<TabIndexStore>(0);
