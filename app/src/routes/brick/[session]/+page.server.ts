import { fail, error} from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import type { FileUploadResponse } from '$lib/types';
import { checkCeleryResults, getErrorMessage } from '$lib/helpers';

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

        // Add user action implementation
        const formData = await request.formData();

        const response = await fetch("http://localhost:8080/files/upload", {
            method: 'POST',
            body: formData
        });

        const fileUploadResponseData: FileUploadResponse = await response.json();

        if (response.ok) {
            try {
                return await checkCeleryResults(
                    `http://localhost:8080/tasks/result/${fileUploadResponseData.task_id}` 
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
};