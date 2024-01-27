
import { TaskStatus, type PydanticValidationError, type TaskStatusResponse } from './types';
import { v4 as uuidv4 } from 'uuid';

export const createUuid = (short: boolean = false) => {
    return short ? uuidv4().substring(0, 8) : uuidv4()
}

export const createSessionId = () => { return uuidv4() };
export const shortenSessionId = (sessionId: string): string => { return sessionId.substring(0,8) };


export async function checkCeleryResults(
  url: string, timeout: number | string = 600000, pollingInterval: number | string = 100, backoffTimeout: number = 15000
): Promise<TaskStatusResponse> {
  
  if (typeof timeout === 'string'){
      timeout = parseEnvInt(timeout, 600000, 'PRIVATE_CELERY_TASK_CHECK_TIMEOUT');
  }

  let pollingIntervalNumber: number;
  if (typeof pollingInterval === 'string'){
      pollingIntervalNumber = parseEnvInt(pollingInterval, 1000, 'PRIVATE_CELERY_TASK_CHECK_INTERVAL');
  }

  const startTime = new Date().getTime();
  let attempts = 0;

  const timeoutPromise = new Promise<TaskStatusResponse>((_, reject) => 
      setTimeout(() => reject(new Error('Operation timed out')), timeout)
  );

  const statusCheck = async (): Promise<TaskStatusResponse> => {
      while (true) {
          const currentTime = new Date().getTime();
          if (currentTime - startTime > timeout) {
              throw new Error('File processing timed out');
          }

          const response = await fetch(url);
          const data: TaskStatusResponse = await response.json();
          
          if (!response.ok) {
              throw new Error(`${data.detail ? data.detail : `${response.status}`}`);
          }

          if (data.status === TaskStatus.SUCCESS) {
              return data;
          }

          await new Promise(resolve => setTimeout(resolve, calculateBackoff(attempts)));
          attempts++;
      }
  };

  function calculateBackoff(attempts: number): number {
      const maxInterval = Math.min(backoffTimeout, (pollingIntervalNumber * (2 ** attempts)) + Math.floor(Math.random() * 1000));
      return maxInterval;
  }

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

export function getErrorMessage(error: unknown): string {
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


export const parseEnvInt = (envVar: string, defaultValue: number, varName: string): number => {
 
  const parsedValue = parseInt(envVar);
  if (isNaN(parsedValue)) {
      console.warn(`Failed to parse environment variable string ${varName}. Using default value: ${defaultValue}`);
      return defaultValue;
  }

  return parsedValue;
};

export function isValidUUIDv4(uuid: string): boolean {
  const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return regex.test(uuid);
}


export function handleEndpointErrorResponse(detail: string | PydanticValidationError[], toastStore: any) {
  if (typeof detail === 'string'){
    toastStore.trigger({
      message: detail,
      background: 'variant-filled-error',
      timeout: 5000,
    })
  } else if (Array.isArray(detail) && detail.every(element =>
      typeof element === 'object' && 
      element !== null &&
      'ctx' in element &&
      'loc' in element &&
      'msg' in element &&
      'type' in element &&
      'url' in element
    )) {
      for (let pydanticError of detail) {
        toastStore.trigger({
          message: pydanticError.msg,
          background: 'variant-filled-error',
          timeout: 5000,
        })
      }
    } else {
      toastStore.trigger({
        message: "Error: an unexpected response error occurred :(",
        background: 'variant-filled-error',
        timeout: 5000,
      })
    }


}

export function capitalize(str: string): string {
  if (str.length === 0) return str;
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}