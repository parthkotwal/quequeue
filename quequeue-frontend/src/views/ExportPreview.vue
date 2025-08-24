<!-- Use queueId from ExportIntro -->
<!-- Fetch exported queue details from GET /api/queues/:id (id = queueId) -->
<!-- Show track using TrackList -->
<!-- Have confirm/continue button -->
<!-- Also have no/back button, which could call DELETE /api/queues/:id -->

<template>
    <div class="space-y-6">
      <h2 class="text-2xl font-silkscreen mb-2">Preview Your Queue</h2>
  
      <div v-if="loading" class="text-secondaryText">Loading your queue...</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
  
      <div v-if="queue && !loading">
        <p class="mb-4 text-secondaryText">
          Here's the current Spotify queue we detected.
        </p>
  
        <TrackList :tracks="queue.tracks" :queueId="props.queueId" @trackRemoved="handleTrackRemoved"/>
  
        <!-- Snapshot Info + Refresh -->
        <div class="flex items-center justify-between mt-4">
          <div v-if="queue">
            <span class="text-sm text-secondaryText">
              Snapshot taken at {{ formattedCreatedAt }}
            </span>
          </div>
  
          <button
            class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen transition-colors duration-200"
            @click="refreshSnapshot"
            :disabled="loading"
          >
            Refresh from Spotify
          </button>
        </div>
  
        <!-- Navigation Buttons -->
        <div class="flex justify-between mt-6">
          <button
            class="bg-divider text-secondaryText px-4 py-2 rounded font-silkscreen hover:bg-accentLight transition-colors duration-200"
            @click="emit('cancel', { queueId: props.queueId })"
            :disabled="loading"
          >
            Back
          </button>
      
          <button
            class="bg-accent hover:bg-accentLight text-black px-6 py-2 rounded font-silkscreen transition-colors duration-200"
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
            image_url: 'https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/queue_covers/default.jpeg',
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

const handleTrackRemoved = ({ removedId, remainingTracks }) => {
    queue.value.tracks = remainingTracks
}


onMounted(fetchQueue)
</script>