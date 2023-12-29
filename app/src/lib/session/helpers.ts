
import { v4 as uuidv4 } from 'uuid';

export const createUuid = (short: boolean = false) => {
    return short ? uuidv4().substring(0, 8) : uuidv4()
}

export const createSessionId = () => { return uuidv4() };
export const shortenSessionId = (sessionId: string): string => { return sessionId.substring(0,8) };
