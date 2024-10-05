<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';
    import { Button } from '$lib/components/ui/button/index.js';
    import { onMount, onDestroy } from 'svelte';

    let imageSrc = ''; 
    let ws: WebSocket | null = null;
    let name = '';
    let status = '';

    onMount(() => {
        ws = new WebSocket('ws://localhost:8080/ws?type=frontend');

        ws.onmessage = (event) => {
            if (typeof event.data === 'string') {
                name = event.data.split(":")[0];
                status = event.data.split(":")[1];
                console.log(`Received message: ${event.data}`);
            } else if (event.data instanceof Blob) {
                const blob = event.data;
                imageSrc = URL.createObjectURL(blob);
            }
        };
    });

    onDestroy(() => {
        if (ws) {
            ws.close();
        }
    });

</script>

<Card.Root class="flex w-full flex-col items-center justify-center">
    <Card.Header>
        <Card.Title class="text-2xl">Guest Face Recognition</Card.Title>
    </Card.Header>
    <Card.Content class="space-y-4">

        <div class="border-2 border-b-gray-200">
            {#if imageSrc}
                <img class="max-h-[720px]" src={imageSrc} alt="Received Image" />
            {:else}
                <div class="flex h-[480px] w-[720px] items-center justify-center bg-gray-50">
                    <p class="text-gray-600">No guest...</p>
                </div>
                <div>
                    <p>{name}</p>
                    <p>{status}</p>
                </div>
            {/if}
        </div>

    </Card.Content>
</Card.Root>