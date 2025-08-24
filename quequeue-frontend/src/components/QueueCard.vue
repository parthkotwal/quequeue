<template>
  <div 
    class="relative border divider rounded-xl shadow-md hover:shadow-lg transition p-4 flex flex-col items-center text-center bg-primary text-white"
  >
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
      <button 
        class="w-full text-left px-3 py-2 text-secondaryText hover:text-accent hover:bg-divider rounded" 
        @click.stop="restoreQueue"
      >
        Restore
      </button>
      <button 
        class="w-full text-left px-3 py-2 text-secondaryText hover:text-accent hover:bg-divider rounded" 
        @click.stop="openDeleteModal"
      >
        Delete
      </button>
    </div>

    <!-- Clickable section: Cover + Title -->
    <div class="cursor-pointer" @click="goToQueue">
      <img 
        :src="queue.image_url" 
        alt="Cover" 
        class="h-32 w-32 object-cover rounded-md mb-3"
      />
      <h2 class="text-lg font-silkscreen mb-1">{{ queue.name }}</h2>
    </div>

    <!-- Non-clickable description -->
    <p class="text-secondaryText text-sm">{{ queue.description }}</p>

    <!-- Delete Modal -->
    <div 
      v-if="showDeleteModal" 
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      @click.stop
    >
      <div class="bg-primary p-6 rounded w-full max-w-md text-white" @click.stop>
        <h3 class="text-xl font-silkscreen mb-4 text-red-600">Confirm Delete</h3>
        <p class="mb-4 text-red-600">Are you sure you want to permanently delete this queue?</p>
        <div class="flex justify-end space-x-2">
          <button @click.stop="showDeleteModal = false" class="px-4 py-2 rounded border border-divider">
            Cancel
          </button>
          <button @click.stop="confirmDeleteQueue" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded font-silkscreen transition-colors duration-200">
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api'

const props = defineProps({
  queue: Object
})

const emit = defineEmits(['deleted'])

const router = useRouter()
const menuOpen = ref(false)
const showDeleteModal = ref(false)
const restoring = ref(false)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function goToQueue() {
  router.push(`/queue/${props.queue.id}`)
}

async function restoreQueue() {
  restoring.value = true
  try {
    const res = await apiClient.get(`/queue/${props.queue.id}/restore/`)
    alert(res.data.message)
  } catch(err) {
    alert("Restore failed: " + (err.response?.data?.error || err.message))
  } finally {
    restoring.value = false
    menuOpen.value = false
  }
}

function openDeleteModal() {
  showDeleteModal.value = true
  menuOpen.value = false
}

async function confirmDeleteQueue() {
  try {
    await apiClient.delete(`/queue/${props.queue.id}/delete/`)
    alert("Queue deleted")
    emit('deleted', props.queue.id) // notify Dashboard
  } catch(err) {
    alert("Delete failed: " + (err.response?.data?.error || err.message))
  }
  showDeleteModal.value = false
}
</script>
