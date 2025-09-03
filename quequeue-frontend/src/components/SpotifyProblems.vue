<template>
  <div class="problems-container">
    <!-- Section Header -->
    <div class="problems-header" :class="{ 'is-visible': isVisible }">
      <h2 class="problems-title">The Problem with Spotify</h2>
      <p class="problems-subtitle">
        Fact: Your perfect queue has a shorter lifespan than a
        <a class="mayfly-link" href="https://en.wikipedia.org/wiki/Mayfly" target="_blank" rel="noopener">mayfly!</a>
      </p>
    </div>

    <!-- Problems Timeline -->
    <div class="problems-timeline">
      <!-- Timeline Line -->
      <div class="timeline-line" :class="{ 'is-visible': isVisible }">
        <div class="timeline-progress"></div>
      </div>

      <!-- Problem Scenarios -->
      <div class="scenario-container">
        <!-- Scenario 1: The Perfect Queue -->
        <div class="scenario perfect-queue" :class="{ 'is-visible': isVisible }" style="animation-delay: 300ms">
          <div class="scenario-number">1</div>
          <div class="scenario-content">
            <div class="scenario-visual">
              <div class="queue-visualization healthy">
                <div class="queue-header">
                  <div class="spotify-dot-mini"></div>
                  <span class="queue-title">Your Queue</span>
                </div>
                <div class="track-stack" :class="{ 'animate-build': isVisible }">
                  <div
                    class="track-item"
                    v-for="(track, i) in 4"
                    :key="i"
                    :style="{ animationDelay: `${i * 100}ms` }"
                  >
                    <div class="track-dot"></div>
                    <div class="track-bar"></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="scenario-text">
              <h3>The Perfect Queue</h3>
              <p>You've crafted the ultimate vibe for that party, road trip, or study session. Every song flows perfectly into the next.</p>
            </div>
          </div>
        </div>

        <!-- Scenario 2: The Disruption -->
        <div class="scenario disruption" :class="{ 'is-visible': isVisible }" style="animation-delay: 600ms">
          <div class="scenario-number">2</div>
          <div class="scenario-content">
            <div class="scenario-visual">
              <div class="disruption-scene">
                <!-- User Action -->
                <div class="user-action" :class="{ 'trigger': isVisible }">
                  <div class="action-options">
                    <div
                      v-for="opt in actionOptions"
                      :key="opt"
                      class="action-option"
                      :class="{ 'selected': selectedAction === opt }"
                      @click="selectAction(opt)"
                      role="button"
                      :aria-pressed="selectedAction === opt"
                      tabindex="0"
                      @keydown.enter.prevent="selectAction(opt)"
                      @keydown.space.prevent="selectAction(opt)"
                    >
                      {{ opt }}
                    </div>
                  </div>
                </div>

                <!-- Danger Zone -->
                <div class="danger-zone" :class="{ 'active': !!selectedAction }" aria-live="polite">
                  <div class="warning-icon">⚠️</div>
                  <div class="danger-text">
                    {{ selectedAction ? 'Queue at Risk' : 'Choose an action' }}
                  </div>
                </div>
              </div>
            </div>
            <div class="scenario-text">
              <h3>The Moment of Truth</h3>
              <p>You click something. Anything. Your queue holds its breath.</p>
            </div>
          </div>
        </div>

        <!-- Scenario 3: The Death -->
        <div class="scenario death" :class="{ 'is-visible': isVisible }" style="animation-delay: 900ms">
          <div class="scenario-number">3</div>
          <div class="scenario-content">
            <div class="scenario-visual">
              <div class="queue-visualization dead">
                <div class="queue-header faded">
                  <div class="spotify-dot-dead"></div>
                  <span class="queue-title">Your Queue</span>
                </div>

                <!-- Tombstone -->
                <div class="tombstone">
                  <div class="tombstone-top-shine"></div>
                  <div class="epitaph">
                    <div class="grave-icon" aria-hidden="true">🪦</div>
                    <div class="death-text">R.I.P.</div>
                    <div class="death-date">2024 – 2024</div>
                    <div class="epitaph-divider"></div>
                    <div class="empty-text">Nothing to play</div>
                  </div>
                  <div class="tombstone-shadow"></div>
                </div>
              </div>
            </div>
            <div class="scenario-text">
              <h3>Queue Obliterated</h3>
              <p>Gone. Vanished. Like it never existed. Your vibe just flatlined.</p>
            </div>
          </div>
        </div>

        <!-- Scenario 4: The Regret -->
        <div class="scenario regret" :class="{ 'is-visible': isVisible }" style="animation-delay: 1200ms">
          <div class="scenario-number">4</div>
          <div class="scenario-content">
            <div class="scenario-visual">
              <div class="regret-scene">
                <div class="thought-bubble" :class="{ 'visible': isVisible }" role="img" aria-label="Remembering a lost queue">
                  <div class="thought-content">
                    <div class="memory-icon">🧠</div>
                    <div class="memory-text">What was that queue from the gym?</div>
                  </div>
                  <div class="thought-tail"></div>
                </div>

                <div class="sad-user">
                  <div class="user-icon" aria-hidden="true">😭</div>
                  <div class="regret-text">Forever Lost</div>
                </div>
              </div>
            </div>
            <div class="scenario-text">
              <h3>The Eternal Question</h3>
              <p>You'll spend the rest of your life wondering what could have been.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Solution Bridge -->
    <div class="solution-bridge" :class="{ 'is-visible': isVisible }">
      <div class="bridge-content">
        <div class="bridge-icon">💡</div>
        <div class="bridge-text">
          <h3>What if queues didn't have to die?</h3>
          <p>Introducing a revolutionary queue resurrection technology.</p>
        </div>
        <div class="bridge-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 19V5M19 12l-7 7-7-7"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isVisible = ref(false)

