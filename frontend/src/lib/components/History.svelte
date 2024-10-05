<script lang="ts">
    import {onMount} from 'svelte';
    import * as Card from '$lib/components/ui/card/index.js';
    import { Separator } from "$lib/components/ui/separator";

    interface HistoryItem {
        id: number;
        imageSrc: string;
        timestamp: string;
        status: 'Approved' | 'Rejected' | 'Ignored';
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

        if (date.toDateString() === today.toDateString()) {
            return 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Yesterday';
        } else {
            return date.toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'});
        }
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
        });
        return grouped;
    }

    onMount(async () => {
        // Simulated data fetch
        // Replace this with actual API call to fetch history data
        const mockData: HistoryItem[] = [
            {id: 1, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-27 10:30:00', status: 'Approved'},
            {id: 2, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-27 11:45:00', status: 'Rejected'},
            {id: 3, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-27 11:45:00', status: 'Rejected'},
            {id: 4, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-26 14:15:00', status: 'Ignored'},
            {id: 5, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-26 14:15:00', status: 'Ignored'},
            {id: 6, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-25 09:00:00', status: 'Approved'},
            {id: 7, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
            {id: 8, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
            {id: 9, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
            {id: 10, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
            {id: 11, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
            {id: 12, imageSrc: '/api/placeholder/300/200', timestamp: '2024-09-02 16:30:00', status: 'Rejected'},
        ];
        historyItems = mockData;
        groupedHistory = groupHistoryByDate(historyItems);


    });






</script>

<div class="container mx-auto px-4 py-8">
    <h1 class="mb-6 text-3xl font-bold">Guest History</h1>
    {#each Object.entries(groupedHistory) as [date, items]}
        <div class="mb-8">
            <h2 class="mb-4 text-2xl">{date}</h2>
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                {#each items as item (item.id)}
                    <Card.Root class="overflow-hidden">
                        <Card.Content class="p-0">
                            <img src={item.imageSrc} alt="Guest at {item.timestamp}" class="h-48 w-full object-cover"/>
                            <div class="p-4">
                                <p class="text-sm text-gray-500">{new Date(item.timestamp).toLocaleTimeString()}</p>
                                <div class="mt-2 flex items-center justify-between">
                                    {#if item.status === 'Approved'}
                                        <span class="text-green-500">Approved</span>
                                    {:else if item.status === 'Rejected'}
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