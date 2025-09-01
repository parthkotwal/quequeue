<template>
  <section class="relative min-h-screen flex flex-col bg-primary text-white overflow-hidden">
    <!-- album covers background -->
    <AlbumBackground class="pointer-events-none"/>

    <!-- top (logo and acct) -->
    <div>
      <!-- top-left logo -->
      <div class="absolute top-6 left-8 z-20">
        <img
          v-if="chosenLogo"
          :src="chosenLogo"
          :alt="logoAlt"
          class="h-12 w-auto select-none"
        />
        <div v-else class="text-2xl font-silkscreen text-accent">Que Queue</div>
      </div>

      <!-- top-right account icon + status -->
      <div class="absolute top-6 right-8 z-30 flex items-center gap-3">
        <!-- account icon -->
        <button
          @click="handleAccountClick"
          class="w-10 h-10 flex items-center justify-center rounded-full bg-[rgba(255,255,255,0.1)] hover:bg-[rgba(255,255,255,0.2)] transition cursor-pointer" 
          :title="isLoggedIn ? 'Go to Dashboard' : 'Login to your account'"
        >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="white" d="M12 2.5a5.5 5.5 0 0 1 3.096 10.047 9.005 9.005 0 0 1 5.9 8.181.75.75 0 1 1-1.499.044 7.5 7.5 0 0 0-14.993 0 .75.75 0 0 1-1.5-.045 9.005 9.005 0 0 1 5.9-8.18A5.5 5.5 0 0 1 12 2.5ZM8 8a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z"></path></svg>
        </button>

        <!-- conditional user state -->
        <div v-if="isLoggedIn" class="flex items-center gap-2">
          <span class="font-inconsolata text-sm text-secondaryText">Hi, {{ user.name }}</span>
        </div>

        <div v-else class="flex items-center gap-2">
          <span class="font-inconsolata text-sm text-secondaryText">Guest</span>
          <router-link
            to="/login"
            class="px-4 py-2 rounded-xl border border-divider bg-[rgba(255,255,255,0.02)] hover:bg-[rgba(255,255,255,0.05)] focus:outline-none focus:ring-2 focus:ring-accentLight transition"
          >
            Login
          </router-link>
        </div>
      </div>
    </div>

    <!-- center tagline + glow -->
    <div class="flex flex-col flex-1 items-center justify-center text-center z-20 px-6">
      <h1 class="text-5xl lg:text-6xl font-silkscreen leading-tight mb-3 relative">
        ¿Qué queue? <span class="block text-accent">Que queue.</span>
        <!-- gold glow behind tagline -->
        <span
          class="absolute inset-0 z-10 blur-3xl glow-bg"
          :style="{ background: 'radial-gradient(circle, rgba(255,215,0,0.18), transparent 70%)' }"
        ></span>
      </h1>
      <p class="text-secondaryText text-lg mb-8 font-inconsolata">
        (which queue? that queue)
      </p>

      <!-- CTA Buttons -->
      <div class="flex items-center justify-center gap-4">
        <a
          href="https://open.spotify.com/"
          target="_blank"
          rel="noopener noreferrer"
          class="px-6 py-3 rounded-2xl bg-spotifyGreen hover:brightness-105 focus:outline-none focus:ring-2 focus:ring-spotifyGreen/40 transition inline-flex items-center gap-2"
        >
          Open
          <img :src="spotifyLogo" alt="Spotify" class="w-5 h-5" />
        </a>

        <!-- Dynamic main CTA button -->
        <router-link
          :to="isLoggedIn ? '/dashboard' : '/login'"
          class="px-6 py-3 rounded-2xl border border-divider bg-[rgba(255,255,255,0.02)] hover:bg-[rgba(255,255,255,0.05)] focus:outline-none focus:ring-2 focus:ring-accentLight transition"
        >
          {{ isLoggedIn ? 'Go to Dashboard' : 'Que Queue Login' }}
        </router-link>
      </div>

      <p class="text-secondaryText text-sm mt-6 font-inconsolata">
        {{ isLoggedIn ? 'Welcome back! Ready to manage your queues?' : 'Build your queue in Spotify and come back OR start exporting!' }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useSessionStore } from '../stores/session.js'
import { storeToRefs } from 'pinia';
import AlbumBackground from './AlbumBackground.vue';
import spotifyLogo from '../assets/Spotify_logo.svg'

const router = useRouter()
const sessionStore = useSessionStore()
const { user, isLoggedIn } = storeToRefs(sessionStore)

const logoModules = import.meta.glob('../assets/qq_logos/*.svg', { eager: true });
const logos = Object.entries(logoModules).map(([p, m]) => ({ path: p, url: m.default }));

function pickPreferredLogo(list) {
  if (!list.length) return null;
  const lowerPaths = list.map(l => ({ ...l, lp: l.path.toLowerCase() }));
  const preferKeywords = ['no', 'transparent', 'nobg'];
  for (const kw of preferKeywords) {
    const found = lowerPaths.find(l => l.lp.includes(kw));
    if (found) return found.url;
  }
  return list[0].url;
}
const chosenLogo = pickPreferredLogo(logos);
const logoAlt = 'Que Queue logo';

// Handle account icon click
const handleAccountClick = () => {
  if (isLoggedIn) {
    router.push('/dashboard')
  } else {
    router.push('/login')
  }
}
</script>


<style scoped>
/* Tailwind covers most layout; we add a few polished rules */

.hero-logo {
  max-width: 340px;
  width: min(48vw, 340px);
  height: auto;

  filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.5))
          drop-shadow(0 0 12px rgba(255, 215, 0, 0.4))
          drop-shadow(0 0 18px rgba(255, 215, 0, 0.3));

  transition: transform 220ms ease, filter 220ms ease;
  will-change: transform, filter;

  animation: logo-pulse 4s ease-in-out infinite;
}

@keyframes logo-pulse {
  0% { transform: translateY(0) scale(1); filter: drop-shadow(0 6px 18px rgba(0,0,0,0.7)); }
  50% { transform: translateY(-3px) scale(1.02); filter: drop-shadow(0 18px 44px rgba(255,215,0,0.12)); }
  100% { transform: translateY(0) scale(1); filter: drop-shadow(0 6px 18px rgba(0,0,0,0.7)); }
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.15; }
  50% { opacity: 0.3; }
}
.glow-bg {
  animation: glowPulse 6s ease-in-out infinite;
}

/* small responsiveness tweaks for desktop-first layout */
@media (max-width: 1024px) {
  .hero-logo { max-width: 280px; }
  h1 { font-size: 2.6rem; }
}

/* reduce motion */
@media (prefers-reduced-motion: reduce) {
  .hero-logo { animation: none !important; transition: none !important; }
}
</style>