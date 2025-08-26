<template>
  <div class="min-h-screen bg-primary text-white">
    <NavBar />
    <router-view />
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
