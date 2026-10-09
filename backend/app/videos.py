"""Links a un segundo exacto de una grabación."""
import base64
import json
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse


def url_en_segundo(url: str | None, segundos: int) -> str | None:
    if not url:
        return None
    try:
        p = urlparse(url)
    except ValueError:
        return None
    if p.scheme not in ("http", "https"):
        return None
    host = p.hostname or ""
    q = dict(parse_qsl(p.query, keep_blank_values=True))
    if "sharepoint.com" in host or "microsoftstream.com" in host:
        nav = base64.b64encode(json.dumps({"playbackOptions": {"startTimeInSeconds": segundos}}).encode()).decode()
        q["nav"] = nav
        return urlunparse(p._replace(query=urlencode(q)))
    if "youtube.com" in host or "youtu.be" in host:
        q["t"] = f"{segundos}s"
        return urlunparse(p._replace(query=urlencode(q)))
    return urlunparse(p._replace(fragment=f"t={segundos}"))
