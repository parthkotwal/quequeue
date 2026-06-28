import time

from celery import shared_task
from django.utils.timezone import now

from queues.models import QueueRestoreJob
from queues.spotify import SpotifyClient


def enqueue_track_with_retries(client, track_uri, max_attempts=4):
    for attempt in range(max_attempts):
        response = client.post("me/player/queue", params={"uri": track_uri})
        if response.status_code in {200, 204}:
            return response

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
            time.sleep(min(delay, 30))
            continue

        if 500 <= response.status_code < 600 and attempt < max_attempts - 1:
            time.sleep(min(2 ** attempt, 10))
            continue

        return response

    return response


@shared_task(bind=True)
def restore_queue_job(self, job_id):
    job = QueueRestoreJob.objects.select_related("user", "queue").get(id=job_id)
    tracks = list(job.queue.tracks.order_by("position"))
    job.status = QueueRestoreJob.STATUS_RUNNING
    job.started_at = now()
    job.total_tracks = len(tracks)
    job.save(update_fields=["status", "started_at", "total_tracks"])

    if not tracks:
        job.status = QueueRestoreJob.STATUS_FAILED
        job.error = "Queue is empty"
        job.completed_at = now()
        job.save(update_fields=["status", "error", "completed_at"])
        return

    try:
        client = SpotifyClient(job.user)
        client.ensure_token()

        devices_response = client.get("me/player/devices")
        if devices_response.status_code != 200:
            job.status = QueueRestoreJob.STATUS_FAILED
            job.error = "Failed to fetch devices"
            job.completed_at = now()
            job.save(update_fields=["status", "error", "completed_at"])
            return

        devices = devices_response.json().get("devices", [])
        active_device = next((device for device in devices if device.get("is_active")), None)
        if not active_device:
            job.status = QueueRestoreJob.STATUS_FAILED
            job.error = "NO_ACTIVE_DEVICE"
            job.completed_at = now()
            job.save(update_fields=["status", "error", "completed_at"])
            return

        failures = []
        succeeded_count = 0
        for track in tracks:
            response = enqueue_track_with_retries(client, track.track_uri)
            if response.status_code in {200, 204}:
                succeeded_count += 1
            else:
                failures.append({
                    "track": track.track_name,
                    "uri": track.track_uri,
                    "status_code": response.status_code,
                    "error": response.text,
                })

            job.succeeded_count = succeeded_count
            job.failed_count = len(failures)
            job.failures = failures
            job.save(update_fields=["succeeded_count", "failed_count", "failures"])

        if succeeded_count == 0:
            job.status = QueueRestoreJob.STATUS_FAILED
            job.error = "Failed to queue any tracks."
        elif failures:
            job.status = QueueRestoreJob.STATUS_PARTIAL_FAILED
        else:
            job.status = QueueRestoreJob.STATUS_SUCCEEDED

        job.completed_at = now()
        job.save(update_fields=["status", "error", "completed_at"])
    except Exception as exc:
        job.status = QueueRestoreJob.STATUS_FAILED
        job.error = str(exc)
        job.completed_at = now()
        job.save(update_fields=["status", "error", "completed_at"])
        raise
