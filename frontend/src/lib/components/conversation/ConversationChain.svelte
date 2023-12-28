<script lang="ts">
    import type { Memory } from '$lib/api/chat';
    import { memory } from '$lib/api/chat';
    import ConversationText from './ConversationText.svelte';
</script>

{#each $memory as item}
    <ConversationText {...item}/>
{/each}