<template>
  <main class="relative bg-primary text-white min-h-screen overflow-x-hidden">
    <!-- Hero section with rainfall background -->
    <Hero />

    <!-- Spotify Problems Section -->
    <section ref="problemsSection" class="relative py-20 z-10 bg-gradient-to-b from-primary/90 to-primary">
      <!-- Subtle grid pattern background -->
      <div class="absolute inset-0 opacity-[0.02]" style="background-image: radial-gradient(circle at 1px 1px, rgba(255,215,0,0.3) 1px, transparent 0); background-size: 20px 20px;"></div>
      
      <!-- Problems component -->
      <SpotifyProblems ref="problemsRef" />
    </section>

    <!-- Walkthrough Section -->
    <section ref="walkthroughSection" class="relative py-20 bg-primary">
      <!-- Background gradient overlay -->
      <div class="absolute inset-0 bg-gradient-to-b from-primary via-primary/95 to-primary"></div>
      
      <!-- Floating particles background -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="floating-particles">
          <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
        </div>
      </div>

      <div class="relative z-10">
        <!-- Section header -->
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-silkscreen text-accent mb-4">
            Export. Save. Restore.
          </h2>
          <p class="text-xl text-secondaryText font-inconsolata max-w-2xl mx-auto">
            Never lose that perfect queue again. Export your current Spotify queue, save it with a custom name, and restore it anytime.
          </p>
        </div>

        <!-- Queue Preview Component -->
        <QueuePreview ref="queuePreviewRef" />
      </div>
    </section>

    <!-- ML Preview Section -->
    <section ref="mlSection" class="relative py-20 bg-gradient-to-b from-primary to-primary/90">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,215,0,0.03),transparent_50%)]"></div>
      
      <div class="relative z-10 max-w-6xl mx-auto px-6">
        <!-- ML Section Header -->
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-silkscreen text-accent mb-4">
            Need 3 tracks to close the vibe?
          </h2>
          <p class="text-xl text-secondaryText font-inconsolata">
            Our ML algorithm analyzes your queue's audio features and embeddings, and suggests perfect additions <span class="text-accent">instantly.</span>
          </p>
        </div>

        <!-- ML Preview Content -->
        <MLPreview ref="mlPreviewRef" />
      </div>
    </section>

    <!-- Final CTA Section -->
    <section class="relative py-20 bg-gradient-to-t from-primary via-primary/95 to-primary">
      <!-- Gold glow background -->
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,215,0,0.08),transparent_60%)]"></div>
      
      <div class="relative z-10 text-center max-w-4xl mx-auto px-6">
        <h2 class="text-5xl lg:text-6xl font-silkscreen leading-tight mb-6">
          ¿Qué queue? <span class="text-accent block">Que queue.</span>
        </h2>
        <p class="text-xl text-secondaryText mb-12 font-inconsolata">
          Start saving your perfect queues today
        </p>

        <!-- Final CTAs -->
        <div class="flex items-center justify-center gap-6 mb-16">
          <a
            href="https://open.spotify.com/"
            target="_blank"
            rel="noopener noreferrer"
            class="px-8 py-4 rounded-2xl bg-spotifyGreen hover:brightness-105 focus:outline-none focus:ring-2 focus:ring-spotifyGreen/40 transition inline-flex items-center gap-3 text-lg font-medium"
          >
            Open Spotify
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.84-.179-.84-.6 0-.359.24-.66.54-.78 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.242 1.021zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
          </a>

          <router-link
            to="/login"
            class="px-8 py-4 rounded-2xl border border-accent bg-accent/10 hover:bg-accent/20 focus:outline-none focus:ring-2 focus:ring-accent/40 transition text-lg font-medium text-accent"
          >
            Start Queueing
          </router-link>
        </div>

        
        <MainFooter />
        
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Hero from '../components/Hero.vue'
import QueuePreview from '../components/QueuePreview.vue'
import MLPreview from '../components/MLPreview.vue'
import MainFooter from '../components/MainFooter.vue'
import SpotifyProblems from '../components/SpotifyProblems.vue'

const walkthroughSection = ref(null)
const mlSection = ref(null)
const problemsSection = ref(null)
const problemsRef = ref(null)
const queuePreviewRef = ref(null)
const mlPreviewRef = ref(null)

let observer = null

onMounted(() => {
  // Determine appropriate root margin based on screen size
  const isMobile = window.innerHeight < 700
  const rootMargin = isMobile ? '-20px' : '-100px'
  
  // Set up Intersection Observer for scroll animations
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        console.log('Observer triggered:', entry.target.className, 'isIntersecting:', entry.isIntersecting)
        
        if (entry.isIntersecting) {
          if (entry.target === walkthroughSection.value && queuePreviewRef.value) {
            queuePreviewRef.value.setVisible(true)
          } else if (entry.target === mlSection.value && mlPreviewRef.value) {
            mlPreviewRef.value.setVisible(true)
          } else if (entry.target === problemsSection.value && problemsRef.value) {
            problemsRef.value.setVisible(true)
          }
        }
      })
    },
    { 
      threshold: 0.1, 
      rootMargin: rootMargin
    }
  )

  // Observe sections
  if (walkthroughSection.value) observer.observe(walkthroughSection.value)
  if (mlSection.value) observer.observe(mlSection.value)
  if (problemsSection.value) observer.observe(problemsSection.value)

  // Fallback for very small screens - show components after a delay
  if (window.innerHeight < 500) {
    setTimeout(() => {
      console.log('Small screen fallback triggered')
      if (problemsRef.value) {
        console.log('Showing problems component')
        problemsRef.value.setVisible(true)
      }
      if (queuePreviewRef.value) {
        console.log('Showing queue preview component')  
        queuePreviewRef.value.setVisible(true)
      }
      if (mlPreviewRef.value) {
        console.log('Showing ML preview component')
        mlPreviewRef.value.setVisible(true)
      }
    }, 1000)
  }
})


onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})

// Generate random particle positions and animations
const getParticleStyle = (index) => {
  const size = Math.random() * 3 + 1
  const left = Math.random() * 100
  const animationDelay = Math.random() * 10
  const animationDuration = Math.random() * 20 + 10
  
  return {
    left: `${left}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${animationDuration}s`
  }
}
</script>

<style scoped>
/* Floating particles animation */
.floating-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(255, 215, 0, 0.3);
  border-radius: 50%;
  animation: floatUp linear infinite;
}

@keyframes floatUp {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-10vh) rotate(360deg);
    opacity: 0;
  }
}

/* Subtle parallax effect for background elements */
@media (prefers-reduced-motion: no-preference) {
  .floating-particles {
    animation: parallaxFloat 20s ease-in-out infinite;
  }
}

@keyframes parallaxFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Reduce motion */
@media (prefers-reduced-motion: reduce) {
  .particle {
    animation: none !important;
  }
  
  .floating-particles {
    animation: none !important;
  }
}

@media (max-height: 400px) {
  section[ref="problemsSection"],
  section[ref="walkthroughSection"], 
  section[ref="mlSection"] {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
}

</style>
