
import { TaskStatus, type TaskStatusResponse } from './types';
import { v4 as uuidv4 } from 'uuid';

export const createUuid = (short: boolean = false) => {
    return short ? uuidv4().substring(0, 8) : uuidv4()
}

export const createSessionId = () => { return uuidv4() };
export const shortenSessionId = (sessionId: string): string => { return sessionId.substring(0,8) };


// Celery results checking

export async function checkCeleryResults(
    url: string, timeout: number = 30000, pollingInterval: number = 1000
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


export const parseEnvInt = (envVar: string | undefined, defaultValue: number, varName: string): number => {
  if (envVar === undefined) {
      console.warn(`Environment variable ${varName} is undefined. Using default value: ${defaultValue}`);
      return defaultValue;
  }

  const parsedValue = parseInt(envVar);
  if (isNaN(parsedValue)) {
      console.warn(`Failed to parse environment variable ${varName}. Using default value: ${defaultValue}`);
      return defaultValue;
  }

  return parsedValue;
};

export function isValidUUIDv4(uuid: string): boolean {
  const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return regex.test(uuid);
}
