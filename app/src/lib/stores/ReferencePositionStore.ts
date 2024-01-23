import { writable} from 'svelte/store';

// Define the type for the store
type ReferencePositionStore = number | undefined;

// Create the store
const referencePosition = writable<ReferencePositionStore>(undefined);


// Export the store and functions
export { referencePosition };