import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
import { useSessionStore } from './stores/session'

import router from './router'
import './style.css'

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

// Only load SDK, don't init player here
// Player will be initialized in AuthCallback after successful login
// or in a dedicated component when needed

// 1. Define SDK ready callback (empty - just logs)
window.onSpotifyWebPlaybackSDKReady = () => {
    console.log("Spotify SDK loaded and ready")
    // Don't auto-init player here anymore
    // Let AuthCallback or user action trigger it
}

// 2. Load the Spotify Web Playback SDK
if (!document.getElementById('spotify-sdk')) {
    const script = document.createElement('script')
    script.id = 'spotify-sdk'
    script.src = 'https://sdk.scdn.co/spotify-player.js'
    script.async = true
    document.body.appendChild(script)
}

// 3. Initialize session, then mount app
sessionStore.initializeAuth().then(() => {
    app.mount('#app')
    
    // If user is already logged in and on a page that needs player,
    // that page component should handle player initialization
    if (sessionStore.isLoggedIn) {
        console.log("User is logged in, player can be initialized when needed")
    }
})