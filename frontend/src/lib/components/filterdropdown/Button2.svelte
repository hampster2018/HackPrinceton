<script lang="ts">
	export let menuOpen2 : boolean;
</script>

<style>	
/* Dropdown Button */
.dropbtn {
  color: black;
  background-color: white;
  width: 12rem;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
	margin: 20px 10px 20px 10px;
}
</style>


  <button on:click class="dropbtn">{!menuOpen2 ? "Find A Skill ▼" : "Close ▲"}</button>
