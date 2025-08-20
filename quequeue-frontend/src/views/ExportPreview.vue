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
            <p class="mb-4 text-gray-700">Here's the current Spotify queue we detected.</p>

            <TrackList :tracks="queue.tracks" />

            <!-- ⬇️ Add this block here -->
            <div class="flex items-center justify-between mt-4">
                <div v-if="queue">
                    <span class="text-sm text-gray-600">
                        Snapshot taken at {{ formattedCreatedAt }}
                    </span>
                </div>

                <button
                    class="bg-blue-600 text-white px-4 py-2 rounded"
                    @click="refreshSnapshot"
                    :disabled="loading"
                >
                    Refresh from Spotify
                </button>
            </div>
            <!-- ⬆️ End new block -->

            <div class="flex justify-between mt-6">
                <button
                    class="bg-gray-400 text-white px-4 py-2 rounded"
                    @click="emit('cancel', { queueId: props.queueId })"
                    :disabled="loading"
                >
                    Back
                </button>
        
                <button
                    class="bg-green-600 text-white px-6 py-2 rounded"
                    @click="confirm"
                    :disabled="loading"
                >
                    Looks Good!
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import TrackList from '../components/TrackList.vue';
import apiClient from '../api';

const props = defineProps({
    queueId: {
        type: Number,
        required: true
    }
})
const emit = defineEmits(['next','back', 'cancel'])

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
            const res = await apiClient.get(`/queue/${props.queueId}/get/`)
            queue.value = res.data
            loading.value = false
            return // success

        } catch (err) {
            if (attempt === maxAttempts) {
                error.value = 'Failed to load queue. Please try again.'
                loading.value = false
                return
            }
            await delay(400 + attempt*100) // wait before retry
        }
    }

    loading.value = false
}

const confirm = () => {
    emit('next', { queueId: props.queueId })
}

const formattedCreatedAt = computed(() => {
    if (!queue.value?.created_at) {
        return ''
    }

    try {
        return new Date(queue.value.created_at).toLocaleTimeString()
    } catch {
        return ''
    }
})

async function refreshSnapshot() {
    if (loading.value) {
        return
    }
    loading.value = true
    error.value = null
    const oldId = props.queueId

    try {
        // 1) create a fresh snapshot
        const createRes = await apiClient.post('/export_queue/', {
            name: 'Dummy',
            image_url: 'Dummy',
            description: 'Dummy'
        })
        const newId = createRes.data.queue_id

        // 2) tell Wizard about the new ID
        emit('next', { queueId: newId })

        // 3) best effort delete the old snapshot
        if (oldId && oldId !== newId) {
            try {
                await apiClient.delete(`/queue/${oldId}/delete/`)
            } catch (e) {
                if (e?.response?.status !== 404) {
                    console.warn('Failed to delete old snapshot after refresh', e)
                }
            }
        }
    } catch (err) {
        error.value = 'Could not refresh queue. Please ensure something is playing!'
    } finally {
        loading.value = false
    }
}

onMounted(fetchQueue)
</script>