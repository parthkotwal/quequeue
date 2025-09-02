import { defineStore } from "pinia";
import apiClient from "../api";

export const useSessionStore = defineStore('session', {
    state: () => ({
        user: null, 
        isLoggedIn: false,
        isLoading: false,
        hasInitialized: false
    }),
    
    getters: {
        userName: (state) => state.user?.display_name || state.user?.name || 'User'
    },
    
    actions: {
        setUser(userObj) {
            this.user = userObj
            this.isLoggedIn = true
        },
        
        clearSession() {
            this.user = null
            this.isLoggedIn = false
        },
        
        async initializeAuth() {
            if (this.hasInitialized) return;
            
            this.isLoading = true
            try {
                const response = await apiClient.get('/api/verify_auth/')
                
                if (response.ok) {
                    const data = await response.json()
                    if (data.authenticated) {
                        this.setUser({
                            display_name: data.user_display_name,
                        })
                    } else {
                        this.clearSession()
                    }
                } else {
                    this.clearSession()
                }
            } catch (error) {
                console.error('Auth verification failed:', error)
                this.clearSession()
            } finally {
                this.isLoading = false
                this.hasInitialized = true
            }
        }
    },
    
    persist: true
})