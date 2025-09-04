<template>
    <NavBar />
    <div class="queue-detail-page min-h-screen bg-primary text-white px-6 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- Loading State -->
            <div v-if="loading" class="text-secondaryText">Loading queue...</div>
    
            <div v-else>
            <!-- Top Bar: Back + Actions -->
            <div class="flex justify-between items-center mb-6 flex-wrap gap-2">
                <button 
                @click="router.push('/dashboard')" 
                class="bg-divider text-white px-3 py-1 rounded hover:bg-accentLight transition-colors font-silkscreen"
                >
                ← Back
                </button>
    
                <div class="flex flex-wrap gap-2">
                <button 
                    :disabled="!suggestAvailable || loadingSuggestions" 
                    @click="openSuggestModal" 
                    :class="suggestAvailable ? 'bg-accent hover:bg-accentLight' : 'bg-divider cursor-not-allowed'" 
                    class="px-4 py-2 rounded text-black font-silkscreen transition-colors duration-200"
                >
                    Suggest
                </button>
                
                <button 
                    @click="showEditModal = true" 
                    class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen transition-colors duration-200"
                >
                    Edit
                </button>
                
                <button 
                    @click="deleteQueue" 
                    class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded font-silkscreen transition-colors duration-200"
                >
                    Delete
                </button>
                </div>
            </div>
    
            <!-- Header Content: Image + Info -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 items-start mb-8">
                <img :src="queue.image_url" class="w-full h-full object-cover rounded shadow-md" alt="Queue Cover" />
    
                <div class="sm:col-span-2 flex flex-col justify-between">
                <h1 class="text-3xl font-silkscreen mb-2 truncate">{{ queue.name }}</h1>
    
                <div class="relative group max-w-lg">
                    <p class="text-secondaryText text-sm sm:text-base line-clamp-3 overflow-hidden">
                    {{ queue.description }}
                    </p>
                </div>
                </div>
    
                <!-- Restore Button -->
                <div class="mt-4 sm:mt-0">
                <button 
                    @click="restoreQueue" 
                    :disabled="restoring" 
                    class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded w-full sm:w-auto font-silkscreen flex items-center justify-center gap-2 transition-colors duration-200"
                >
                    <svg v-if="restoring" class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                    </svg>
                    <span>{{ restoring ? 'Restoring...' : 'Restore to Spotify' }}</span>
                </button>
                </div>
            </div>
    
            <!-- Tracks -->
            <div v-if="queue.tracks.length">
                <h2 class="text-xl font-silkscreen mb-2">Tracks</h2>
                <TrackList :tracks="queue.tracks" :queue-id="queue.id" @trackRemoved="handleTrackRemoved"/>
            </div>
            </div>
    
            <!-- Modals -->
            <!-- Edit Modal -->
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-primary p-6 rounded w-full max-w-md text-white">
                <h3 class="text-xl font-silkscreen mb-4">Edit Queue</h3>
                <label class="block mb-2 text-secondaryText">
                Name
                <input v-model="editForm.name" class="w-full border divider px-2 py-1 rounded bg-primary text-white" />
                </label>
                <label class="block mb-4 text-secondaryText">
                Description
                <textarea v-model="editForm.description" class="w-full border divider px-2 py-1 rounded bg-primary text-white"></textarea>
                </label>
                <div class="flex justify-end space-x-2">
                    <button @click="showEditModal = false" class="px-4 py-2 rounded border border-divider">Cancel</button>
                    <button @click="updateQueue" class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen transition-colors duration-200">Save</button>
                </div>
            </div>
            </div>
    
            <!-- Delete Modal -->
            <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-primary p-6 rounded w-full max-w-md text-white">
                <h3 class="text-xl font-silkscreen mb-4 text-red-600">Confirm Delete</h3>
                <p class="mb-4 text-red-600">Are you sure you want to permanently delete this queue?</p>
                <div class="flex justify-end space-x-2">
                <button @click="showDeleteModal = false" class="px-4 py-2 rounded border border-divider">Cancel</button>
                <button @click="confirmDeleteQueue" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded font-silkscreen transition-colors duration-200">Delete</button>
                </div>
            </div>
            </div>
    
            <!-- Suggest Modal -->
            <div v-if="showSuggestModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-primary p-6 rounded w-full max-w-md text-white">
                <h3 class="text-xl font-silkscreen mb-4">Suggested Tracks</h3>
                <div v-if="loadingSuggestions" class="text-secondaryText">Loading suggestions...</div>
                <div v-else>
                <div v-if="suggestions.length === 0" class="text-secondaryText">No suggestions available</div>
                <div v-for="track in suggestions" :key="track.track_uri" class="flex justify-between items-center mb-2">
                    <div class="flex items-center space-x-2">
                    <img :src="track.album_image_url" class="w-12 h-12 object-cover rounded" />
                    <div>
                        <p class="font-silkscreen">{{ track.track_name }}</p>
                        <p class="text-secondaryText text-sm">{{ track.artist_name }}</p>
                    </div>
                    </div>
                    <button v-if="!queueTrackUris.has(track.track_uri)" @click="addSuggestedTrack(track)" class="bg-accent hover:bg-accentLight text-black px-3 py-1 rounded font-silkscreen transition-colors duration-200">Add</button>
                    <span v-else class="bg-divider text-secondaryText px-3 py-1 rounded cursor-not-allowed">Added</span>
                </div>
                </div>
                <div class="flex justify-end mt-4">
                    <button @click="showSuggestModal = false" class="px-4 py-2 border border-divider rounded font-silkscreen">Close</button>
                </div>
            </div>
            </div>
    
        </div>
    </div>
