<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { onMount, onDestroy } from 'svelte';
    import {CircleAlert, CircleCheck} from "lucide-svelte";

	let imageSrc = '';
	let showImage = false; // Controls the image visibility
	let countdown = 0;
	let isIgnored = false;
	let ws: WebSocket | null = null;

    let showSentMessageStatus = false;
    let sentMessageStatus = '';

	onMount(() => {
		ws = new WebSocket('ws://localhost:8080/ws?type=receiver');

		ws.onmessage = (event) => {
			if (event.data instanceof Blob) {
				const blob = event.data;
				const url = URL.createObjectURL(blob);
				imageSrc = url;
				showImage = true; // Show the image after receiving
				countdown = 15; // Reset the countdown
				isIgnored = true;
			}
		};
	});

	onDestroy(() => {
		if (ws) {
			ws.close();
		}
	});

	setInterval(() => {
		if (countdown > 0) {
			countdown--;
		} else if (countdown === 0 && isIgnored) {
			handleIgnore();
		}
	}, 1000);

	const sendMessage = (message: string) => {
        showSentMessageStatus = true;
		if (ws) {
			ws.send(message);
			console.log(`Sent message: ${message}`);

            sentMessageStatus =  message + ' successfully';
		} else {
			console.error('WebSocket connection is not established');

            sentMessageStatus = 'Error';
		}
	};

	const handleApprove = () => {
		isIgnored = false;
		countdown = 0;
		sendMessage('Approved');
	};

	const handleReject = () => {
		isIgnored = false;
		countdown = 0;
		sendMessage('Rejected');
	};

	const handleIgnore = () => {
		isIgnored = true;
		sendMessage('Ignored');
		isIgnored = false;
	};

    // when the status is updated, hide it after 1 seconds
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
		{#if countdown > 0}
			<p class="text-bold text-center text-xl text-red-600">
				Ignoring this guest in {countdown} seconds
			</p>
		{/if}

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
			{#if showImage && countdown > 0}
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
