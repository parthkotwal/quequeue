import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
import { useSessionStore } from './stores/session.js'

import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import AuthCallback from './views/AuthCallback.vue'
import Dashboard from './views/Dashboard.vue'
import QueueDetail from './views/QueueDetail.vue'

const routes = [
    { 
        path: '/login', 
        component: Login 
    },
    { 
        path: '/callback', 
        component: AuthCallback 
    },
    { 
        path: '/dashboard', 
        component: Dashboard, 
        meta: { requiresAuth: true }
    },
    {
        path: '/queue/:id', 
        component: QueueDetail,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

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

app.mount('#app')
