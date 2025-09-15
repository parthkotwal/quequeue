import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
import { initSpotifyPlayer } from './stores/player'
import { useSessionStore } from './stores/session'

import router from './router'
import './style.css'
import apiClient from './api'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(pinia)
app.use(router)

router.beforeEach((to, from, next) => {
    console.log("Navigating to:", to.path)
    next()
})

router.afterEach((to) => {
    console.log("Navigated to:", to.path)
})

const sessionStore = useSessionStore(pinia)

// Helper function to initialize Spotify player if authenticated
async function setupSpotifyPlayer() {
    if (!sessionStore.isLoggedIn) {
        console.log("User not logged in, skipping player init")
        return
    }

    if (!window.Spotify) {
        console.warn("Spotify SDK not loaded yet")
        return
    }

    try {
        const res = await apiClient.get('/get_token/')
        const { access_token } = await res.json()
        if (!access_token) throw new Error("No access token returned from backend")

        await initSpotifyPlayer(access_token)
        console.log("Spotify player initialized")
    } catch (err) {
        console.error("Failed to initialize Spotify player:", err)
    }
}

// 1️. Define SDK ready callback BEFORE loading the script
window.onSpotifyWebPlaybackSDKReady = () => {
    console.log("Spotify SDK ready")
    setupSpotifyPlayer()
}

// 2️. Load the Spotify Web Playback SDK
if (!document.getElementById('spotify-sdk')) {
    const script = document.createElement('script')
    script.id = 'spotify-sdk'
    script.src = 'https://sdk.scdn.co/spotify-player.js'
    script.async = true
    document.body.appendChild(script)
}

// 3️. Initialize session, then mount app
sessionStore.initializeAuth().then(async () => {
    app.mount('#app')

    // If SDK already loaded, init player immediately
    if (window.Spotify && sessionStore.isLoggedIn) {
        await setupSpotifyPlayer()
    }
})