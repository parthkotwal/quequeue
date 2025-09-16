<template>
  <div class="auth-callback">
      <p>Logging you in with Spotify...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import apiClient from '../api';
import { useSessionStore } from '../stores/session';
import { initSpotifyPlayer, playerState } from '../stores/player';

const router = useRouter();
const session = useSessionStore();
const route = useRoute();

onMounted(async () => {
try {
  // 1. Verify auth
  const res = await apiClient.get('/verify_auth/');
  
  const data = res.data;
  
  if (!data.authenticated) {
    console.error("User not authenticated");
    router.push('/login');
    return;
  }

  // 2. IMPORTANT: Set user in session store FIRST
  session.setUser({ 
    display_name: data.user_display_name 
  });

  // 3. Get fresh token for player
  const tokenRes = await apiClient.get('/get_token/');
  
  const tokenData = tokenRes.data;
  const { access_token } = tokenData;

  if (!access_token) {
    console.error("No access token received");
    router.push('/login');
    return;
  }

  // 4. Check if player already initialized (from main.js)
  if (!playerState.ready) {
    // Only init if not already ready
    console.log("Initializing Spotify player...");
    
    // Wait for SDK if not loaded yet
    if (!window.Spotify) {
      await new Promise((resolve) => {
        const checkInterval = setInterval(() => {
          if (window.Spotify) {
            clearInterval(checkInterval);
            resolve();
          }
        }, 100);
      });
    }

    await initSpotifyPlayer(access_token);
  } else {
    console.log("Player already initialized");
  }

  // 5. Successfully authenticated and player ready
  console.log("Authentication complete, navigating to dashboard");
  router.push('/dashboard');

} catch (err) {
  console.error("Error during authentication:", err);
  router.push('/login');
}
});
</script>

<style scoped>
.auth-callback {
  text-align: center;
  padding: 3rem;
}
</style>