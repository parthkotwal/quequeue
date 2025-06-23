<template>
    <div class="border rounded-xl shadow-md hover:shadow-lg cursor-pointer transition p-4 flex flex-col items-center text-center"
    @click="$emit('click')">
        <img :src="queue.image_url" alt="Cover" class="h-32 w-32 object-cover rounded-md mb-3" />
        <h2 class="text-lg font-semibold">{{ queue.name }}</h2>
        <p class="text-gray-500 text-sm">{{ queue.description }}</p>
    </div>
</template>

<script setup>
defineProps({
  queue: Object
})
</script>