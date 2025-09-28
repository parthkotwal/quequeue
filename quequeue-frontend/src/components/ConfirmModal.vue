<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm z-50 p-4"
      @click.self="onCancel"
    >
      <div
        class="bg-primary border border-divider p-8 rounded-xl w-full max-w-md text-white shadow-2xl transform transition-all duration-300"
        :class="isOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
      >
        <!-- Icon and Header -->
        <div class="flex items-center mb-6">
          <div :class="iconBackgroundClass" class="w-12 h-12 rounded-full flex items-center justify-center mr-4">
            <component :is="iconComponent" class="w-6 h-6" :class="iconClass" />
          </div>
          <div>
            <h3 class="text-xl font-silkscreen mb-1" :class="titleClass">{{ title }}</h3>
            <p class="text-secondaryText text-sm">{{ subtitle }}</p>
          </div>
        </div>
        
        <!-- Custom Content Slot (for forms, etc.) -->
        <slot name="custom-content"></slot>
        
        <!-- Message (only show if no custom content) -->
        <div v-if="!$slots['custom-content']" class="mb-6 text-secondaryText" v-html="message"></div>
        
        <!-- Actions -->
        <div class="flex justify-end space-x-3">
          <button
            @click="onCancel"
            class="px-6 py-2 rounded-lg border border-divider hover:bg-divider/30 transition-colors duration-200 font-medium"
            :disabled="loading"
          >
            {{ cancelText }}
          </button>
          <button
            @click="onConfirm"
            :class="confirmButtonClass"
            class="px-6 py-2 rounded-lg font-silkscreen transition-all duration-200 shadow-lg hover:shadow-xl flex items-center gap-2"
            :disabled="loading"
          >
            <div v-if="loading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
            {{ loading ? loadingText : confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['warning', 'danger', 'info'].includes(value)
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  subtitle: {
    type: String,
    default: 'This action cannot be undone'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loadingText: {
    type: String,
    default: 'Processing...'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const onConfirm = () => {
  if (!props.loading) {
    emit('confirm')
  }
}

const onCancel = () => {
  if (!props.loading) {
    emit('cancel')
  }
}

const iconComponent = computed(() => {
  const icons = {
    warning: 'ExclamationTriangleIcon',
    danger: 'TrashIcon',
    info: 'InformationCircleIcon'
  }
  return icons[props.type] || icons.warning
})

const iconBackgroundClass = computed(() => {
  const classes = {
    warning: 'bg-accent/20',
    danger: 'bg-red-500/20',
    info: 'bg-blue-500/20'
  }
  return classes[props.type] || classes.warning
})

const iconClass = computed(() => {
  const classes = {
    warning: 'text-accent',
    danger: 'text-red-400',
    info: 'text-blue-400'
  }
  return classes[props.type] || classes.warning
})

const titleClass = computed(() => {
  const classes = {
    warning: 'text-accent',
    danger: 'text-red-400',
    info: 'text-blue-400'
  }
  return classes[props.type] || classes.warning
})

const confirmButtonClass = computed(() => {
  const classes = {
    warning: 'bg-accent hover:bg-accentLight text-black',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    info: 'bg-blue-600 hover:bg-blue-700 text-white'
  }
  return classes[props.type] || classes.warning
})

// Icon components
const ExclamationTriangleIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>`
}

const TrashIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>`
}

const InformationCircleIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
}
</script>