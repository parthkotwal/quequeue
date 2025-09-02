<template>
  <div class="queue-preview-container">
    <!-- Export Queue Preview (Left Side - Spotify-styled) -->
    <div class="export-section" :class="{ 'is-visible': isVisible }">
      <!-- Step label -->
      <div class="step-label">
        <span class="step-number">1</span>
        <span class="step-text">From Spotify</span>
      </div>
      
      <div class="spotify-queue-card">
        <!-- Spotify-style header -->
        <div class="spotify-header">
          <div class="spotify-logo-section">
            <img :src="spotifyLogo" alt="Spotify" class="spotify-mini-logo" />
            <div class="spotify-title">Queue</div>
          </div>
          <div class="spotify-status">
            <div class="spotify-dot"></div>
            <span>Now Playing</span>
          </div>
        </div>
        
        <!-- Now Playing section -->
        <div class="now-playing-section">
          <div class="now-playing-label">Now playing</div>
          <div class="now-playing-track">
            <div class="track-cover">
              <img :src="exportTracks[1].cover" :alt="exportTracks[1].name" />
              <div class="playing-indicator">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
              </div>
            </div>
            <div class="track-info">
              <div class="track-name">{{ exportTracks[1].name }}</div>
              <div class="track-artist">{{ exportTracks[1].artist }}</div>
            </div>
            <div class="spotify-controls">
              <svg class="control-icon" viewBox="0 0 16 16" fill="currentColor">
                <path d="M3 1.713a.7.7 0 0 1 1.05-.607l10.89 6.288a.7.7 0 0 1 0 1.212L4.05 14.894A.7.7 0 0 1 3 14.287V1.713z"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Next in queue -->
        <div class="next-section">
          <div class="next-label">Next in queue</div>
          <div class="next-tracks">
            <div 
              v-for="(track, index) in exportTracks.slice(0, 1).concat(exportTracks.slice(2))" 
              :key="track.id"
              class="spotify-track-item"
              :class="{ 'is-visible': isVisible }"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <div class="track-cover small">
                <img :src="track.cover" :alt="track.name" />
              </div>
              <div class="track-info">
                <div class="track-name">{{ track.name }}</div>
                <div class="track-artist">{{ track.artist }}</div>
              </div>
              <div class="track-duration">{{ track.duration }}</div>
              <div class="spotify-menu">⋯</div>
            </div>
          </div>
        </div>
        
        <!-- Export button styled for Spotify context -->
        <div class="export-button-section" :class="{ 'is-visible': isVisible }">
          <div class="export-hint">Save this queue to QueQueue</div>
          <button class="btn-export-spotify">
            <svg class="export-icon" viewBox="0 0 24 24" fill="none">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Export to QueQueue
          </button>
        </div>
      </div>
    </div>

    <!-- Center Arrow & Process -->
    <div class="process-center" :class="{ 'is-visible': isVisible }">
      <div class="step-number center">2</div>
      <div class="process-arrow">
        <div class="arrow-line"></div>
        <div class="arrow-head"></div>
      </div>
      <div class="process-text">Save & Name Your Queue</div>
      <div class="floating-icons">
        <div class="icon-save">💾</div>
        <div class="icon-cloud">☁️</div>
        <div class="icon-sync">🔄</div>
      </div>
    </div>

    <!-- Import Queue Preview (Right Side - Your App) -->
    <div class="import-section" :class="{ 'is-visible': isVisible }">
      <!-- Step label -->
      <div class="step-label">
        <span class="step-number">3</span>
        <span class="step-text">In QueQueue</span>
      </div>
      
      <div class="saved-queues">
        <div class="saved-queue-header">
          <span class="que-queue-logo">🎵 QueQueue</span>
          <span class="saved-subtitle">Your Saved Queues</span>
        </div>
        <div 
          v-for="(savedQueue, index) in savedQueues" 
          :key="savedQueue.id"
          class="saved-queue-item"
          :class="{ 'is-visible': isVisible, 'featured': index === 0 }"
          :style="{ animationDelay: `${(index + 3) * 150}ms` }"
        >
          <div class="queue-thumbnail">
            <div class="thumbnail-grid">
              <div class="thumb-img" v-for="i in 4" :key="i"></div>
            </div>
          </div>
          <div class="saved-queue-info">
            <div class="saved-queue-name">{{ savedQueue.name }}</div>
            <div class="saved-queue-meta">{{ savedQueue.trackCount }} tracks • {{ savedQueue.duration }}</div>
            <div class="saved-queue-date">Saved {{ savedQueue.savedAgo }}</div>
          </div>
          <button class="restore-btn" :class="{ 'primary': index === 0 }">
            <svg class="restore-icon" xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" width="24" height="24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"
            >
              <path d="M12 8v4l3 3" />
              <path d="M3 12a9 9 0 1 0 9 -9" />
              <path d="M3 3v5h5" />
            </svg>
  Restore to Spotify