/* Scenario 2: interactive action state */
const actionOptions = ['New Playlist', 'Switch Device', "Friend's Song"]
const selectedAction = ref(null)
const selectAction = (opt) => {
  selectedAction.value = opt
}

// Expose the visibility setter for parent component
defineExpose({
  setVisible: (visible) => {
    isVisible.value = visible
  }
})
</script>

<style scoped>
.problems-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.problems-header {
  text-align: center;
  margin-bottom: 4rem;
  opacity: 0;
  transform: translateY(-30px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.problems-header.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.problems-title {
  font-family: 'Silkscreen', monospace;
  font-size: clamp(2.5rem, 5vw, 4rem);
  color: #FFD700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #FFD700, #FF6B6B);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.problems-subtitle {
  font-family: 'Inconsolata', monospace;
  font-size: 1.2rem;
  color: #B3B3B3;
  max-width: 600px;
  margin: 0 auto;
}

/* Fancy mayfly link */
.mayfly-link {
  position: relative;
  color: #FFD700;
  text-decoration: none;
  padding-inline: 2px;
  border-bottom: 1px dotted rgba(255, 215, 0, 0.6);
  transition: color .2s ease, text-shadow .2s ease, transform .2s ease;
}
.mayfly-link::after {
  /* tiny wing accent */
  content: '🪰';
  position: absolute;
  top: -0.9em;
  right: -0.6em;
  font-size: .8em;
  transform: rotate(15deg);
  opacity: .8;
  transition: transform .3s ease;
}
.mayfly-link:hover {
  color: #FFF4A3;
  text-shadow: 0 0 10px rgba(255, 215, 0, .35);
  transform: translateY(-1px);
}
.mayfly-link:hover::after {
  transform: translateY(-2px) rotate(25deg);
}

/* Timeline Structure */
.problems-timeline {
  position: relative;
  margin-bottom: 4rem;
}

.timeline-line {
  position: absolute;
  top: 60px;
  left: 5%;
  right: 5%;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), rgba(255, 107, 107, 0.8), transparent);
  border-radius: 2px;
  opacity: 0;
  transition: opacity 1s ease 0.5s;
}

.timeline-line.is-visible {
  opacity: 1;
}

.timeline-progress {
  height: 100%;
  background: linear-gradient(90deg, #FFD700, #FF6B6B);
  border-radius: 2px;
  width: 0;
  transition: width 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1s;
}

.timeline-line.is-visible .timeline-progress {
  width: 100%;
}

.scenario-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  position: relative;
  align-items: stretch;
}

/* Scenario Cards - Fixed height and alignment */
.scenario {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
  height: 100%;
  min-height: 420px;
}

.scenario.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.scenario-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #121212;
  font-family: 'Silkscreen', monospace;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

