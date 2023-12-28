<script lang="ts">

</script>

<div class="info-cont">
    <!-- <div class="line">
        <p class="info-txt">Your tree is</p>
        <p class="info-txt-emph">personalized to your textbook!</p>
    </div> -->
    <p class="info-txt">Your tree is
    <span class="info-txt-emph">personalized to your textbook</span>!</p>
    <p class="info-txt">Each <span class="info-txt-emph">leaf</span> represents a concept.</p>
    <p class="info-txt">Start exploring your textbook by <span class="info-txt-emph">zooming in and out on the forest</span>!</p>
    <p class="info-txt">If you want to learn more about a concept, <span class="info-txt-emph">click the concept leaf</span> to see a summary of the topic and to chat with your tutor!</p>
</div>

<style>
    .info-cont{
        background-color: white;
        /* border: solid 1px black; */
        border-radius: 5px;
        width: 200px;
        height: 60vh;
        padding: 20px;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-left: 10px;
        margin-top: 15px;
        box-shadow: 1px 1px 3px 1px grey;
        background-color: white;
        position:absolute;
        z-index: 1000;
    }

    .line{
        display: flex;
    }

    .info-txt{
        font-size: 20px;
        font-family: Noto Sans, sans-serif;
        letter-spacing: 1px;
    }

    .info-txt-emph{
        font-size: 23px;
        font-family: Noto Sans, sans-serif;
        color: #00a7e1;
        letter-spacing: 1px;
        font-weight: bold;
        animation-name: gr;
        animation-duration: 3s;
        animation-iteration-count: 1;
        
    }

    @keyframes gr {
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
</style>
