<template>
    <div class="space-y-2">
        <div
            v-for="(track, index) in tracks"
            :key="track.id"
            class="flex items-center gap-4 py-3 px-4 bg-divider rounded-xl shadow-sm hover:shadow-md transition relative"
        >
            <!-- Position Number -->
            <div class="w-6 text-right text-secondaryText font-medium">
            {{ index + 1 }}
            </div>
    
            <!-- Album Cover -->
            <img
                :src="track.album_image_url"
                alt="Album Art"
                class="w-12 h-12 object-cover rounded-[2px] lg:rounded-[4px] shadow-sm flex-shrink-0"
            />

    
            <!-- Track Info -->
            <div class="flex-1 min-w-0">
            <p class="text-base font-silkscreen text-white truncate">
                {{ track.track_name }}
            </p>
            <p class="text-sm text-secondaryText truncate">
                {{ track.artist_name }}
            </p>
            </div>
    
            <!-- Three Dot Menu -->
            <div class="relative">
            <button
                @click="toggleMenu(track.id)"
                class="text-secondaryText hover:text-accent transition"
            >
                <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
                >
                <circle cx="4" cy="10" r="2" />
                <circle cx="10" cy="10" r="2" />
                <circle cx="16" cy="10" r="2" />
                </svg>
            </button>
    
            <!-- Dropdown -->
            <div
                v-if="openMenu === track.id"
                class="absolute right-0 mt-2 w-32 bg-primary border divider rounded-md shadow-lg z-10"
            >
                <button
                @click="removeTrack(track)"
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-divider rounded"
                >
                Remove
                </button>
            </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import apiClient from '../api'

const props = defineProps({
    tracks: {
        type: Array,
        required: true
    },
    queueId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['trackRemoved'])

const openMenu = ref(null)


const toggleMenu = (id) => {
    openMenu.value = openMenu.value === id ? null : id
}

// Make a local reactive copy of tracks
const localTracks = ref([...props.tracks])

const removeTrack = async (track) => {
    try {
        const res = await apiClient.delete(`/queue/${props.queueId}/remove_track/${track.id}/`)
        localTracks.value = localTracks.value.filter(t => t.id !== track.id)

        emit('trackRemoved', { 
            removedId: track.id, 
            remainingTracks: localTracks.value 
        })
        openMenu.value = null
    } catch (err) {
        alert('Failed to remove track: ' + (err.response?.data?.error || err.message))
    }
}
</script>
  