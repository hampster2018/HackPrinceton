import { writable, get } from 'svelte/store';
import type { Writable } from 'svelte/store';
import { localURL } from './config';

export interface Goal {
    weekNum: number;
    anticipatedKeywords: number;
}

export const currentlyUploading : Writable<boolean> = writable(false);
export const filesize : Writable<number> = writable(0);
export const uploadStage : Writable<number> = writable(0);

export const getUploadStage = async () => {

    const stage = await fetch(localURL + '/get_upload_status', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': 'true',
            mode: 'no-cors'
        }
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log(data);
        return data["upload in progress"];
    });

    if (stage != null) {
        uploadStage.set(stage);
    }

}

export const getApproximateKeywords = () : number => {
    
    const characters = get(filesize) * 1000;

    const chunks = Math.ceil(Math.pow(Math.round(characters), .2));

    const expectedKeywords = chunks * 11;

    return expectedKeywords;

}