<template>
    <div class="login-page min-h-screen flex flex-col justify-center items-center bg-primary text-white px-4">
        <h1 class="text-4xl font-silkscreen mb-2">Que Queue</h1>
          <p class="text-secondaryText mb-8 text-center">Save and restore your Spotify queue.</p>
          <button 
            @click="connectSpotify"
            class="bg-accent hover:bg-accentLight text-black font-silkscreen px-6 py-3 rounded-lg transition-colors duration-200"
          >
            Login with Spotify
          </button>
    </div>
</template>

<script setup>
import { browserBaseURL } from '../api';

function connectSpotify() {
  window.location.href = `${browserBaseURL}/login/`;
}
</script>

<style scoped>
</style>