<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';
    import { Button } from '$lib/components/ui/button/index.js';
    import { onMount, onDestroy } from 'svelte';

    let imageSrc = ''; 
    let ws: WebSocket | null = null; 

    let showSentMessageStatus = false; 
    let sentMessageStatus = ''; 

    onMount(() => {
        ws = new WebSocket('ws://localhost:8080/ws?type=frontend');

        ws.onmessage = (event) => {
            if (typeof event.data === 'string') {
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

    const sendMessage = (message: string) => {
        showSentMessageStatus = true; 
        if (ws) {
            ws.send(message); 
            console.log(`Sent message: ${message}`);
            sentMessageStatus = message + ' successfully'; 
        } else {
            console.error('WebSocket connection is not established');
            sentMessageStatus = 'Error'; 
        }
    };

    const handleApprove = () => {
        sendMessage('Approved');
    };

    const handleReject = () => {
        sendMessage('Rejected');
    };

    $: if (showSentMessageStatus) {
        setTimeout(() => {
            showSentMessageStatus = false;
        }, 1000);
    }
</script>

<Card.Root class="flex w-full flex-col items-center justify-center">
    <Card.Header>
        <Card.Title class="text-2xl">Verify Guest</Card.Title>
    </Card.Header>
    <Card.Content class="space-y-4">

        {#if showSentMessageStatus}
            <div class="text-bold text-xl">
                {#if sentMessageStatus === 'Error'}
                    <p class="text-red-600 flex flex-row gap-2 justify-center items-center">
                        {sentMessageStatus}
                    </p>
                {:else}
                    <p class="text-green-600 flex flex-row gap-2 justify-center items-center">
                        {sentMessageStatus}
                    </p>
                {/if}
            </div>
        {/if}

        <div class="border-2 border-b-gray-200">
            {#if imageSrc}
                <img class="max-h-[720px]" src={imageSrc} alt="Received Image" />
            {:else}
                <div class="flex h-[480px] w-[720px] items-center justify-center bg-gray-50">
                    <p class="text-gray-600">No guest...</p>
                </div>
            {/if}
        </div>

        <div class="flex justify-center gap-4">
            <Button class="bg-green-500 hover:bg-green-500" on:click={handleApprove}>Approve</Button>
            <Button variant="destructive" on:click={handleReject}>Reject</Button>
        </div>
    </Card.Content>
</Card.Root>