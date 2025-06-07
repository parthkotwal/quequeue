from django.shortcuts import render
import requests
import urllib.parse
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from .models import User, Queue, Track
import uuid
import boto3
import mimetypes
from .spotify import SpotifyClient

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_ME_URL = "https://api.spotify.com/v1/me"
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

def login(request):
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": SCOPE,
    }
    full_auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return HttpResponseRedirect(full_auth_url)


@csrf_exempt
def callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data)
    if response.status_code != 200:
        return JsonResponse({"error": "Token exchange failed"}, status=400)
    
    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")


    headers = {"Authorization": f"Bearer {access_token}"}
    user_resp = requests.get(SPOTIFY_ME_URL, headers=headers)
    user_data = user_resp.json()

    spotify_id = user_data.get("id")
    display_name = user_data.get("display_name", "")

    token_expiration = now() + timedelta(seconds=expires_in)


    user, created = User.objects.update_or_create(
        spotify_id=spotify_id,
        defaults={
            "display_name": display_name,
            "access_token": access_token,
            "refresh_token": refresh_token or "",
            "expiration_time": token_expiration,
        },
    )

    request.session["user_id"] = user.id
    return JsonResponse({
        "message": "Login successful", 
        "user": display_name,
        "token_expires": token_expiration.isoformat()
        })


@csrf_exempt
@require_http_methods(["POST"])
def export_queue(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)
    
    body = json.loads(request.body)
    queue_name = body.get("name")
    image_url = body.get("image_url")
    description = body.get("description")

    if not queue_name or not image_url:
        return JsonResponse({"error": "Missing name or image_url"}, status=400)


    user = User.objects.get(id=user_id)
    client = SpotifyClient(user)
    response = client.get("me/player/queue")
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch queue"}, status=500)
    
    queue_data = response.json()
    new_queue = Queue.objects.create(
        user=user,
        name=queue_name,
        image_url=image_url,
        description=description
    )

    def extract_track(track_json):
        return {
            "track_name": track_json.get("name"),
            "track_uri": track_json.get("uri"),
            "artist_name": track_json.get("artists", [{}])[0].get("name"),
            "album_image_url": track_json.get("album", {}).get("images", [{}])[0].get("url"),
        }
    
    tracks = []
    now_playing = queue_data.get("currently_playing")
    if now_playing:
        tracks.append(extract_track(now_playing))

    for track in queue_data.get("queue", []):
        data = extract_track(track)
        tracks.append(data)
    
    for idx, track in enumerate(tracks):
        Track.objects.create(
            queue = new_queue, 
            position = idx,
            **track
        )

    return JsonResponse({"message": "Queue exported to app successfully", "queue_id": new_queue.id})

@csrf_exempt
@require_http_methods(['POST'])
def upload_queue_image(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)
    
    queue_id = request.POST.get("queue_id")
    image_file = request.FILES.get("image")

    if not queue_id or not image_file:
        return JsonResponse({"error": "Missing queue_id or image"}, status=400)
    
    filename = f"queue_covers/{uuid.uuid4()}_{image_file.name}"
    content_type = image_file.content_type or mimetypes.guess_type(image_file.name)[0] or "image/jpeg"

    try:
        settings.S3.upload_fileobj(
            image_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            filename,
            ExtraArgs={
                "ContentType": content_type
            }
        )
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        Queue.objects.filter(id=queue_id, user_id=user_id).update(image_url=image_url)

        return JsonResponse({"image_url": image_url})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@require_http_methods(["GET"])
def restore_queue(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    tracks = queue.tracks.order_by("position")
    if not tracks:
        return JsonResponse({"error": "Queue is empty"}, status=400)
    
    success = 0
    failed = []

    access_token = user.access_token
    client = SpotifyClient(user)
    for track in tracks:
        queue_uri = track.track_uri
        response = client.post("me/player/queue", params={"uri": queue_uri})

        if response.status_code in {204, 200}:
            success += 1
        else:
            failed.append({
                "track": track.track_name,
                "uri": queue_uri,
                "error": response.text
            })

    if success == 0:
        return JsonResponse({
            "error": "Failed to queue any tracks.",
            "details": failed
        }, status=500)

    return JsonResponse({
        "message": f"Restored {success} tracks to the queue.",
        "failures": failed if failed else None
    }, status=207 if failed else 200)


@require_http_methods(['GET'])
def list_user_queues(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    user = get_object_or_404(User, id=user_id)
    queues = Queue.objects.filter(user=user).order_by("-created_at")

    data = [
        {
            "id": q.id,
            "name": q.name,
            "created_at": q.created_at.isoformat(),
            "image_url": q.image_url,
            "description": q.description
        }
        for q in queues
    ]

    return JsonResponse({"queues":data})
