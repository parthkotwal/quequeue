<!-- Use queueId from ExportPreview -->
<!-- Form fields: -->
<!-- Queue name (required) -->
<!-- Queue description (optional) -->
<!-- Cover image upload - POST /api/upload_queue_image, requires queue_id and image and returns image_url ideally -->
<!-- Export button which - PATCH /api/queues/:id and updates name, description, image_url -->
<!-- Handle success -> emit done -->
<!-- Back button -> emit back -->

<template>
    <div class="space-y-6">
      <h2 class="text-2xl font-silkscreen mb-4">Queue Details</h2>
      <form @submit.prevent="submitForm" class="space-y-4">
        <!-- Queue Name -->
        <div>
          <label class="block font-silkscreen text-secondaryText mb-1">Queue Name *</label>
          <input 
            class="border divider px-3 py-2 rounded w-full bg-primary text-white focus:outline-none focus:ring-2 focus:ring-accent" 
            v-model="name" 
            type="text" 
            required
          >
        </div>
  
        <!-- Queue Description -->
        <div>
          <label class="block font-silkscreen text-secondaryText mb-1">Queue Description</label>
          <textarea 
            v-model="description" 
            rows="3" 
            class="border divider px-3 py-2 rounded w-full bg-primary text-white focus:outline-none focus:ring-2 focus:ring-accent"
          ></textarea>
        </div>
  
        <!-- Cover Image -->
        <div>
          <label class="block font-silkscreen text-secondaryText mb-1">Cover Image *</label>

          <!-- Dropzone container -->
          <div
            class="relative flex flex-col items-center justify-center border-2 border-dashed border-divider rounded-2xl p-6 cursor-pointer hover:border-accent transition"
            @click="triggerFileInput"
            @keydown.enter.prevent="triggerFileInput"
            @dragover.prevent
            @dragenter.prevent
            @drop.prevent="handleDrop"
            tabindex="0"
            role="button"
            aria-label="Upload cover image"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFile"
            />

            <!-- Preview state -->
            <div v-if="previewURL" class="relative">
              <img
                :src="previewURL"
                alt="Cover Preview"
                class="w-40 h-40 object-cover rounded-xl shadow-md"
              />
              <button
                type="button"
                @click.stop="removeCover"
                class="absolute -top-3 -right-3 bg-accent text-black rounded-full w-7 h-7 flex items-center justify-center shadow hover:bg-accentLight"
                aria-label="Remove image"
              >
                ✕
              </button>
            </div>

            <!-- Empty state -->
            <div v-else class="text-center text-secondaryText">
              <svg
                class="mx-auto h-10 w-10 text-secondaryText"
                xmlns="http://www.w3.org/2000/svg"
                fill="none" viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M7 16V4m0 0L3 8m4-4l4 4m6 0h2a2 2 0 012 2v12a2 2 0 
                    01-2 2H7a2 2 0 01-2-2v-2" />
              </svg>
              <p class="mt-2 text-sm">Click or drag an image here to upload</p>
            </div>
          </div>
        </div>


  
        <!-- Error Message -->
        <div v-if="error" class="text-red-600">
          {{ error }}
        </div>
  
        <!-- Navigation Buttons -->
        <div class="flex justify-between mt-6">
          <button 
            type="button" 
            class="bg-divider text-secondaryText px-4 py-2 rounded font-silkscreen hover:bg-accentLight transition-colors duration-200" 
            @click="onBack" 
            :disabled="submitting"
          >
            Back
          </button>
  
          <button 
            type="submit" 
            class="bg-accent hover:bg-accentLight text-black px-6 py-2 rounded font-silkscreen transition-colors duration-200" 
            :disabled="submitting || !name"
          >
            Export
          </button>
        </div>
      </form>
    </div>
</template>
  

<script setup>
import { ref, onBeforeUnmount } from 'vue';
import apiClient from '../api';

const props = defineProps({
  queueId: {
    type: Number,
    required: true
  }
})
const emit = defineEmits(['done', 'back'])

const name = ref('')
const description = ref('')
const imageURL = ref('')
const previewURL = ref('')
const error = ref(null)
const submitting = ref(false)

let objectURLToRevoke = null
const fileInput = ref(null)
let uploadTimeout = null   // store debounce timer

const onBack = () => {
  emit('back')
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const removeCover = () => {
  previewURL.value = null
  imageURL.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Handle drag & drop
const handleDrop = (event) => {
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    processFile(file)
  }
}

// Handle normal file input
const handleFile = (event) => {
  const file = event.target.files?.[0]

  // Cancel = do nothing
  if (!file) {
    event.target.value = fileInput.value?.value || ''
    return
  }

  processFile(file)
}

// Core file logic
const processFile = (file) => {
  error.value = null

  // Revoke old preview URL
  if (objectURLToRevoke) {
    URL.revokeObjectURL(objectURLToRevoke)
  }
  objectURLToRevoke = URL.createObjectURL(file)
  previewURL.value = objectURLToRevoke

  // Debounce upload
  if (uploadTimeout) {
    clearTimeout(uploadTimeout)
  }
  uploadTimeout = setTimeout(() => {
    uploadFile(file)
  }, 500)
}

// Actual upload
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('queue_id', props.queueId)
  formData.append('image', file)

  try {
    const { data } = await apiClient.post('/upload_image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
    imageURL.value = data.image_url
  } catch (err) {
    error.value = 'Failed to upload image. Try again later.'
  }
}

const submitForm = async () => {
  error.value = null
  submitting.value = true

  if (!name.value) {
    error.value = 'Queue name is required.'
    submitting.value = false
    return 
  }

  try {
    await apiClient.patch(`/queue/${props.queueId}/update/`, {
      name: name.value,
      description: description.value,
      image_url: imageURL.value
    })        
    emit('done')
  } catch (err) {
    error.value = 'Failed to export queue.'
  } finally {
    submitting.value = false
  }
}

onBeforeUnmount(() => {
  if (objectURLToRevoke) {
    URL.revokeObjectURL(objectURLToRevoke)
  }
  if (uploadTimeout) {
    clearTimeout(uploadTimeout)
  }
})


</script>