<template>
    <div>
        <div 
        v-for="track in tracks" 
        :key="track.id" 
        class="flex items-center space-x-4 mb-4 p-4 border rounded-md"
        >
            <img 
                :src="track.album_image_url" 
                alt="Album Art" 
                class="w-16 h-16 object-cover rounded"
            />
            <div>
                <p class="font-semibold">
                {{ track.position + 1 }}. {{ track.track_name }}
                </p>
                <p class="text-gray-500 text-sm">{{ track.artist_name }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    tracks: {
        type: Array,
        required: true
    }
})
</script>