from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from django.core.cache import cache
from .models import User, Queue, Track
from .spotify import SpotifyClient
from functools import wraps
import time
import requests
import urllib.parse
import json
import uuid
import mimetypes
import joblib
import pandas as pd
import numpy as np
import sklearn.preprocessing
import sklearn.cluster
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
from io import BytesIO

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_ME_URL = "https://api.spotify.com/v1/me"
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-read streaming"

ml_data = joblib.load("song_data/ml_bundle.joblib")
DF:pd.DataFrame = ml_data['data']
DF.set_index("uri", inplace=True)
URIS = DF.index.values
SCALED_FEATURE_MATRIX = ml_data['features']
KMEANS:sklearn.cluster.KMeans = ml_data['kmeans']
SCALER:sklearn.preprocessing.StandardScaler = ml_data['scaler']
FEATURE_COLUMNS = [
    'danceability', 'energy', 'key', 'loudness', 'mode', 
    'speechiness', 'acousticness', 'instrumentalness', 
    'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'
]

def health(request):
    return HttpResponse("OK", status=200)


def login(request):
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": "true"
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
    request.session["user_display_name"] = display_name
    request.session.save()

    return HttpResponseRedirect(f"{settings.FRONTEND_URL.rstrip('/')}/callback?status=ok")


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
def get_token(request):
    user = get_object_or_404(User, pk=request.session["user_id"])
    return JsonResponse({
        "access_token": user.access_token,
    })

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
    print(response)
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
def upload_image(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)
    
    queue_id = request.POST.get("queue_id")
    image_file = request.FILES.get("image")

    if not queue_id or not image_file:
        return JsonResponse({"error": "Missing queue_id or image"}, status=400)

    filename = f"queue_covers/{uuid.uuid4()}_{image_file.name}"
    content_type = "image/jpeg"

    try:
        img = Image.open(image_file).convert("RGB")

        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        img = img.crop((left, top, right, bottom))

        target_size = (512, 512)
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)

        settings.S3.upload_fileobj(
            buffer,
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

@csrf_exempt
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
        "tracks": track_data
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
def restore_queue(request, queue_id: int):
    start = time.time()
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    tracks = list(queue.tracks.order_by("position"))  # Ensure it's evaluated
    if not tracks:
        return JsonResponse({"error": "Queue is empty"}, status=400)

    success = 0
    failed = []

    client = SpotifyClient(user)

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
        return JsonResponse({
            "error": "Failed to queue any tracks.",
            "details": failed
        }, status=500)

    print(time.time() - start)
    return JsonResponse({
        "message": f"Restored {success} tracks to the queue.",
        "failures": failed if failed else None
    }, status=207 if failed else 200)




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
            "description": q.description
        }
        for q in queues
    ]

    return JsonResponse({"queues":data})


def get_feature_rows(uris):
    existing = DF.index.intersection(uris)
    rows = [DF.loc[uri, FEATURE_COLUMNS].values for uri in existing]
    return rows

def uri_to_id(uri):
    return uri.split(":")[-1]

@csrf_exempt
@require_http_methods(['GET'])
def suggest(request, queue_id:int):
    # extract queue tracks
    # match track names to any in dataset
    # average their features into a feature vector
    # scale vector w/ scaler.transform(vector)
    # assign cluster w/ kmeans.predict
    # query songs from that cluster, exlcuding queue tracks
    # Return top 3 tracks by cosine distance
    
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)
    
    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    # Cache
    cache_key = f'smart_sugg_u{user.id}_q{queue.id}'
    if request.GET.get('refresh') != '1':
        cached = cache.get(cache_key)
        if cached:
            return JsonResponse({'suggestions': cached})
        

    # extract queue tracks
    uris = list(queue.tracks.order_by('position').values_list('track_uri', flat=True))
    
    # match tracks to dataset
    feature_rows = get_feature_rows(uris)
    if len(feature_rows) < 2:
        # not enough data for reliable vector
        return JsonResponse({
            "error": "Not enough feature-matched tracks for smart suggestions"
        }, status=400)
    
    # compute vector
    mood_vector = np.mean(feature_rows, axis=0).reshape(1,-1)
    scaled_vector = SCALER.transform(mood_vector)

    # predict cluster
    cluster_id = int(KMEANS.predict(scaled_vector)[0])
    print(f"Cluster: {cluster_id}")

    # filter dataset to this cluster
    candidate_indices = np.where(KMEANS.labels_ == cluster_id)[0]
    candidate_uris = np.array(URIS)[candidate_indices]
    candidate_feats = SCALED_FEATURE_MATRIX[candidate_indices]

    # filter out seen uris
    seen_uris = set(uris)
    unseen = [(uri, feat) for uri, feat in zip(candidate_uris, candidate_feats) if uri not in seen_uris]
    if not unseen:
        return JsonResponse({"error": "No unseen songs in matching cluster"}, status=404)
    
    # calculate distance
    unseen_uris, unseen_feats = zip(*unseen)
    unseen_feats_scaled = SCALER.transform(unseen_feats)
    similarities = cosine_similarity(scaled_vector, unseen_feats_scaled).flatten()
    # rank and return top 3
    top_3 = sorted(zip(unseen_uris, similarities), key=lambda x: -x[1])[:3]
    selected_uris = [uri for uri, _ in top_3]

    # extract metadata
    tracks = Track.objects.filter(track_uri__in=selected_uris)
    track_dict = {t.track_uri: t for t in tracks}
    response_payload = []

    for uri in selected_uris:
        if uri in track_dict:
            track = track_dict[uri]
            response_payload.append({
                "track_uri": uri,
                "track_name": track.track_name,
                "artist_name": track.artist_name,
                "album_image_url": track.album_image_url,
            })

    # fallback in case track not in DB
    client = SpotifyClient(user)   
    track_ids = [uri_to_id(uri) for uri in selected_uris]
    response = client.get(f"tracks?ids={','.join(track_ids)}")
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch track metadata from Spotify"}, status=500)

    items = response.json().get("tracks", [])
    metadata = {item["id"]:item for item in items}
    for uri in selected_uris:
        if uri not in track_dict:
            sid = uri_to_id(uri)
            item = metadata.get(sid)
            if item:
                response_payload.append({
                    "track_uri": uri,
                    "track_name": item.get("name"),
                    "artist_name": item.get("artists", [{}])[0].get("name"),
                    "album_image_url": item.get("album", {}).get("images", [{}])[0].get("url"),
                })
    
    if response_payload:
        cache.set(cache_key, response_payload, timeout=60*60*24)

    return JsonResponse({"suggestions": response_payload})

    # USE FUZZY MATCHING DUE TO EXPLICIT VS NOT EXPLICIT
    # ALSO IMPROVE BY ARTIST MATCHING BY ASKING NEW CHAT

@csrf_exempt
@require_http_methods(['GET'])
def suggest_available(request, queue_id:int):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    user = get_object_or_404(User, id=user_id)
    queue = get_object_or_404(Queue, id=queue_id, user=user)

    uris = list(queue.tracks.order_by('position').values_list('track_uri', flat=True))
    feature_rows = get_feature_rows(uris)
    
    if len(feature_rows) < 2:
        return JsonResponse({"available": False})
    else:
        cache_key = f'smart_sugg_u{user.id}_q{queue.id}'
        cached = cache.get(cache_key)
        return JsonResponse({"available": True if cached or len(feature_rows) >= 2 else False})
