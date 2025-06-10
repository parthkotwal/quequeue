import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
const pinia = createPinia()

import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
pinia.use(piniaPluginPersistedstate)

import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import AuthCallback from './views/AuthCallback.vue'
import Dashboard from './views/Dashboard.vue'
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
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})
router.beforeEach((to, from, next) => {
    const session = useSesssionStore()

    if (to.meta.requiresAuth && !session.user) {
        next('/login')
    } else {
        next()
    }
})

import './style.css'

const app = createApp(App)
app.use(router)
app.use(pinia)
app.mount('#app')
