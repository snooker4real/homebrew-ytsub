import pytest

from ytsub import core


def test_extract_video_id_variants():
    vid = "bqMBqcwR8vg"
    for ref in [
        vid,
        f"https://www.youtube.com/watch?v={vid}",
        f"https://www.youtube.com/watch?v={vid}&t=124s",
        f"https://youtu.be/{vid}",
        f"https://www.youtube.com/shorts/{vid}",
        f"https://www.youtube.com/embed/{vid}",
    ]:
        assert core.extract_video_id(ref) == vid


def test_extract_video_id_invalid():
    with pytest.raises(core.YtsubError):
        core.extract_video_id("pas une url")


def test_playlist_detection():
    pl = "PLabcdefghij12345"
    assert core.extract_playlist_id(f"https://www.youtube.com/playlist?list={pl}") == pl
    assert core.is_playlist_only(f"https://www.youtube.com/playlist?list={pl}")
    assert not core.is_playlist_only(f"https://www.youtube.com/watch?v=bqMBqcwR8vg&list={pl}")
    assert core.extract_playlist_id("bqMBqcwR8vg") is None


def test_join_paragraphs():
    out = core._join_paragraphs("A. B. C. D.\nE.")
    assert out == "A. B. C.\n\nD. E."


def test_slugify():
    assert core.slugify("Mon titre: super/vidéo ?") == "Mon-titre-super-vidéo"
    assert core.slugify("???") == "video"
