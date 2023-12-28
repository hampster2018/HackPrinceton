<script lang="ts">
    import { currentlyUploading } from "$lib/api/goals";
    import { uploadStage, getUploadStage, getApproximateKeywords, filesize } from "$lib/api/goals";
    import type { Goal } from "$lib/api/goals";

    let goals : Goal[] = []
    let numWeeks : number = 1;

    if ($currentlyUploading) {
        setInterval(async () => {
            console.log(numWeeks)
            await getUploadStage();
        }, 50000);
    }

    const suggestedGoal = () => {
        let anticipatedKeywords = getApproximateKeywords();

        let newGoals : Goal[] = []
        for (let i = 0; i < numWeeks; i++) {
            const weeklyKeywords = Math.ceil(anticipatedKeywords / (numWeeks - i));
            newGoals.push({
                weekNum: i + 1,
                anticipatedKeywords: weeklyKeywords
            })
            anticipatedKeywords -= weeklyKeywords;
        }
        goals = newGoals;
    }

    const submitGoal = () => {
        console.log(goals);
    }
    
</script>

{#if $currentlyUploading}
    <div id="blurer">
        {#key $uploadStage}
            <div class="goalsContainer">
                <div class="splitLeft">
                    <div class="header">
                        <h1>Upload a Goal</h1>
                    </div>
                    <div class="numWeeksDiv">
                        <label for="numWeeks">Num Weeks to Finish:</label>
                        <input type="number" id="numWeeks" name="numWeeks" min="1" max="52" value={numWeeks} on:change={(e) => numWeeks = parseInt(e.target?.value)}>
                        <br/>
                        {#key $filesize}
                            <label for="numWeeks" class="rightlabel">Approximate Number Terms: {getApproximateKeywords()}</label>
                        {/key}
                    </div>
                    <div class="topbuttonsdiv">
                        <button id="suggested" on:click={() => suggestedGoal()}>Generate Plan</button>
                    </div>
                    {#key goals}
                        <div class="weeksDiv">
                            <div class="weeklyDiv">
                                {#each goals as goal}
                                    <div class="weeklyCard">
                                        <h3>Week {goal.weekNum}:</h3>
                                        <p>{goal.anticipatedKeywords} Terms</p>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/key}
                    <div class="topbuttonsdiv">
                        <button id="addGoal" on:click={() => submitGoal()}>
                            Add Goal
                        </button>
                    </div>
                    
                </div>
                <div class="splitRight">
                    sup
                </div>
            </div>
        {/key}
    </div>
{/if}

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
    .goalsContainer {
        display: flex;
        flex-direction: row;
        position: absolute;
        top: calc(15% - 40px);
        left: 15%;
        height: 70%;
        width: 70%;
        background-color: white;
        box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        border-radius: 20px;
        padding: 40px;
        backdrop-filter: blur(20px);
    }
    .splitLeft {
        height: 100%;
        width: 70%;
        position: fixed;
        z-index: 1;
        top: 0;
        overflow-x: hidden;
        padding-top: 20px;
    }
    .splitRight {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
        width: 30%;
        position: fixed;
        z-index: 1;
        top: 0;
        right: 0;
        overflow-x: hidden;
        padding-top: 20px;
    }
    .header {
        display: flex;
        height: 15%;
        width: 70%;
        position: relative;
        z-index: 1;
        top: 0;
        right: 0;
        overflow-x: hidden;
        padding-top: 10px;
        text-align: center;
        justify-content: center;
    }
    .numWeeksDiv {
        display: flex;
        height: 5%;
        width: 70%;
        position: relative;
        z-index: 1;
        top: 0;
        right: 0;
        overflow-x: hidden;
        padding-top: 10px;
        text-align: center;
        justify-content: start;
        align-items: center;
    }
    label {
        margin-right: 15px;
    }
    .rightlabel {
        margin-left: 30px;
    }
    .topbuttonsdiv {
        display: flex;
        height: 5%;
        width: 70%;
        position: relative;
        z-index: 1;
        top: 0;
        right: 0;
        overflow-x: hidden;
        padding-top: 10px;
        text-align: center;
        justify-content: space-around;
        align-items: center;
        margin-top: 10px;
    }
    .weeksDiv {
        display: flex;
        flex-direction: column;
        max-height: 200px;
        height: 45%;
        width: 70%;
        position: relative;
        z-index: 1;
        top: 0;
        right: 0;
        padding-top: 50px;
        padding-left: 40px;
        text-align: center;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 100px;
    }
    .weeklyDiv {
        justify-self: center;
        overflow: auto;
        position: absolute;
        width: 100%;
        height: 100%;
        margin: 10px;
        padding: 10px;
    }
    .weeklyDiv::-webkit-scrollbar {
        width: 10px;
    }
    .weeklyCard {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        height: 40px;
        width: 80%;
        background-color: white;
        box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>