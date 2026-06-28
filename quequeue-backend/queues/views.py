from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from .models import User, Queue, Track
from .spotify import SpotifyClient
from functools import wraps
from django_ratelimit.decorators import ratelimit
import time
import requests
import urllib.parse
import json
import uuid
import secrets
from PIL import Image
import logging
from tempfile import NamedTemporaryFile

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_ME_URL = "https://api.spotify.com/v1/me"
REQUIRED_SCOPES = {
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-library-read",
    "streaming",
    "user-read-email", 
    "user-read-private"
}

logger = logging.getLogger(__name__)



def health(request):
    return HttpResponse("OK", status=200)


def login(request):
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": " ".join(REQUIRED_SCOPES),
        "show_dialog": "true",
        "state": state,
    }
    full_auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    response = HttpResponseRedirect(full_auth_url)
    response.set_cookie(
        "oauth_state",
        state,
        max_age=600,
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    return response


@csrf_exempt
def callback(request):
    state = request.GET.get("state")
    expected_state = request.COOKIES.get("oauth_state")
    logger.info(f"OAuth callback - state from URL: {state}")
    logger.info(f"OAuth callback - state from cookie: {expected_state}")
    logger.info(f"OAuth callback - all cookies: {list(request.COOKIES.keys())}")
    if not state or state != expected_state:
        return JsonResponse({"error": "Invalid OAuth state"}, status=403)

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

    granted_scopes = set(token_data.get("scope", "").split())
    if not REQUIRED_SCOPES.issubset(granted_scopes):
        print(granted_scopes)

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
    request.session["user_display_name"] = display_name
    request.session.save()

    response = HttpResponseRedirect(f"{settings.FRONTEND_URL.rstrip('/')}/auth-callback?status=ok")
    response.delete_cookie("oauth_state")
    return response


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if "user_id" not in request.session:
            return JsonResponse({"authenticated": False}, status=401)
    
        try:
            user = User.objects.get(pk=request.session["user_id"])
        except User.DoesNotExist:
            request.session.flush()
            return JsonResponse({"authenticated": False}, status=401)
            
        return view_func(request, *args, **kwargs)
    return wrapped_view

@login_required
def verify_auth(request):
    try:
        user = get_object_or_404(User, pk=request.session["user_id"])
        return JsonResponse({
            "authenticated": True,
            "user_display_name": user.display_name
        })
    except (User.DoesNotExist, KeyError):
        request.session.flush()
        return JsonResponse({"authenticated": False}, status=401)
    
@login_required
@require_http_methods(["GET"])
def get_token(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    try:
        client = SpotifyClient(user)
        client.ensure_token()

        return JsonResponse({
            "access_token": client.access_token,
            "expires_at": user.expiration_time.isoformat(),
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
def current_user(request):
    user = get_object_or_404(User, pk=request.session["user_id"])
    return JsonResponse({
        "authenticated": True,
        "user_id": user.id,
        "display_name": user.display_name,
        "spotify_id": user.spotify_id,
    })

@csrf_exempt
@require_http_methods(["POST"])
@login_required
@ratelimit(key='user_or_ip', rate='30/m', block=True)
def transfer_player(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    data = json.loads(request.body.decode("utf-8"))
    device_id = data.get("device_id")

    if not device_id:
        return JsonResponse({"error": "Missing device_id"}, status=400)

    try:
        client = SpotifyClient(user)
        resp = client.put("me/player", data={
            "device_ids": [device_id],
            "play": True,
        })

        if resp.status_code not in (200, 204):
            return JsonResponse({
                "error": "Spotify API error",
                "status_code": resp.status_code,
                "response": resp.json()
            }, status=resp.status_code)

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@login_required
@require_http_methods(["GET"])
@ratelimit(key='user_or_ip', rate='60/m', block=True)
def current_playback(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    client = SpotifyClient(user)
    
    # This Spotify endpoint gets the user's current playback state
    response = client.get("me/player")

    if response.status_code == 200:
        return JsonResponse(response.json())
    elif response.status_code == 204:
        # 204 No Content means nothing is playing
        return JsonResponse({}, status=200)
    else:
        return JsonResponse(response.json(), status=response.status_code)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Log out the current user by clearing the session."""
    request.session.flush()
    return JsonResponse({"message": "Logged out successfully"})

@csrf_exempt
@require_http_methods(["POST"])
@ratelimit(key='user_or_ip', rate='10/m', block=True)
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

    return JsonResponse({"message": "Queue exported to app successfully!", "queue_id": new_queue.id})

@csrf_exempt
@require_http_methods(["POST"])
def cancel_export(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        queue_id = data.get("queue_id")
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "Missing queue_id"}, status=400)

    queue = Queue.objects.filter(id=queue_id, user_id=user_id).first()
    if not queue:
        return JsonResponse({"error": "Queue not found"}, status=404)

    if queue.image_url:
        key = queue.image_url.split(".amazonaws.com/")[1]
        settings.S3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)

    queue.delete()
    return JsonResponse({"message": "Export canceled, queue deleted"})

@csrf_exempt
@require_http_methods(['POST'])
@ratelimit(key='user_or_ip', rate='10/m', block=True)
def upload_image(request):
    MAX_FILE_SIZE = 50 * 1024 * 1024  # Increased to 50MB
    ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
    
    logger.info(f"Upload request received. Content-Length: {request.META.get('CONTENT_LENGTH', 'Unknown')}")
    logger.info(f"Content-Type: {request.META.get('CONTENT_TYPE', 'Unknown')}")
    
    user_id = request.session.get("user_id")
    if not user_id:
        logger.warning("Upload attempt without authentication")
        return JsonResponse({"error": "Not logged in"}, status=401)
    
    try:
        queue_id = request.POST.get("queue_id")
        image_file = request.FILES.get("image")
        
        logger.info(f"Queue ID: {queue_id}")
        logger.info(f"Image file: {image_file.name if image_file else 'None'}")
        logger.info(f"Image size: {image_file.size if image_file else 'None'} bytes")

        if not queue_id or not image_file:
            logger.error("Missing queue_id or image")
            return JsonResponse({"error": "Missing queue_id or image"}, status=400)

        # Validate file size
        if image_file.size > MAX_FILE_SIZE:
            logger.error(f"Image too large: {image_file.size} bytes (max: {MAX_FILE_SIZE})")
            return JsonResponse({"error": f"Image too large (max {MAX_FILE_SIZE//1024//1024}MB)"}, status=400)

        # Validate content type
        content_type = image_file.content_type.lower()
        logger.info(f"Detected content type: {content_type}")
        
        if content_type not in ALLOWED_TYPES:
            logger.error(f"Invalid content type: {content_type}")
            return JsonResponse({"error": "Invalid image format"}, status=400)

        filename = f"queue_covers/{uuid.uuid4()}_{image_file.name}"
        logger.info(f"Processing filename: {filename}")

        # Process image in chunks to reduce memory usage
        img = Image.open(image_file)
        logger.info(f"Original image size: {img.size}, mode: {img.mode}")
        
        # Convert only if needed
        if img.mode != 'RGB':
            img = img.convert("RGB")
            logger.info("Converted image to RGB")

        # Calculate crop dimensions
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        # Crop and resize in one operation if possible
        target_size = (512, 512)
        img = img.crop((left, top, right, bottom)).resize(
            target_size, 
            Image.Resampling.LANCZOS
        )
        logger.info(f"Processed image to size: {img.size}")

        # Use a temporary file instead of BytesIO to reduce memory usage
        with NamedTemporaryFile() as tmp:
            img.save(tmp, format="JPEG", quality=85, optimize=True)
            tmp.seek(0)
            
            logger.info("Starting S3 upload...")
            settings.S3.upload_fileobj(
                tmp,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={
                    "ContentType": "image/jpeg"
                }
            )
            logger.info("S3 upload completed")

        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        updated = Queue.objects.filter(id=queue_id, user_id=user_id).update(image_url=image_url)
        
        if not updated:
            logger.error(f"Queue {queue_id} not found for user {user_id}")
            return JsonResponse({"error": "Queue not found"}, status=404)
        
        logger.info(f"Successfully uploaded image: {image_url}")
        return JsonResponse({"image_url": image_url})
    
    except Exception as e:
        logger.error(f"Image upload failed: {str(e)}", exc_info=True)
        return JsonResponse({"error": f"Failed to process image: {str(e)}"}, status=500)

@require_http_methods(['GET'])
def get_queue(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, user=user, id=queue_id)

    track_data = [
        {
            "id": t.id,
            "track_name": t.track_name,
            "track_uri": t.track_uri,
            "artist_name": t.artist_name,
            "album_image_url": t.album_image_url,
            "position": t.position
        }
        for t in queue.tracks.order_by("position")
    ]

    return JsonResponse({
        "id": queue.id,
        "name": queue.name,
        "description": queue.description,
        "created_at": queue.created_at.isoformat(),
        "image_url": queue.image_url,
        "share_token": str(queue.share_token) if queue.share_token else None,
        "tracks": track_data,
    })


@csrf_exempt
@require_http_methods(["PATCH"])
def update_queue(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    

    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")

    if name:
        queue.name = name
    
    if description is not None:
        queue.description = description

    if image_url:
        queue.image_url = image_url

    queue.save()
    return JsonResponse({"message": "Queue updated successfully"})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_queue(request, queue_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    if queue.image_url:
        key = queue.image_url.split(".amazonaws.com/")[1]
        settings.S3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)

    queue.delete()
    
    return JsonResponse({"message": "Queue deleted"})

@csrf_exempt
@require_http_methods(["POST"])
def add_track_to_queue(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    try:
        data = json.loads(request.body)
        track_uri = data["track_uri"]
        track_name = data.get("track_name", "")
        artist_name = data.get("artist_name", "")
        album_image_url = data.get("album_image_url", "")
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "Missing or invalid track data"}, status=400)

    queue = get_object_or_404(Queue, id=queue_id, user_id=user_id)
    
    # Determine next position
    last_track = queue.tracks.order_by("-position").first()
    next_position = (last_track.position + 1) if last_track else 0

    track = Track.objects.create(
        queue=queue,
        track_uri=track_uri,
        track_name=track_name,
        artist_name=artist_name,
        album_image_url=album_image_url,
        position=next_position
    )

    return JsonResponse({
        "message": "Track added",
        "track": {
            "id": track.id,
            "track_uri": track.track_uri,
            "track_name": track.track_name,
            "artist_name": track.artist_name,
            "album_image_url": track.album_image_url,
            "position": track.position
        }
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_track_from_queue(request, queue_id:int, track_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    queue = get_object_or_404(Queue, id=queue_id, user_id=user_id)
    track = get_object_or_404(Track, id=track_id, queue=queue)

    track.delete()

    # Reorder remaining tracks
    for idx, t in enumerate(queue.tracks.order_by("position")):
        if t.position != idx:
            t.position = idx
            t.save()

    return JsonResponse({
        "message": "Track removed successfully",
        "remaining_tracks": [
            {
                "id": t.id,
                "track_name": t.track_name,
                "track_uri": t.track_uri,
                "artist_name": t.artist_name,
                "album_image_url": t.album_image_url,
                "position": t.position,
            }
            for t in queue.tracks.order_by("position")
        ]
    })



@csrf_exempt
@require_http_methods(["POST"])
@ratelimit(key='user_or_ip', rate='30/m', block=True)
def play_track(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    client = SpotifyClient(user)
    
    response = client.put("me/player/play")
    
    if response.status_code == 204:
        return JsonResponse({"message": "Playback started"})
    else:
        return JsonResponse({"error": "Failed to start playback"}, status=response.status_code)


@csrf_exempt
@require_http_methods(["POST"])
@ratelimit(key='user_or_ip', rate='30/m', block=True)
def pause_track(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    client = SpotifyClient(user)

    response = client.put("me/player/pause")

    if response.status_code == 204:
        return JsonResponse({"message": "Playback paused"})
    else:
        return JsonResponse({"error": "Failed to pause playback"}, status=response.status_code)


@require_http_methods(["GET"])
@ratelimit(key='user_or_ip', rate='5/m', block=True)
def restore_queue(request, queue_id: int):
    start = time.time()
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    tracks = list(queue.tracks.order_by("position"))
    if not tracks:
        return JsonResponse({"error": "Queue is empty"}, status=400)

    client = SpotifyClient(user)
    client.ensure_token()

    # Step 1: Check devices
    devices_resp = client.get("me/player/devices")
    if devices_resp.status_code != 200:
        return JsonResponse(
            {"error": "Failed to fetch devices", "details": devices_resp.text},
            status=devices_resp.status_code,
        )

    devices = devices_resp.json().get("devices", [])
    active_device = next((d for d in devices if d.get("is_active")), None)

    if not active_device:
        # No active Spotify app (mobile often goes inactive in background)
        return JsonResponse(
            {"error": "NO_ACTIVE_DEVICE", "message": "Please start playback in Spotify first."},
            status=400,
        )

    # Step 2: Enqueue tracks into active device
    success = 0
    failed = []

    for track in tracks:
        uri = track.track_uri
        response = client.post("me/player/queue", params={"uri": uri})

        if response.status_code in {204, 200}:
            success += 1
        else:
            failed.append({
                "track": track.track_name,
                "uri": uri,
                "error": response.text
            })

    if success == 0:
        return JsonResponse(
            {"error": "Failed to queue any tracks.", "details": failed},
            status=500,
        )

    elapsed = time.time() - start
    return JsonResponse(
        {
            "message": f"Restored {success} tracks to the queue.",
            "failures": failed if failed else None,
            "elapsed_time": f"{elapsed:.2f}s"
        },
        status=207 if failed else 200,
    )






@require_http_methods(['GET'])
def my_queues(request):
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
            "description": q.description,
            "share_token": str(q.share_token) if q.share_token else None,
        }
        for q in queues
    ]

    return JsonResponse({"queues":data})


@require_http_methods(['GET'])
@ratelimit(key='user_or_ip', rate='10/m', block=True)
def suggest(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    user = get_object_or_404(User, id=user_id)
    get_object_or_404(Queue, id=queue_id, user=user)

    return JsonResponse(
        {
            "error": "Smart suggestions are being rebuilt.",
            "code": "SUGGESTIONS_UNAVAILABLE",
            "suggestions": [],
        },
        status=501,
    )

@require_http_methods(['GET'])
def suggest_available(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    user = get_object_or_404(User, id=user_id)
    get_object_or_404(Queue, id=queue_id, user=user)

    return JsonResponse(
        {
            "available": False,
            "code": "SUGGESTIONS_UNAVAILABLE",
            "message": "Smart suggestions are being rebuilt.",
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def toggle_share(request, queue_id: int):
    user = get_object_or_404(User, id=request.session["user_id"])
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    if queue.share_token:
        queue.share_token = None
        queue.save()
        return JsonResponse({"shared": False, "share_token": None})

    queue.share_token = uuid.uuid4()
    queue.save()
    return JsonResponse({"shared": True, "share_token": str(queue.share_token)})


@require_http_methods(["GET"])
def get_shared_queue(request, share_token):
    queue = get_object_or_404(Queue, share_token=share_token)

    track_data = [
        {
            "track_name": t.track_name,
            "track_uri": t.track_uri,
            "artist_name": t.artist_name,
            "album_image_url": t.album_image_url,
            "position": t.position,
        }
        for t in queue.tracks.order_by("position")
    ]

    return JsonResponse({
        "id": queue.id,
        "name": queue.name,
        "description": queue.description,
        "created_at": queue.created_at.isoformat(),
        "image_url": queue.image_url,
        "owner": queue.user.display_name,
        "track_count": len(track_data),
        "tracks": track_data,
    })


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def clone_shared_queue(request, share_token):
    source = get_object_or_404(Queue, share_token=share_token)
    user = get_object_or_404(User, id=request.session["user_id"])

    new_queue = Queue.objects.create(
        user=user,
        name=source.name,
        image_url=source.image_url,
        description=source.description,
    )

    tracks = source.tracks.order_by("position")
    for t in tracks:
        Track.objects.create(
            queue=new_queue,
            track_name=t.track_name,
            track_uri=t.track_uri,
            artist_name=t.artist_name,
            album_image_url=t.album_image_url,
            position=t.position,
        )

    return JsonResponse({
        "message": "Queue cloned successfully",
        "queue_id": new_queue.id,
    })
