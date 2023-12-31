import { writable } from 'svelte/store';
import { RingType, type Ring } from '$lib/types';

// Define the type for the store
type RingStore = Ring[];

// Create the store
const rings = writable<RingStore>([]);

// Function to add a new ring using the addNewRing logic
function addRing(newRing: Ring, newIndex?: number) {
    rings.update(currentRings => {
        // Use the provided addNewRing function to add the ring
        return addNewRing(currentRings, newRing, newIndex);
    });
}

// Function to remove a ring by index
function removeRing(index: number) {
    rings.update(currentRings => {
        // Remove the ring and update indexes of remaining rings
        const updatedRings = currentRings.filter(ring => ring.index !== index);
        return updatedRings.map((ring, idx) => ({ ...ring, index: idx }));
    });
}

// Function to toggle visibility of a ring
function toggleRingVisibility(index: number) {
    rings.update(currentRings => {
        return currentRings.map(ring => {
            if (ring.index === index) {
                ring.visible = !ring.visible;
            }
            return ring;
        });
    });
}

// Export the store and functions
export { rings, addRing, removeRing, toggleRingVisibility };

// Add new ring helper function
function addNewRing(rings: Ring[], newRing: Ring, newIndex: number = rings.length): Ring[] {
    if (rings.length > 0 && newIndex === rings.length && rings[rings.length - 1].type === RingType.LABEL) {
        newIndex = rings.length - 1;
    }

    let newArray = [...rings];
    newArray.splice(newIndex, 0, newRing);
    return newArray.map((item, idx) => ({ ...item, index: idx }));
}