.scenario.death .scenario-number {
  background: linear-gradient(135deg, #FF6B6B, #FF4757);
}

.scenario-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.scenario-visual {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.scenario.perfect-queue .scenario-visual {
  border-color: rgba(29, 185, 84, 0.3);
  background: linear-gradient(145deg, rgba(29, 185, 84, 0.05), rgba(29, 185, 84, 0.02));
}

.scenario.death .scenario-visual {
  border-color: rgba(255, 107, 107, 0.3);
  background: linear-gradient(145deg, rgba(255, 107, 107, 0.05), rgba(255, 107, 107, 0.02));
}

.scenario-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 120px;
}

.scenario-text h3 {
  margin-top: 0;
}

/* Perfect Queue Visual */
.queue-visualization {
  padding: 1rem;
  width: 100%;
}

.queue-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  opacity: 1;
  transition: opacity 0.8s ease;
}

.queue-header.faded {
  opacity: 0.35;
}

.spotify-dot-mini {
  width: 8px;
  height: 8px;
  background: #1DB954;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.spotify-dot-dead {
  width: 8px;
  height: 8px;
  background: #666;
  border-radius: 50%;
}

.queue-title {
  font-size: 0.8rem;
  color: #B3B3B3;
  font-weight: 600;
}

.track-stack {
  margin-bottom: 1rem;
}

.track-stack.animate-build .track-item {
  animation: buildTrack 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
  opacity: 0;
  transform: translateX(-20px);
}

.track-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.25rem 0;
}

.track-dot {
  width: 6px;
  height: 6px;
  background: linear-gradient(45deg, #FFD700, #1DB954);
  border-radius: 50%;
  flex-shrink: 0;
}

.track-bar {
  height: 3px;
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.6), rgba(29, 185, 84, 0.6));
  border-radius: 2px;
  flex: 1;
}

/* Disruption Scene */
.disruption-scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  width: 100%;
  height: 100%;
}

.user-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.action-options {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.action-option {
  padding: 0.35rem 0.9rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid transparent;
  border-radius: 12px;
  font-size: 0.78rem;
  color: #B3B3B3;
  transition: all 0.2s ease;
  cursor: pointer;
  user-select: none;
}
.action-option:hover {
  background: rgba(255, 255, 255, 0.12);
}
.action-option.selected {
  background: rgba(255, 107, 107, 0.15);
  border-color: rgba(255, 107, 107, 0.5);
  color: #FF8C8C;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(255, 107, 107, 0.25);
}

.danger-zone {
  opacity: 0.4;
  transform: scale(0.95);
  transition: all 0.35s ease;
  text-align: center;
}
.danger-zone.active {
  opacity: 1;
  transform: scale(1);
}
.warning-icon {
  font-size: 1.8rem;
  margin-bottom: 0.25rem;
}
.danger-text {
  font-size: 0.85rem;
  color: #FF6B6B;
  font-weight: 700;
  font-family: 'Silkscreen', monospace;
}

/* Death / Tombstone */
.tombstone {
  position: relative;
  width: min(180px, 70%);
  margin: 0.25rem auto 0.5rem;
  aspect-ratio: 3 / 4;
  background: radial-gradient(120% 100% at 50% 0%, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.03) 40%, rgba(0,0,0,0.12) 100%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-bottom-width: 2px;
  border-radius: 22px 22px 10px 10px / 30px 30px 10px 10px; /* arched top */
  box-shadow: inset 0 8px 24px rgba(0,0,0,0.25), 0 20px 30px rgba(0,0,0,0.25);
  display: grid;
  place-items: center;
  padding: 1rem 0.75rem;
}
.tombstone::before {
  /* subtle grain */
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background-image:
    radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 6px 6px, 10px 10px;
  background-position: 0 0, 3px 3px;
  pointer-events: none;
}
.tombstone-top-shine {
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 10px;
  background: linear-gradient(180deg, rgba(255,255,255,0.25), rgba(255,255,255,0));
  border-radius: 10px;
  filter: blur(1px);
  pointer-events: none;
}
.tombstone-shadow {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 70%;
  height: 12px;
  background: radial-gradient(50% 100% at 50% 0%, rgba(0,0,0,0.45), transparent 80%);
  border-radius: 50%;
  filter: blur(6px);
}
.epitaph {
  text-align: center;
  display: grid;
  gap: 0.15rem;
  align-content: center;
}
.grave-icon {
  font-size: 1.8rem;
  line-height: 1;
}
.death-text {
  font-family: 'Silkscreen', monospace;
  color: #FF7575;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.08em;
}
.death-date {
  font-size: 0.7rem;
  color: #9a9a9a;
  font-style: italic;
}
.epitaph-divider {
  width: 60%;
  height: 1px;
  margin: 0.2rem auto 0.1rem;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.empty-text {
  font-size: 0.75rem;
  color: #b0b0b0;
  font-style: italic;
}

/* Regret Scene */
.regret-scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem; /* Reduced gap to bring elements closer */
  padding: 1rem;
  width: 100%;
  height: 100%;
  position: relative;
}

/* ensure bubble can float above the card nicely */
.scenario.regret .scenario-visual {
  overflow: visible;
}

.thought-bubble {
  position: relative;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.6s ease;
  text-align: center;
  padding: 1rem 0.9rem 0.9rem;
  border-radius: 20px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.12);
  width: 160px;
  margin-bottom: 1rem;
}
.thought-bubble.visible {
  opacity: 1;
  transform: translateY(0);
}

