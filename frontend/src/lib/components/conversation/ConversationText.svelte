<script lang="ts">
    import { fly } from 'svelte/transition';

    export let speaker: string;
    export let userTxt: string;

    let botTxt = "DEFAULT BOT TXT";


    if(speaker == "Initial"){
        botTxt = "Hi, I'm Tutor! I'm here to help you learn. What do you need help with?";
    } else if(speaker == "Initial2"){
        botTxt = "I can help you with all kinds of topics! Ask me anything using the input below!"
    } else if(speaker == "user"){
        botTxt = ""
    } else if(speaker == "botFollow1"){
        botTxt = "Would you like me to elaborate?"
    } else if(speaker == "botFollow2"){
        botTxt = "Do you understand? I can explain more if you want. :)"
    } else {
        botTxt = "This will be the bot's answer."
    }

    let botName: string = "Tutor";

    let userName: string = "User";


</script>
<div class="conversation-text-container">
    {#if speaker=="user"}
        <div class="user-response">
            <div class="text-meta-info-user">
                <img src="data:image/jpeg;base64,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" alt="user" width="30px" height="30px">
                <p class="speaker">{userName}</p>
            </div>

            <div class="text-container">
                <div class="user-text">
                    <p>{userTxt}</p>
                </div>
            </div>
        </div>

    {:else}
        <div class="text-meta-info" transition:fly={{
            x: -100,
            delay,
        }}>
            <img src="https://i.imgur.com/8Km9tLL.png" alt="user" width="30px" height="30px">
            <p class="speaker">{botName}</p>
        </div>

        <div class="text-container">
            <div class="text">
                {#if userTxt !== ''}
                <p>{userTxt}</p>
                {:else}
                <p>{botTxt}</p>
                {/if}
            </div>
        </div>
    {/if}
    
    
</div>

<style>
    .conversation-text-container{
        font-family: Noto Sans, sans-serif;
        font-size: 15px;
    }

    .user-response {
        /* background: red; */
        text-align: end;
    }

    .user-text {
        /* background: blue; */
        text-align: end;
        padding-right: 20px;
    }

    .text-meta-info-user {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 20px;
        color: #00a7e1;
    }

    .text-container {
        border-radius: 7px;
        width: 95%;
        padding: 20px 0px 20px 20px;
        background-color: rgb(247, 247, 247);
        box-shadow: 3px 1px 1px 1px rgba(0, 0, 0, 0.1);
    }

    .text-meta-info{
        display: flex;
        align-items: center;
        padding-left: 20px;
        color: #00a7e1;
    }

    img {
        border-radius: 50%;
    }

    .speaker {
        padding-left: 20px;
        font-weight: 700;
    }
</style>