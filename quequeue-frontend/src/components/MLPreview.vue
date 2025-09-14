<template>
  <div class="ml-preview-container">
    <!-- Saved Queue Analysis (Left Side) -->
    <div class="analysis-section" :class="{ 'is-visible': isVisible }">
      <div class="queue-analysis-card">
        <div class="analysis-header">
          <div class="queue-name">Friday Night Vibes</div>
          <div class="analysis-status">
            <div class="analyzing-dot"></div>
            <span>Analyzing audio features...</span>
          </div>
        </div>

        <!-- Audio feature visualization -->
        <div class="audio-features" :class="{ 'is-visible': isVisible }">
          <div class="feature-title">Audio DNA</div>
          <div class="feature-bars">
            <div 
              v-for="(feature, index) in audioFeatures" 
              :key="feature.name"
              class="feature-bar-container"
              :style="{ animationDelay: `${index * 150}ms` }"
            >
              <div class="feature-label">{{ feature.name }}</div>
              <div class="feature-bar-bg">
                <div 
                  class="feature-bar-fill"
                  :class="{ 'is-visible': isVisible }"
                  :style="{ 
                    width: `${feature.value}%`, 
                    animationDelay: `${(index * 150) + 300}ms`,
                    background: feature.color 
                  }"
                ></div>
              </div>
              <div class="feature-value">{{ feature.value }}%</div>
            </div>
          </div>
        </div>

        <!-- Queue preview tracks -->
        <div class="preview-tracks" :class="{ 'is-visible': isVisible }">
          <div class="preview-title">Current Tracks</div>
          <div class="track-thumbnails">
            <div 
              v-for="(track, index) in previewTracks" 
              :key="track.id"
              class="track-thumb"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <img :src="track.cover" :alt="track.name" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Processing Visualization (Center) -->
    <div class="ai-processing" :class="{ 'is-visible': isVisible }">
      <div class="ai-brain">
        <div class="brain-core">
          <svg class="brain-icon" viewBox="0 0 100 100" fill="none">
            <!-- Neural network visualization -->
            <circle cx="20" cy="30" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
            </circle>
            <circle cx="50" cy="20" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="0.5s" />
            </circle>
            <circle cx="80" cy="30" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="1s" />
            </circle>
            <circle cx="20" cy="70" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="1.5s" />
            </circle>
            <circle cx="50" cy="80" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="0.3s" />
            </circle>
            <circle cx="80" cy="70" r="3" fill="currentColor" class="node">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="0.8s" />
            </circle>
            
            <!-- Connections -->
            <path d="M20,30 L50,20 M50,20 L80,30 M20,30 L20,70 M80,30 L80,70 M20,70 L50,80 M50,80 L80,70" 
                  stroke="currentColor" 
                  stroke-width="1" 
                  opacity="0.4"
                  class="connections">
              <animate attributeName="opacity" values="0.1;0.6;0.1" dur="3s" repeatCount="indefinite" />
            </path>
          </svg>
        </div>
        <div class="processing-text">
          <div class="ai-label">QueQueue Engine</div>
          <div class="processing-steps">
            <div class="step" :class="{ active: currentStep >= 1 }">Analyzing tempo patterns</div>
            <div class="step" :class="{ active: currentStep >= 2 }">Finding energy matches</div>
            <div class="step" :class="{ active: currentStep >= 3 }">Generating recommendations</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ML Recommendations (Right Side) -->
    <div class="recommendations-section" :class="{ 'is-visible': isVisible }">
      <div class="recommendations-card">
        <div class="recommendations-header">
          <div class="recommendations-title">Perfect Additions</div>
          <div class="confidence-badge">96% match confidence</div>
        </div>

        <div class="recommended-tracks">
          <div 
            v-for="(track, index) in recommendedTracks" 
            :key="track.id"
            class="recommended-track"
            :class="{ 'is-visible': isVisible }"
            :style="{ animationDelay: `${(index + 5) * 200}ms` }"
          >
            <div class="track-number">{{ index + 1 }}</div>
            <div class="track-cover-container">
              <img :src="track.cover" :alt="track.name" class="track-cover" />
              <div class="match-score">{{ track.matchScore }}%</div>
            </div>
            <div class="track-details">
              <div class="track-name">{{ track.name }}</div>
              <div class="track-artist">{{ track.artist }}</div>
              <div class="match-reasons">
                <span 
                  v-for="reason in track.reasons" 
                  :key="reason"
                  class="reason-tag"
                >
                  {{ reason }}
                </span>
              </div>
            </div>
            <button class="add-track-btn">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="add-all-section" :class="{ 'is-visible': isVisible }">
          <button class="add-all-btn">
            <svg class="magic-wand" viewBox="0 0 24 24" fill="none">
              <path d="M15 4V2M15 16V14M8 9H10M20 9H22M17.8 11.8L19.2 13.2M17.8 6.2L19.2 4.8M3 21L9 15L21 3L18 0L6 12L0 18L3 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Add All 3 Recommendations
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isVisible = ref(false)
const currentStep = ref(0)

