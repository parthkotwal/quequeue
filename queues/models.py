from django.db import models

class User(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.spotify_id
    
class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queues")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(default="https://example.com/default.jpg")

    def __str__(self):
        return f"{self.name} ({self.user})"
    
class Track(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name="tracks")
    track_name = models.CharField(max_length=200)
    track_uri = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=200)
    album_image_url = models.URLField()
    position = models.IntegerField()

    def __str__(self):
        return f"{self.position}. {self.track_name} by {self.artist_name}"