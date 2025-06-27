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
        />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Children Components
import ExportIntro from './ExportIntro.vue'
import ExportPreview from './ExportPreview.vue';
import ExportDetails from './ExportDetails.vue';

const step = ref(0);
const queueId = ref(null);
const queueData = ref(null);

const steps = [
    ExportIntro,
    ExportPreview,
    ExportDetails
];

const currentComponent = computed(() => steps[step.value]);

function handleNext(payload = {}) {
    if (payload.queueId) {
        queueId.value = payload.queueId;
    }

    if (payload.queueData) {
        queueData.value = payload.queueData;
    }
    step.value++;
}

function handleBack() {
    if (step.value > 0) {
        step.value--;
    }
}

function resetWizard() {
    step.value = 0;
    queueId.value = null
    queueData.value = null
}

</script>