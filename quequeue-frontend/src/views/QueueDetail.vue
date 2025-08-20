<template>
    <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading">Loading queue...</div>
    
        <div v-else>
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h1 class="text-3xl font-bold mb-2">{{ queue.name }}</h1>
                    <p class="text-gray-700 mb-2">{{ queue.description }}</p>
                </div>

                <!-- Edit & Delete Buttons -->
                <div class="space-x-2">
                    <button :disabled="!suggestAvailable || loadingSuggestions" @click="openSuggestModal" :class="suggestAvailable ? 'bg-green-500' : 'bg-gray-300 cursor-not-allowed'" class="px-4 py-2 rounded text-white">Suggest</button>
                    <span class="text-gray-500 text-sm cursor-pointer" title="Green = suggestions available">i</span>

                    <button @click="showEditModal = true" class="bg-yellow-500 text-white px-4 py-2 rounded">Edit</button>
                    <button @click="deleteQueue" class="bg-red-600 text-white px-4 py-2 rounded">Delete</button>
                </div>
            </div>

            <img :src="queue.image_url" class="w-full max-w-md mb-6" alt="Queue Cover" />

            <button @click="restoreQueue" class="bg-blue-600 text-white px-4 py-2 mb-6 rounded">Restore to Spotify</button>

            <div v-if="queue.tracks.length">
                <h2 class="text-xl font-semibold mb-2">Tracks</h2>
                <TrackList :tracks="queue.tracks"/>
            </div>
        </div>

        <!-- Edit Modal -->
        <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white p-6 rounded w-full max-w-md">
                <h3 class="text-xl font-bold mb-4">Edit Queue</h3>
                <label class="block mb-2 text-black">
                    Name
                    <input v-model="editForm.name" class="w-full border px-2 py-1 rounded" />
                </label>
                <label class="block mb-4 text-black">
                    Description
                    <textarea v-model="editForm.description" class="w-full border px-2 py-1 rounded"></textarea>
                </label>
                <div class="flex justify-end space-x-2">
                    <button @click="showEditModal = false" class="px-4 py-2 rounded border">Cancel</button>
                    <button @click="updateQueue" class="bg-green-600 text-white px-4 py-2 rounded">Save</button>
                </div>
            </div>
        </div>

        <!-- Delete Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white p-6 rounded w-full max-w-md">
                <h3 class="text-xl font-bold mb-4 text-red-600">Confirm Delete</h3>
                <p class="mb-4 text-red-600">Are you sure you want to permanently delete this queue?</p>
                <div class="flex justify-end space-x-2">
                    <button @click="showDeleteModal = false" class="px-4 py-2 rounded border">Cancel</button>
                    <button @click="confirmDeleteQueue" class="bg-red-600 text-white px-4 py-2 rounded">Delete</button>
                </div>
            </div>
        </div>

        <div v-if="showSuggestModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 text-black">
            <div class="bg-white p-6 rounded w-full max-w-md">
                <h3 class="text-xl font-bold mb-4">Suggested Tracks</h3>
                <div v-if="loadingSuggestions">Loading suggestions...</div>
                <div v-else>
                    <div v-if="suggestions.length === 0">No suggestions available</div>
                    <div v-for="track in suggestions" :key="track.track_uri" class="flex justify-between items-center mb-2">
                        <div class="flex items-center space-x-2">
                            <img :src="track.album_image_url" class="w-12 h-12 object-cover rounded" />
                            <div>
                                <p class="font-semibold">{{ track.track_name }}</p>
                                <p class="text-sm text-gray-600">{{ track.artist_name }}</p>
                            </div>
                        </div>
                        <button @click="addSuggestedTrack(track)" class="bg-blue-500 text-white px-3 py-1 rounded">Add</button>
                    </div>
                </div>
                <div class="flex justify-end mt-4">
                    <button @click="showSuggestModal = false" class="px-4 py-2 border rounded text-white">Close</button>
                </div>
            </div>
        </div>


    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TrackList from '../components/TrackList.vue';
import apiClient from '../api';

const route = useRoute()
const router = useRouter()
const queueId = route.params.id

const queue = ref(null)
const loading = ref(true)
const error = ref(null)
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const suggestAvailable = ref(false);
const showSuggestModal = ref(false);
const suggestions = ref([]);
const loadingSuggestions = ref(false);


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
    try {
        const res = await apiClient.get(`/queue/${queueId}/restore/`)
        alert(res.data.message)
    } catch(err) {
        alert("Restore failed: " + err.response?.data?.error || err.message)
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
        await apiClient.post(`/queue/${queueId}/add_track/`, {
            track_uri: track.track_uri
        });

        // Map to TrackList format
        const newTrack = {
            id: track.track_uri, // use track_uri as a temporary unique key
            track_uri: track.track_uri,
            track_name: track.track_name,
            artist_name: track.artist_name,
            album_image_url: track.album_image_url,
            position: queue.value.tracks.length // add position for display
        };

        // Add to queue tracks
        queue.value.tracks.push(newTrack);

        alert(`${track.track_name} added!`);
    } catch(err) {
        alert("Failed to add track: " + err.response?.data?.error || err.message);
    }
};



onMounted(fetchQueue);
onMounted(checkSuggestions);

</script>
