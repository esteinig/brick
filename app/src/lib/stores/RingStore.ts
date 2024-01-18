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

// Function to remove a ring by id and reindex rings in the specified index group
function removeRing(id: string, indexGroup: string[]) {
    rings.update(currentRings => {
        // Remove the specified ring
        const ringsAfterRemoval = currentRings.filter(ring => ring.id !== id);

        // Filter the remaining rings to include only those in the index group
        const indexGroupRings = ringsAfterRemoval.filter(ring => indexGroup.includes(ring.id));

        // Sort these rings based on their current index
        indexGroupRings.sort((a, b) => a.index - b.index);

        // Update the indices to be continuous, starting from 0
        for (let i = 0; i < indexGroupRings.length; i++) {
            indexGroupRings[i].index = i;
        }

        // Create a map of updated index group rings for easy lookup
        const updatedIndexGroupRingsMap = new Map(indexGroupRings.map(ring => [ring.id, ring]));

        // Merge the updated index group rings back into the full list
        return ringsAfterRemoval.map(ring => updatedIndexGroupRingsMap.get(ring.id) || ring);
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

// Function to move a ring inside and adjust the indices
function moveRingInside(id: string) {
    rings.update(currentRings => {
        // Find the ring to move and its current index
        const ringToMove = currentRings.find(ring => ring.id === id);
        if (!ringToMove) return currentRings; // Ring not found

        const currentIndex = ringToMove.index;
        // Check if the ring is already at the innermost position
        if (currentIndex === 0) return currentRings;

        // Find the ring currently inside the position we want to move to
        const innerRing = currentRings.find(ring => ring.index === currentIndex - 1);
        if (!innerRing) return currentRings; // Inner ring not found

        // Swap indices of the two rings
        ringToMove.index = currentIndex - 1;
        innerRing.index = currentIndex;

        // Return the updated list of rings
        return [...currentRings];
    });
}

// Function to move a ring outside and adjust the indices
function moveRingOutside(id: string, maxIndex: number) {
    rings.update(currentRings => {
        // Find the ring to move and its current index
        const ringToMove = currentRings.find(ring => ring.id === id);
        if (!ringToMove) return currentRings; // Ring not found

        const currentIndex = ringToMove.index;
        // Check if the ring is already at the outermost position
        if (currentIndex === maxIndex) return currentRings;

        // Find the ring currently outside the position we want to move to
        const outerRing = currentRings.find(ring => ring.index === currentIndex + 1);
        if (!outerRing) return currentRings; // Outer ring not found

        // Swap indices of the two rings
        ringToMove.index = currentIndex + 1;
        outerRing.index = currentIndex;

        // Return the updated list of rings
        return [...currentRings];
    });
}




// Derived store

import type { RingReference } from '$lib/types'; 

// Function to create a derived store based on RingReference
function createFilteredRingsStore(ringReference: RingReference) {
    return derived(rings, $rings => {
        let filteredRings = $rings.filter(ring => 
            ring.reference.reference_id === ringReference.reference_id && 
            ring.reference.session_id === ringReference.session_id &&
            ring.reference.sequence.id === ringReference.sequence.id
        );
        
        filteredRings.sort((a, b) => a.index - b.index);

        return filteredRings // .map((ring, index) => ({ ...ring, index })); updates the indices by the order of the filtered rings 
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


