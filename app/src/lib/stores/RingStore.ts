import { writable, derived } from 'svelte/store';
import { RingType, type Ring } from '$lib/types';

// Define the type for the store
type RingStore = Ring[];

// Create the store
const rings = writable<RingStore>([]);

function addRing(newRing: Ring) {
    rings.update(currentRings => {
        return addNewRing([...currentRings], newRing);
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
function createFilteredRingsStore(ringReference: RingReference | null) {
    return derived(rings, $rings => {
        
        if (ringReference === null) return $rings;

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

// Helper to compute index for insertion and add/merge the new ring
function addNewRing(rings: Ring[], newRing: Ring): Ring[] {
    // Filter rings with the same reference
    let sameRefRings = rings.filter(ring =>
        ring.reference.reference_id === newRing.reference.reference_id &&
        ring.reference.sequence.id === newRing.reference.sequence.id
    );

    // Sort these rings by their index
    sameRefRings.sort((a, b) => a.index - b.index);

    // Check for the existence of a LABEL ring
    const labelRingIndex = sameRefRings.findIndex(ring => ring.type === RingType.LABEL);
    const isLabelRingLast = labelRingIndex !== -1 && labelRingIndex === sameRefRings.length - 1;

    if (newRing.type === RingType.LABEL) {
        // If the new ring is a LABEL ring and a LABEL ring already exists, merge their data
        if (isLabelRingLast) {
            sameRefRings[labelRingIndex].data = [...sameRefRings[labelRingIndex].data, ...newRing.data];
            return [...rings];
        } else {
            // If no LABEL ring exists, add the new LABEL ring to the last position
            newRing.index = sameRefRings.length > 0 ? sameRefRings[sameRefRings.length - 1].index + 1 : 0;
            rings.push(newRing);
        }
    } else {
        // For non-LABEL rings, assign the appropriate index
        newRing.index = isLabelRingLast ? sameRefRings.length - 1 : sameRefRings.length;
        rings.splice(newRing.index, 0, newRing);

        // Adjust indices if necessary
        if (isLabelRingLast) {
            sameRefRings[labelRingIndex].index += 1;
        }
    }
    console.log(rings)
    return rings
}

