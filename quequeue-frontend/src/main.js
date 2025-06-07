import { createApp } from 'vue'
import App from './App.vue'

import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'

const routes = [
    { path: '/login', component: Login },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

import './style.css'

createApp(App)
    .use(router)
    .mount('#app')