</button>

        </div>
      </div>

      <!-- Restore Preview -->
      <div class="restore-preview" :class="{ 'is-visible': isVisible }">
        <div class="restore-header">
          <div class="restore-title">
            <span class="restore-icon-text">🔄</span>
            Restoring "Friday Night Vibes" to your Spotify queue...
          </div>
          <div class="restore-progress">
            <div class="progress-bar"></div>
          </div>
        </div>
        <div class="restore-tracks">
          <div 
            v-for="(track, index) in restoreTracks" 
            :key="track.id"
            class="restore-track"
            :class="{ 'is-visible': isVisible }"
            :style="{ animationDelay: `${(index + 6) * 100}ms` }"
          >
            <div class="restore-track-cover">
              <img :src="track.cover" :alt="track.name" />
              <div class="restore-checkmark">✓</div>
            </div>
            <div class="restore-track-name">{{ track.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const spotifyLogo = '/src/assets/Primary_Logo_Green_RGB.svg'

const isVisible = ref(false)

// Mock data for export queue
const exportTracks = [
  { id: 1, name: "Blinding Lights", artist: "The Weeknd", duration: "3:22", cover: "/src/assets/album_covers/44.webp" },
  { id: 2, name: "Good 4 U", artist: "Olivia Rodrigo", duration: "2:58", cover: "/src/assets/album_covers/45.webp" },
  { id: 3, name: "Levitating", artist: "Dua Lipa", duration: "3:23", cover: "/src/assets/album_covers/46.webp" },
  { id: 4, name: "As It Was", artist: "Harry Styles", duration: "2:47", cover: "/src/assets/album_covers/47.webp" },
]

// Mock data for saved queues (updated with more realistic data)
const savedQueues = [
  { id: 1, name: "Friday Night Vibes", trackCount: 9, duration: "1h 12m", savedAgo: "2 days ago" },
  { id: 2, name: "Study Session", trackCount: 15, duration: "2h 34m", savedAgo: "1 week ago" },
  { id: 3, name: "Workout Energy", trackCount: 18, duration: "58m", savedAgo: "3 days ago" },
]

// Mock data for restore preview
const restoreTracks = [
  { id: 1, name: "Watermelon Sugar", cover: "/src/assets/album_covers/48.webp" },
  { id: 2, name: "Don't Start Now", cover: "/src/assets/album_covers/46.webp" },
  { id: 3, name: "Save Your Tears", cover: "/src/assets/album_covers/44.webp" },
]

// Expose the visibility ref for parent component
defineExpose({
  setVisible: (visible) => {
    isVisible.value = visible
  }
})
</script>

<style scoped>
.queue-preview-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 4rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Step Labels */
.step-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.6s ease;
}

.export-section.is-visible .step-label,
.import-section.is-visible .step-label {
  opacity: 1;
  transform: translateY(0);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #121212;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.9rem;
  font-family: 'Silkscreen', monospace;
}

.step-number.center {
  background: linear-gradient(135deg, #1DB954, #1ED760);
  color: white;
}

.step-text {
  font-family: 'Silkscreen', monospace;
  color: #FFD700;
  font-size: 0.95rem;
}

/* Export Section (Left) - Spotify-styled */
.export-section {
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.export-section.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.spotify-queue-card {
  background: #121212;
  border: 1px solid #2a2a2a;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.spotify-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #2a2a2a;
}

.spotify-logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.spotify-mini-logo {
  width: 20px;
  height: 20px;
}

.spotify-title {
  font-weight: 700;
  font-size: 1.5rem;
  color: white;
}

.spotify-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #b3b3b3;
}

.spotify-dot {
  width: 8px;
  height: 8px;
  background: #1DB954;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

/* Now Playing Section */
.now-playing-section {
  margin-bottom: 2rem;
}

.now-playing-label {
  color: #b3b3b3;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.now-playing-track {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
}

/* Next Section */
.next-section {
  margin-bottom: 1.5rem;
}

.next-label {
  color: #b3b3b3;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.spotify-track-item {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 1rem;
  padding: 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.25rem;
  transition: background 0.2s ease;
  opacity: 0;
  transform: translateX(-20px);
}

.spotify-track-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.spotify-track-item.is-visible {
  opacity: 1;
  transform: translateX(0);
  animation: slideInLeft 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.track-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.track-cover.small {
  width: 32px;
  height: 32px;
}

.track-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playing-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  display: flex;
  gap: 1px;
  align-items: end;
}

.playing-indicator .bar {
  width: 2px;
  background: #1DB954;
  animation: musicBars 0.8s ease-in-out infinite alternate;
}

.playing-indicator .bar:nth-child(1) { height: 6px; animation-delay: 0s; }
.playing-indicator .bar:nth-child(2) { height: 10px; animation-delay: 0.2s; }
.playing-indicator .bar:nth-child(3) { height: 4px; animation-delay: 0.4s; }

@keyframes musicBars {
  0% { height: 2px; }
  100% { height: 10px; }
}

.track-info {
  min-width: 0;
}

.track-name {
  font-weight: 400;
  color: white;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  color: #b3b3b3;
  font-size: 0.8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  color: #b3b3b3;
  font-size: 0.8rem;
}

.spotify-controls {
  color: #b3b3b3;
}

.control-icon {
  width: 16px;
  height: 16px;
}

.spotify-menu {
  color: #b3b3b3;
  cursor: pointer;
  padding: 0.25rem;
}

/* Export Button Section */
.export-button-section {
  border-top: 1px solid #2a2a2a;
  padding-top: 1.5rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.5s;
}

.export-button-section.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.export-hint {
  color: #b3b3b3;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
  text-align: center;
}

.btn-export-spotify {
  width: 100%;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border: none;
  border-radius: 50px;
  padding: 0.75rem 1rem;
  color: #121212;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-export-spotify:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
}

.export-icon {
  width: 18px;
  height: 18px;
}

/* Process Center */
.process-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.3s;
  gap: 1rem;
}

.process-center.is-visible {
  opacity: 1;
  transform: scale(1);
}

.process-arrow {
  position: relative;
}

.arrow-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #FFD700, #FFA500);
  border-radius: 1px;
  position: relative;
}

.arrow-head {
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid #FFA500;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
}

.process-text {
  font-family: 'Silkscreen', monospace;
  color: #FFD700;
  font-size: 0.9rem;
  text-align: center;
}

.floating-icons {
  display: flex;
  gap: 1rem;
}

.floating-icons > div {
  font-size: 1.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* Import Section (Right) */
.import-section {
  opacity: 0;
  transform: translateX(50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.2s;
}

.import-section.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.saved-queues {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(29, 185, 84, 0.2);
  border-radius: 20px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.saved-queue-header {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(29, 185, 84, 0.1);
}

.que-queue-logo {
  font-family: 'Silkscreen', monospace;
  font-size: 1.2rem;
  color: #1DB954;
}

.saved-subtitle {
  color: #b3b3b3;
  font-size: 0.9rem;
}

.saved-queue-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  opacity: 0;
  transform: translateX(20px);
  transition: background 0.3s ease;
  border: 1px solid transparent;
}

.saved-queue-item.featured {
  background: rgba(29, 185, 84, 0.05);
  border-color: rgba(29, 185, 84, 0.2);
}

.saved-queue-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.saved-queue-item.is-visible {
  opacity: 1;
  transform: translateX(0);
  animation: slideInRight 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.queue-thumbnail {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.1);
  position: relative;
}

.thumbnail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  width: 100%;
  height: 100%;
}

.thumb-img {
  background: linear-gradient(45deg, #FFD700, #1DB954);
  opacity: 0.6;
}

.thumb-img:nth-child(2) { opacity: 0.4; }
.thumb-img:nth-child(3) { opacity: 0.3; }
.thumb-img:nth-child(4) { opacity: 0.5; }

.saved-queue-info {
  min-width: 0;
}

.saved-queue-name {
  font-weight: 600;
  color: white;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.saved-queue-meta {
  color: #b3b3b3;
  font-size: 0.8rem;
}

.saved-queue-date {
  color: #666;
  font-size: 0.7rem;
  margin-top: 0.25rem;
}

.restore-btn {
  background: transparent;
  border: 1px solid rgba(29, 185, 84, 0.5);
  border-radius: 50px;
  padding: 0.5rem 1rem;
  color: #1DB954;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
  font-weight: 600;
}

.restore-btn.primary {
  background: rgba(29, 185, 84, 0.1);
  border-color: #1DB954;
}

.restore-btn:hover {
  background: rgba(29, 185, 84, 0.2);
  transform: translateY(-1px);
}

.restore-icon {
  width: 16px;
  height: 16px;
}

.restore-preview {
  background: linear-gradient(145deg, rgba(29, 185, 84, 0.1), rgba(29, 185, 84, 0.05));
  border: 1px solid rgba(29, 185, 84, 0.3);
  border-radius: 20px;
  padding: 1.5rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.6s;
}

.restore-preview.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.restore-header {
  margin-bottom: 1rem;
}

.restore-title {
  color: #1DB954;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.restore-icon-text {
  font-size: 1.1rem;
}

.restore-progress {
  background: rgba(255, 255, 255, 0.1);
  height: 4px;
  border-radius: 2px;
  margin-top: 0.5rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #1DB954, #1ED760);
  border-radius: 2px;
  width: 0;
  animation: progressFill 2s ease-out 0.8s forwards;
}

@keyframes progressFill {
  to { width: 75%; }
}

.restore-tracks {
  display: flex;
  gap: 0.75rem;
}

.restore-track {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0;
  transform: translateY(20px);
}

.restore-track.is-visible {
  animation: slideInUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.restore-track-cover {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.restore-track-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.restore-checkmark {
  position: absolute;
  bottom: -2px;
  right: -2px;
  background: #1DB954;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
  border: 2px solid #121212;
}

.restore-track-name {
  font-size: 0.8rem;
  color: white;
  text-align: center;
  max-width: 60px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Common animations */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

/* Responsive */
@media (max-width: 1024px) {
  .queue-preview-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .process-center .process-arrow .arrow-line {
    transform: rotate(90deg);
  }
  
  .process-center .process-arrow .arrow-head {
    top: auto;
    bottom: -8px;
    right: 50%;
    transform: translateX(50%) rotate(90deg);
  }
  
  .step-text {
    font-size: 0.85rem;
  }
}

/* Reduce motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>