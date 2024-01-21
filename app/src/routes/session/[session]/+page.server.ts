import { fail, error} from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import type { FileUploadResponse, CreateRingResponse, SessionResponse } from '$lib/types';
import { RingType } from '$lib/types';
import { checkCeleryResults, getErrorMessage, isValidUUIDv4, parseEnvInt } from '$lib/helpers';
import { env } from '$env/dynamic/private';


export const load: PageServerLoad = async ({ depends, params }) => {

    depends("app:session")

    if (!params.session || !isValidUUIDv4(params.session)) {
        throw error(400, 'Invalid URL');
    }

    const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/${params.session}`);

    try {
        const sessionResponseData: SessionResponse = await response.json();

        if (response.ok) {
            return { session: sessionResponseData }
        } else {
            if (response.status === 404){
                // Create a new session request
                const newSessionResponse = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/${params.session}`, {method: 'POST'});

                try {
                    const sessionResponseData: SessionResponse = await newSessionResponse.json();

                    if (newSessionResponse.ok) {
                        return { session: sessionResponseData }
                    } else {
                        return fail(newSessionResponse.status, sessionResponseData)
                    }
                } catch(error){
                    // Catch if something bad happens during validation with pydantic
                    // there is no JSON object returned (error only)
                    return fail(response.status, { detail: getErrorMessage(error) })
                }
            } else {
                return fail(response.status, { detail: response.statusText })
            }
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
                        `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${fileUploadResponseData.task_id}`, 
                        env.PRIVATE_CELERY_TASK_CHECK_TIMEOUT, env.PRIVATE_CELERY_TASK_CHECK_INTERVAL
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
            body: ringConfig
        });

        try {
            const createRingResponseData: CreateRingResponse = await response.json();

            if (response.ok) {
                try {
                    return await checkCeleryResults(
                        `${env.PRIVATE_DOCKER_API_URL}/tasks/result/${createRingResponseData.task_id}`, 
                        env.PRIVATE_CELERY_TASK_CHECK_TIMEOUT, env.PRIVATE_CELERY_TASK_CHECK_INTERVAL
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
        
        
    },
    // Atomic updates to rings in database from user style selection
    updateSessionRing: async ({ request }) => {

        const formData = await request.formData();

        const sessionId = formData.get("session_id") as string;
        const ringUpdate = formData.get("ring_update");
        

        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/${sessionId}/ring`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: ringUpdate
        });
        
        try {
            const sessionResponseData: SessionResponse = await response.json();
    
            if (response.ok) {
                return { session: sessionResponseData }
            } else {
                return fail(response.status, sessionResponseData)
            }
        } catch(error) {
            // Catch if something bad happens during validation with pydantic
            // there is no JSON object returned (error only)
            return fail(response.status, {
                detail: getErrorMessage(error)
            })
        }
    },
    deleteSessionRing: async ({ request }) => {

        const formData = await request.formData();

        const sessionId = formData.get("session_id") as string;
        const ringUpdate = formData.get("ring_update");
        
        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/sessions/${sessionId}/ring`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: ringUpdate
        });
        
        try {
            const sessionResponseData: SessionResponse = await response.json();
    
            if (response.ok) {
                return { session: sessionResponseData }
            } else {
                return fail(response.status, sessionResponseData)
            }
        } catch(error) {
            // Catch if something bad happens during validation with pydantic
            // there is no JSON object returned (error only)
            return fail(response.status, {
                detail: getErrorMessage(error)
            })
        }
    },
    deleteSessionFile: async ({ request }) => {

        const formData = await request.formData();

        const sessionId = formData.get("session_id") as string;
        const fileId = formData.get("file_id") as string;
        
        const response = await fetch(`${env.PRIVATE_DOCKER_API_URL}/files/${sessionId}/${fileId}`, {
            method: 'DELETE'
        });
        
        try {
            const sessionResponseData: SessionResponse = await response.json();
    
            if (response.ok) {
                return { session: sessionResponseData }
            } else {
                return fail(response.status, sessionResponseData)
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