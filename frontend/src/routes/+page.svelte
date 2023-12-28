<script lang="ts">
    import { onMount } from "svelte";
    import Graph from "$lib/components/Graph.svelte";
    import { blurred } from "$lib/api/chat";
    import { getNodes, refresh } from "$lib/api/nodes";
    import Conversation from "$lib/components/conversation/Conversation.svelte";
    import Topic from "$lib/components/topic/topic.svelte";
    import { Shadow } from 'svelte-loading-spinners';
    import { fade } from 'svelte/transition';
    import Info from '$lib/components/Info.svelte'
	import { selectedTextbook, getTextbookName, textbookNames } from "$lib/api/textbooks";
    import { nodeNames } from "$lib/api/nodes";
    import Cross from '$lib/components/icons/Cross.svelte'
    import { currentlyUploading, filesize } from "$lib/api/goals";
    import Goals from "$lib/components/goals/goals.svelte";

    export const prerender = true;
    export const ssr = true;

    onMount(async () => {
        await getNodes();
        await getTextbookName();
        options.push(...$textbookNames);
        options = options
    });
    
    let textbookSelected = 0;
    let loadingFlag = 0;
    let textbook = "default";
    let count = 0;
    let timerFlag = 0;
    let showAdd = 0;
    let dropdownVal = "Select"
    let options : string[] = ["Select"];

    let setTextbook = () => {
        if (dropdownVal != "Select") {
            selectedTextbook.set(dropdownVal);
            loadingFlag = 1;
            textbookSelected = 1;
            console.log(dropdownVal)
            
            setTimeout(() => {
                timerFlag = 1;
            }, $nodeNames.length * 50 + 3000);
        }
    }

    let toggleView = () => {
        blurred.set(false);
    }

    let onFileUploadClick = () => {
        document.getElementById('selectedFile')?.click();
        currentlyUploading.set(!($currentlyUploading));
        $currentlyUploading = $currentlyUploading
    }

    let onInputChange = (e : any) => {
        let file : File = e.target.files[0];
        let fileSize = Math.round(e.target.files[0].size / 1000);
        filesize.set(fileSize);
        

    }

</script>

