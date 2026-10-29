"""Recuperation des transcriptions YouTube (video et playlist)."""

import re

from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi
from youtube_transcript_api._errors import CouldNotRetrieveTranscript
from youtube_transcript_api.formatters import (
    JSONFormatter,
    SRTFormatter,
    TextFormatter,
    WebVTTFormatter,
)

FORMATS = {
    "text": TextFormatter(),
    "json": JSONFormatter(),
    "srt": SRTFormatter(),
    "vtt": WebVTTFormatter(),
}
EXTENSIONS = {"text": "txt", "json": "json", "srt": "srt", "vtt": "vtt"}

_VIDEO_RE = re.compile(r"(?:v=|/videos/|embed/|shorts/|live/|youtu\.be/)([A-Za-z0-9_-]{11})")
_BARE_ID_RE = re.compile(r"[A-Za-z0-9_-]{11}")
_PLAYLIST_RE = re.compile(r"[?&]list=([A-Za-z0-9_-]+)")


class YtsubError(Exception):
    """Erreur affichable telle quelle a l'utilisateur."""


def extract_video_id(ref: str) -> str:
    ref = ref.strip()
    if _BARE_ID_RE.fullmatch(ref):
        return ref
    match = _VIDEO_RE.search(ref)
    if not match:
        raise YtsubError(f"Impossible d'extraire un ID de video depuis: {ref}")
    return match.group(1)


def extract_playlist_id(ref: str):
    ref = ref.strip()
    match = _PLAYLIST_RE.search(ref)
    if match:
        return match.group(1)
    if re.fullmatch(r"(PL|UU|OL|FL|RD)[A-Za-z0-9_-]{10,}", ref):
        return ref
    return None


def is_playlist_only(ref: str) -> bool:
    """Vrai si la reference designe une playlist et pas une video precise."""
    return extract_playlist_id(ref) is not None and not _VIDEO_RE.search(ref)


def _list(video_id: str):
    try:
        return YouTubeTranscriptApi().list(video_id)
    except CouldNotRetrieveTranscript as exc:
        raise YtsubError(_clean(exc)) from exc


def _clean(exc: Exception) -> str:
    # Les erreurs de youtube-transcript-api sont multi-lignes et tres verbeuses.
    lines = [l.strip() for l in str(exc).strip().splitlines() if l.strip()]
    return lines[0] if lines else exc.__class__.__name__


def list_languages(ref: str) -> list:
    return [
        {
            "language": t.language,
            "code": t.language_code,
            "generated": t.is_generated,
            "translatable": t.is_translatable,
        }
        for t in _list(extract_video_id(ref))
    ]


def fetch(ref: str, fmt: str = "text", languages=("fr", "en"), join: bool = False) -> str:
    if fmt not in FORMATS:
        raise YtsubError(f"Format inconnu: {fmt} (attendu: {', '.join(FORMATS)})")
    transcripts = _list(extract_video_id(ref))
    try:
        transcript = transcripts.find_transcript(list(languages))
    except NoTranscriptFound:
        transcript = next(iter(transcripts), None)
        if transcript is None:
            raise YtsubError("Aucun sous-titre disponible pour cette video.")
    try:
        fetched = transcript.fetch()
    except CouldNotRetrieveTranscript as exc:
        raise YtsubError(_clean(exc)) from exc
    if join and fmt == "text":
        return _join_paragraphs(" ".join(s.text.replace("\n", " ") for s in fetched))
    return FORMATS[fmt].format_transcript(fetched)


def _join_paragraphs(text: str) -> str:
    """Regroupe le texte en paragraphes (environ une phrase sur trois)."""
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = [" ".join(sentences[i : i + 3]) for i in range(0, len(sentences), 3)]
    return "\n\n".join(paragraphs)


def playlist_videos(ref: str) -> list:
    import yt_dlp

    playlist_id = extract_playlist_id(ref)
    if not playlist_id:
        raise YtsubError(f"Playlist invalide: {ref}")
    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    opts = {"extract_flat": True, "quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:  # yt-dlp leve des exceptions variees
        raise YtsubError(f"Impossible de lire la playlist: {exc}") from exc
    videos = [{"id": e["id"], "title": e.get("title") or e["id"]} for e in info.get("entries") or [] if e.get("id")]
    if not videos:
        raise YtsubError("Playlist introuvable ou vide.")
    return videos


def slugify(title: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^\w\-]+", "-", title, flags=re.UNICODE).strip("-")
    return slug[:max_len] or "video"
