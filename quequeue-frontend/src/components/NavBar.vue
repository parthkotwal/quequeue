<template>
  <div class="fixed top-0 left-0 right-0 z-50 bg-primary px-4 sm:px-8 py-4 flex justify-between items-center shadow-md">
    <!-- H1 top-left -->
    <router-link to="/" class="">
      <img src="../assets/qq_logos/qq_nobg.svg" class="h-12 w-auto"></img>
    </router-link>

    <!-- <div class="absolute top-6 left-8 z-20">
      <router-link to="/" class="flex items-center space-x-2 hover:opacity-80 transition">
        <img src="../assets/qq_logos/qq_nobg.svg" class="h-12 w-auto"></img>
      </router-link>
    </div> -->

    <!-- Hamburger button top-right -->
    <div class="relative">
      <button
        @click="toggleMenu"
        class="p-2 bg-primary text-accent rounded-md shadow-md focus:outline-none"
        aria-label="Menu"
        :aria-expanded="isOpen.toString()"
      >
        <svg
          v-if="!isOpen"
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Fly-in menu -->
      <transition name="slide-left">
        <div
          v-if="isOpen"
          class="absolute z-50 bg-primary rounded-md shadow-lg px-4 py-2 flex sm:flex-row flex-col items-center
                 sm:top-0 sm:right-full sm:mr-2 sm:space-x-6 sm:space-y-0 space-y-2 top-full right-0 w-max"
        >
          <RouterLink
            to="/dashboard"
            class="text-white font-inconsolata hover:text-accent transition whitespace-nowrap"
            @click="toggleMenu"
            tabindex="0"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/export"
            class="text-white font-inconsolata hover:text-accent transition whitespace-nowrap"
            @click="toggleMenu"
            tabindex="0"
          >
            Export
          </RouterLink>
          <a
            href="https://open.spotify.com/"
            target="_blank"
            class="text-white font-inconsolata hover:text-accent transition whitespace-nowrap"
            @click="toggleMenu"
            tabindex="0"
          >
            Spotify
          </a>
          <RouterLink
            to="/"
            class="text-white font-inconsolata hover:text-accent transition whitespace-nowrap"
            @click.prevent="handleLogout"
          >
            Logout
          </RouterLink>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../stores/session";

const isOpen = ref(false);
const router = useRouter();
const session = useSessionStore();

function toggleMenu() {
  isOpen.value = !isOpen.value;
}

async function handleLogout() {
  await session.logout();
  router.push("/login");   // send user to login page
  isOpen.value = false;    // close dropdown
}
</script>

<style scoped>
/* Slide-left animation for menu */
.slide-left-enter-from {
  transform: translateX(20px);
  opacity: 0;
}
.slide-left-enter-to {
  transform: translateX(0);
  opacity: 1;
}
.slide-left-enter-active {
  transition: all 0.25s ease-out;
}

.slide-left-leave-from {
  transform: translateX(0);
  opacity: 1;
}
.slide-left-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
.slide-left-leave-active {
  transition: all 0.25s ease-in;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  /* Menu becomes vertical and spaced nicely */
  .flex.flex-col {
    flex-direction: column;
    align-items: flex-start;
  }
  .space-y-2 > :not(:last-child) {
    margin-bottom: 0.5rem;
  }
}
</style>
