from queues.models import Queue, Track
from queues.spotify import SpotifyClient


def spotify_id_from_uri(uri):
    if not uri:
        return ""
    return uri.rsplit(":", 1)[-1]


def release_year_from_date(release_date):
    if not release_date:
        return None
    try:
        return int(release_date[:4])
    except (TypeError, ValueError):
        return None


def first_album_image_url(album):
    images = album.get("images") or []
    return images[0].get("url") if images else ""


def extract_spotify_track(track_json):
    artists = track_json.get("artists", [])
    album = track_json.get("album", {})
    uri = track_json.get("uri")

    return {
        "track_name": track_json.get("name"),
        "track_uri": uri,
        "spotify_track_id": track_json.get("id") or spotify_id_from_uri(uri),
        "artist_name": artists[0].get("name") if artists else "",
        "artist_ids": [
            artist.get("id") for artist in artists if artist.get("id")
        ],
        "album_name": album.get("name", ""),
        "album_image_url": first_album_image_url(album),
        "release_year": release_year_from_date(album.get("release_date")),
        "popularity": track_json.get("popularity"),
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
