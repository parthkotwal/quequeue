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
    if (!res.ok) {
      throw new Error('Failed to get token');
    }
    const data = await res.json();
    return data.access_token;
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
        playerState.player = null; // Reset on error
        reject(new Error(message));
      });

      player.addListener("account_error", ({ message }) => {
        console.error("Account error (Premium required):", message);
        playerState.player = null; // Reset on error
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

// Manual transfer function
export async function transferPlayback(play = false) {
  if (!playerState.deviceId) {
    throw new Error("No device ID available");
  }

  playerState.isTransferring = true;
  
  try {
    const res = await apiClient.post("/transfer_player/", {
      device_id: playerState.deviceId,
      play: play
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || "Transfer failed");
    }

    const data = await res.json();
    console.log("Playback transferred successfully", data);
    return data;
  } catch (err) {
    console.error("Failed to transfer playback:", err);
    throw err;
  } finally {
    playerState.isTransferring = false;
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