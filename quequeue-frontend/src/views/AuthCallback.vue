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
    const res = await apiClient.get(`/verify_auth/`);
    const { authenticated, user_display_name } = res.data;

    if (!authenticated) {
      router.push('/login');
      return;
    }

    session.setUser({ name: user_display_name });

    // 2. Get token
    const tokenRes = await apiClient.get(`/get_token/`);
    const { access_token } = tokenRes.data;

    // 3. Init Spotify Web Playback SDK
    await initSpotifyPlayer(access_token);

    // 4. Navigate to dashboard
    router.push('/dashboard');
  } catch (err) {
    console.error("Failed to authenticate with Spotify:", err);
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