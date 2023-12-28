<script lang="ts">
    import Sidebar2 from "./Sidebar2.svelte";
    import ArrorRight from "./ArrorRight.svelte";
  
    let sidebar_show = false;
  
    function handleButtonClick() {
      sidebar_show = !sidebar_show;
    }
    console.log(sidebar_show);
</script>

<div class="sidecarContainer">
  <div class="button-container" style="transform: translateX({sidebar_show ? '250px' : '0'})">
    <button on:click={handleButtonClick}>
      <ArrorRight {sidebar_show}/>
    </button>
  </div>

  <Sidebar2 bind:show={sidebar_show}/>
</div>

<style>
  .button-container {
    transition: transform 0.3s;
    position: absolute;
  }

  button {
    transition: transform 0.3s;
    position: absolute;
  }

  .sidecarContainer {
    position: absolute;
    top: 10px;
    left: 10px;
  }
</style>
  