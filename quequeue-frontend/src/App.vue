<template>
  <div class="min-h-screen bg-primary text-white">
    <!-- Add top padding equal to header height -->
    <div>
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
</style>
