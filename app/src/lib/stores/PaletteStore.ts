import { MOMA_PALETTES, NZ_PALETTES, NATIONAL_PARK_PALETTES } from '$lib/data';
import type { Palette } from '$lib/types';
import { writable } from 'svelte/store';


function createPaletteStore() {
    const { subscribe, set, update } = writable<Palette[]>([
        NZ_PALETTES[1], MOMA_PALETTES[11], MOMA_PALETTES[2], MOMA_PALETTES[3],
        NATIONAL_PARK_PALETTES[0], NATIONAL_PARK_PALETTES[4], NATIONAL_PARK_PALETTES[10], NATIONAL_PARK_PALETTES[11]
    ]);

    return {
        subscribe,
        addPalette: (newPalette: Palette) => {
            update(palettes => {
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