<div class="master-container">
    <Goals />
    <div class="navbar">
        <p class="logo">REDWOOD</p>
        <div class="dropdown">
            <p class="dd-txt">Current Textbook:</p>
            {#key options}
            <select class="dd" bind:value={dropdownVal} on:change={setTextbook()}>
                {#each options as option}
                    <option value={option}>{option}</option>
                {/each}
            </select>
            {/key}
            <input type="file" id="selectedFile" style="display: none;" on:change={(e) => onInputChange(e)}/>
            <input type="button" value="Upload" on:click={() => onFileUploadClick()} />
        </div>
    </div>

    

    {#if loadingFlag}
        <!-- wait msg -->
        {#if timerFlag == 0}
            <div class="wait-msg-container" transition:fade={{delay: 250, duration: 700}}>
                <p class="load-msg">Growing your learning tree!</p>
                <div class="loading" transition:fade={{delay: 300, duration: 700}}>
                    <Shadow size="30" color="#00a7e1" unit="px" duration="2s"/>
                </div>
            </div>
        {:else}
            <div class="txtbk-container" transition:fade={{delay: 1000, duration: 700}}>
                <p class="txtbk-unan">Explore your</p> 
                <p class="txtbk">{$selectedTextbook}</p> 
                <p class="txtbk-unan">forest!</p>
            </div>

            <Info />

        {/if}

        <!-- graph -->
        <div class="graph-container">
            {#key dropdownVal || $refresh}
                    <Graph />
            {/key}
        </div>

        {#if $blurred}
        <div id="blurer">
            <div class="conversationContainer">
                <Topic/>
                <Conversation/>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="close-button" on:click={toggleView}>
                    <Cross />
                </div>
            </div>
        </div>
        {/if}

    {:else}
        <div class="start-prmpt">
            <div class="lets-prmp">
                <p class="lets-txt">Let's get</p> 
                <p class="start-prmpt-ani">started</p>
                <p class="lets-txt">!</p> 
            </div>
            <div class="lets-prmp">
                <p class="lets-txt">Use the</p>
                <p class="start-prmpt-ani2">dropdown menu above</p> 
                <p class="lets-txt">to select your textbook.</p>
            </div> 
        </div>     
        <!-- {#if $blurred}
                <div class="conversation">
                    <Conversation/>
                </div>
            {/if}
        {#key $nodes}
            <div class="graph-container">
                <Graph />
            </div>
        {/key}

        
        <div class="txtbk-container">
            <p class="txtbk-unan">Explore your</p> 
            <p class="txtbk">{textbook}</p> 
            <p class="txtbk-unan">forest!</p>
        </div> -->

            

            <!-- {:else} -->
    {/if}
    <!-- 9 seconds -->
</div>

 <style>
    
    #blurer {
        position: absolute;
        height: 100vh;
        width: 100vw;
        top: 0;
        left: 0;
        backdrop-filter: blur(10px);
        z-index: 9999;
    }

    .lets-prmp{
        display: flex;
        text-align: center;
        align-items: center;
        justify-content: center;
        /* border: solid 1px blue; */
    }

    .start-prmpt{
        /* border: solid 1px red; */
        font-size: 30px;
        height: 100vh;
        text-align: center;
        padding-top: 25vh;
        /* display: flex; */
    }

    .start-prmpt-ani{
        font-size: 30px;
        text-align: center;
        animation-name: start-prm;
        animation-duration: 3s;
        margin-left: 10px;
        font-weight: 700;
        color: #00a7e1;
    }

    .start-prmpt-ani2{
        font-size: 30px;
        text-align: center;
        animation-name: start-prm2;
        animation-duration: 4s;
        margin-left: 10px;
        margin-right: 10px;
        font-weight: 700;
        color: #00a7e1;
        /* border: solid 1px red; */
        animation-delay: 1s;
    }

    @keyframes start-prm {
        0%  {
            /* letter-spacing: 0px; */
            color: black;
            box-shadow: inset 0 0 0 0 #00a7e1;
        }
        25% {
            /* letter-spacing: 2px; */
            color: white;
            box-shadow: inset 100px 0 0 #00a7e1;
        }
        50% {
            /* letter-spacing: 4px; */
            color: white;
            box-shadow: inset 100px 0 0 0 #00a7e1;

        }
        100% {
            /* letter-spacing: 0px; */
            color: #00a7e1;
            box-shadow: inset 0 0 0 0 #00a7e1;

        }
    }

    @keyframes start-prm2 {
        0%  {
            /* letter-spacing: 0px; */
            color: black;
            box-shadow: inset 0 0 0 0 #00a7e1;
        }
        25% {
            /* letter-spacing: 2px; */
            color: white;
            box-shadow: inset 400px 0 0 0 #00a7e1;
        }
        50% {
            /* letter-spacing: 4px; */
            color: white;
            box-shadow: inset 400px 0 0 0 #00a7e1;

        }
        100% {
            /* letter-spacing: 0px; */
            color: #00a7e1;
            box-shadow: inset 0 0 0 0 #00a7e1;

        }
    }


    .txtbk-container{
        border: solid 1px grey;
        min-height: 150px;
        max-height: 150px;
        display: flex;
        text-align: center;
        align-items: center;
        justify-content: center;
   }
    :global(html) {
        overflow: hidden;
        padding: 0;
        margin: 0;
    }
    .bodyContainer {
        height: 100vh;
        width: 100vw;
    }
    .conversationContainer {
        display: flex;
        flex-direction: row;
        position: absolute;
        top: calc(15% - 40px);
        left: 15%;
        height: 70%;
        width: 70%;
        background-color: white;
        /* add some drop shadow */
        box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        border-radius: 20px;
        padding: 40px;
        backdrop-filter: blur(20px);
    }
    .txtbk {
        font-size: 30px;
        font-weight: 500;
        letter-spacing: 1px;
        padding-left: 30px;
        padding-top: 30px;
        /* border: solid 1px pink; */
        text-align: center;
    }
    .txtbk{
        /* padding-left: 20px;
        padding-right: 20px; */
        animation-name: txt-forest;
        color: #00a7e1;
        animation-duration: 3s;
        animation-iteration-count: 1;
        box-shadow: inset 0 0 0 0 #00a7e1;
        transition: color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }
    .txtbk-unan{
        padding-left: 20px;
        padding-right: 20px;
    }

    @keyframes txt-forest {
        0%  {
            color: #00a7e1;
            /* letter-spacing: 0px; */
            box-shadow: inset 0 0 0 0 #00a7e1;
        }
        25% {
            color: white;
            /* letter-spacing: 2px; */
            box-shadow: inset 0 -100px 0 0 #00a7e1;
        }
        50% {
            color: white;
            /* letter-spacing: 4px; */
            box-shadow: inset 0 -100px 0 0 #00a7e1;

        }
        100% {
            color: #2887a6;
            /* letter-spacing: 0px; */
            box-shadow: inset 0 0 0 0 #00a7e1;

        }
    }

    .load-msg{
        /* color: blue; */
        animation-name: example;
        animation-duration: 5s;
        animation-iteration-count: infinite;      
    }

    @keyframes example {
        0%  {
            color: #00a7e1;
            letter-spacing: 0px;
        }
        25% {
            color: #2887a6;
            letter-spacing: 2px;
        }
        50% {
            color: #2887a6;
            letter-spacing: 4px;
        }
        100% {
            color: #2887a6;
            letter-spacing: 0px;
        }
    }

    .conversation{
        position: fixed;
        top: 50%;
        left: 50%;
        background-color: white;
        flex-direction: row;
        padding: 10px;
        border-radius: 7px;
        box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.1);
    }
    .close-button{
        position: relative;
        top: 5px;
        right: 20px;
        cursor: pointer;
    }

    .sidebar{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .dd-txt{
        padding-right: 15px;
    }

    select{
        background-color: white;
        border: solid 1px #00a7e1;
        font-size: 18px;
        letter-spacing: 1px;
        padding: 10px;
        padding-right: 30px;
        border-radius: 5px;
    }

    option{
        background-color: white;
        font-size: 18px;
        height: 200px;
        /* padding-left: 20px; */
        padding: 20px;
    }

    .logo{
        letter-spacing: 3px;
        /* border: solid 1px purple; */
        width: 20%;
        padding-left: 25px;
        /* box-shadow: inset 0 0 0 0 green; */
        color: white;
        /* margin: 0 -0.25rem; */
        /* padding 0 .25rem; */
        /* transition: color 0.3s ease-in-out, box-shadow 0.3s ease-in-out; */
    }

    .logo:hover{
        cursor: pointer;
        /* box-shadow: inset 100px 0 0 0 green; */
        color: white;
        font-weight: 100;
    }

    .navbar{
        /* border: solid 1px transparent; */
        background-color: #00a7e1;
        height: 75px;
        color: white;
        font-weight: 700;
        min-width: 100%;
        display: flex;
        align-items: center;
    }

    .dropdown{
        /* border: solid 1px pink; */
        width: 80%;
        text-align: end;
        padding-right: 30px;
        font-size: 20px;
        display: flex;
        justify-content: flex-end;
        /* background-color: #00a7e1; */

    }

    .loading {
        /* border: solid 1px red; */
        min-height: 50px;
        max-height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .master-container{
        font-family: Noto Sans, sans-serif;
    }

    .wait-msg-container{
        font-size: 35px;
        /* font-weight: 500; */
        border-bottom: solid 1px grey;
        /* box-shadow: 2px 0px 5px 2px rgba(0, 0, 0, 0.1); */
        min-height: 150px;
        max-height: 150px;
        text-align: center;
    }

 </style>
