<template>
  <div 
    class="group relative border border-divider rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-0 flex flex-col bg-primary text-white overflow-hidden hover:border-accent/30"
  >
    <!-- Subtle gradient overlay -->
    <div class="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    
    <!-- Three-dot menu -->
    <button 
      @click.stop="toggleMenu" 
      class="absolute top-3 right-3 text-secondaryText hover:text-accent focus:outline-none z-20 p-1 rounded-full hover:bg-divider/50 transition-all duration-200"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <circle cx="4" cy="10" r="2" />
        <circle cx="10" cy="10" r="2" />
        <circle cx="16" cy="10" r="2" />
      </svg>
    </button>

    <!-- Dropdown menu with improved styling -->
    <div 
      v-if="menuOpen" 
      class="absolute top-12 right-3 bg-primary border border-divider rounded-lg shadow-xl py-2 w-36 z-30 backdrop-blur-sm"
    >
      <button 
        class="w-full text-left px-4 py-2 text-secondaryText hover:text-accent hover:bg-divider/50 transition-all duration-200 flex items-center space-x-2" 
        @click.stop="restoreQueue"
        :disabled="restoring"
      >
        <svg v-if="!restoring" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <div v-else class="w-4 h-4 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
        <span>{{ restoring ? 'Restoring...' : 'Restore' }}</span>
      </button>
      <button 
        class="w-full text-left px-4 py-2 text-secondaryText hover:text-red-400 hover:bg-red-400/10 transition-all duration-200 flex items-center space-x-2" 
        @click.stop="openDeleteModal"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        <span>Delete</span>
      </button>
    </div>

    <!-- Clickable section: Cover + Title -->
    <div class="cursor-pointer p-6 pb-4 flex flex-col items-center" @click="goToQueue">
      <!-- Cover image with enhanced styling -->
      <div class="relative mb-4 group-hover:scale-[1.02] transition-transform duration-300">
        <img 
          :src="queue.image_url" 
          alt="Cover" 
          class="h-36 w-36 object-cover rounded-lg shadow-lg"
        />
        <!-- Subtle overlay on hover -->
        <div class="absolute inset-0 bg-black/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
          <svg class="w-8 h-8 text-accent opacity-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </div>
      </div>
      
      <h2 class="text-xl font-silkscreen mb-2 text-center leading-tight group-hover:text-accent transition-colors duration-300">
        {{ queue.name }}
      </h2>
    </div>

    <!-- Description and metadata -->
    <div class="px-6 pb-6 flex-grow">
      <p class="text-secondaryText text-sm mb-3 line-clamp-2 leading-relaxed">
        {{ queue.description || '' }}
      </p>
      
      <!-- Created date with icon -->
      <div class="flex items-center text-xs text-secondaryText/80 mt-auto">
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ formatDate(queue.created_at) }}</span>
      </div>
    </div>

    <!-- Delete Modal with improved styling -->
    <div 
      v-if="showDeleteModal" 
      class="fixed inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm z-50 p-4"
      @click.stop="showDeleteModal = false"
    >
      <div class="bg-primary border border-divider p-8 rounded-xl w-full max-w-md text-white shadow-2xl" @click.stop>
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mr-4">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-silkscreen mb-1 text-red-400">Confirm Delete</h3>
            <p class="text-secondaryText text-sm">This action cannot be undone</p>
          </div>
        </div>
        
        <p class="mb-6 text-secondaryText">
          Are you sure you want to permanently delete <strong class="text-white">"{{ queue.name }}"</strong>?
        </p>
        
        <div class="flex justify-end space-x-3">
          <button 
            @click.stop="showDeleteModal = false" 
            class="px-6 py-2 rounded-lg border border-divider hover:bg-divider/30 transition-colors duration-200 font-medium"
          >
            Cancel
          </button>
          <button 
            @click.stop="confirmDeleteQueue" 
            class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-silkscreen transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            Delete Queue
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
    emit('deleted', props.queue.id)
  } catch(err) {
    alert("Delete failed: " + (err.response?.data?.error || err.message))
  }
  showDeleteModal.value = false
}

function formatDate(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  
  // Calculate difference in hours first for more accurate recent time handling
  const diffTime = Math.abs(now - date)
  const diffHours = diffTime / (1000 * 60 * 60)
  const diffDays = diffTime / (1000 * 60 * 60 * 24)
  
  // If less than 1 hour, show "Just now"
  if (diffHours < 1) return 'Just now'
  
  if (diffHours < 24 && Math.floor(diffHours) == 1) return `${Math.floor(diffHours)} hour ago`

  // If less than 24 hours, show "X hours ago"
  if (diffHours < 24) return `${Math.floor(diffHours)} hours ago`
  
  // If less than 48 hours and it was actually yesterday in local time, show "Yesterday"
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) return 'Yesterday'
  
  // For other recent dates, show days
  if (diffDays < 7) return `${Math.floor(diffDays)} days ago`
  if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`
  
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
}

// Close dropdown when clicking outside
document.addEventListener('click', () => {
  menuOpen.value = false
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>