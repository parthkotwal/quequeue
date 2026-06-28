import re

from django.db.models import Max

from queues.models import Track
from queues.services.serialization import serialize_track


TOKEN_RE = re.compile(r"[a-z0-9]+")


def track_tokens(track):
    return set(TOKEN_RE.findall(f"{track.track_name} {track.artist_name}".lower()))


def queue_profile(queue):
    tracks = list(queue.tracks.order_by("position"))
    artist_ids = set()
    artist_names = set()
    years = []
    popularity = []
    tokens = set()

    for track in tracks:
        artist_ids.update(track.artist_ids or [])
        if track.artist_name:
            artist_names.add(track.artist_name.lower())
        if track.release_year:
            years.append(track.release_year)
        if track.popularity is not None:
            popularity.append(track.popularity)
        tokens.update(track_tokens(track))

    return {
        "tracks": tracks,
        "artist_ids": artist_ids,
        "artist_names": artist_names,
        "avg_year": sum(years) / len(years) if years else None,
        "avg_popularity": sum(popularity) / len(popularity) if popularity else None,
        "tokens": tokens,
        "seen_uris": {track.track_uri for track in tracks},
    }


def score_candidate(candidate, profile):
    score = 0.0
    reasons = []

    candidate_artist_ids = set(candidate.artist_ids or [])
    artist_overlap = candidate_artist_ids & profile["artist_ids"]
    if artist_overlap:
        score += 6.0
        reasons.append("same artist network")
    elif candidate.artist_name and candidate.artist_name.lower() in profile["artist_names"]:
        score += 5.0
        reasons.append("same artist")

    candidate_tokens = track_tokens(candidate)
    if candidate_tokens and profile["tokens"]:
        token_score = len(candidate_tokens & profile["tokens"]) / len(candidate_tokens | profile["tokens"])
        if token_score:
            score += token_score * 2.0
            reasons.append("similar metadata")

    if candidate.release_year and profile["avg_year"] is not None:
        year_distance = abs(candidate.release_year - profile["avg_year"])
        year_score = max(0.0, 1.0 - (year_distance / 20.0))
        if year_score:
            score += year_score
            reasons.append("similar era")

    if candidate.popularity is not None and profile["avg_popularity"] is not None:
        popularity_distance = abs(candidate.popularity - profile["avg_popularity"])
        popularity_score = max(0.0, 1.0 - (popularity_distance / 100.0))
        score += popularity_score
        if popularity_score >= 0.75:
            reasons.append("similar popularity")

    return score, reasons


def continuation_candidates(user, queue):
    profile = queue_profile(queue)
    if len(profile["tracks"]) < 2:
        return []

    latest_track_ids = (
        Track.objects
        .filter(queue__user=user)
        .exclude(queue=queue)
        .exclude(track_uri__in=profile["seen_uris"])
        .values("track_uri")
        .annotate(latest_id=Max("id"))
        .values_list("latest_id", flat=True)
    )
    candidates = Track.objects.filter(id__in=latest_track_ids).select_related("queue")

    scored = []
    for candidate in candidates:
        score, reasons = score_candidate(candidate, profile)
        if score <= 0:
            score = 0.1
            reasons = ["from another saved queue"]
        scored.append((score, candidate, reasons))

    scored.sort(key=lambda item: (-item[0], item[1].position, item[1].id))
    return scored


def continue_queue(user, queue, limit=10):
    suggestions = []
    for score, track, reasons in continuation_candidates(user, queue)[:limit]:
        payload = serialize_track(track)
        payload["score"] = round(score, 3)
        payload["reasons"] = reasons[:3]
        suggestions.append(payload)
    return suggestions


def continuation_available(user, queue):
    return bool(continuation_candidates(user, queue)[:1])
