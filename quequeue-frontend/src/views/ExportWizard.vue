<template>
    <div class="max-w-3xl mx-auto p-6">
        <component 
            :is="currentComponent"
            :queue-id="queueId"
            :queue-data="queueData"
            @next="handleNext"
            @back="handleBack"
            @update-queue-data="(data) => (queueData = data)"
            @cancel="resetWizard"
            @done="handleDone"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// Children Components
import ExportIntro from './ExportIntro.vue'
import ExportPreview from './ExportPreview.vue';
import ExportDetails from './ExportDetails.vue';
import { useRouter } from 'vue-router';
import apiClient from '../api';

const step = ref(0);
const queueId = ref(null);
const queueData = ref(null);
const router = useRouter()
const unblock = ref(null)
const finishing = ref(false)

const steps = [
    ExportIntro,
    ExportPreview,
    ExportDetails
];

const currentComponent = computed(() => steps[step.value]);


function handleNext(payload = {}) {
    const prevStep = step.value
    if (payload.queueId) {
        queueId.value = payload.queueId;
    }

    if (payload.queueData) {
        queueData.value = payload.queueData;
    }
    
    step.value++
    persistWizard()
}

function handleBack() {
    if (step.value > 0) {
        step.value--
        
        if (step.value === 0) {
            queueId.value = null
            queueData.value = null
            persistWizard()
        } else {
            persistWizard()
        }
    }
}

async function handleCancel(payload = {}) {
    const id = payload.queueId ?? queueId.value
    if (id) {
        try {
            await apiClient.delete(`/queue/${id}/delete/`)
        } catch (err) {
            const status = err?.response?.status
            if (status !== 404) {
                console.warn('Failed to delete queue on cancel', err)
            }
        }
    }
    resetWizard()
}

function handleDone() {
    finishing.value = true
    clearPersistedWizard()
    router.push('/dashboard')
}


function resetWizard() {
    step.value = 0;
    queueId.value = null
    queueData.value = null
    clearPersistedWizard()
}

const STORAGE_KEY = 'qq_export_wizard'

function persistWizard() {
    const payload = { step: step.value, queueId: queueId.value }
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
}

function restoreWizard() {
    try {
        const raw = sessionStorage.getItem(STORAGE_KEY)
        if (!raw) {
            return
        }
        
        const { step: s, queueId: q } = JSON.parse(raw)
        if (Number.isInteger(s) && s >= 0 && s < steps.length) {
            step.value = s
        }
        if (q) {
            queueId.value = q
        }
    } catch { }
}

function clearPersistedWizard() {
    sessionStorage.removeItem(STORAGE_KEY)
}

onMounted(() => {
    restoreWizard()

    unblock.value = router.beforeEach((to, from, next) => {
        if (!finishing.value && queueId.value && step.value > 0 && to.path !== from.path) {
            const ok = confirm('Leave export? Your current snapshot will be discarded.')
            if (ok) {
                handleCancel({ queueId: queueId.value }).then(() => next())
            } else {
                next(false)
            }
            return

        } 
        
        next()
    })

})

onBeforeUnmount(() => {
    if (unblock.value) {
        unblock.value()
    }
})

</script>