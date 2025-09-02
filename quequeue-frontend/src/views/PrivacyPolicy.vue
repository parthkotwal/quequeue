<!-- PrivacyPolicy.vue -->
<template>
  <div class="min-h-screen bg-[#121212] text-gray-200">
    <!-- Navigation -->
    <nav class="bg-[#1a1a1a] border-b border-[#2C2C2C] sticky top-0 z-10">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="flex items-center space-x-2 hover:opacity-80 transition">
            <img src="../assets/qq_logos/qq_nobg.svg" class="h-12 w-auto"></img>
          </router-link>
          <router-link to="/terms" class="text-[#B3B3B3] hover:text-[#FFD700] transition">
            Terms of Service →
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
      <h1 class="text-4xl font-['Silkscreen'] text-[#FFD700] mb-2">Privacy Policy</h1>
      <p class="text-[#B3B3B3] mb-8">Last updated: {{ lastUpdated }}</p>

      <!-- Table of Contents -->
      <div class="bg-[#1a1a1a] rounded-lg p-6 mb-8 border border-[#2C2C2C]">
        <h2 class="text-xl font-['Silkscreen'] text-[#FFEC99] mb-4">Quick Navigation</h2>
        <ul class="space-y-2">
          <li v-for="section in sections" :key="section.id">
            <a 
              :href="`#${section.id}`" 
              class="text-[#B3B3B3] hover:text-[#FFD700] transition flex items-center"
            >
              <span class="text-[#FFD700] mr-2">→</span>
              {{ section.title }}
            </a>
          </li>
        </ul>
      </div>

      <!-- Sections -->
      <div class="space-y-12">
        <section id="overview" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">Overview</h2>
          <div class="prose prose-invert max-w-none">
            <p class="text-gray-300 leading-relaxed">
              QueQueue ("we", "our", "the app") is a personal project that helps Spotify Premium users 
              save and restore their music queues. We believe in transparency about what data we collect 
              and how we use it.
            </p>
            <div class="bg-[#1a1a1a] border-l-4 border-[#1DB954] p-4 my-4">
              <p class="text-sm text-[#B3B3B3]">
                <strong class="text-[#1DB954]">TL;DR:</strong> We only collect what's needed to save your 
                queues. No tracking, no ads, no selling data. You can delete everything anytime.
              </p>
            </div>
          </div>
        </section>

        <section id="data-collected" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">What We Collect</h2>
          
          <div class="space-y-6">
            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-lg font-semibold text-[#FFD700] mb-3">From Spotify (via OAuth)</h3>
              <ul class="space-y-2 text-gray-300">
                <li class="flex items-start">
                  <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                  <span><strong>Basic Profile:</strong> Your Spotify ID and display name</span>
                </li>
                <li class="flex items-start">
                  <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                  <span><strong>Authentication Tokens:</strong> Short-lived access tokens (encrypted)</span>
                </li>
                <li class="flex items-start">
                  <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                  <span><strong>Queue Data:</strong> Track names, artists, album art URLs, playback order</span>
                </li>
              </ul>
            </div>

            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-lg font-semibold text-[#FFD700] mb-3">What You Provide</h3>
              <ul class="space-y-2 text-gray-300">
                <li class="flex items-start">
                  <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                  <span>Custom queue names and descriptions</span>
                </li>
                <li class="flex items-start">
                  <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                  <span>Optional cover images for your saved queues</span>
                </li>
              </ul>
            </div>

            <div class="bg-red-900/20 rounded-lg p-6 border border-red-800/50">
              <h3 class="text-lg font-semibold text-red-400 mb-3">What We DON'T Collect</h3>
              <ul class="space-y-2 text-gray-300">
                <li class="flex items-start">
                  <span class="text-red-400 mr-2 mt-1">✗</span>
                  <span>Email addresses or passwords</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-400 mr-2 mt-1">✗</span>
                  <span>Payment information</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-400 mr-2 mt-1">✗</span>
                  <span>Listening history beyond current queue</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-400 mr-2 mt-1">✗</span>
                  <span>Analytics, tracking cookies, or behavioral data</span>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <section id="data-usage" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">How We Use Your Data</h2>
          <div class="grid md:grid-cols-2 gap-4">
            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-[#FFD700] font-semibold mb-2">Core Functionality</h3>
              <p class="text-gray-300 text-sm">Save, manage, and restore your Spotify queues</p>
            </div>
            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-[#FFD700] font-semibold mb-2">Smart Suggestions</h3>
              <p class="text-gray-300 text-sm">Analyze saved tracks to recommend similar songs</p>
            </div>
            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-[#FFD700] font-semibold mb-2">Authentication</h3>
              <p class="text-gray-300 text-sm">Keep you logged in securely via Spotify OAuth</p>
            </div>
            <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
              <h3 class="text-[#FFD700] font-semibold mb-2">Display</h3>
              <p class="text-gray-300 text-sm">Show your queue data back to you in the app</p>
            </div>
          </div>
        </section>

        <section id="storage-security" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">Storage & Security</h2>
          <div class="space-y-4">
            <div class="flex items-start space-x-4">
              <div class="text-3xl">🔒</div>
              <div class="flex-1">
                <h3 class="text-[#FFD700] font-semibold mb-1">Encryption</h3>
                <p class="text-gray-300 text-sm">All data transmitted via HTTPS. Tokens encrypted at rest.</p>
              </div>
            </div>
            <div class="flex items-start space-x-4">
              <div class="text-3xl">☁️</div>
              <div class="flex-1">
                <h3 class="text-[#FFD700] font-semibold mb-1">AWS Infrastructure</h3>
                <p class="text-gray-300 text-sm">Data stored on AWS (RDS for database, S3 for images) with industry-standard security.</p>
              </div>
            </div>
            <div class="flex items-start space-x-4">
              <div class="text-3xl">⏱️</div>
              <div class="flex-1">
                <h3 class="text-[#FFD700] font-semibold mb-1">Token Expiration</h3>
                <p class="text-gray-300 text-sm">Spotify tokens are short-lived and automatically refreshed as needed.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="ml-recommendations" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">Smart Suggestions</h2>
          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
            <p class="text-gray-300 mb-4">
              Our ML-powered suggestions analyze the audio features of tracks in your saved queues to recommend 
              similar songs you might enjoy.
            </p>
            <div class="space-y-2 text-sm text-[#B3B3B3]">
              <p>• <strong>Data Source:</strong> External dataset (not from Spotify API)</p>
              <p>• <strong>Processing:</strong> Done server-side when you view a queue</p>
              <p>• <strong>No Training:</strong> We don't use your data to train models</p>
              <p>• <strong>Cached:</strong> Suggestions cached for 24 hours to improve performance</p>
            </div>
          </div>
        </section>

        <section id="your-rights" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">Your Rights</h2>
          <div class="grid md:grid-cols-2 gap-4">
            <div class="bg-gradient-to-br from-[#1a1a1a] to-[#1f1f1f] rounded-lg p-6 border border-[#2C2C2C] hover:border-[#FFD700] transition">
              <h3 class="text-[#FFD700] font-semibold mb-3">Delete Everything</h3>
              <p class="text-gray-300 text-sm mb-3">Remove your account and all associated data permanently.</p>
              <button class="text-[#1DB954] hover:text-[#FFEC99] text-sm font-semibold transition">
                Coming Soon →
              </button>
            </div>
            <div class="bg-gradient-to-br from-[#1a1a1a] to-[#1f1f1f] rounded-lg p-6 border border-[#2C2C2C] hover:border-[#FFD700] transition">
              <h3 class="text-[#FFD700] font-semibold mb-3">Export Your Data</h3>
              <p class="text-gray-300 text-sm mb-3">Download all your queues as JSON files.</p>
              <button class="text-[#1DB954] hover:text-[#FFEC99] text-sm font-semibold transition">
                Coming Soon →
              </button>
            </div>
          </div>
          <div class="mt-4 p-4 bg-blue-900/20 rounded-lg border border-blue-700/50">
            <p class="text-sm text-blue-300">
              <strong>Note:</strong> You can always revoke QueQueue's access through your 
              <a href="https://www.spotify.com/account/apps/" target="_blank" class="underline hover:text-blue-200">
                Spotify account settings
              </a>.
            </p>
          </div>
        </section>

        <section id="third-parties" class="scroll-mt-20">
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">Third Parties</h2>
          <div class="space-y-4">
            <p class="text-gray-300">We share data with these services only as necessary for functionality:</p>
            <ul class="space-y-3">
              <li class="bg-[#1a1a1a] rounded-lg p-4 border border-[#2C2C2C]">
                <strong class="text-[#1DB954]">Spotify:</strong>
                <span class="text-gray-300 ml-2">For authentication and queue operations</span>
              </li>
              <li class="bg-[#1a1a1a] rounded-lg p-4 border border-[#2C2C2C]">
                <strong class="text-[#FFD700]">AWS:</strong>
                <span class="text-gray-300 ml-2">For hosting and data storage</span>
              </li>
            </ul>
            <div class="p-4 bg-green-900/20 rounded-lg border border-green-700/50">
              <p class="text-sm text-green-300">
                ✓ No advertising networks<br>
                ✓ No analytics trackers<br>
                ✓ No data brokers
              </p>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">11. Contact</h2>
          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
            <p class="text-gray-300 mb-4">
                Any questions? This is a personal project, but I'm happy to help:
            </p>
            <div class="space-y-2">
              <p class="text-[#B3B3B3]">
                <strong class="text-[#FFD700]">Email:</strong> 
                <a href="mailto:legal@quequeue.app" class="text-[#1DB954] hover:text-[#FFEC99] transition">
                  admin@quequeue.app
                </a>
              </p>
              <p class="text-[#B3B3B3]">
                <strong class="text-[#FFD700]">GitHub:</strong> 
                <a href="https://github.com/parthkotwal" target="_blank" class="text-[#1DB954] hover:text-[#FFEC99] transition">
                  github.com/parthkotwal
                </a>
              </p>
            </div>
          </div>
        </section>
      </div>

      <!-- Footer -->
      <MainFooter />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MainFooter from '../components/MainFooter.vue'


const lastUpdated = ref(new Date().toLocaleDateString('en-US', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric' 
}))

const sections = [
  { id: 'overview', title: 'Overview' },
  { id: 'data-collected', title: 'What We Collect' },
  { id: 'data-usage', title: 'How We Use Your Data' },
  { id: 'storage-security', title: 'Storage & Security' },
  { id: 'ml-recommendations', title: 'Smart Suggestions' },
  { id: 'your-rights', title: 'Your Rights' },
  { id: 'third-parties', title: 'Third Parties' },
  { id: 'contact', title: 'Contact' }
]

onMounted(() => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href'))
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    })
  })
})
</script>