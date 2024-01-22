import { writable } from 'svelte/store';

// Define the type for the store
type FileDropzoneStateStore = Map<string, boolean>;

// Create the store
export const fileDropzoneStateStore = writable<FileDropzoneStateStore>(
    new Map<string, boolean>([
        ['referenceDropzone', false], 
        ['genbankDropzone', false], 
        ['blastDropzone', false], 
        ['customDropzone', false], 
        ['sessionDropzone', false]
    ])
);

// Set a dropzone to loading state
export function startDropzoneLoading(dropzoneId: string): void {
    fileDropzoneStateStore.update((state) => {
      if (state.has(dropzoneId)) {
        state.set(dropzoneId, true);
      }
      return state;
    });
  }
  
  
// Set a dropzone to completed state
export function completeDropzoneLoading(dropzoneId: string): void {
    fileDropzoneStateStore.update((state) => {
        if (state.has(dropzoneId)) {
        state.set(dropzoneId, false);
        }
        return state;
    });
}