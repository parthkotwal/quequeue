import { defineStore } from "pinia";

export const useSessionStore = defineStore('session', {
    state: () => ({
        user: null, 
        isLoggedIn: false,
    }),
    actions: {
        setUser(userObj) {
            this.user = userObj
            this.isLoggedIn = true
        },
        clearSession() {
            this.user = null
            this.isLoggedIn = false
        }
    },
    persist: true
})