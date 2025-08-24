<template>
  <div class="relative border divider rounded-xl shadow-md hover:shadow-lg cursor-pointer transition p-4 flex flex-col items-center text-center bg-primary text-white" @click="$emit('click')">
    <!-- Three-dot menu -->
    <button 
      @click.stop="toggleMenu" 
      class="absolute top-2 right-2 text-secondaryText hover:text-accent focus:outline-none"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <circle cx="4" cy="10" r="2" />
        <circle cx="10" cy="10" r="2" />
        <circle cx="16" cy="10" r="2" />
      </svg>
    </button>

    <!-- Dropdown menu -->
    <div 
      v-if="menuOpen" 
      class="absolute top-8 right-2 bg-primary border divider rounded shadow-md py-1 w-36 z-10"
    >
      <button class="w-full text-left px-3 py-2 text-secondaryText hover:text-accent hover:bg-divider rounded" @click="editQueue">Edit</button>
      <button class="w-full text-left px-3 py-2 text-secondaryText hover:text-accent hover:bg-divider rounded" @click="deleteQueue">Delete</button>
    </div>

    <img 
      :src="queue.image_url" 
      alt="Cover" 
      class="h-32 w-32 object-cover rounded-md mb-3"
    />
    <h2 class="text-lg font-orbitron mb-1">{{ queue.name }}</h2>
    <p class="text-secondaryText text-sm">{{ queue.description }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  queue: Object
})

const menuOpen = ref(false);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function editQueue() {
  alert(`Edit queue: ${queue.name}`);
  menuOpen.value = false;
}

function deleteQueue() {
  alert(`Delete queue: ${queue.name}`);
  menuOpen.value = false;
}
</script>
