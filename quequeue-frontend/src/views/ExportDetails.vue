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
          <input type="file" @change="handleFile" accept="image/*" class="text-secondaryText">
          <div v-if="imageURL" class="mt-2">
            <img :src="imageURL" alt="Cover Preview" class="w-40 h-40 object-cover rounded shadow">
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

const onBack = () => {
    emit('back')
}

const handleFile = async (event) => {
    error.value = null
    const file = event.target.files?.[0]
    if (!file) {
        return
    }

    if (objectURLToRevoke) {
        URL.revokeObjectURL(objectURLToRevoke)
    }
    objectURLToRevoke = URL.createObjectURL(file)
    previewURL.value = objectURLToRevoke

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
        // console.log(err)
    }
}

const submitForm = async() => {
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
})

</script>