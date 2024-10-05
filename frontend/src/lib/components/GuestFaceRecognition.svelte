<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';
    import { Button } from '$lib/components/ui/button/index.js';
    import { onMount, onDestroy } from 'svelte';

    let imageSrc = ''; 
    let ws: WebSocket | null = null;
    let name = '';
    let status = '';
    let countDown = 0;

    onMount(() => {
        ws = new WebSocket('ws://175.41.178.14:8080?type=frontend');

        ws.onmessage = (event) => {
            if (typeof event.data === 'string') {
                name = event.data.split(":")[0];
                status = event.data.split(": ")[1];
                console.log(`Received message: ${event.data}`);
                countDown = 10;
            } else if (event.data instanceof Blob) {
                const blob = event.data;
                imageSrc = URL.createObjectURL(blob);
                countDown = 10
            }
        };
    });

    onDestroy(() => {
        if (ws) {
            ws.close();
        }
    });

    setInterval(() => {
        if (countDown > 0) {
            countDown--;
        } else {
            imageSrc = '';
            name = '';
            status = '';
        }
    }, 1000);

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
                </div>
            {/if}
        </div>
        {#if imageSrc}
            <div class="flex flex-col items-center justify-center text-xl font-bold">
                <p>name: {name}</p>
                <p>status:
                    {#if status === "Accept"}
                        <span class="text-green-500">Accepted</span>
                    {:else if status === "Reject"}
                        <span class="text-red-500">Rejected</span>
                    {/if}
                </p>
            </div>
        {/if}

    </Card.Content>
</Card.Root>