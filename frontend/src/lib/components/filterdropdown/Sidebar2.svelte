<script lang="ts">
    import { fly } from "svelte/transition";
    import { fade } from "svelte/transition";
    import FilterDropDown from "$lib/components/filterdropdown/filterdropdown.svelte";
    
    export let show = false;
</script>

{#if show}
  <nav transition:fly={{x: -250, opacity: 1}}>
    <div>
      <FilterDropDown/>
      <button>
        +
      </button>
    </div>
  </nav>
{/if}
    
<style>
  nav {
    position: fixed;
    display: flex;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 15rem;
    overflow-y: auto;
    background-color: #00A7E1;
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 20%;
    height: 20%;
    /* background: rgba(0, 0, 0, 0.5); */
    cursor: default;
  }
  div{
    display: flex;
  }
  button{
    height: 25px;
    margin-top: 105px;
    margin-left: 15px;
    background: none;
    color: inherit;
    border: none;
    width: 25px;
    font-weight: bold;
    font-size: larger;
    cursor: pointer;
    outline: inherit;
  }
</style>