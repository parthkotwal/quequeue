import time

from queues.spotify import SpotifyClient


def restore_saved_queue_to_spotify(user, queue):
    start = time.time()
    tracks = list(queue.tracks.order_by("position"))
    if not tracks:
        return {
            "status": 400,
            "payload": {"error": "Queue is empty"},
        }

    client = SpotifyClient(user)
    client.ensure_token()

    devices_response = client.get("me/player/devices")
    if devices_response.status_code != 200:
        return {
            "status": devices_response.status_code,
            "payload": {
                "error": "Failed to fetch devices",
                "details": devices_response.text,
            },
        }

    devices = devices_response.json().get("devices", [])
    active_device = next((device for device in devices if device.get("is_active")), None)
    if not active_device:
        return {
            "status": 400,
            "payload": {
                "error": "NO_ACTIVE_DEVICE",
                "message": "Please start playback in Spotify first.",
            },
        }

    success = 0
    failures = []
    for track in tracks:
        response = client.post("me/player/queue", params={"uri": track.track_uri})
        if response.status_code in {200, 204}:
            success += 1
            continue

        failures.append({
            "track": track.track_name,
            "uri": track.track_uri,
            "error": response.text,
        })

    if success == 0:
        return {
            "status": 500,
            "payload": {
                "error": "Failed to queue any tracks.",
                "details": failures,
            },
        }

    elapsed = time.time() - start
    return {
        "status": 207 if failures else 200,
        "payload": {
            "message": f"Restored {success} tracks to the queue.",
            "failures": failures if failures else None,
            "elapsed_time": f"{elapsed:.2f}s",
        },
    }
