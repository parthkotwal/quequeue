<template>
    <NavBar />
    <div class="queue-detail-page bg-primary text-white px-6 py-8 pt-20 min-h-screen">
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
                    @click="openDeleteModal" 
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
    
            <!-- Edit Modal -->
            <ConfirmModal
                :is-open="showEditModal"
                type="info"
                title="Edit Queue"
                subtitle="Update queue information"
                :message="editModalMessage"
                confirm-text="Save Changes"
                cancel-text="Cancel"
                loading-text="Saving..."
                :loading="updating"
                @confirm="updateQueue"
                @cancel="cancelEdit"
            >
                <template #custom-content>
                    <div class="space-y-4 mb-6">
                        <div>
                            <label class="block mb-2 text-secondaryText font-silkscreen">Name</label>
                            <input 
                                v-model="editForm.name" 
                                class="w-full border border-divider px-3 py-2 rounded bg-primary text-white focus:outline-none focus:ring-2 focus:ring-accent" 
                                placeholder="Enter queue name"
                            />
                        </div>
                        <div>
                            <label class="block mb-2 text-secondaryText font-silkscreen">Description</label>
                            <textarea 
                                v-model="editForm.description" 
                                rows="3"
                                class="w-full border border-divider px-3 py-2 rounded bg-primary text-white focus:outline-none focus:ring-2 focus:ring-accent"
                                placeholder="Enter queue description"
                            ></textarea>
                        </div>
                    </div>
                </template>
            </ConfirmModal>
    
            <!-- Delete Modal -->
            <ConfirmModal
                :is-open="showDeleteModal"
                type="danger"
                title="Delete Queue"
                subtitle="This action cannot be undone"
                :message="`Are you sure you want to permanently delete <strong class='text-white'>&quot;${queue?.name}&quot;</strong>? All tracks in this queue will be lost.`"
                confirm-text="Delete Queue"
                cancel-text="Cancel"
                loading-text="Deleting..."
                :loading="deleting"
                @confirm="confirmDeleteQueue"
                @cancel="showDeleteModal = false"
            />

            <!-- Restore Success Modal -->
            <div v-if="showRestoreSuccessModal" class="fixed inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm z-50 p-4">
                <div class="bg-primary border border-divider p-8 rounded-xl w-full max-w-md text-white shadow-2xl">
                    <div class="text-center">
                        <!-- Success Icon -->
                        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-spotifyGreen/20 mb-6">
                            <svg class="h-8 w-8 text-spotifyGreen" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-silkscreen mb-3 text-spotifyGreen">Queue Restored!</h3>
                        <p class="text-secondaryText mb-8 leading-relaxed">Your queue has been successfully added to Spotify. Check it out in your Spotify app!</p>
                        <div class="flex flex-col sm:flex-row gap-3 justify-center">
                            <button 
                                @click="openSpotifyQueue" 
                                class="bg-spotifyGreen hover:bg-green-600 text-black px-6 py-3 rounded-lg font-silkscreen transition-colors duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
                            >
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
                                </svg>
                                Open Spotify
                            </button>
                            <button 
                                @click="showRestoreSuccessModal = false" 
                                class="px-6 py-3 rounded-lg border border-divider font-silkscreen hover:bg-divider/30 transition-colors duration-200"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            </div>
    
            <!-- Suggest Modal -->
            <div v-if="showSuggestModal" class="fixed inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm z-50 p-4">
                <div class="bg-primary border border-divider p-6 rounded-xl w-full max-w-2xl text-white shadow-2xl max-h-[80vh] overflow-hidden flex flex-col">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-silkscreen text-accent">Suggested Tracks</h3>
                        <button 
                            @click="showSuggestModal = false"
                            class="text-secondaryText hover:text-white transition-colors p-1 rounded-full hover:bg-divider/50"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    
                    <div class="flex-1 overflow-y-auto">
                        <div v-if="loadingSuggestions" class="flex items-center justify-center py-12">
                            <div class="flex items-center space-x-3">
                                <div class="w-6 h-6 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
                                <span class="text-secondaryText">Finding perfect matches...</span>
                            </div>
                        </div>
                        
                        <div v-else-if="suggestions.length === 0" class="text-center py-12">
                            <svg class="w-12 h-12 text-secondaryText mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.467.901-6.062 2.375L5.5 17.5V15H4a2 2 0 01-2-2V7a2 2 0 012-2h16a2 2 0 012 2v6a2 2 0 01-2 2h-1.5v2.5l-.438-.375z" />
                            </svg>
                            <p class="text-secondaryText">No suggestions available at the moment.</p>
                        </div>
                        
                        <div v-else class="space-y-3">
                            <div 
                                v-for="track in suggestions" 
                                :key="track.track_uri" 
                                class="flex justify-between items-center p-4 bg-divider/50 rounded-lg hover:bg-divider transition-colors"
                            >
                                <div class="flex items-center space-x-3 flex-1 min-w-0">
                                    <img 
                                        :src="track.album_image_url" 
                                        class="w-12 h-12 object-cover rounded shadow-sm flex-shrink-0" 
                                        :alt="`${track.track_name} album art`"
                                    />
                                    <div class="min-w-0 flex-1">
                                        <p class="font-silkscreen text-white truncate">{{ track.track_name }}</p>
                                        <p class="text-secondaryText text-sm truncate">{{ track.artist_name }}</p>
                                    </div>
                                </div>
                                <button 
                                    v-if="!queueTrackUris.has(track.track_uri)" 
                                    @click="addSuggestedTrack(track)" 
                                    :disabled="addingTrack === track.track_uri"
                                    class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded-lg font-silkscreen transition-colors duration-200 flex items-center gap-2 flex-shrink-0 ml-3"
                                >
                                    <div v-if="addingTrack === track.track_uri" class="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                                    <span>{{ addingTrack === track.track_uri ? 'Adding...' : 'Add' }}</span>
                                </button>
                                <span v-else class="bg-divider text-secondaryText px-4 py-2 rounded-lg cursor-not-allowed flex-shrink-0 ml-3 font-silkscreen">
                                    Added
                                </span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex justify-end mt-6 pt-4 border-t border-divider">
                        <button 
                            @click="showSuggestModal = false" 
                            class="px-6 py-2 border border-divider rounded-lg font-silkscreen hover:bg-divider/30 transition-colors"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <MainFooter />
