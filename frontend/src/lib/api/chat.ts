import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import { localURL } from "./config";

export interface Memory {
    speaker: string;
    userTxt: string;
}

export const memory : Writable<Memory[]> = writable([]);
export const blurred = writable(false);

export const getOpenAIChat = async (question : string) : Promise<string> => {
  const chatString = JSON.stringify([{question: question, answer: ""}])

  const response = await fetch(localURL + "/chat_textbook?textbook_name=database_textbook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true",
      mode: "no-cors"
    },
    body: chatString  
  });
  const data = await response.json();
  console.log(data);
  return data.answer;
};