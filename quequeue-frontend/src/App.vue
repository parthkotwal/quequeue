<template>
  <div class="min-h-screen bg-primary text-white">
    <NavBar />
    <!-- Add top padding equal to header height -->
    <div class="pt-16">
      <router-view />
    </div>
  </div>
</template>
<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: 'App',
  components: {
    NavBar,
  },
}
</script>

<style>
</style>
