<template>
  <main class="relative bg-primary text-white min-h-screen overflow-x-hidden">
    <!-- Hero section with rainfall background -->
    <Hero />

    <!-- Spacer to allow scrolling to see evaporation effect -->
    <div class="h-[150vh] bg-primary"></div>
  </main>
</template>

<script setup>
import Hero from '../components/Hero.vue';
</script>
