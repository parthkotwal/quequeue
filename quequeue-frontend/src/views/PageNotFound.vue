<template>
  <div class="min-h-screen bg-[#121212] flex items-center justify-center px-4 relative overflow-hidden">
    <!-- Background animated elements -->
    <div class="absolute inset-0 pointer-events-none">
      <!-- Floating album covers with subtle animation -->
      <div class="absolute top-20 left-10 w-16 h-16 bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg opacity-20 animate-float-slow"></div>
      <div class="absolute top-40 right-20 w-12 h-12 bg-gradient-to-br from-gray-600 to-gray-700 rounded-lg opacity-15 animate-float-slow" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-32 left-20 w-20 h-20 bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg opacity-10 animate-float-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-20 right-10 w-14 h-14 bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg opacity-20 animate-float-slow" style="animation-delay: 0.5s;"></div>
      
      <!-- Subtle glow effects -->
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[#FFD700] rounded-full opacity-5 blur-3xl"></div>
    </div>

    <!-- Main content -->
    <div class="text-center z-10 max-w-2xl mx-auto">
      <!-- 404 Number with glow effect -->
      <div class="relative mb-8">
        <h1 class="font-['Silkscreen'] text-8xl md:text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#FFD700] to-[#FFEC99] mb-4 select-none">
          404
        </h1>
        <!-- Glow effect behind text -->
        <div class="absolute inset-0 font-['Silkscreen'] text-8xl md:text-9xl font-bold text-[#FFD700] opacity-30 blur-md -z-10">
          404
        </div>
      </div>

      <!-- Main message -->
      <h2 class="font-['Silkscreen'] text-2xl md:text-3xl text-white mb-4">
        Page Not Found
      </h2>
      
      <p class="font-['Inconsolata'] text-lg text-[#B3B3B3] mb-8 leading-relaxed max-w-md mx-auto">
        Looks like this page got lost in the shuffle. Let's get you back to queueing.
      </p>

      <!-- Action buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <!-- Primary CTA -->
        <router-link 
          to="/"
          class="group relative px-8 py-3 bg-gradient-to-r from-[#FFD700] to-[#FFEC99] text-[#121212] font-['Inconsolata'] font-semibold rounded-full hover:shadow-[0_0_20px_rgba(255,215,0,0.3)] transition-all duration-300 transform hover:scale-105 active:scale-95"
        >
          <span class="relative z-10">Go Home</span>
          <!-- Hover glow effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-[#FFD700] to-[#FFEC99] rounded-full opacity-0 group-hover:opacity-20 blur transition-opacity duration-300"></div>
        </router-link>

        <!-- Secondary CTA -->
        <button 
          @click="goBack"
          class="px-8 py-3 border border-[#2C2C2C] text-[#B3B3B3] font-['Inconsolata'] font-semibold rounded-full hover:border-[#FFD700] hover:text-[#FFD700] transition-all duration-300 transform hover:scale-105 active:scale-95"
        >
          Go Back
        </button>
      </div>
      
    </div>

  </div>
</template>

<script>
export default {
  name: 'PageNotFound',
  methods: {
    goBack() {
      // Check if there's history to go back to
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        // If no history, go to home
        this.$router.push('/');
      }
    }
  },
  mounted() {
    // Optional: Add some metadata for SEO
    document.title = '404 - Page Not Found | Que Queue';
  }
}
</script>

<style scoped>
@keyframes float-slow {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) rotate(3deg);
  }
}

.animate-float-slow {
  animation: float-slow 6s ease-in-out infinite;
}

</style>