</template>
  

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TrackList from '../components/TrackList.vue';
import apiClient from '../api';
import NavBar from '../components/NavBar.vue';

const route = useRoute()
const router = useRouter()
const queueId = route.params.id

const queue = ref(null)
const loading = ref(true)
const restoring = ref(false)
const error = ref(null)
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const suggestAvailable = ref(false);
const showSuggestModal = ref(false);
const suggestions = ref([]);
const loadingSuggestions = ref(false);

const queueTrackUris = computed(() =>
    new Set(queue.value?.tracks.map(t => t.track_uri) || [])
);

const editForm = ref({
    name: '',
    description: ''
})

const fetchQueue = async () => {
    loading.value = true
    try {
        const res = await apiClient.get(`/queue/${queueId}/get/`)
        queue.value = res.data
        editForm.value.name = queue.value.name
        editForm.value.description = queue.value.description
    } catch (err) {
        console.error("Error loading queue:", err)
    } finally {
        loading.value = false
    }
}

const restoreQueue = async () => {
    restoring.value = true
    try {
        const res = await apiClient.get(`/queue/${queueId}/restore/`)
        alert(res.data.message)
    } catch(err) {
        alert("Restore failed: " + err.response?.data?.error || err.message)
    } finally {
        restoring.value = false
    }
}

const updateQueue = async () => {
    try {
        await apiClient.patch(`/queue/${queueId}/update/`, {
        name: editForm.value.name,
        description: editForm.value.description
        })
        alert("Queue updated successfully")
        showEditModal.value = false
        fetchQueue()
    } catch(err) {
        alert("Update failed: " + err.response?.data?.error || err.message)
    }
}

// Show delete modal
const deleteQueue = () => {
    showDeleteModal.value = true
}

// Confirm delete action
const confirmDeleteQueue = async () => {
    try {
        await apiClient.delete(`/queue/${queueId}/delete/`)
        alert("Queue deleted")
        router.push('/dashboard')
    } catch(err) {
        alert("Delete failed: " + err.response?.data?.error || err.message)
    }
    showDeleteModal.value = false
}


const checkSuggestions = async () => {
    try {
        const res = await apiClient.get(`/queue/${queueId}/suggest_available/`);
        suggestAvailable.value = res.data.available;
    } catch(err) {
        console.error(err);
    }
}

const openSuggestModal = async () => {
    showSuggestModal.value = true;
    loadingSuggestions.value = true;
    try {
        const res = await apiClient.get(`/queue/${queueId}/suggest/`);
        suggestions.value = res.data.suggestions;
    } catch(err) {
        console.error(err);
        suggestions.value = [];
    } finally {
        loadingSuggestions.value = false;
    }
}

const addSuggestedTrack = async (track) => {
    try {
        const res = await apiClient.post(`/queue/${queueId}/add_track/`, {
            track_uri: track.track_uri,
            track_name: track.track_name,
            artist_name: track.artist_name,
            album_image_url: track.album_image_url
        });

        // Map to TrackList format
        const newTrack = res.data.track;
        queue.value.tracks.push(newTrack);

        suggestions.value = suggestions.value.filter(s => s.track_uri !== track.track_uri);

        alert(`${track.track_name} added!`);
    } catch(err) {
        alert("Failed to add track: " + err.response?.data?.error || err.message);
    }
};

const handleTrackRemoved = async () => {
    await fetchQueue()
}


onMounted(fetchQueue);
onMounted(checkSuggestions);

</script>
