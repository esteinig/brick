
import { RingType, type Ring } from '$lib/types';
import { v4 as uuidv4 } from 'uuid';
import { TaskStatus, type TaskStatusResponse } from './types';

export const createUuid = (short: boolean = false) => {
    return short ? uuidv4().substring(0, 8) : uuidv4()
}

export const createSessionId = () => { return uuidv4() };
export const shortenSessionId = (sessionId: string): string => { return sessionId.substring(0,8) };


export function addNewRing(rings: Ring[], newRing: Ring, newIndex: number = rings.length): Ring[] {

    // If rings are present, and addition to the last index is requested, but the outer
    // ring is `RingType.LABEL`, insert the new ring into the second-to-last index instead
    if (rings.length > 0 && newIndex === rings.length && rings[rings.length - 1].type === RingType.LABEL) {
        
        newIndex = rings.length - 1;
    }

    // Create a copy of the array
    let newArray = [...rings];

    // Add a new object at the specified index
    newArray.splice(newIndex, 0, newRing); // with temporary index

    // Update the index of each object to match its position
    newArray = newArray.map((item, idx) => ({ ...item, index: idx }));

    return newArray;
}



export async function checkCeleryResults(
    url: string,
    toastStore: any, 
    successMessage: string = "Task completed successfully"
): Promise<TaskStatusResponse> {

    const startTime = new Date().getTime();
    const timeout = 30000; 
    const pollingInterval = 2000; 

    const timeoutPromise = new Promise<TaskStatusResponse>((_, reject) => 
      setTimeout(() => reject(new Error('Operation timed out')), timeout)
    );

    const statusCheck = async (): Promise<TaskStatusResponse> => {
      while (true) {
        const currentTime = new Date().getTime();
        if (currentTime - startTime > timeout) {
          throw new Error('Processing checks timed out');
        }

        const response = await fetch(url);

        if (!response.ok) {
          const data = await response.json();
          throw new Error(`${data.detail ? data.detail : `${response.status}`}`);
        }

        const data: TaskStatusResponse = await response.json();
        
        if (data.status === TaskStatus.SUCCESS) {
          toastStore.trigger({
            message: successMessage,
            background: 'variant-filled-success',
            timeout: 3000
          });
          return data;
        }
        await new Promise(resolve => setTimeout(resolve, pollingInterval));
      }
    };

    return await Promise.race([statusCheck(), timeoutPromise]);
}

