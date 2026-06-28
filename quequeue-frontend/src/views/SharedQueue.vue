<template>
    <NavBar />
    <div class="bg-primary text-white px-6 py-8 pt-20 min-h-screen">
        <div class="max-w-4xl mx-auto">
            <!-- Loading -->
            <div v-if="loading" class="text-secondaryText">Loading shared queue...</div>

            <!-- Not Found -->
            <div v-else-if="error" class="text-center py-20">
                <h1 class="text-3xl font-silkscreen text-accent mb-4">Queue Not Found</h1>
                <p class="text-secondaryText mb-8">This shared link may have expired or been removed by the owner.</p>
                <router-link to="/" class="bg-accent hover:bg-accentLight text-black px-6 py-3 rounded font-silkscreen transition-colors duration-200">
                    Go Home
                </router-link>
            </div>

            <!-- Queue Content -->
            <div v-else>
                <!-- Header -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 items-start mb-8">
                    <img :src="queue.image_url" class="w-full h-full object-cover rounded shadow-md" alt="Queue Cover" />

                    <div class="sm:col-span-2 flex flex-col justify-between">
                        <div>
                            <p class="text-secondaryText text-sm mb-1 font-silkscreen">Shared Queue</p>
                            <h1 class="text-3xl font-silkscreen mb-2 truncate">{{ queue.name }}</h1>
                            <p class="text-secondaryText text-sm mb-1">by {{ queue.owner }}</p>
                        </div>

                        <div class="relative group max-w-lg mt-2">
                            <p class="text-secondaryText text-sm sm:text-base line-clamp-3 overflow-hidden">
                                {{ queue.description }}
                            </p>
                        </div>

                        <div class="flex items-center text-xs text-secondaryText/80 mt-3">
                            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                            </svg>
                            <span>{{ queue.track_count }} tracks</span>
                        </div>

                        <!-- Clone Button -->
                        <div class="mt-4">
                            <button
                                v-if="sessionStore.isLoggedIn"
                                @click="cloneQueue"
                                :disabled="cloning"
                                class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen flex items-center gap-2 transition-colors duration-200"
                            >
                                <svg v-if="cloning" class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                                </svg>
                                <span>{{ cloning ? 'Cloning...' : 'Clone to My Account' }}</span>
                            </button>
                            <router-link
                                v-else-if="!sessionStore.isLoggedIn"
                                to="/login"
                                class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen inline-block transition-colors duration-200"
                            >
                                Log in to Clone
                            </router-link>
                        </div>
                    </div>
                </div>

                <!-- Tracks (read-only, no menu) -->
                <div v-if="queue.tracks.length">
                    <h2 class="text-xl font-silkscreen mb-2">Tracks</h2>
                    <div class="space-y-2">
                        <div
                            v-for="(track, index) in queue.tracks"
                            :key="track.track_uri + index"
                            class="flex items-center gap-4 py-3 px-4 bg-divider rounded-xl shadow-sm"
                        >
                            <div class="w-6 text-right text-secondaryText font-medium">{{ index + 1 }}</div>
                            <img :src="track.album_image_url" alt="Album Art" class="w-12 h-12 object-cover rounded-[2px] lg:rounded-[4px] shadow-sm flex-shrink-0" />
                            <div class="flex-1 min-w-0">
                                <p class="text-base font-silkscreen text-white truncate">{{ track.track_name }}</p>
                                <p class="text-sm text-secondaryText truncate">{{ track.artist_name }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <MainFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../api'
import { useSessionStore } from '../stores/session'
import { notificationStore } from '../stores/notification'
import NavBar from '../components/NavBar.vue'
import MainFooter from '../components/MainFooter.vue'

const route = useRoute()
const router = useRouter()
const sessionStore = useSessionStore()

const token = route.params.token
const queue = ref(null)
const loading = ref(true)
const error = ref(false)
const cloning = ref(false)

const fetchSharedQueue = async () => {
    try {
        const res = await apiClient.get(`/shared/${token}/`)
        queue.value = res.data
    } catch {
        error.value = true
    } finally {
        loading.value = false
    }
}

const cloneQueue = async () => {
    cloning.value = true
    try {
        const res = await apiClient.post(`/shared/${token}/clone/`)
        notificationStore.success('Queue Cloned', `"${queue.value.name}" has been added to your queues.`)
        router.push(`/queue/${res.data.queue_id}`)
    } catch (err) {
        const msg = err.response?.data?.error || 'Failed to clone queue'
        notificationStore.error('Clone Failed', msg)
    } finally {
        cloning.value = false
    }
}

onMounted(async () => {
    await sessionStore.initializeAuth()
    await fetchSharedQueue()
})
</script>
