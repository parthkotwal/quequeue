<template>
    <div class="space-y-6">
      <h2 class="text-2xl font-silkscreen mb-2">Export Your Current Spotify Queue</h2>
      <p class="text-secondaryText mb-4">
        We'll grab and save the currently playing track and the next songs in your queue.
      </p>
  
      <div class="bg-divider p-4 rounded">
        <p class="mb-2 text-secondaryText">
          For this to work, Spotify requires a playback device to be active. If nothing is playing, click below to nudge it:
        </p>
        <button 
          @click="tryPlayback" 
          class="bg-accent hover:bg-accentLight text-black px-4 py-2 rounded font-silkscreen transition-colors duration-200" 
          :disabled="loading"
        >
          ▶ Play for 1s
        </button>
        <p v-if="playbackError" class="text-red-600 mt-2">{{ playbackError }}</p>
      </div>
  
      <div class="mt-4">
        <button 
          @click="startExport" 
          class="bg-accent hover:bg-accentLight text-black px-6 py-3 rounded font-silkscreen transition-colors duration-200" 
          :disabled="loading"
        >
          {{ loading ? 'Working…' : 'Continue to Preview' }}
        </button>
        <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
      </div>
    </div>
  </template>
  

<script setup>
import { ref } from 'vue';
import apiClient from '../api';


const emit = defineEmits(['next']);
const loading = ref(false);
const playbackError = ref(null);
const error = ref(null);


const tryPlayback = async () => {
    playbackError.value = null;
    try {
        await apiClient.post('/play_track/', null);
        setTimeout(() => {
            apiClient.post('/pause_track/', null)
        }, 1000);
    } catch (err) {
        playbackError.value = "Playback failed. Please open Spotify on your desired device and press play on the current track.";
    }
}

const startExport = async () => {
    loading.value = true;
    error.value = null;
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    try {
        const res = await apiClient.post("/export_queue/", {
            name: "Dummy",
            image_url: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/queue_covers/default.jpeg",
            description: "Dummy"
        })
        await delay(200)
        emit('next', {
            queueId: res.data.queue_id
        })
    } catch (err) {
        error.value = "Could not export queue. Please ensure something is playing!"
  } finally {
    loading.value = false
  }
}

</script>