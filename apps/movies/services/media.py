from decouple import config

from apps.movies.services.tmdb import TMDBClient, TMDBClientError, pick_best_search_result


DIRECT_VIDEO_EXTENSIONS = (".mp4", ".webm", ".ogg", ".m3u8")


def detect_full_video_mode(movie) -> str:
    if getattr(movie, "full_video_file", None):
        return "file"

    url = (getattr(movie, "full_video_url", "") or "").strip()
    if not url:
        return "none"

    clean_url = url.lower().split("?")[0]
    if clean_url.endswith(DIRECT_VIDEO_EXTENSIONS):
        return "direct"

    return "iframe"


def build_trailer_embed_url(site: str, key: str) -> str:
    if not site or not key:
        return ""

    if site.lower() == "youtube":
        return f"https://www.youtube.com/embed/{key}"
    if site.lower() == "vimeo":
        return f"https://player.vimeo.com/video/{key}"
    return ""


def pick_best_trailer(videos: list[dict]) -> dict | None:
    if not videos:
        return None

    type_priority = {
        "Trailer": 4,
        "Teaser": 3,
        "Clip": 2,
        "Featurette": 1,
    }
    site_priority = {
        "YouTube": 3,
        "Vimeo": 2,
    }

    def score(item: dict):
        site = item.get("site", "")
        video_type = item.get("type", "")
        official = 1 if item.get("official") else 0
        published_at = item.get("published_at", "")
        return (
            site_priority.get(site, 0),
            type_priority.get(video_type, 0),
            official,
            published_at,
        )

    return sorted(videos, key=score, reverse=True)[0]


def resolve_tmdb_id(client: TMDBClient, movie) -> str:
    if movie.tmdb_id:
        return str(movie.tmdb_id)

    if movie.imdb_id:
        found = client.find_by_imdb_id(movie.imdb_id)
        if found:
            movie.tmdb_id = str(found["id"])
            movie.save(update_fields=["tmdb_id"])
            return movie.tmdb_id

    search_results = client.search_movie(movie.title, movie.release_year)
    best = pick_best_search_result(search_results, movie.title, movie.release_year)
    if best:
        movie.tmdb_id = str(best["id"])
        movie.save(update_fields=["tmdb_id"])
        return movie.tmdb_id

    return ""


def ensure_movie_trailer(movie) -> str:
    if movie.trailer_url:
        return movie.trailer_url

    if movie.trailer_site == "unavailable":
        return ""

    bearer_token = config("TMDB_API_READ_TOKEN", default="").strip()
    if not bearer_token:
        return ""

    try:
        client = TMDBClient(bearer_token=bearer_token)
        tmdb_id = resolve_tmdb_id(client, movie)
        if not tmdb_id:
            movie.trailer_site = "unavailable"
            movie.save(update_fields=["trailer_site"])
            return ""

        videos_payload = client._get(f"/movie/{tmdb_id}/videos", params={"language": "en-US"})
        best_video = pick_best_trailer(videos_payload.get("results") or [])
        if not best_video:
            movie.trailer_site = "unavailable"
            movie.save(update_fields=["trailer_site"])
            return ""

        embed_url = build_trailer_embed_url(best_video.get("site", ""), best_video.get("key", ""))
        if not embed_url:
            movie.trailer_site = "unavailable"
            movie.save(update_fields=["trailer_site"])
            return ""

        movie.trailer_url = embed_url
        movie.trailer_site = best_video.get("site", "")
        movie.save(update_fields=["trailer_url", "trailer_site"])
        return movie.trailer_url

    except TMDBClientError:
        return ""