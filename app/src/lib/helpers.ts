import { RingType, type Ring } from '$lib/types';
import { TaskStatus, type TaskStatusResponse } from './types';
import { v4 as uuidv4 } from 'uuid';

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

// Celery results checking

export async function checkCeleryResults(
    url: string, timeout: number = 30000, pollingInterval: number = 2000
): Promise<TaskStatusResponse> {

    const startTime = new Date().getTime();

    const timeoutPromise = new Promise<TaskStatusResponse>((_, reject) => 
      setTimeout(() => reject(new Error('Operation timed out')), timeout)
    );

    const statusCheck = async (): Promise<TaskStatusResponse> => {
      while (true) {
        const currentTime = new Date().getTime();
        if (currentTime - startTime > timeout) {
          throw new Error('File processings timed out');
        }

        const response = await fetch(url);
        const data: TaskStatusResponse = await response.json();
        
        if (!response.ok) {
          throw new Error(`${data.detail ? data.detail : `${response.status}`}`);
        }

        if (data.status === TaskStatus.SUCCESS) {
          return data;
        }
        await new Promise(resolve => setTimeout(resolve, pollingInterval));
      }
    };

    return await Promise.race([statusCheck(), timeoutPromise]);
}

// Error handling from unknown type error response in try/catch statements

type ErrorWithMessage = {
  message: string
}

function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as Record<string, unknown>).message === 'string'
  )
}

function toErrorWithMessage(maybeError: unknown): ErrorWithMessage {
  if (isErrorWithMessage(maybeError)) return maybeError

  try {
    return new Error(JSON.stringify(maybeError))
  } catch {
    // Fallback in case there's an error stringifying the maybeError
    // like with circular references for example.
    return new Error(String(maybeError))
  }
}

export function getErrorMessage(error: unknown) {
  return toErrorWithMessage(error).message
}


// Notification toast helper

export enum ToastType {
  ERROR = "error",
  SUCCESS = "success",
  WARNING = "warning",
  DEFAULT = "default"
}

export function triggerToast(message: string, toastType: ToastType, toastStore: any, backgroundDefault: string = 'variant-filled-primary', timeoutDefault: number = 5000) {

  if (toastType === ToastType.ERROR) {
    toastStore.trigger({
      message: message,
      background: 'variant-filled-error',
      timeout: 5000,
    })
  } else if (toastType === ToastType.SUCCESS) {
    toastStore.trigger({
      message: message,
      background: 'variant-filled-success',
      timeout: 3000,
    })
  } else if (toastType === ToastType.WARNING) {
    toastStore.trigger({
      message: message,
      background: 'variant-filled-warning',
      timeout: 5000,
    })
  } else {
    toastStore.trigger({
      message: message,
      background: backgroundDefault,
      timeout: timeoutDefault,
    })
  }
}
