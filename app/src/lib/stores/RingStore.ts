import { writable, derived } from 'svelte/store';
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
function removeRing(id: string) {
    rings.update(currentRings => {
        // Remove the ring and update ides of remaining rings
        const updatedRings = currentRings.filter(ring => ring.id !== id);
        return updatedRings.map((ring, idx) => ({ ...ring, index: idx }));
    });
}

// Function to toggle visibility of a ring
function toggleRingVisibility(id: string) {
    rings.update(currentRings => {
        return currentRings.map(ring => {
            if (ring.id === id) {
                ring.visible = !ring.visible;
            }
            return ring;
        });
    });
}

// Function to toggle visibility of a ring
function changeRingColor(id: string, color: string) {
    rings.update(currentRings => {
        return currentRings.map(ring => {
            if (ring.id === id) {
                ring.color = color
            }
            return ring;
        });
    });
}

function isRingTypePresent(type: RingType): boolean {
    let typePresent = false;
    rings.subscribe(currentRings => {
        typePresent = currentRings.some(ring => ring.type === type);
    })();
    return typePresent; 
}

function clearRings() {
    rings.update(_ => [])
}

// Function to move a ring up (decrease its index)
function moveRingInside(currentIndex: number) {
    rings.update(currentRings => {
        if (currentIndex > 0 && currentIndex < currentRings.length) {
            [currentRings[currentIndex - 1], currentRings[currentIndex]] = 
            [currentRings[currentIndex], currentRings[currentIndex - 1]];

            // Update indexes
            return currentRings.map((ring, idx) => ({ ...ring, index: idx }));
        }
        return currentRings;
    });
}

// Function to move a ring down (increase its index)
function moveRingOutside(currentIndex: number) {
    rings.update(currentRings => {
        if (currentIndex >= 0 && currentIndex < currentRings.length - 1) {
            [currentRings[currentIndex], currentRings[currentIndex + 1]] = 
            [currentRings[currentIndex + 1], currentRings[currentIndex]];

            // Update indexes
            return currentRings.map((ring, idx) => ({ ...ring, index: idx }));
        }
        return currentRings;
    });
}

function changeRingTitle(id: string, title: string) {
    rings.update(currentRings => {
        return currentRings.map(ring => {
            if (ring.id === id) {
                ring.title = title
            }
            return ring;
        });
    });
}


// Derived store

import type { RingReference } from '$lib/types'; // adjust the import path as needed

// Function to create a derived store based on RingReference
function createFilteredRingsStore(ringReference: RingReference) {
    return derived(rings, $rings => {
        let filteredRings = $rings.filter(ring => 
            ring.reference.reference_id === ringReference.reference_id && 
            ring.reference.session_id === ringReference.session_id &&
            ring.reference.sequence.id === ringReference.sequence.id
        );
        return filteredRings.map((ring, index) => ({ ...ring, index }));
    });
}

// Export the store and functions
export { rings, addRing, removeRing, clearRings, toggleRingVisibility, moveRingInside, moveRingOutside, changeRingTitle, isRingTypePresent, createFilteredRingsStore, changeRingColor};

// Add new ring helper function
function addNewRing(rings: Ring[], newRing: Ring, newIndex: number = rings.length): Ring[] {
    if (rings.length > 0 && newIndex === rings.length && rings[rings.length - 1].type === RingType.LABEL) {
       
        if (newRing.type === RingType.LABEL) { 
            rings[rings.length - 1].data = [
                ...rings[rings.length - 1].data, ...newRing.data
            ] // add labels to outer label ring
            return rings
        }
        newIndex = rings.length - 1;
    }

    let newRings = [...rings];
    newRings.splice(newIndex, 0, newRing);
    return newRings.map((ring, idx) => ({ ...ring, index: idx }));
}