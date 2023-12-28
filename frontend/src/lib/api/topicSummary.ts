import { localURL } from "./config";

export const getTopicSummary = async (textbook : string, topicName : string) : Promise<string> => {

    return fetch(localURL + "/topic_summary?textbook_name=" + textbook + "&topic=" + topicName, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
            mode: "no-cors"
        }
    }).then(async (response) => {
        const data = await response.json();
        return data.answer;
    })

}