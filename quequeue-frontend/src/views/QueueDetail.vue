<template>
    <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading">Loading queue...</div>
        
        <div v-else>
            <h1 class="text-3xl font-bold mb-2">{{ queue.name }}</h1>
            <p class="text-gray-700 mb-4">{{ queue.description }}</p>
            <img :src="queue.image_url" class="w-full max-w-md mb-6" alt="Queue Cover" />

            <button @click="restoreQueue" class="bg-blue-600 text-white px-4 py-2 mb-6 rounded">
                Restore to Spotify
            </button>

            <div v-if="queue.tracks.length">
                <h2 class="text-xl font-semibold mb-2">Tracks</h2>
                <TrackList :tracks="queue.tracks"/>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import TrackList from '../components/TrackList.vue';
import axios from 'axios';

const route = useRoute()
const queueId = route.params.id

const queue = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchQueue = async() => {
    loading.value = true
    try {
        const res = await axios.get('/api/queue/'+ queueId +'/get/', {
            withCredentials: true,
        })

        queue.value = res.data
    } catch (err) {
        console.error("Error loading queue:", err)
    } finally {
        loading.value = false
    }
}

const restoreQueue = async() => {
    try {
        const res = await axios.get('/api/restore_queue/' + queueId + '/', {
            withCredentials: true
        })
        alert(res.data.message)
    } catch(err) {
        alert("Restore failed: " + err.response?.data?.error || err.message)
    }
}

onMounted(fetchQueue)

</script>