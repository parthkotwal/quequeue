import { reactive } from "vue";

export const playerState = reactive({
  player: null,
  deviceId: null,
  ready: false,
});

export function initSpotifyPlayer(token) {
  return new Promise((resolve, reject) => {
    if (!window.Spotify) {
      reject("Spotify SDK not loaded");
      return;
    }

    const player = new window.Spotify.Player({
      name: "QueQueue Web Player",
      getOAuthToken: cb => cb(token),
      volume: 0.8,
    });

    player.addListener("ready", ({ device_id }) => {
      console.log("Player ready with device ID", device_id);
      playerState.deviceId = device_id;
      playerState.ready = true;
      resolve(device_id);
    });

    player.addListener("not_ready", ({ device_id }) => {
      console.warn("Device ID has gone offline", device_id);
      playerState.ready = false;
    });

    player.addListener("initialization_error", ({ message }) => {
      console.error("Init error:", message);
      reject(message);
    });

    player.addListener("authentication_error", ({ message }) => {
      console.error("Auth error:", message);
      reject(message);
    });

    player.addListener("account_error", ({ message }) => {
      console.error("Account error:", message);
      reject(message);
    });

    player.connect();
    playerState.player = player;
  });
}
