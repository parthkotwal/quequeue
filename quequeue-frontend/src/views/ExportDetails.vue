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
        <h2 class="text-2xl font-bold">Queue Details</h2>
        <form @submit.prevent="submitForm">
            <div>
                <label class="block font-semibold">Queue Name *</label>
                <input class="border px-3 py-2 rounded w-full" v-model="name" type="text" required>
            </div>

            <div>
                <label class="block font-semibold">Queue Description</label>
                <textarea v-model="description" rows="3" class="border px-3 py-2 rounded w-full"></textarea>
            </div>

            <div>
                <label class="block font-semibold">Cover Image</label>
                <input type="file" @change="handleFile" accept="image/*">
                <div v-if="imageURL" class="mt-2">
                    <img :src="imageURL" alt="Cover Preview" class="w-40 h-40 object-cover rounded shadow">
                </div>
            </div>

            <div v-if="error" class="text-red-600">
                {{ error }}
            </div>

            <div class="flex justify-between mt-6">
                <button type="button" class="bg-gray-400 text-white px-4 py-2 rounded">
                    Back
                </button>

                <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded" :disabled="submitting">
                    Export
                </button>
            </div>

        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
    queueId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['done', 'back'])

const name = ref('')
const description = ref('')
const imageFile = ref(null)
const imageURL = ref('')
const error = ref(null)
const submitting = ref(false)


const handleFile = async (event) => {
    const file = event.target.files[0]
    if (!file) {
        return
    }

    const formData = new FormData()
    formData.append('queue_id', props.queueId)
    formData.append('image', file)

    try {
        const res = await axios.post('/api/upload_queue_image/', formData, {
            withCredentials: true,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    } catch (err) {
        error.value = 'Failed to upload image. Try again later.'
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
        await axios.patch('/api/queues/'+ props.queueId + '/update/', {
            name: name.value,
            description: description.value,
            image_url: imageURL.value
        }, {
            withCredentials: true
        })
        
        emit('done')

    } catch (err) {
        error.value = 'Failed to export queue.'
    } finally {
        submitting.value = False
    }
}

</script>