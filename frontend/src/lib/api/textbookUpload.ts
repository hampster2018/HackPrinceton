import { localURL } from "$lib/api/config";

export const textbookUpload = async (file : File) : Promise<void> => {

    const formData = new FormData();
    formData.append("file", file);

    fetch(localURL + "/upload_textbook", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "ngrok-skip-browser-warning": "true",
            'mode': 'no-cors',
        },
        body: formData,
    });

}