<template>
  <footer class="backdrop-blur  rounded-t-xl shadow-lg mt-auto">
    <div class="max-w-6xl mx-auto px-6 py-4">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-[#B3B3B3] text-sm">
          © 2025 QueQueue. Not affiliated with Spotify.
        </p>
        <div class="flex items-center gap-6">
          <router-link
            to="/privacy"
            class="text-[#B3B3B3] hover:text-[#FFD700] text-sm transition"
          >
            Privacy
          </router-link>
          <router-link
            to="/terms"
            class="text-[#B3B3B3] hover:text-[#FFD700] text-sm transition"
          >
            Terms
          </router-link>
          <a
            href="https://github.com/parthkotwal/quequeue"
            target="_blank"
            class="text-[#B3B3B3] hover:text-[#FFD700] text-sm transition"
          >
            Project GitHub!
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>