<script lang="ts">
    import ConversationText from "$lib/components/conversation/ConversationText.svelte";
    import ConversationChain from '$lib/components/conversation/ConversationChain.svelte';
    import { SyncLoader } from 'svelte-loading-spinners';
    import { blurred } from '$lib/api/chat';
    import { memory, getOpenAIChat } from '$lib/api/chat';

    let accentColor = "#00a7e1";
    let backgroundColor = "#ffffff";
    let textColor = "#040303";

    let submitIcon = './paper-plane.png'

    let userInput = "";

    let userTxtToSend = "";

    let showLoad = false;
    let seconds = 0;

    let showExtraBotResponse = false;

    $memory.push({speaker: "Initial", userTxt: ""});

    let forcedSpeaker = "";

    let t = 0;

    let pushBot = () => {
        t = Math.random()* 1;
        if(t < 0.5){
            showExtraBotResponse = true;
            t = Math.random()* 1;
            console.log(t)
            if(t < 0.5){
                forcedSpeaker = "botFollow1";
            } else {
                forcedSpeaker = "botFollow2";
            }
        } else {
            showExtraBotResponse = false;
        }
        showLoad = false;
        $memory.push({speaker: "speaker", userTxt: ""});
        if(showExtraBotResponse){
            $memory.push({speaker: forcedSpeaker, userTxt: ""});
        }
    }

    let submit = async () => {
        if(userInput == ""){
            return;
        }
        showLoad = true;
        memory.set([...$memory, {speaker: "user", userTxt: userInput}])
        const aiResponse = await getOpenAIChat(userInput);
        console.log(aiResponse);
        userInput = "";
        memory.set([...$memory, {speaker: "speaker", userTxt: aiResponse}])
        console.log($memory[$memory.length - 1])
        showLoad = false;
        $memory = $memory;
    };
    
</script>

<div class="work">
    <div class="container">
        <div class="chat-container">
            {#key $memory}
                <ConversationChain/>
            {/key}
            {#if showLoad}
                <div class="sync-con">
                    <SyncLoader size="40" color="#00a7e1" unit="px" duration="1s"/>
                </div>
            {/if}       
        </div>
        <div class="btm-container">
            <textarea bind:value={userInput} placeholder="Your tutor is ready..." maxlength="200"/>
            <div on:click="{submit}">
                <img src="https://cdn-icons-png.flaticon.com/512/149/149446.png" alt="user" width="30px" height="30px" class="submitBtn">
            </div>
        </div>
    </div>  
</div>

<style>
    .container {
        height: 100%;
        width: 80%;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        background-color: white;
    }

    .sync-con {
        /* border: solid 1px black; */
        margin-top: 20px;
    }

    .cbtn{
        font-size: 25px;
        padding-right: 20px;
        padding-top: 20px;
        color: black;
        margin: 0px;
        font-family: Noto Sans, sans-serif;
    }

    .cbtn:hover{
        cursor: pointer;
        font-weight: bold;
    }

    .btm-container{
        position: absolute;
        bottom: 0px;
        width: 100%;
        /* background: white; */
        border-top: solid 1px grey;
        display: flex;
        align-items: center;
        /* box-shadow: 0px -3px 2px 1px rgba(0, 0, 0, 0.1); */
        background-color: white;
    }

    .work {
        height: 100%;
        min-width: 50%;
        
    }

    .submitBtn {
        /* border: solid 1px red; */
        height: 35px;
        width: 35px;
        margin: 25px 0px 0px 10px;
    }

    .submitBtn:hover {
        cursor: pointer;
        height: 30px;
        width: 30px;
    }

    .chat-container {
        /* border: solid 1px red; */
        overflow-x: hidden;
        overflow-y: scroll;
        width: 100%;
        height: 100%;
        padding-bottom: 100px;
    }

    textarea {
        /* border: solid 1px black; */
        border-radius: 7px;
        width: 90%;
        margin-top: 30px;
        min-height: 50px;
        resize: none;
        font-family: Noto Sans, sans-serif;
        padding: 10px;
    }

    .ConTxt {
        padding-top: 20px;
    }

    .chat-container::-webkit-scrollbar {
        width: 10px; 
    }

    .chat-container::-webkit-scrollbar-thumb {
        background-color: #00a7e1;  
        border-radius: 10px; 
    }
</style>