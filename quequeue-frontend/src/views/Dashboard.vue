<template>
    <div class="dashboard-page min-h-screen bg-primary text-white px-6 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- Welcome Header -->
            <h1 class="text-3xl md:text-4xl font-silkscreen mb-6">
            Welcome, {{ session.user?.name || 'User' }}
            </h1>
    
            <!-- Action Buttons -->
            <div class="mb-8 flex flex-wrap gap-4">
                <button 
                    @click="fetchQueues" 
                    class="bg-accent hover:bg-accentLight text-black font-silkscreen px-5 py-2 rounded-lg transition-colors duration-200"
                >
                    Refresh Queues
                </button>
                <button 
                    @click="goToExport" 
                    class="bg-accent hover:bg-accentLight text-black font-silkscreen px-5 py-2 rounded-lg transition-colors duration-200"
                >
                    Export Queue
                </button>
            </div>
    
            <!-- Loading / Empty State -->
            <div class="text-secondaryText mb-6" v-if="loading">
                Loading queues...
            </div>
            <div class="text-secondaryText mb-6" v-else-if="queues && queues.length === 0">
                No queues yet. Try exporting one.
            </div>
    
            <!-- Queue Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6" v-else>
                <QueueCard 
                    v-for="queue in queues"
                    :key="queue.id"
                    :queue="queue"
                    @deleted="removeQueue"
                />

            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../api';
import { useSessionStore } from '../stores/session';
import { useRouter } from 'vue-router';
import QueueCard from '../components/QueueCard.vue';

const session = useSessionStore()
const router = useRouter()

const queues = ref([])
const loading = ref(true)

const fetchQueues = async () => {
    loading.value = true
    try {
        const res = await apiClient.get('/my_queues/')
        console.log('Queues response:', res.data)
        queues.value = res.data.queues
    } catch(err) {
        console.error("Failed to fetch queues:", err)
    } finally {
        loading.value = false
    }
}

const goToQueue = (id) => {
    router.push('/queue/' + id)
}

const goToExport = () => {
    router.push('/export')
}

const removeQueue = (id) => {
  queues.value = queues.value.filter(q => q.id !== id)
}

onMounted(fetchQueues)
</script>