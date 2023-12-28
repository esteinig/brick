import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

function isValidUUIDv4(uuid: string): boolean {
    const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return regex.test(uuid);
}

export const load: PageServerLoad = async ({ url, params }) => {

    // Validate the session parameter
    if (!params.session || !isValidUUIDv4(params.session)) {
        throw error(400, 'Invalid URL');
    }

    // If valid, return whatever data you need for your page
    return {
        // your data here
    };
};