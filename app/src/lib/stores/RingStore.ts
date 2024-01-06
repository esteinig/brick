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

function changeRingTitle(index: number, title: string) {
    rings.update(currentRings => {
        currentRings[index].title = title
        return currentRings;
    })
}

// Export the store and functions
export { rings, addRing, removeRing, clearRings, toggleRingVisibility, moveRingInside, moveRingOutside, changeRingTitle, isRingTypePresent};

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