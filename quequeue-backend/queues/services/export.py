from queues.models import Queue, Track
from queues.spotify import SpotifyClient


def extract_spotify_track(track_json):
    return {
        "track_name": track_json.get("name"),
        "track_uri": track_json.get("uri"),
        "artist_name": track_json.get("artists", [{}])[0].get("name"),
        "album_image_url": track_json.get("album", {}).get("images", [{}])[0].get("url"),
    }


def export_current_spotify_queue(user, *, name, image_url, description=None):
    client = SpotifyClient(user)
    response = client.get("me/player/queue")
    if response.status_code != 200:
        return None, response

    queue_data = response.json()
    queue = Queue.objects.create(
        user=user,
        name=name,
        image_url=image_url,
        description=description,
    )

    tracks = []
    now_playing = queue_data.get("currently_playing")
    if now_playing:
        tracks.append(extract_spotify_track(now_playing))

    for track_json in queue_data.get("queue", []):
        tracks.append(extract_spotify_track(track_json))

    Track.objects.bulk_create(
        Track(queue=queue, position=index, **track)
        for index, track in enumerate(tracks)
    )

    return queue, response