</template>
  

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TrackList from '../components/TrackList.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import apiClient from '../api';
import { ensureActiveDevice } from '../stores/player';
import { notificationStore } from '../components/NotificationStore.js';
import NavBar from '../components/NavBar.vue';
import MainFooter from '../components/MainFooter.vue';

const route = useRoute()
const router = useRouter()
const queueId = route.params.id

const queue = ref(null)
const loading = ref(true)
const restoring = ref(false)
const updating = ref(false)
const deleting = ref(false)
const addingTrack = ref(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showRestoreSuccessModal = ref(false)

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

const editModalMessage = computed(() => {
    return `Update the details for <strong class="text-white">"${queue.value?.name}"</strong>.`
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
        notificationStore.error(
            'Failed to Load Queue',
            'Unable to load queue details. Please try again.'
        )
    } finally {
        loading.value = false
    }
}

const restoreQueue = async () => {
    restoring.value = true
    try {
        // Don't force the web player — just enqueue on whatever device is active
        await ensureActiveDevice({ forceWebPlayer: false });
        const res = await apiClient.get(`/queue/${queueId}/restore/`);
        
        showRestoreSuccessModal.value = true;
        
        // Show additional info if there were failures
        if (res.data.failures && res.data.failures.length > 0) {
            notificationStore.warning(
                'Partial Restore',
                `${res.data.failures.length} tracks could not be restored. Check if they're still available.`
            )
        }
    } catch(err) {
        if (err.response?.data?.error === "NO_ACTIVE_DEVICE") {
            notificationStore.warning(
                'No Active Device',
                'Please open Spotify and start playback on your device, then try again.'
            )
        } else {
            const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred'
            notificationStore.error(
                'Restore Failed',
                `Failed to restore queue: ${errorMessage}`
            )
        }
    } finally {
        restoring.value = false
    }
}

const openSpotifyQueue = () => {
    // Try to open Spotify app first, fallback to web player
    const spotifyAppUrl = 'spotify:queue';
    const spotifyWebUrl = 'https://open.spotify.com/queue';
    
    // Create a temporary link to try opening the app
    const link = document.createElement('a');
    link.href = spotifyAppUrl;
    link.click();
    
    // Fallback to web after a short delay if app didn't open
    setTimeout(() => {
        window.open(spotifyWebUrl, '_blank');
    }, 1000);
    
    showRestoreSuccessModal.value = false;
}

const cancelEdit = () => {
    showEditModal.value = false
    // Reset form to original values
    editForm.value.name = queue.value.name
    editForm.value.description = queue.value.description
}

const updateQueue = async () => {
    updating.value = true
    try {
        await apiClient.patch(`/queue/${queueId}/update/`, {
            name: editForm.value.name,
            description: editForm.value.description
        })
        
        notificationStore.success(
            'Queue Updated',
            'Queue details have been updated successfully.'
        )
        
        showEditModal.value = false
        await fetchQueue()
    } catch(err) {
        const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred'
        notificationStore.error(
            'Update Failed',
            `Failed to update queue: ${errorMessage}`
        )
    } finally {
        updating.value = false
    }
}

const openDeleteModal = () => {
    showDeleteModal.value = true
}

const confirmDeleteQueue = async () => {
    deleting.value = true
    try {
        await apiClient.delete(`/queue/${queueId}/delete/`)
        
        notificationStore.success(
            'Queue Deleted',
            `"${queue.value.name}" has been permanently deleted.`
        )
        
        router.push('/dashboard')
    } catch(err) {
        const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred'
        notificationStore.error(
            'Delete Failed',
            `Failed to delete queue: ${errorMessage}`
        )
    } finally {
        deleting.value = false
        showDeleteModal.value = false
    }
}

const checkSuggestions = async () => {
    try {
        const res = await apiClient.get(`/queue/${queueId}/suggest_available/`);
        suggestAvailable.value = res.data.available;
    } catch(err) {
        console.error('Failed to check suggestions availability:', err);
    }
}

const openSuggestModal = async () => {
    showSuggestModal.value = true;
    loadingSuggestions.value = true;
    try {
        const res = await apiClient.get(`/queue/${queueId}/suggest/`);
        suggestions.value = res.data.suggestions;
        
        if (suggestions.value.length === 0) {
            notificationStore.info(
                'No Suggestions',
                'No new track suggestions found for this queue at the moment.'
            )
        }
    } catch(err) {
        console.error('Failed to load suggestions:', err);
        const errorMessage = err.response?.data?.error || 'Failed to load suggestions'
        notificationStore.error(
            'Suggestions Error',
            errorMessage
        )
        suggestions.value = [];
    } finally {
        loadingSuggestions.value = false;
    }
}

const addSuggestedTrack = async (track) => {
    addingTrack.value = track.track_uri
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

        // Remove from suggestions
        suggestions.value = suggestions.value.filter(s => s.track_uri !== track.track_uri);

        notificationStore.success(
            'Track Added',
            `"${track.track_name}" by ${track.artist_name} has been added to your queue.`
        )
    } catch(err) {
        const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred'
        notificationStore.error(
            'Failed to Add Track',
            `Could not add "${track.track_name}": ${errorMessage}`
        )
    } finally {
        addingTrack.value = null
    }
};

const handleTrackRemoved = async () => {
    await fetchQueue()
}

onMounted(fetchQueue);
onMounted(checkSuggestions);

</script>