<template>
  <div class="min-h-screen bg-primary text-white">
    <!-- Add top padding equal to header height -->
    <div>
      <router-view />

      <NotificationContainer />
    </div>
  </div>
</template>

<script>
import NotificationContainer from '../src/components/NotificationContainer.vue'

export default {
  name: 'App'
}
</script>

<style>
</style>
