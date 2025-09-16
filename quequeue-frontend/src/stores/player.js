import { reactive } from "vue";
import apiClient from "../api";

export const playerState = reactive({
  player: null,
  deviceId: null,
  ready: false,
  isTransferring: false,
});

// Helper to get fresh token
async function getFreshToken() {
  try {
    const res = await apiClient.get('/get_token/');
    return res.data.access_token;
  } catch (err) {
    console.error('Error fetching token:', err);
    throw err;
  }
}

export async function initSpotifyPlayer(initialToken) {
  // Prevent double initialization
  if (playerState.player) {
    console.log("Player already exists, skipping initialization");
    return playerState.deviceId;
  }

  return new Promise((resolve, reject) => {
    function createPlayer() {
      const player = new window.Spotify.Player({
        name: "QueQueue Web Player",
        getOAuthToken: async (cb) => {
          try {
            // Always fetch fresh token when SDK needs it
            const token = await getFreshToken();
            cb(token);
          } catch (err) {
            console.error("Failed to get fresh token:", err);
            // Fallback to initial token if fetch fails
            cb(initialToken);
          }
        },
        volume: 0.5,
      });

      player.addListener("ready", async ({ device_id }) => {
        console.log("Player ready with device ID", device_id);
        playerState.deviceId = device_id;
        playerState.ready = true;
        playerState.player = player;

        // Don't auto-transfer - let user decide or do it from UI
        // If you want auto-transfer, make it optional
        if (!playerState.isTransferring) {
          console.log("Player ready. Use transfer button to activate playback on this device.");
        }

        resolve(device_id);
      });

      player.addListener("not_ready", ({ device_id }) => {
        console.warn("Device ID has gone offline", device_id);
        playerState.ready = false;
      });

      player.addListener("initialization_error", ({ message }) => {
        console.error("Init error:", message);
        playerState.player = null; // Reset on error
        reject(new Error(message));
      });

      player.addListener("authentication_error", ({ message }) => {
        console.error("Auth error:", message);
        // Clean up the player completely on auth error
        if (playerState.player) {
          playerState.player.disconnect();
        }
        playerState.player = null;
        playerState.ready = false;
        playerState.deviceId = null;
        reject(new Error(message));
      });

      player.addListener("account_error", ({ message }) => {
        console.error("Account error (Premium required):", message);
        // Clean up the player completely on account error
        if (playerState.player) {
          playerState.player.disconnect();
        }
        playerState.player = null;
        playerState.ready = false;
        playerState.deviceId = null;
        reject(new Error(message));
      });

      player.addListener("playback_error", ({ message }) => {
        console.error("Playback error:", message);
      });

      player.connect().then(success => {
        if (!success) {
          console.error("Failed to connect to Spotify");
          playerState.player = null;
          reject(new Error("Failed to connect"));
        }
      });
    }

    // Check if SDK is loaded
    if (window.Spotify) {
      createPlayer();
    } else {
      reject(new Error("Spotify SDK not loaded"));
    }
  });
}

// Manual transfer function with better error handling
export async function transferPlayback(play = false, waitForConfirmation = true) {
  if (!playerState.deviceId) {
    throw new Error("No device ID available");
  }

  playerState.isTransferring = true;
  
  try {
    const res = await apiClient.post("/transfer_player/", {
      device_id: playerState.deviceId,
      play: play
    });

    console.log("Playback transferred successfully", res.data);
    
    // Optionally wait for transfer to be confirmed
    if (waitForConfirmation) {
      let attempts = 0;
      const maxAttempts = 10;
      
      while (attempts < maxAttempts) {
        try {
          await new Promise(resolve => setTimeout(resolve, 500));
          const currentState = await apiClient.get('/current_playback/');
          
          if (currentState.data && currentState.data.device && 
              currentState.data.device.id === playerState.deviceId && 
              currentState.data.device.is_active) {
            console.log("Transfer confirmed - device is now active");
            break;
          }
        } catch (checkErr) {
          console.warn("Error checking transfer status:", checkErr);
        }
        
        attempts++;
      }
      
      if (attempts >= maxAttempts) {
        console.warn("Could not confirm transfer completion, but continuing anyway");
      }
    }
    
    return res.data;
  } catch (err) {
    console.error("Failed to transfer playback:", err.response?.data || err.message);
    throw err;
  } finally {
    playerState.isTransferring = false;
  }
}

// Helper function to ensure device is active before queue operations
export async function ensureActiveDevice() {
  if (!playerState.deviceId || !playerState.ready) {
    throw new Error("Player not ready. Please wait for the player to initialize.");
  }

  try {
    // Check if our device is already active
    const currentStateRes = await apiClient.get('/current_playback/');
    
    if (currentStateRes.data && currentStateRes.data.device && 
        currentStateRes.data.device.id === playerState.deviceId && 
        currentStateRes.data.device.is_active) {
      console.log("Device is already active");
      return true;
    }

    // Transfer playback to our device if not active
    console.log("Transferring playback to web player...");
    await transferPlayback(false); // Don't auto-play
    
    // Wait a moment for transfer to complete
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return true;
  } catch (err) {
    console.error("Failed to ensure active device:", err);
    throw err;
  }
}

// Function to restore queue with proper device activation
export async function restoreQueueWithDeviceCheck(queueData) {
  try {
    // First ensure our device is active
    await ensureActiveDevice();
    
    // Now restore the queue
    const res = await apiClient.post('/restore_queue/', queueData);
    console.log("Queue restored successfully:", res.data);
    return res.data;
  } catch (err) {
    console.error("Failed to restore queue:", err);
    throw err;
  }
}

// Cleanup function
export function disconnectPlayer() {
  if (playerState.player) {
    playerState.player.disconnect();
    playerState.player = null;
    playerState.ready = false;
    playerState.deviceId = null;
  }
}