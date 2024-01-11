import { fail, error} from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import type { FileUploadResponse, CreateRingResponse, SessionResponse } from '$lib/types';
import { RingType } from '$lib/types';
import { checkCeleryResults, getErrorMessage } from '$lib/helpers';
import { env } from '$env/dynamic/private';

function isValidUUIDv4(uuid: string): boolean {
    const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return regex.test(uuid);
}

export const load: PageServerLoad = async ({ url, params }) => {

    if (!params.session || !isValidUUIDv4(params.session)) {
        throw error(400, 'Invalid URL');
    }

    const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/${params.session}?session_files_exist=true`);

    try {
        const sessionResponseData: SessionResponse = await response.json();

        if (response.ok) {
            return { session: sessionResponseData }
        } else {
            return { session: null, detail: sessionResponseData.detail }
        }
    } catch(error) {
        // Catch if something bad happens during validation with pydantic
        // there is no JSON object returned (error only)
        return fail(response.status, {
            detail: getErrorMessage(error)
        })
    }
};


export const actions: Actions = {
    uploadFile: async ({ request }) => {

        const formData = await request.formData();

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/files/upload`, {
            method: 'POST',
            body: formData
        });

        try {
            const fileUploadResponseData: FileUploadResponse = await response.json();

            if (response.ok) {
                try {
                    return await checkCeleryResults(
                        `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${fileUploadResponseData.task_id}` 
                    );
                } catch (error) {
                    return fail(500, { 
                        detail: getErrorMessage(error), 
                        task_id: fileUploadResponseData.task_id 
                    })
                }
            } else {
                return fail(response.status, fileUploadResponseData)
            }
        } catch(error) {
            // Catch if something bad happens during validation with pydantic
            // there is no JSON object returned (error only)
            return fail(response.status, {
                detail: getErrorMessage(error)
            })
        }
        
    },
    createRing: async ({ request }) => {

        const formData = await request.formData();

        const ringConfig = formData.get("ring_config");
        const ringType: RingType | null = formData.get("ring_type") as RingType;

        if (ringType === null){
            return fail(400, {detail: "Request did not contain the required `ring_type` value"})
        }
        

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/rings/${ringType}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: ringConfig,
        });
        
        
        try {
            const createRingResponseData: CreateRingResponse = await response.json();

            if (response.ok) {
                try {
                    return await checkCeleryResults(
                        `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${createRingResponseData.task_id}` 
                    );
                } catch (error) {
                    return fail(500, { 
                        detail: getErrorMessage(error), 
                        task_id: createRingResponseData.task_id 
                    })
                }
            } else {
                return fail(response.status, createRingResponseData)
            }
        } catch(error) {
            // Catch if something bad happens during validation with pydantic
            // there is no JSON object returned (error only)
            return fail(response.status, {
                detail: getErrorMessage(error)
            })
        }
        
        
    }
};