<template>
  <div>
    <!-- Top bar with hamburger -->
    <header
      class="flex items-center justify-between px-4 py-3 bg-primary text-white shadow-md"
    >
      <h1 class="text-xl font-silkscreen text-accent">Que Queue</h1>

      <!-- Hamburger button -->
      <button
        @click="toggleMenu"
        class="focus:outline-none"
        aria-label="Menu"
      >
        <svg
          v-if="!isOpen"
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 text-accent"
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
          class="h-6 w-6 text-accent"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </header>

    <!-- Side drawer -->
    <transition name="slide">
      <aside
        v-if="isOpen"
        class="fixed top-0 left-0 h-full w-64 bg-primary shadow-xl z-40 flex flex-col"
      >
        <!-- Header -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-divider">
          <h2 class="text-lg font-silkscreen text-accent">Menu</h2>
          <button @click="toggleMenu" class="focus:outline-none">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-accent"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Nav links -->
        <nav class="flex-1 px-4 py-6 space-y-4">
          <RouterLink
            to="/dashboard"
            class="block text-white hover:text-accent font-inconsolata transition"
            @click="toggleMenu"
          >
            Dashboard
          </RouterLink>

          <RouterLink
            to="/export"
            class="block text-white hover:text-accent font-inconsolata transition"
            @click="toggleMenu"
          >
            Export Queue
          </RouterLink>

          <a
            href="https://open.spotify.com/"
            target="_blank"
            class="block text-white hover:text-accent font-inconsolata transition"
            @click="toggleMenu"
          >
            Open Spotify
          </a>
        </nav>
      </aside>
    </transition>

    <!-- Overlay -->
    <transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black bg-opacity-50 z-30"
        @click="toggleMenu"
      ></div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from "vue";

const isOpen = ref(false);

function toggleMenu() {
  isOpen.value = !isOpen.value;
}
</script>

<style scoped>
/* Slide-in animation */
.slide-enter-from {
  transform: translateX(-100%);
}
.slide-enter-active {
  transition: transform 0.3s ease;
}
.slide-enter-to {
  transform: translateX(0%);
}

.slide-leave-from {
  transform: translateX(0%);
}
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-leave-to {
  transform: translateX(-100%);
}

/* Fade overlay */
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