// Mock data for audio features
const audioFeatures = [
  { name: 'Energy', value: 78, color: 'linear-gradient(90deg, #ff6b6b, #ee5a52)' },
  { name: 'Dance', value: 85, color: 'linear-gradient(90deg, #4ecdc4, #44a08d)' },
  { name: 'Valence', value: 72, color: 'linear-gradient(90deg, #45b7d1, #96c93d)' },
  { name: 'Acoustic', value: 23, color: 'linear-gradient(90deg, #f093fb, #f5576c)' },
  { name: 'Tempo', value: 91, color: 'linear-gradient(90deg, #ffd89b, #19547b)' }
]

// Mock data for preview tracks
const previewTracks = [
  { id: 1, name: "9", cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/24.webp" },
  { id: 2, name: "Antidote", cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/26.webp" },
  { id: 3, name: "No Role Modelz", cover:"https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/17_2.webp" },
  { id: 4, name: "I Serve the Base", cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/26_2.webp" },
]

// Mock data for recommended tracks
const recommendedTracks = [
  { 
    id: 1, 
    name: "STARGAZING", 
    artist: "Travis Scott", 
    cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/22.webp",
    matchScore: 94,
    reasons: ['High Energy', 'Adlib Style']
  },
  { 
    id: 2, 
    name: "Flashing Lights", 
    artist: "Kanye West", 
    cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/13_2.webp",
    matchScore: 92,
    reasons: ['Beautiful Synths', 'Top-Tier Hook']
  },
  { 
    id: 3, 
    name: "Over My Dead Body", 
    artist: "Drake", 
    cover: "https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/31.webp",
    matchScore: 89,
    reasons: ['Melodic Rap', 'Night Vibe']
  }
]

// Simulate AI processing steps
const simulateProcessing = () => {
  setTimeout(() => currentStep.value = 1, 800)
  setTimeout(() => currentStep.value = 2, 1600)
  setTimeout(() => currentStep.value = 3, 2400)
}

// Expose the visibility ref for parent component
defineExpose({
  setVisible: (visible) => {
    isVisible.value = visible
    if (visible) {
      simulateProcessing()
    }
  }
})
</script>

<style scoped>
.ml-preview-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 3rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Analysis Section (Left) */
.analysis-section {
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.analysis-section.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.queue-analysis-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
}

.queue-name {
  font-family: 'Silkscreen', monospace;
  font-size: 1.2rem;
  color: #FFD700;
}

.analysis-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #B3B3B3;
}

.analyzing-dot {
  width: 8px;
  height: 8px;
  background: #FFD700;
  border-radius: 50%;
  animation: analyzePulse 1.5s infinite;
}

@keyframes analyzePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.audio-features {
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease 0.3s;
}

.audio-features.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.feature-title {
  font-family: 'Silkscreen', monospace;
  font-size: 0.9rem;
  color: #FFD700;
  margin-bottom: 1rem;
}

.feature-bars {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-bar-container {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.75rem;
  align-items: center;
  opacity: 0;
  transform: translateX(-20px);
  animation: slideInFeature 0.6s ease forwards;
}

@keyframes slideInFeature {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.feature-label {
  font-size: 0.8rem;
  color: #B3B3B3;
  min-width: 60px;
}

.feature-bar-bg {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  min-width: 120px;
}

.feature-bar-fill {
  height: 100%;
  border-radius: 3px;
  width: 0;
  transition: width 1.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.feature-bar-fill.is-visible {
  width: var(--width);
}

@keyframes fillBar {
  to { width: var(--fill-width, 0%); }
}

.feature-value {
  font-size: 0.8rem;
  color: #FFD700;
  font-family: 'Inconsolata', monospace;
  min-width: 35px;
  text-align: right;
}

.preview-tracks {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease 0.6s;
}

.preview-tracks.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.preview-title {
  font-family: 'Silkscreen', monospace;
  font-size: 0.9rem;
  color: #FFD700;
  margin-bottom: 1rem;
}

.track-thumbnails {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.track-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  opacity: 0;
  transform: scale(0.8);
  animation: popIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

@keyframes popIn {
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.track-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* AI Processing (Center) */
.ai-processing {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.2s;
}

.ai-processing.is-visible {
  opacity: 1;
  transform: scale(1);
}

.ai-brain {
  text-align: center;
}

.brain-core {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  animation: brainPulse 3s ease-in-out infinite;
}

@keyframes brainPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
  50% { transform: scale(1.05); box-shadow: 0 0 30px rgba(255, 215, 0, 0.5); }
}

.brain-icon {
  width: 40px;
  height: 40px;
  color: #FFD700;
}

.processing-text {
  min-width: 200px;
}

.ai-label {
  font-family: 'Silkscreen', monospace;
  color: #FFD700;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.processing-steps {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.step {
  font-size: 0.8rem;
  color: #666;
  transition: color 0.3s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.02);
}

.step.active {
  color: #FFD700;
  background: rgba(255, 215, 0, 0.1);
  transform: translateX(5px);
  transition: all 0.3s ease;
}

/* Recommendations Section (Right) */
.recommendations-section {
  opacity: 0;
  transform: translateX(50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.4s;
}

.recommendations-section.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.recommendations-card {
  background: linear-gradient(145deg, rgba(29, 185, 84, 0.1), rgba(29, 185, 84, 0.05));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(29, 185, 84, 0.3);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.recommendations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(29, 185, 84, 0.1);
}

.recommendations-title {
  font-family: 'Silkscreen', monospace;
  font-size: 1.2rem;
  color: #1DB954;
}

.confidence-badge {
  background: rgba(29, 185, 84, 0.2);
  color: #1DB954;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-family: 'Inconsolata', monospace;
}

.recommended-tracks {
  margin-bottom: 1.5rem;
}

.recommended-track {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(29, 185, 84, 0.1);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
}

.recommended-track:hover {
  background: rgba(29, 185, 84, 0.05);
  transform: translateY(-2px);
}

.recommended-track.is-visible {
  opacity: 1;
  transform: translateY(0);
  animation: slideInRecommendation 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

@keyframes slideInRecommendation {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.track-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1DB954, #1ED760);
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inconsolata', monospace;
}

.track-cover-container {
  position: relative;
  width: 50px;
  height: 50px;
}

.track-cover {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.match-score {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #FFD700;
  color: #121212;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 8px;
  font-family: 'Inconsolata', monospace;
}

.track-details {
  min-width: 0;
}

.track-name {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  color: #B3B3B3;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.match-reasons {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.reason-tag {
  background: rgba(29, 185, 84, 0.2);
  color: #1DB954;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 6px;
  font-family: 'Inconsolata', monospace;
}

.add-track-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: transparent;
  border: 1px solid rgba(29, 185, 84, 0.5);
  color: #1DB954;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-track-btn:hover {
  background: rgba(29, 185, 84, 0.2);
  transform: scale(1.1);
}

.add-track-btn svg {
  width: 16px;
  height: 16px;
}

.add-all-section {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease 1.2s;
}

.add-all-section.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.add-all-btn {
  width: 100%;
  background: linear-gradient(135deg, #1DB954, #1ED760);
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.add-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(29, 185, 84, 0.3);
}

.magic-wand {
  width: 20px;
  height: 20px;
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .ml-preview-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .ai-processing {
    order: -1;
  }
  
  .analysis-section,
  .recommendations-section {
    transform: none;
  }
  
  .analysis-section.is-visible,
  .recommendations-section.is-visible {
    transform: none;
  }
}

/* Reduce motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .brain-core {
    animation: none !important;
  }
  
  .analyzing-dot {
    animation: none !important;
  }
}
</style>