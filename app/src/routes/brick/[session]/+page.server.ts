import { fail, error} from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import type { BlastRingResponse, FileUploadResponse, AnnotationRingResponse } from '$lib/types';
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

    return {}
};


export const actions: Actions = {
    uploadFile: async ({ request }) => {

        const formData = await request.formData();

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/files/upload`, {
            method: 'POST',
            body: formData
        });

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
    },
    createBlastRing: async ({ request }) => {

        const formData = await request.formData();

        const ringConfig = formData.get("ring_config")

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/rings/blast`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: ringConfig,
        });

        const blastRingResponseData: BlastRingResponse = await response.json();

        if (response.ok) {
            try {
                return await checkCeleryResults(
                    `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${blastRingResponseData.task_id}` 
                );
            } catch (error) {
                return fail(500, { 
                    detail: getErrorMessage(error), 
                    task_id: blastRingResponseData.task_id 
                })
            }
        } else {
            return fail(response.status, blastRingResponseData)
        }
    },
    createAnnotationRing: async ({ request }) => {

        const formData = await request.formData();

        const ringConfig = formData.get("ring_config")

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/rings/annotation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: ringConfig,
        });

        const annotationRingResponseData: AnnotationRingResponse = await response.json();

        if (response.ok) {
            try {
                return await checkCeleryResults(
                    `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${annotationRingResponseData.task_id}` 
                );
            } catch (error) {
                return fail(500, { 
                    detail: getErrorMessage(error), 
                    task_id: annotationRingResponseData.task_id 
                })
            }
        } else {
            return fail(response.status, annotationRingResponseData)
        }
    },
};