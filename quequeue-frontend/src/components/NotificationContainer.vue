<template>
  <div class="fixed top-4 right-4 z-50 space-y-3 max-w-sm w-full">
    <TransitionGroup
      name="notification"
      tag="div"
      class="space-y-3"
    >
      <div
        v-for="notification in notificationStore.notifications"
        :key="notification.id"
        :class="notificationClasses(notification.type)"
        class="relative p-4 rounded-xl shadow-lg border backdrop-blur-sm transform transition-all duration-300"
      >
        <!-- Icon -->
        <div class="flex items-start gap-3">
          <div :class="iconClasses(notification.type)" class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center">
            <component :is="getIcon(notification.type)" class="w-4 h-4" />
          </div>
          
          <!-- Content -->
          <div class="flex-1 min-w-0">
            <h4 v-if="notification.title" class="font-silkscreen text-sm text-white mb-1">
              {{ notification.title }}
            </h4>
            <p class="text-sm text-secondaryText leading-relaxed">
              {{ notification.message }}
            </p>
          </div>
          
          <!-- Close button -->
          <button
            @click="notificationStore.removeNotification(notification.id)"
            class="flex-shrink-0 text-secondaryText hover:text-white transition-colors duration-200"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Progress bar for timed notifications -->
        <div
          v-if="notification.duration > 0"
          class="absolute bottom-0 left-0 h-1 bg-accent rounded-b-xl notification-progress"
          :style="{ animationDuration: notification.duration + 'ms' }"
        ></div>
      </div>
    </TransitionGroup>
  </div>
</template>


<script setup>
import { notificationStore } from '../stores/notification'

const notificationClasses = (type) => {
  const base = 'bg-primary/90 border-divider'
  const variants = {
    success: 'border-l-4 border-l-spotifyGreen',
    error: 'border-l-4 border-l-red-500',
    warning: 'border-l-4 border-l-accent',
    info: 'border-l-4 border-l-blue-500'
  }
  return `${base} ${variants[type] || variants.info}`
}

const iconClasses = (type) => {
  const variants = {
    success: 'bg-spotifyGreen/20 text-spotifyGreen',
    error: 'bg-red-500/20 text-red-400',
    warning: 'bg-accent/20 text-accent',
    info: 'bg-blue-500/20 text-blue-400'
  }
  return variants[type] || variants.info
}

const getIcon = (type) => {
  const icons = {
    success: () => 'CheckIcon',
    error: () => 'ExclamationIcon',
    warning: () => 'ExclamationTriangleIcon',
    info: () => 'InformationCircleIcon'
  }
  return icons[type] || icons.info
}

// Icon components (you can replace with your preferred icon library)
const CheckIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`
}

const ExclamationIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
}

const ExclamationTriangleIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>`
}

const InformationCircleIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
}
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-progress {
  animation: shrink linear forwards;
}

@keyframes shrink {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}
</style>