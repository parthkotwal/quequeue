<template>
    <div class="p-6 max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-4">Welcome, {{ session.user?.name || 'User' }}</h1>

        <div class="mb-6 flex gap-4">
            <button @click="fetchQueues" class="bg-green-600 text-white px-4 py-2 rounded">Refresh Queues</button>
            <button @click="goToExport" class="bg-blue-600 text-white px-4 py-2 rounded">Export Current Queue</button>
        </div>

        <div v-if="loading">
            Loading queues...
        </div>

        <div v-else-if="queues && queues.length === 0">
            No queues yet. Try exporting one.
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4" v-else>
            <QueueCard 
                v-for="queue in queues"
                :key="queue.id"
                :queue="queue"
                @click="goToQueue(queue.id)"
            />
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

onMounted(fetchQueues)
</script>