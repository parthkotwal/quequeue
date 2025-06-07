<template>
    <div class="login-page">
        <h1>Que Queue</h1>
        <p>Save and restore your Spotify queue.</p>
        <button @click="connectSpotify">
            Login with Spotify
        </button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
function connectSpotify() {
    window.location.href = import.meta.env.VITE_API_URL + '/login'
}
</script>

<style scoped>
.login-page {
  max-width: 320px;
  margin: 4rem auto;
  text-align: center;
}
button {
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}
</style>