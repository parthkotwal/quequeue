import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AuthCallback from '../views/AuthCallback.vue'
import Dashboard from '../views/Dashboard.vue'
import QueueDetail from '../views/QueueDetail.vue'
import ExportWizard from '../views/ExportWizard.vue'
import Landing from '../views/Landing.vue'

const routes = [
    {
        path: '/', 
        component: Landing
    },
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
    },
    {
        path: '/export',
        component: ExportWizard,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;