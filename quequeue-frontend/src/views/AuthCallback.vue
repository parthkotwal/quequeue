<template>
    <div class="auth-callback">
        <p>Processing login...</p>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { useSessionStore } from '@/stores/session';

const router = useRouter();
const session = useSessionStore();

onMounted(async () => { // async arrow function
    try {
        const apiURL = import.meta.env.VITE_API_URL + '/list_user_queues'
        const res = await axios.get(apiURL, {
            withCredentials: true, // needed for Django to use session cookies
        })

        if (res.status === 200) {
            // Store user login state
            session.setUser({ name: res.data.queues[0]?.user_display_name || "User" })
            router.push('/dashboard')
        } else {
            router.push('/login')
        }
    } catch (err) {
        console.error("Auth failed:", err)
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