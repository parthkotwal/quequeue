def serialize_track(track):
    return {
        "id": track.id,
        "track_name": track.track_name,
        "track_uri": track.track_uri,
        "spotify_track_id": track.spotify_track_id,
        "artist_name": track.artist_name,
        "artist_ids": track.artist_ids,
        "album_name": track.album_name,
        "album_image_url": track.album_image_url,
        "release_year": track.release_year,
        "popularity": track.popularity,
        "position": track.position,
    }


def serialize_queue(queue):
    return {
        "id": queue.id,
        "name": queue.name,
        "description": queue.description,
        "created_at": queue.created_at.isoformat(),
        "image_url": queue.image_url,
        "share_token": str(queue.share_token) if queue.share_token else None,
        "tracks": [
            serialize_track(track)
            for track in queue.tracks.order_by("position")
        ],
    }


def serialize_queue_summary(queue):
    return {
        "id": queue.id,
        "name": queue.name,
        "created_at": queue.created_at.isoformat(),
        "image_url": queue.image_url,
        "description": queue.description,
        "share_token": str(queue.share_token) if queue.share_token else None,
    }


def serialize_restore_job(job):
    return {
        "id": job.id,
        "queue_id": job.queue_id,
        "status": job.status,
        "total_tracks": job.total_tracks,
        "succeeded_count": job.succeeded_count,
        "failed_count": job.failed_count,
        "failures": job.failures,
        "error": job.error,
        "created_at": job.created_at.isoformat(),
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
    }
