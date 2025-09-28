<template>
  <div class="space-y-2">
    <div
      v-for="(track, index) in localTracks"
      :key="track.id"
      class="flex items-center gap-4 py-3 px-4 bg-divider rounded-xl shadow-sm hover:shadow-md transition relative"
    >
      <!-- Position Number -->
      <div class="w-6 text-right text-secondaryText font-medium">
        {{ index + 1 }}
      </div>

      <!-- Album Cover -->
      <img
        :src="track.album_image_url"
        alt="Album Art"
        class="w-12 h-12 object-cover rounded-[2px] lg:rounded-[4px] shadow-sm flex-shrink-0"
      />

      <!-- Track Info -->
      <div class="flex-1 min-w-0">
        <p class="text-base font-silkscreen text-white truncate">
          {{ track.track_name }}
        </p>
        <p class="text-sm text-secondaryText truncate">
          {{ track.artist_name }}
        </p>
      </div>

      <!-- Three Dot Menu -->
      <div class="relative">
        <button
          @click.stop="toggleMenu(track.id)"
          class="text-secondaryText hover:text-accent transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <circle cx="4" cy="10" r="2" />
            <circle cx="10" cy="10" r="2" />
            <circle cx="16" cy="10" r="2" />
          </svg>
        </button>

        <!-- Dropdown -->
        <div
          v-if="openMenu === track.id"
          class="absolute right-0 mt-2 w-32 bg-primary border divider rounded-md shadow-lg z-10"
        >
          <button
            @click="openRemoveModal(track)"
            class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-divider rounded"
          >
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Remove Track Confirmation Modal -->
    <ConfirmModal
      :is-open="showRemoveModal"
      type="warning"
      title="Remove Track"
      subtitle="Remove from this queue"
      :message="`Are you sure you want to remove <strong class='text-white'>&quot;${selectedTrack?.track_name}&quot;</strong> by ${selectedTrack?.artist_name} from this queue?`"
      confirm-text="Remove Track"
      cancel-text="Cancel"
      loading-text="Removing..."
      :loading="removing"
      @confirm="confirmRemoveTrack"
      @cancel="cancelRemove"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import apiClient from '../api'
import { notificationStore } from '../stores/notification'
import ConfirmModal from '../components/ConfirmModal.vue'

const props = defineProps({
  tracks: {
    type: Array,
    required: true
  },
  queueId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['trackRemoved'])

const openMenu = ref(null)
const showRemoveModal = ref(false)
const selectedTrack = ref(null)
const removing = ref(false)

// Local copy of tracks
const localTracks = ref([...props.tracks])
watch(
  () => props.tracks,
  (newTracks) => {
    localTracks.value = [...newTracks]
  }
)

const toggleMenu = (id) => {
  openMenu.value = openMenu.value === id ? null : id
}

const openRemoveModal = (track) => {
  selectedTrack.value = track
  showRemoveModal.value = true
  openMenu.value = null
}

const cancelRemove = () => {
  showRemoveModal.value = false
  selectedTrack.value = null
}

const confirmRemoveTrack = async () => {
  if (!selectedTrack.value) return

  removing.value = true
  try {
    await apiClient.delete(`/queue/${props.queueId}/remove_track/${selectedTrack.value.id}/`)

    // Update local tracks
    localTracks.value = localTracks.value.filter(t => t.id !== selectedTrack.value.id)

    // Emit to parent
    emit('trackRemoved', {
      removedId: selectedTrack.value.id,
      remainingTracks: localTracks.value
    })

    // Notify
    notificationStore.success(
      'Track Removed',
      `"${selectedTrack.value.track_name}" has been removed from the queue.`
    )

    // Close modal
    showRemoveModal.value = false
    selectedTrack.value = null
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred'
    notificationStore.error(
      'Remove Failed',
      `Failed to remove track: ${errorMessage}`
    )
  } finally {
    removing.value = false
  }
}

// Handle outside click
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    openMenu.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
