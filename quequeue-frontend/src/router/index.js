import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AuthCallback from '../views/AuthCallback.vue'
import Dashboard from '../views/Dashboard.vue'
import QueueDetail from '../views/QueueDetail.vue'
import ExportWizard from '../views/ExportWizard.vue'
import Landing from '../views/Landing.vue'
import PrivacyPolicy from '../views/PrivacyPolicy.vue'
import Terms from '../views/Terms.vue'
import PageNotFound from '../views/PageNotFound.vue'

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
    },
    {
        path: '/privacy',
        component: PrivacyPolicy
    },
    {
        path: '/terms',
        component: Terms
    },

    // MUST BE LAST ONE
    {
        path: '/:pathMatch(.*)*',
        name: 'PageNotFound',
        component: PageNotFound
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;