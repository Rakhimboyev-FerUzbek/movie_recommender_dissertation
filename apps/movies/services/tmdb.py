import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


class TMDBClientError(Exception):
    pass


def normalize_title(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9\s]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, bearer_token: str, timeout: int = 20):
        if not bearer_token:
            raise TMDBClientError("TMDB bearer token is required.")
        self.bearer_token = bearer_token
        self.timeout = timeout
        self._configuration = None

    def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.BASE_URL}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"

        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.bearer_token}",
            },
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise TMDBClientError(f"TMDB HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise TMDBClientError(f"TMDB connection error: {exc}") from exc

    def get_configuration(self) -> dict:
        if self._configuration is None:
            self._configuration = self._get("/configuration")
        return self._configuration

    def build_poster_url(self, poster_path: str, preferred_size: str = "w500") -> str:
        if not poster_path:
            return ""

        config = self.get_configuration()
        images = config.get("images", {})
        secure_base_url = images.get("secure_base_url", "https://image.tmdb.org/t/p/")
        poster_sizes = images.get("poster_sizes") or ["w500", "original"]

        if preferred_size in poster_sizes:
            size = preferred_size
        elif "w500" in poster_sizes:
            size = "w500"
        else:
            size = poster_sizes[-1]

        return f"{secure_base_url.rstrip('/')}/{size}/{poster_path.lstrip('/')}"

    def get_movie_details(self, tmdb_id: str | int) -> dict:
        return self._get(f"/movie/{tmdb_id}")

    def find_by_imdb_id(self, imdb_id: str) -> dict | None:
        data = self._get(f"/find/{quote(imdb_id)}", params={"external_source": "imdb_id"})
        results = data.get("movie_results") or []
        return results[0] if results else None

    def search_movie(self, title: str, year: int | None = None) -> list[dict]:
        params = {"query": title}
        if year:
            params["year"] = year
        data = self._get("/search/movie", params=params)
        return data.get("results") or []


def pick_best_search_result(results: list[dict], title: str, year: int | None = None) -> dict | None:
    if not results:
        return None

    target_title = normalize_title(title)

    def score(item: dict) -> tuple:
        candidate_title = normalize_title(item.get("title") or item.get("original_title") or "")
        release_date = item.get("release_date") or ""
        release_year = int(release_date[:4]) if release_date[:4].isdigit() else None

        exact_title = 1 if candidate_title == target_title else 0
        partial_title = 1 if target_title and target_title in candidate_title else 0
        year_match = 1 if year and release_year == year else 0
        has_poster = 1 if item.get("poster_path") else 0
        popularity = float(item.get("popularity") or 0.0)

        return (exact_title, year_match, partial_title, has_poster, popularity)

    return sorted(results, key=score, reverse=True)[0]