<template>
  <section class="relative min-h-screen flex flex-col bg-primary text-white overflow-hidden">
    <!-- album covers background -->
    <AlbumBackground />

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

    <!-- center tagline + glow -->
    <div class="flex flex-col flex-1 items-center justify-center text-center z-20 px-6">
      <h1 class="text-5xl lg:text-6xl font-silkscreen leading-tight mb-3 relative">
        ¿Qué queue? <span class="block">Que queue.</span>
        <!-- gold glow behind tagline -->
        <span
          class="absolute inset-0 z-10 blur-3xl"
          :style="{ background: 'radial-gradient(circle, rgba(255,215,0,0.18), transparent 70%)' }"
        />
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

        <router-link
          to="/login"
          class="px-6 py-3 rounded-2xl border border-divider bg-[rgba(255,255,255,0.02)] hover:bg-[rgba(255,255,255,0.05)] focus:outline-none focus:ring-2 focus:ring-accentLight transition"
        >
          Que Queue Login
        </router-link>
      </div>

      <p class="text-secondaryText text-sm mt-6 font-inconsolata">
        Build your queue in Spotify and come back OR start exporting!
      </p>
    </div>
  </section>
</template>

<script setup>
import AlbumBackground from './AlbumBackground.vue';
import spotifyLogo from '../assets/Spotify_logo.svg'

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
</script>


<style scoped>
/* Tailwind covers most layout; we add a few polished rules */

.hero-logo {
  max-width: 340px;
  width: min(48vw, 340px);
  height: auto;

  /* gold glow */
  filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.5))
          drop-shadow(0 0 12px rgba(255, 215, 0, 0.4))
          drop-shadow(0 0 18px rgba(255, 215, 0, 0.3));

  transition: transform 220ms ease, filter 220ms ease;
  will-change: transform, filter;

  /* animated subtle pulse using CSS variable for accent */
  animation: logo-pulse 4s ease-in-out infinite;
}


/* subtle scale pulse + glow */
@keyframes logo-pulse {
  0% { transform: translateY(0) scale(1); filter: drop-shadow(0 6px 18px rgba(0,0,0,0.7)); }
  50% { transform: translateY(-3px) scale(1.02); filter: drop-shadow(0 18px 44px rgba(255,215,0,0.12)); }
  100% { transform: translateY(0) scale(1); filter: drop-shadow(0 6px 18px rgba(0,0,0,0.7)); }
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
