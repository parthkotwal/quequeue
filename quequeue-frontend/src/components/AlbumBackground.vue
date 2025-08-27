<template>
  <div
    class="absolute inset-0 pointer-events-none overflow-hidden"
    style="z-index: 1;"
    aria-hidden="true"
  >
    <div 
      class="album-layer" 
      v-for="(cover, idx) in visibleCovers" 
      :key="idx"
      :style="layerStyle(idx)"
      :class="{ 'evaporating': scrollY > 100 }"
    >
      <img :src="cover" :alt="`album ${idx+1}`" class="album-img" />
    </div>
    <!-- subtle overlay to dim background -->
    <div class="absolute inset-0 bg-gradient-to-b from-transparent to-[rgba(0,0,0,0.2)]" style="z-index: 2;"></div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const modules = import.meta.glob('../assets/album_covers/*.webp', { eager: true });
const coversAll = Object.values(modules).map(m => m.default);

// Choose up to 12 covers
const visibleCovers = coversAll.slice(0, 12);

// Track scroll position
const scrollY = ref(0);

// Scroll handler
const handleScroll = () => {
  scrollY.value = window.scrollY;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true });
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

// deterministic positioning for rainfall effect
function layerStyle(i) {
  // Spread horizontally across viewport
  const left = (i * 83) % 100; // wrap around 0..99
  
  // Start above viewport for rainfall effect
  const startTop = -150 - (i * 50); // stagger start positions
  
  // Scale varies
  const scale = 0.4 + ((i % 5) * 0.15); // 0.4 to 0.85
  
  // Slight rotation
  const rotation = ((i * 19) % 30) - 15; // -15 to 15 deg
  
  // Animation timing - staggered for continuous rainfall
  const duration = 8 + (i % 4) * 3; // 8-20 seconds
  const delay = (i % 8) * -2; // staggered delays
  
  // Calculate evaporation based on scroll
  const evaporationIntensity = Math.min(scrollY.value / 300, 1); // 0 to 1
  const finalOpacity = 0.25 * (1 - evaporationIntensity * 0.7); // More visible initially
  
  return {
    left: `${left}%`,
    top: `${startTop}px`,
    transform: `translate(-50%, 0) scale(${scale}) rotate(${rotation}deg)`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`,
    zIndex: 1,
    opacity: finalOpacity,
    '--evaporate-amount': `${evaporationIntensity * 30}px`
  };
}
</script>

<style scoped>
.album-layer {
  position: absolute;
  will-change: transform, opacity;
  transform-origin: center top;
  animation-name: rainfall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.album-layer.evaporating {
  transform: translate(-50%, var(--evaporate-amount, 0px)) scale(0.8) rotate(5deg) !important;
  filter: blur(2px) !important;
}

.album-img {
  display: block;
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 2px;
}

@media (min-width: 1024px) {
  .album-img {
    border-radius: 4px;        /* like your lg:rounded-[4px] */
  }
}

.album-img {
  filter: blur(0.5px) saturate(0.95) brightness(1.1);
  box-shadow: 0 4px 20px rgba(0,0,0,0.3), 0 0 15px rgba(255, 215, 0, 0.06);
  transition: filter 0.6s ease-out;
}

/* Rainfall animation: falls from top to bottom of viewport + extra */
@keyframes rainfall {
  0% {
    transform: translate(-50%, 0) translateY(0);
    opacity: 0;
  }
  10% {
    opacity: 0.25;
  }
  90% {
    opacity: 0.25;
  }
  100% {
    transform: translate(-50%, 0) translateY(calc(100vh + 300px));
    opacity: 0;
  }
}

/* Add some subtle sway during fall */
.album-layer:nth-child(odd) {
  animation-name: rainfall-sway-left;
}

.album-layer:nth-child(even) {
  animation-name: rainfall-sway-right;
}

@keyframes rainfall-sway-left {
  0% {
    transform: translate(-50%, 0) translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.25;
  }
  25% {
    transform: translate(-50%, 0) translateY(25vh) translateX(-8px);
  }
  50% {
    transform: translate(-50%, 0) translateY(50vh) translateX(5px);
  }
  75% {
    transform: translate(-50%, 0) translateY(75vh) translateX(-3px);
  }
  90% {
    opacity: 0.25;
  }
  100% {
    transform: translate(-50%, 0) translateY(calc(100vh + 300px)) translateX(0);
    opacity: 0;
  }
}

@keyframes rainfall-sway-right {
  0% {
    transform: translate(-50%, 0) translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.25;
  }
  25% {
    transform: translate(-50%, 0) translateY(25vh) translateX(6px);
  }
  50% {
    transform: translate(-50%, 0) translateY(50vh) translateX(-4px);
  }
  75% {
    transform: translate(-50%, 0) translateY(75vh) translateX(8px);
  }
  90% {
    opacity: 0.25;
  }
  100% {
    transform: translate(-50%, 0) translateY(calc(100vh + 300px)) translateX(0);
    opacity: 0;
  }
}

/* Respects users who reduce motion */
@media (prefers-reduced-motion: reduce) {
  .album-layer {
    animation: none !important;
    transition: opacity 0.3s ease !important;
    position: static;
    opacity: 0.08 !important;
  }
  
  .album-layer.evaporating {
    opacity: 0.02 !important;
  }
}
</style>