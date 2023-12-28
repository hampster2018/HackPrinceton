<script lang="ts">
	export let menuOpen : boolean;
</script>

<style>	
/* Dropdown Button */
.dropbtn {
  color: black;
  background-color: white;
  padding: 16px;
  width: 12rem;
  font-size: 16px;
  border: none;
  cursor: pointer;
	margin: 20px 10px 20px 10px;
}
	
</style>

  <button on:click class="dropbtn">{!menuOpen ? "Select A Textbook ▼" : "Close ▲"}</button>