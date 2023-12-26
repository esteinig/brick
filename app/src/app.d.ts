// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces

import type { BrickInterfaceConfiguration } from "$lib/session/types";

// and what to do when importing types
declare namespace App {
	// interface Locals {}
	interface PageData {
		userSettings: BrickInterfaceConfiguration
	}
	// interface Error {}
	// interface Platform {}
}
