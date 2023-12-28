<script lang="ts">

    import { completeNode, selectedNode, nodeNames, refresh } from "$lib/api/nodes";
    import { getTopicSummary } from "$lib/api/topicSummary";
    import { selectedTextbook } from "$lib/api/textbooks";
    import { onMount } from "svelte";

    let node : Node;
    let label : string = "";
    let summary : string = "";

    onMount(async () => {
        if ($selectedNode != null && $selectedTextbook != null) {
            label = $nodeNames[$selectedNode].split(' ').map((word) => word.charAt(0).toUpperCase() + word.substr(1)).join(' ');
            summary = await getTopicSummary($selectedTextbook, label);
        }
    });

    const onClick = () => {
        if ($selectedNode != null) {
            completeNode($selectedNode);
            refresh.set(!$refresh);
        }
    }
</script>

<div class="topicContainer">
  <h1>{label}</h1>
  <div class="scrollableText">
    {#if summary == ""}
    <div class="centerer">
        <div class="loader"></div> 
    </div>
    {:else}
        <h3>{summary}</h3>
    {/if}
  </div>
  <div class="containerRow">
    <button id="understandButton" on:click={() => onClick()}>I Understand</button>
  </div>
</div>

<style>
    .topicContainer {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        min-width: 50%;
        height: 100%;
        background-color: white;
    }
    .scrollableText {
        height: 500px;
        width: 80%;
        overflow: hidden;
        padding-bottom: 5%;
        background-color: white;
    }
    .containerRow {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        background-color: white;
        opacity: 1;
        width: 100%;
        height: 80px;
    }

    .loader {
        border: 16px solid #f3f3f3; /* Light grey */
        border-top: 16px solid #3498db; /* Blue */
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 2s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .centerer {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    #understandButton {
        width: 30%;
        height: 100%;
        background-color: white;
        color: black;
        font-size: 15px;
        border: 0;
        /* add some drop shadow all around the button */
        box-shadow: 0px 0px 3px 1px rgba(0, 0, 0, 0.2);
        border-radius: 5px;
        cursor: pointer;
        transition: 0.1s;
    }
    
    #understandButton:hover {
        background-color: #f2f2f2;
        font-size: 16px;
    }
</style>