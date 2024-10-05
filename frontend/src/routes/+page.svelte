<script lang="ts">
    import * as Tabs from '$lib/components/ui/tabs/index.js';
    import Verify from "$lib/components/GuestFaceRecognition.svelte";
    import History from "$lib/components/History.svelte";
</script>

<Tabs.Root value="verify" class="w-full">
    <Tabs.List class="flex justify-start gap-4 p-8 bg-gray-100 border-2 border-bg-gray-200">
        <h1 class="mb-1 text-2xl font-extrabold text-black">Smart Doorbell</h1>
        <Tabs.Trigger value="verify" class="text-xl border-2 border-bg-gray-200">Guest</Tabs.Trigger>
        <Tabs.Trigger value="history" class="text-xl border-2 border-bg-gray-200">History</Tabs.Trigger>
    </Tabs.List>
    -
    <Tabs.Content value="verify">
        <Verify/>
    </Tabs.Content>
    <Tabs.Content value="history">
        <History/>
    </Tabs.Content>
</Tabs.Root>
