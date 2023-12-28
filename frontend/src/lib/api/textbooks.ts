import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import { localURL } from '$lib/api/config';

export const textbookNames : Writable<string[]> = writable([]);
export const selectedTextbook : Writable<string | null> = writable("database_textbook");

export const getTextbookName = async () => {
    const response = await fetch(localURL + '/get_textbooks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': 'true',
            mode: 'no-cors',
        },
    });
    const data = await response.json();
    console.log(data)
    textbookNames.set(data.textbooks);
}