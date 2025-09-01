<template>
  <div class="queue-preview-container">
    <!-- Export Queue Preview (Left Side) -->
    <div class="export-section" :class="{ 'is-visible': isVisible }">
      <div class="queue-card">
        <div class="queue-header">
          <div class="queue-title">Current Queue</div>
          <div class="queue-status">
            <div class="status-dot"></div>
            <span>Now Playing</span>
          </div>
        </div>
        
        <div class="queue-tracks">
          <div 
            v-for="(track, index) in exportTracks" 
            :key="track.id"
            class="track-item"
            :class="{ 'current-track': index === 1, 'is-visible': isVisible }"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <div class="track-cover">
              <img :src="track.cover" :alt="track.name" />
              <div v-if="index === 1" class="playing-indicator">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
              </div>
            </div>
            <div class="track-info">
              <div class="track-name">{{ track.name }}</div>
              <div class="track-artist">{{ track.artist }}</div>
            </div>
            <div class="track-duration">{{ track.duration }}</div>
          </div>
        </div>
        
        <div class="export-button" :class="{ 'is-visible': isVisible }">
          <button class="btn-export">
            <svg class="export-icon" viewBox="0 0 24 24" fill="none">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Export Queue
          </button>
        </div>
      </div>
    </div>

    <!-- Center Arrow & Process -->
    <div class="process-center" :class="{ 'is-visible': isVisible }">
      <div class="process-arrow">
        <div class="arrow-line"></div>
        <div class="arrow-head"></div>
      </div>
      <div class="process-text">Save & Restore</div>
      <div class="floating-icons">
        <div class="icon-cloud">☁️</div>
        <div class="icon-save">💾</div>
        <div class="icon-sync">🔄</div>
      </div>
    </div>

    <!-- Import Queue Preview (Right Side) -->
    <div class="import-section" :class="{ 'is-visible': isVisible }">
      <div class="saved-queues">
        <div class="saved-queue-header">Saved Queues</div>
        <div 
          v-for="(savedQueue, index) in savedQueues" 
          :key="savedQueue.id"
          class="saved-queue-item"
          :class="{ 'is-visible': isVisible }"
          :style="{ animationDelay: `${(index + 3) * 150}ms` }"
        >
          <div class="saved-queue-info">
            <div class="saved-queue-name">{{ savedQueue.name }}</div>
            <div class="saved-queue-meta">{{ savedQueue.trackCount }} tracks • {{ savedQueue.duration }}</div>
          </div>
          <button class="restore-btn" :class="{ 'featured': index === 0 }">
            <svg class="restore-icon" viewBox="0 0 24 24" fill="none">
              <path d="M3 12C3 12 5.5 17 12 17S21 12 21 12S18.5 7 12 7S3 12 3 12Z" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
            </svg>
            Restore
          </button>
        </div>
      </div>

      <!-- Restore Preview -->
      <div class="restore-preview" :class="{ 'is-visible': isVisible }">
        <div class="restore-header">
          <span class="restore-title">Restoring: "Friday Night Vibes" to Spotify</span>
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

const isVisible = ref(false)

// Mock data for export queue
const exportTracks = [
  { id: 1, name: "Blinding Lights", artist: "The Weeknd", duration: "3:22", cover: "/src/assets/album_covers/44.webp" },
  { id: 2, name: "Good 4 U", artist: "Olivia Rodrigo", duration: "2:58", cover: "/src/assets/album_covers/45.webp" },
  { id: 3, name: "Levitating", artist: "Dua Lipa", duration: "3:23", cover: "/src/assets/album_covers/46.webp" },
  { id: 4, name: "As It Was", artist: "Harry Styles", duration: "2:47", cover: "/src/assets/album_covers/47.webp" },
]

// Mock data for saved queues
const savedQueues = [
  { id: 1, name: "Friday Night Vibes", trackCount: 23, duration: "1h 12m" },
  { id: 2, name: "Study Session", trackCount: 10, duration: "2h 34m" },
  { id: 3, name: "Workout Energy", trackCount: 18, duration: "58m" },
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

/* Export Section (Left) */
.export-section {
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.export-section.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.queue-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
}

.queue-title {
  font-family: 'Silkscreen', monospace;
  font-size: 1.2rem;
  color: #FFD700;
}

.queue-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #B3B3B3;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #1DB954;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.queue-tracks {
  margin-bottom: 1.5rem;
}

.track-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateX(-20px);
}

.track-item.is-visible {
  opacity: 1;
  transform: translateX(0);
  animation: slideInLeft 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.track-item.current-track {
  background: rgba(29, 185, 84, 0.1);
  border: 1px solid rgba(29, 185, 84, 0.3);
}

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

.track-cover {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
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
  gap: 2px;
  align-items: end;
}

.playing-indicator .bar {
  width: 2px;
  background: #1DB954;
  animation: musicBars 0.8s ease-in-out infinite alternate;
}

.playing-indicator .bar:nth-child(1) { height: 8px; animation-delay: 0s; }
.playing-indicator .bar:nth-child(2) { height: 12px; animation-delay: 0.2s; }
.playing-indicator .bar:nth-child(3) { height: 6px; animation-delay: 0.4s; }

@keyframes musicBars {
  0% { height: 2px; }
  100% { height: 12px; }
}

.track-info {
  min-width: 0;
}

.track-name {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  color: #B3B3B3;
  font-size: 0.8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  color: #B3B3B3;
  font-size: 0.8rem;
  font-family: 'Inconsolata', monospace;
}

.export-button {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 0.5s;
}

.export-button.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.btn-export {
  width: 100%;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: #121212;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-export:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
}

.export-icon {
  width: 20px;
  height: 20px;
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
}

.process-center.is-visible {
  opacity: 1;
  transform: scale(1);
}

.process-arrow {
  position: relative;
  margin-bottom: 1rem;
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
  margin-bottom: 1rem;
}

.floating-icons {
  display: flex;
  gap: 1rem;
}

.floating-icons > div {
  font-size: 1.5rem;
  animation: float 3s ease-in-out infinite;
}

/* .floating-icons > div:nth-child(2) { animation-delay: 1s; }
.floating-icons > div:nth-child(3) { animation-delay: 2s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
} */

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
  font-family: 'Silkscreen', monospace;
  font-size: 1.2rem;
  color: #1DB954;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(29, 185, 84, 0.1);
}

.saved-queue-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  opacity: 0;
  transform: translateX(20px);
  transition: background 0.3s ease;
}

.saved-queue-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.saved-queue-item.is-visible {
  opacity: 1;
  transform: translateX(0);
  animation: slideInRight 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
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

.saved-queue-name {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}

.saved-queue-meta {
  color: #B3B3B3;
  font-size: 0.8rem;
  font-family: 'Inconsolata', monospace;
}

.restore-btn {
  background: transparent;
  border: 1px solid rgba(29, 185, 84, 0.5);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #1DB954;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
}

.restore-btn.featured {
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
  gap: 0.5rem;
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

.restore-track-cover {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
}

.restore-track-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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