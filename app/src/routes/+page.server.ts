import type { SessionResponse } from '$lib/types';
import { env } from '$env/dynamic/private';
import type { PageServerLoad } from './$types';
import { FALLBACK_REFERENCE, FALLBACK_RINGS, FALLBACK_SESSION } from '$lib/data';



export const load: PageServerLoad = async ({ depends }) => {

    depends("app:landing")

    const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/default`);

    try {
        const sessionResponseData: SessionResponse = await response.json();

        if (response.ok) {
            if (sessionResponseData.rings.length){
                return { reference: sessionResponseData.rings[0].reference, rings: sessionResponseData.rings }
            } else {
                return { reference: FALLBACK_REFERENCE, rings: FALLBACK_RINGS }
            }
           
        } else {
            if (response.status === 404){
                return { reference: FALLBACK_REFERENCE, rings: FALLBACK_RINGS }
            } else {
                return { reference: FALLBACK_REFERENCE, rings: FALLBACK_RINGS }
            }
        }
    } catch(error) {
        return { reference: FALLBACK_REFERENCE, rings: FALLBACK_RINGS }
    }
};