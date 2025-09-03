<!-- TermsOfService.vue -->
<template>
  <div class="min-h-screen bg-[#121212] text-gray-200">
    <!-- Navigation -->
    <nav class="bg-[#1a1a1a] border-b border-[#2C2C2C] sticky top-0 z-10">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="flex items-center space-x-2 hover:opacity-80 transition">
            <img src="../assets/qq_logos/qq_nobg.svg" class="h-12 w-auto"></img>
          </router-link>
          <router-link to="/privacy" class="text-[#B3B3B3] hover:text-[#FFD700] transition">
            Privacy Policy →
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
      <h1 class="text-4xl font-['Silkscreen'] text-[#FFD700] mb-2">Terms of Service</h1>
      <p class="text-[#B3B3B3] mb-8">Last updated: {{ lastUpdated }}</p>

      <!-- Quick Accept Box -->
      <div class="bg-gradient-to-r from-[#1a1a1a] to-[#1f1f1f] rounded-lg p-6 mb-8 border border-[#2C2C2C]">
        <h2 class="text-lg font-semibold text-[#FFEC99] mb-3">The Basics</h2>
        <ul class="space-y-2 text-sm text-gray-300">
          <li>• You need a Spotify Premium account to use QueQueue</li>
          <li>• This is a personal project, not affiliated with Spotify</li>
          <li>• Use at your own risk - no warranties provided</li>
          <li>• Don't abuse the service or use it for illegal purposes</li>
          <li>• We can terminate access if you violate these terms</li>
        </ul>
      </div>

      <!-- Main Terms -->
      <div class="space-y-10">
        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">1. Acceptance of Terms</h2>
          <p class="text-gray-300 leading-relaxed">
            By using QueQueue, you agree to these Terms of Service. If you don't agree, 
            please don't use the service. We may update these terms occasionally, and your 
            continued use means you accept any changes.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">2. Service Description</h2>
          <p class="text-gray-300 leading-relaxed mb-4">
            QueQueue allows Spotify Premium users to save and restore their playback queues. 
            The service includes:
          </p>
          <ul class="list-disc list-inside space-y-1 text-gray-300 ml-4">
            <li>Exporting current Spotify queue</li>
            <li>Saving multiple named queues</li>
            <li>Restoring queues to Spotify</li>
            <li>ML-powered song suggestions</li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">3. Requirements</h2>
          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-[#2C2C2C]">
            <h3 class="text-[#FFD700] font-semibold mb-3">You must have:</h3>
            <ul class="space-y-2 text-gray-300">
              <li class="flex items-start">
                <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                <span>An active Spotify Premium account</span>
              </li>
              <li class="flex items-start">
                <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                <span>Be 18 years or older (or have parental consent)</span>
              </li>
              <li class="flex items-start">
                <span class="text-[#1DB954] mr-2 mt-1">✓</span>
                <span>Authorization to use the Spotify account</span>
              </li>
            </ul>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">4. Acceptable Use</h2>
          <div class="grid md:grid-cols-2 gap-4">
            <div class="bg-green-900/20 rounded-lg p-4 border border-green-700/50">
              <h3 class="text-green-400 font-semibold mb-2">✓ You CAN:</h3>
              <ul class="text-sm text-gray-300 space-y-1">
                <li>• Save unlimited queues</li>
                <li>• Upload custom cover images</li>
                <li>• Share queue links with friends</li>
                <li>• Use on multiple devices</li>
              </ul>
            </div>
            <div class="bg-red-900/20 rounded-lg p-4 border border-red-700/50">
              <h3 class="text-red-400 font-semibold mb-2">✗ You CANNOT:</h3>
              <ul class="text-sm text-gray-300 space-y-1">
                <li>• Upload inappropriate content</li>
                <li>• Attempt to hack or abuse the service</li>
                <li>• Sell or commercialize the service</li>
                <li>• Violate Spotify's Terms of Service</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">5. Intellectual Property</h2>
          <p class="text-gray-300 leading-relaxed">
            All music content belongs to respective copyright holders. QueQueue only stores 
            references (URIs) to tracks, not the music itself. The QueQueue name, logo, and 
            interface are property of this project.
          </p>
          <div class="mt-4 p-4 bg-[#1a1a1a] rounded-lg border border-[#2C2C2C]">
            <p class="text-sm text-[#B3B3B3]">
              <strong class="text-[#1DB954]">Note:</strong> Spotify and all related marks are 
              trademarks of Spotify AB. QueQueue is not affiliated with or endorsed by Spotify.
            </p>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">6. Disclaimers & Limitations</h2>
          <div class="bg-yellow-900/20 rounded-lg p-6 border border-yellow-700/50">
            <h3 class="text-yellow-400 font-semibold mb-3">⚠️ Important</h3>
            <div class="space-y-3 text-gray-300 text-sm">
              <p>
                <strong>No Warranty:</strong> QueQueue is provided "as is" without any warranties, 
                express or implied.
              </p>
              <p>
                <strong>Service Availability:</strong> We don't guarantee 100% uptime. The service 
                may be unavailable for maintenance or other reasons.
              </p>
              <p>
                <strong>Data Loss:</strong> While we try our best, we're not responsible for any 
                lost queues or data.
              </p>
              <p>
                <strong>Spotify Changes:</strong> If Spotify changes their API, some features may 
                stop working.
              </p>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">7. Liability</h2>
          <p class="text-gray-300 leading-relaxed">
            To the maximum extent permitted by law, QueQueue and its creator shall not be liable 
            for any indirect, incidental, special, consequential, or punitive damages resulting 
            from your use or inability to use the service.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">8. Termination</h2>
          <p class="text-gray-300 leading-relaxed mb-4">
            We reserve the right to terminate or suspend your access to QueQueue at any time, 
            with or without notice, for:
          </p>
          <ul class="list-disc list-inside space-y-1 text-gray-300 ml-4">
            <li>Violation of these terms</li>
            <li>Abusive or fraudulent behavior</li>
            <li>Request by law enforcement</li>
            <li>Extended periods of inactivity</li>
            <li>Discontinuation of the service</li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">9. Changes to Terms</h2>
          <p class="text-gray-300 leading-relaxed">
            We may modify these terms at any time. Significant changes will be noted on the 
            homepage or through the app. Your continued use after changes constitutes acceptance 
            of the new terms.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-['Silkscreen'] text-[#FFEC99] mb-4">10. Governing Law</h2>
          <p class="text-gray-300 leading-relaxed">
            These terms are governed by the laws of the United States and the State of Washington, 
            without regard to conflict of law principles.
          </p>
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

      <MainFooter />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MainFooter from '../components/MainFooter.vue'

const lastUpdated = ref(new Date().toLocaleDateString('en-US', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric' 
}))
</script>