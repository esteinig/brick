import { writable, get} from 'svelte/store';
import type { FileType, SessionFile } from '$lib/types';

// Define the type for the store
type SessionFileStore = SessionFile[];

// Create the store
const sessionFiles = writable<SessionFileStore>([]);

// Function to add a new session file
function addSessionFile(file: SessionFile) {
    sessionFiles.update(currentFiles => [...currentFiles, file]);
}

// Function to remove a session file by id
function removeSessionFile(id: string) {
    sessionFiles.update(currentFiles => currentFiles.filter(file => file.id !== id));
}

function sessionFileTypeAvailable(fileType: FileType): boolean {
    const currentFiles = get(sessionFiles);
    return currentFiles.some(file => file.type === fileType);
}

function clearSessionFiles() {
    sessionFiles.update(_ => [])
}

function getSessionFileById(id: string): SessionFile | undefined {
    const currentFiles = get(sessionFiles);
    return currentFiles.find(file => file.id === id);
}

// Export the store and functions
export { sessionFiles, addSessionFile, removeSessionFile, sessionFileTypeAvailable, clearSessionFiles, getSessionFileById};