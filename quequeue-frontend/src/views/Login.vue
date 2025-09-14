<template>
  <div class="login-page min-h-screen flex flex-col justify-center items-center bg-primary text-white px-4 py-8">
    <!-- Main heading -->
    <div class="text-center mb-8">
      <img src="../assets/qq_logos/qq_nobg.svg" class="h-24 w-auto"></img>
    </div>

    <!-- Info cards -->
    <div class="max-w-2xl w-full mb-8 space-y-4">
      <!-- Premium requirement card -->
      <div class="bg-[#1a1a1a] rounded-xl p-6 border border-divider">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-gradient-to-r from-accent to-accentLight rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M10.75 3h2.5c.464 0 .909.184 1.237.513.329.328.513.773.513 1.237V7h5.25c.464 0 .909.184 1.237.513.329.328.513.773.513 1.237v10.5c0 .464-.184.909-.513 1.237A1.746 1.746 0 0 1 20.25 21H3.75A1.75 1.75 0 0 1 2 19.25V8.75c0-.464.184-.909.513-1.237A1.746 1.746 0 0 1 3.75 7H9V4.75c0-.464.184-.909.513-1.237A1.746 1.746 0 0 1 10.75 3Zm3.646 6.573A1.753 1.753 0 0 1 13.25 10h-2.5a1.753 1.753 0 0 1-1.732-1.5H3.75a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h16.5a.25.25 0 0 0 .25-.25V8.75a.25.25 0 0 0-.25-.25h-5.268c-.06.416-.268.797-.586 1.073Zm-8.25 1.573A.504.504 0 0 1 6.5 11h3c.133 0 .26.053.354.146A.504.504 0 0 1 10 11.5v5c0 .133-.053.26-.146.354A.504.504 0 0 1 9.5 17h-3a.504.504 0 0 1-.354-.146A.504.504 0 0 1 6 16.5v-5c0-.133.053-.26.146-.354ZM10.5 4.75v3.5a.25.25 0 0 0 .25.25h2.5a.25.25 0 0 0 .25-.25v-3.5a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Zm.72 7.47a.747.747 0 0 1 .53-.22h5.5c.199 0 .39.079.53.22a.747.747 0 0 1 0 1.06.747.747 0 0 1-.53.22h-5.5a.747.747 0 0 1-.53-.22.747.747 0 0 1 0-1.06Zm0 2.525a.747.747 0 0 1 .53-.22h3.5c.199 0 .39.079.53.22a.747.747 0 0 1 0 1.06.747.747 0 0 1-.53.22h-3.5a.747.747 0 0 1-.53-.22.747.747 0 0 1 0-1.06Z"></path></svg>
            </div>
          </div>
          <div>
            <h3 class="text-lg font-silkscreen text-accent mb-2">Spotify Premium Required</h3>
            <p class="text-secondaryText text-sm leading-relaxed">
              Queue control requires Spotify Premium. Free users can view saved queues but cannot export or restore them.
            </p>
          </div>
        </div>
      </div>

      <!-- Privacy & Security card -->
      <div class="bg-[#1a1a1a] rounded-xl p-6 border border-divider">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-gradient-to-r from-accent to-accentLight rounded-full flex items-center justify-center">
              <svg class="text-primary" fill="currentColor" viewBox="0 0 20 20" width="24">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
          <div>
            <h3 class="text-lg font-silkscreen text-accent mb-2">Privacy First</h3>
            <p class="text-secondaryText text-sm leading-relaxed">
              We only access your queue data and display name. No email, passwords, or personal information stored. 
              <router-link to="/privacy" class="text-accent hover:text-accentLight underline">Learn more</router-link>
            </p>
          </div>
        </div>
      </div>

      <!-- Features preview -->
      <div class="bg-[#1a1a1a] rounded-xl p-6 border border-divider">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-gradient-to-r from-accent to-accentLight rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M1 12C1 5.925 5.925 1 12 1s11 4.925 11 11-4.925 11-11 11S1 18.075 1 12Zm16.28-2.72a.751.751 0 0 0-.018-1.042.751.751 0 0 0-1.042-.018l-5.97 5.97-2.47-2.47a.751.751 0 0 0-1.042.018.751.751 0 0 0-.018 1.042l3 3a.75.75 0 0 0 1.06 0Z"></path></svg>
            </div>
          </div>
          <div>
            <h3 class="text-lg font-silkscreen text-accent mb-2">What You Get</h3>
            <ul class="text-secondaryText text-sm space-y-1">
              <li>• Export your current Spotify queue</li>
              <li>• Save unlimited named queues</li>
              <li>• Restore queues anytime, anywhere</li>
              <li>• Smart song suggestions powered by ML</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Login button -->
    <div class="text-center mb-8">
      <button 
        @click="connectSpotify"
        class="group px-8 py-4 rounded-2xl bg-spotifyGreen hover:brightness-105 focus:outline-none focus:ring-2 focus:ring-spotifyGreen/40 transition-all duration-200 inline-flex items-center gap-3 text-primary font-inconsolata font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
      >
        <span>Continue with Spotify</span>
        <img :src="spotifyLogo" alt="Spotify" class="w-5 h-auto" />
      </button>
      
      <!-- Small disclaimer -->
      <p class="text-xs text-secondaryText mt-4 opacity-70">
        By continuing, you agree to our 
        <router-link to="/terms" class="text-accent hover:text-accentLight underline">Terms of Service</router-link>
        and 
        <router-link to="/privacy" class="text-accent hover:text-accentLight underline">Privacy Policy</router-link>
      </p>
    </div>

    <!-- Footer links -->
    <div class="flex gap-6 text-sm text-secondaryText">
      <router-link to="/" class="hover:text-accent transition-colors">← Back to Home</router-link>
      <a href="https://spotify.com/premium" target="_blank" rel="noopener noreferrer" class="hover:text-accent transition-colors">
        Get Spotify Premium →
      </a>
    </div>
  </div>
</template>

<script setup>
import { browserBaseURL } from '../api';
import spotifyLogo from '../assets/Spotify_logo.svg';

function connectSpotify() {
  window.location.href = `${browserBaseURL}/login/`;
}
</script>