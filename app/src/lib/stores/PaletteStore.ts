import { writable } from 'svelte/store';

export interface Palette {
    name: string;
    colors: string[]; // Array of hex color strings
}

function createPaletteStore() {
    const { subscribe, set, update } = writable<Palette[]>([]);

    return {
        subscribe,
        addPalette: (newPalette: Palette) => {
            update(palettes => {
                // Add new palette, if more than 3 palettes, remove the first
                if (palettes.length >= 5) {
                    palettes.shift(); // Remove the first palette
                }
                return [...palettes, newPalette];
            });
        },
        removePalette: (paletteName: string) => {
            update(palettes => {
                return palettes.filter(p => p.name !== paletteName);
            });
        },
        checkPaletteExists: (paletteName: string): boolean => {
            let exists = false;
            update(palettes => {
                exists = palettes.some(p => p.name === paletteName);
                return palettes; // No change to the palettes
            });
            return exists;
        },
        reset: () => set([])
    };
}

export const paletteStore = createPaletteStore();