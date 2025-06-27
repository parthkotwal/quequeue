<!-- Use queueId from ExportIntro -->
<!-- Fetch exported queue details from GET /api/queues/:id (id = queueId) -->
<!-- Show track using TrackList -->
<!-- Have confirm/continue button -->
<!-- Also have no/back button, which could call DELETE /api/queues/:id -->

<template>
    <div class="space-y-6">
        <h2 class="text-2xl font-bold">Preview Your Queue</h2>

        <div v-if="loading">Loading your queue...</div>
        <div v-else-if="error" class="text-red-600">{{ error }}</div>

        <div v-if="queue && !loading">
            <p class="mb-4 text-gray-700">
                Here's the current Spotify queue we detected.
            </p>

            <TrackList :tracks="queue.tracks" />

            <div class="flex justify-between mt-6">
                <button class="bg-gray-400 text-white px-4 py-2 rounded" @click="cancel" :disabled="loading">Cancel</button>
                
                <button class="bg-green-600 text-white px-6 py-2 rounded" @click="confirm" :disabled="loading">Looks Good!</button>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import TrackList from '../components/TrackList.vue';

const props = defineProps({
    queueId: {
        type: Number,
        required: true
    }
})
const emit = defineEmits(['next','back'])

const queue = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchQueue = async () => {
    loading.value = true
    error.value = null

    const maxAttempts = 5
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            const res = await axios.get(`/api/queue/${props.queueId}/get/`, {
            withCredentials: true
        })
            queue.value = res.data
            loading.value = false
            return // success
        } catch (err) {
            if (attempt === maxAttempts) {
                error.value = 'Failed to load queue. Please try again.'
                loading.value = false
                return
            }
            console.warn(`Retry ${attempt}...`)
            await delay(500) // wait before retry
        }
    }

    loading.value = false
}

const confirm = () => {
    emit('next', { queueId: props.queueId })
}

const cancel = async () => {
    loading.value = true
    try {
        await axios.delete('/api/queues/'+ props.queueId + '/delete/', {
            withCredentials: true
        })
        emit('back')
    } catch (err) {
        error.value = 'Failed to cancel. Try again.'
        loading.value = false
    }
}

onMounted(fetchQueue)
</script>