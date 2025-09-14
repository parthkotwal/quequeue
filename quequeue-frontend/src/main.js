import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
import { useSessionStore } from './stores/session.js'

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
sessionStore.initializeAuth().then(() => {
    app.mount('#app')
})

if (!document.getElementById('spotify-sdk')) {
    const script = document.createElement('script')
    script.id = 'spotify-sdk'
    script.src = 'https://sdk.scdn.co/spotify-player.js'
    script.async = true
    document.body.appendChild(script)
  }