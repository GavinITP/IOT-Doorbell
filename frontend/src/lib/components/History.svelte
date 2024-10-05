<script lang="ts">
    import {onMount} from 'svelte';
    import * as Card from '$lib/components/ui/card/index.js';
    import { Separator } from "$lib/components/ui/separator";

    interface HistoryItem {
        id: number;
        name: string;
        imageSrc: string;
        timestamp: string;
        status: 'Accept' | 'Reject' | 'Ignore';
    }

    interface GroupedHistory {
        [date: string]: HistoryItem[];
    }

    let historyItems: HistoryItem[] = [];
    let groupedHistory: GroupedHistory = {};

    function formatDate(date: Date): string {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        return date.toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'});
    }

    function groupHistoryByDate(items: HistoryItem[]): GroupedHistory {
        let grouped: GroupedHistory = {};
        items.forEach(item => {
            const date = new Date(item.timestamp);
            const dateKey = formatDate(date);
            if (!grouped[dateKey]) {
                grouped[dateKey] = [];
            }
            grouped[dateKey].push(item);
            grouped[dateKey].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
        });


        return grouped;
    }

    onMount(async () => {
        await fetch('http://0.0.0.0:8000/history')
            .then(response => response.json())
            .then(data => {
                for (let i = 0; i < data.history.length; i++) {
                    let item = data.history[i];
                    item.timestamp = new Date(item.timestamp).toLocaleString();
                    console.log(item);
                    let status = item.name.split('_')[3];
                    if (status === 'Accept.jpg') {
                        status = 'Accept';
                    } else {
                        status = 'Reject';
                    }
                    let name:string = item.name.split('_')[2];
                    if (name.includes('.jpg')) {
                        name = "Unknown";
                    }
                    historyItems.push({
                        id: i,
                        name: name,
                        imageSrc: item.url,
                        timestamp: item.timestamp,
                        status: status
                    });
                }
                groupedHistory = groupHistoryByDate(historyItems);
            });
    });






</script>

<div class="container mx-auto px-4 py-8">
    <h1 class="mb-6 text-3xl font-bold">Guest History</h1>
    {#each Object.entries(groupedHistory).sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime()) as [date, items]}
        <div class="mb-16">
            {#if date === formatDate(new Date())}
                <h2 class="mb-4 text-2xl">Today</h2>
            {:else if date === formatDate(new Date(new Date().setDate(new Date().getDate() - 1)))}
                <h2 class="mb-4 text-2xl">Yesterday</h2>
            {:else}
                <h2 class="mb-4 text-2xl">{date}</h2>
            {/if}
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                {#each items as item (item.id)}
                    <Card.Root class="overflow-hidden">
                        <Card.Content class="p-0">
                            <img src={item.imageSrc} alt="Guest at {item.timestamp}" class="w-full h-full object-cover"/>
                            <div class="p-4">
                                <p class="text-sm text-gray-500">{new Date(item.timestamp).toLocaleTimeString()}</p>
                                <p class="text-lg font-bold">{item.name}</p>
                                <div class="mt-2 flex items-center justify-between">
                                    {#if item.status === 'Accept'}
                                        <span class="text-green-500">Accepted</span>
                                    {:else if item.status === 'Reject'}
                                        <span class="text-red-500">Rejected</span>
                                    {:else}
                                        <span class="text-yellow-500">Ignored</span>
                                    {/if}
                                </div>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            </div>
        </div>
    {/each}
</div>