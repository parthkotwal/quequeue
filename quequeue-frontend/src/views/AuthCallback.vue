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

  // 4. Validate token has required scopes before initializing player
  console.log("Validating token scopes...");
  
  // 5. Check if player already initialized (from main.js)
  if (!playerState.ready && !playerState.player) {
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
        
        // Timeout after 10 seconds
        setTimeout(() => {
          clearInterval(checkInterval);
          resolve();
        }, 10000);
      });
    }

    if (!window.Spotify) {
      throw new Error("Spotify SDK failed to load");
    }

    try {
      await initSpotifyPlayer(access_token);
    } catch (playerError) {
      console.error("Player initialization failed:", playerError);
      
      // If it's a scope error, redirect to re-authenticate with proper scopes
      if (playerError.message.includes("Invalid token scopes") || 
          playerError.message.includes("scope")) {
        console.log("Token scope error - redirecting to login for re-authentication");
        // Clear session to force fresh login
        session.clearSession();
        router.push('/login?reauth=scope');
        return;
      }
      
      throw playerError;
    }
  } else if (playerState.player && !playerState.ready) {
    console.log("Player exists but not ready, waiting...");
    // Wait for existing player to be ready
    await new Promise((resolve) => {
      const checkReady = setInterval(() => {
        if (playerState.ready) {
          clearInterval(checkReady);
          resolve();
        }
      }, 100);
      
      // Timeout after 5 seconds
      setTimeout(() => {
        clearInterval(checkReady);
        resolve();
      }, 5000);
    });
  } else {
    console.log("Player already initialized and ready");
  }

  // 6. Successfully authenticated and player ready (or at least attempted)
  console.log("Authentication complete, navigating to dashboard");
  router.push('/dashboard');

} catch (err) {
  console.error("Error during authentication:", err);
  
  // Don't redirect to login if we're already handling a scope error
  if (!err.message.includes("scope")) {
    router.push('/login');
  }
}
});
</script>

<style scoped>
.auth-callback {
  text-align: center;
  padding: 3rem;
}
</style>