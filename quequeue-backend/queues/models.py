import uuid
from django.db import models
from django.utils.timezone import now
from fernet_fields import EncryptedCharField

class User(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    access_token = EncryptedCharField(max_length=500)
    refresh_token = EncryptedCharField(max_length=500, blank=True, null=True)
    expiration_time = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.spotify_id

    
class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queues")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(default="https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/queue_covers/default.png")
    description = models.TextField(blank=True, null=True)
    share_token = models.UUIDField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name} ({self.user})"
    
class Track(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name="tracks")
    track_name = models.CharField(max_length=200)
    track_uri = models.CharField(max_length=100, db_index=True)
    spotify_track_id = models.CharField(max_length=100, blank=True, db_index=True)
    artist_name = models.CharField(max_length=200)
    artist_ids = models.JSONField(default=list, blank=True)
    album_name = models.CharField(max_length=200, blank=True)
    album_image_url = models.URLField()
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)
    popularity = models.PositiveSmallIntegerField(blank=True, null=True)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.position}. {self.track_name} by {self.artist_name}"


class QueueRestoreJob(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_SUCCEEDED = "succeeded"
    STATUS_PARTIAL_FAILED = "partial_failed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_SUCCEEDED, "Succeeded"),
        (STATUS_PARTIAL_FAILED, "Partial failed"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restore_jobs")
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name="restore_jobs")
    celery_task_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total_tracks = models.PositiveIntegerField(default=0)
    succeeded_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    failures = models.JSONField(default=list, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Restore job {self.id} for {self.queue}"
