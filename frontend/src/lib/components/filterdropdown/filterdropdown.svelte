<script lang="ts">
	import Link from './Link.svelte';
	import Button from './Button.svelte';
	import Input from './Input.svelte';
	import Button2 from './Button2.svelte';
	import Input2 from './Input2.svelte';
	import Button3 from './Button3.svelte';
	import Input3 from './Input3.svelte';
	import { textbookNames, getTextbookName } from '$lib/api/textbooks';
	import { nodeNames } from '$lib/api/nodes';
  	import { onMount } from 'svelte';

	onMount(() => {
		getTextbookName();
	})

	// button 1
	let menuOpen = false;
	let inputValue = "";
	console.log($textbookNames)
	let filteredItems : string[] = [];
	
	const handleInput = () => {
		return filteredItems = $textbookNames.filter(item => item.toLowerCase().match(inputValue.toLowerCase()));	
	}

	// button 2
	let menuOpen2 = false;
	let inputValue2 = "";
	$:console.log(inputValue2)
	
	let filteredItems2 : string[] = [];
	
	const handleInput2 = () => {
		return filteredItems2 = $nodeNames.filter(item => item.toLowerCase().match(inputValue2.toLowerCase()));	
	}

	// button 3
	let menuOpen3 = false;
	let inputValue3 = "";
	
	const menuItems3 = ["Book1", "Book2", "Book3", "Book4", "Book5", "Book6", "Book7", "Book8", "Book9", "Book10", "Book11", "Book12", "Book13", "Book14", "Book15"];
	let filteredItems3 : string[] = [];
	
	const handleInput3 = () => {
		return filteredItems3 = menuItems3.filter(item => item.toLowerCase().match(inputValue3.toLowerCase()));	
	}


</script>


<section class="dropdown">
	<h1>Redwood</h1>
  <Button on:click={() => menuOpen = !menuOpen} {menuOpen} /><br/>
	
  <div id="myDropdown" class:show={menuOpen} class="dropdown-content">		
  <Input bind:inputValue on:input={handleInput} />
		{#if filteredItems.length > 0}
			{#each filteredItems as item}
				<Link link={item} />
			{/each}
		{:else}
			{#each $textbookNames as item}
				<Link link={item} />
			{/each}
		{/if}		
  </div>	

	<!-- button2 -->
	<Button2 on:click={() => menuOpen2 = !menuOpen2} {menuOpen2} /><br/>
	
  <div id="myDropdown2" class:show={menuOpen2} class="dropdown-content">		
  <Input2 bind:inputValue2 on:input={handleInput2} />		
		<!-- MENU -->
		{#if filteredItems2.length > 0}
			{#each filteredItems2 as item}
				<Link link={item} />
			{/each}
		{:else}
			{#each $nodeNames as item}
				<Link link={item} />
			{/each}
		{/if}		
  </div>

	<!-- button3 -->
	<Button3 on:click={() => menuOpen3 = !menuOpen3} {menuOpen3} />
	
  <div id="myDropdown3" class:show={menuOpen3} class="dropdown-content">		
  <Input3 bind:inputValue3 on:input={handleInput3} />		
		<!-- MENU -->
		{#if filteredItems3.length > 0}
			{#each filteredItems3 as item}
				<Link link={item} />
			{/each}
		{:else}
			{#each menuItems3 as item}
				<Link link={item} />
			{/each}
		{/if}		
  </div>	

</section>
	
	
<style>		
.dropdown {
	position: relative;
	display: inline-block;
	width: 12rem;
}
	
h1{
	color: white;
	width: 10rem;
	padding: 16px;
	font-size: 28px;
	font-weight: bold;
	margin: 10px;
}

.dropdown-content {
	display: none;
	position: absolute;
	background-color: #f6f6f6;
	width: 12rem;
	border: 1px solid #ddd;
	z-index: 1;
	overflow-y: auto;
	height: 100%;
	margin: 10px;
}

/* Show the dropdown menu */	
.show {display:block;}	
</style>