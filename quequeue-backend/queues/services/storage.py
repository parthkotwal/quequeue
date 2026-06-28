from urllib.parse import urlparse

from django.conf import settings


DEFAULT_QUEUE_COVER_KEY = "queue_covers/default.png"


def s3_configured():
    return bool(settings.S3 and settings.AWS_STORAGE_BUCKET_NAME)


def s3_key_from_url(url):
    if not url:
        return None

    parsed = urlparse(url)
    if not parsed.netloc.endswith(".amazonaws.com"):
        return None

    key = parsed.path.lstrip("/")
    return key or None


def delete_queue_cover(image_url):
    if not s3_configured():
        return False

    key = s3_key_from_url(image_url)
    if not key or key == DEFAULT_QUEUE_COVER_KEY:
        return False

    settings.S3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
    return True
