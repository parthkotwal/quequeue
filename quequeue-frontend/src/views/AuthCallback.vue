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

const router = useRouter();
const session = useSessionStore();

const route = useRoute()
const code = route.query.code

onMounted(async () => { // async arrow function
    try {
        const res = await apiClient.get(`/verify_auth/`)
        const { authenticated, user_display_name } = res.data;

        if (authenticated) {
            session.setUser({ name: user_display_name });
            router.push('/dashboard');
        } else {
            router.push('/login');
        }

    } catch (err) {
        console.error("Failed to authenticate with Spotify:", err)
        router.push('/login')
    }
});
</script>

<style scoped>
.auth-callback {
    text-align: center;
    padding: 3rem;
}
</style>