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
import { browserBaseURL } from '../api';

function connectSpotify() {
  window.location.href = `${browserBaseURL}/login/`;
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