/* cloud top made of soft circles */
.thought-cloud,
.thought-cloud::before,
.thought-cloud::after {
  content: '';
  position: absolute;
  top: -16px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  filter: blur(0.2px);
}
.thought-cloud {
  left: 50%;
  transform: translateX(-50%);
  width: 100px; height: 28px;
}
.thought-cloud::before {
  left: -30px; top: 4px;
  width: 24px; height: 24px;
}
.thought-cloud::after {
  left: 90px; top: 6px;
  width: 20px; height: 20px;
}

/* tail */
.thought-tail {
  position: absolute;
  bottom: -10px; left: 50%;
  transform: translateX(-50%);
  width: 0; height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid rgba(255,255,255,0.12);
}

.memory-icon {
  font-size: 1.3rem;
  margin-bottom: 0.4rem;
}
.memory-text {
  font-size: 0.75rem;
  color: #B3B3B3;
  margin-bottom: 0.45rem;
  line-height: 1.35;
}
.memory-fade {
  display: flex;
  gap: 0.25rem;
  justify-content: center;
}
.memory-fade span {
  color: #FFD700;
  font-weight: 700;
  animation: questionFade 1.5s ease-in-out infinite;
}
.memory-fade span:nth-child(2) { animation-delay: 0.3s; }
.memory-fade span:nth-child(3) { animation-delay: 0.6s; }

.sad-user {
  display: grid;
  place-items: center;
  text-align: center;
}
.user-icon {
  font-size: 2rem;
  margin-top: 0.25rem;
  margin-bottom: 0.1rem;
  line-height: 1;
}
.regret-text {
  font-size: 0.8rem;
  color: #b0b0b0;
  font-style: italic;
  line-height: 1.2;
  margin-top: 0.1rem;
}

/* Scenario Text */
.scenario-text h3 {
  font-family: 'Silkscreen', monospace;
  color: #FFD700;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.scenario.death .scenario-text h3 {
  color: #FF6B6B;
}

.scenario-text p {
  font-family: 'Inconsolata', monospace;
  color: #B3B3B3;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
}

/* Solution Bridge */
.solution-bridge {
  text-align: center;
  background: linear-gradient(145deg, rgba(29, 185, 84, 0.08), rgba(29, 185, 84, 0.03));
  border: 1px solid rgba(29, 185, 84, 0.2);
  border-radius: 30px;
  padding: 3rem 2rem;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1) 1.5s;
  position: relative;
  overflow: hidden;
}

.solution-bridge::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(29, 185, 84, 0.05) 0%, transparent 70%);
  animation: rotateGlow 20s linear infinite;
}

.solution-bridge.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.bridge-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.bridge-icon {
  font-size: 4rem;
  filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.4));
}

.bridge-text h3 {
  font-family: 'Silkscreen', monospace;
  color: #1DB954;
  font-size: 1.8rem;
  margin-bottom: 0.75rem;
}

.bridge-text p {
  font-family: 'Inconsolata', monospace;
  color: #B3B3B3;
  font-size: 1.1rem;
}

.bridge-arrow {
  color: #1DB954;
  width: 3rem;
  height: 3rem;
  animation: bounceDown 2s ease-in-out infinite;
}

/* Animations */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

@keyframes buildTrack {
  to { opacity: 1; transform: translateX(0); }
}

@keyframes questionFade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

@keyframes bounceDown {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

@keyframes rotateGlow {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .scenario-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem 2rem;
  }
  .timeline-line { display: none; }
}

@media (max-width: 768px) {
  .scenario-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .scenario {
    min-height: 380px;
  }
  .scenario-visual { 
    height: 180px;
    margin-bottom: 1rem;
  }
  .problems-title { font-size: 2rem; }
  .bridge-text h3 { font-size: 1.4rem; }
}

/* Reduce motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .bridge-icon { animation: none !important; }
}
</style>