"""Interface en ligne de commande de ytsub."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__, core


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ytsub",
        description="Affiche ou telecharge la transcription d'une video ou playlist YouTube.",
        epilog="exemples:\n"
        "  ytsub https://youtu.be/bqMBqcwR8vg\n"
        "  ytsub <url> -o transcript.txt\n"
        "  ytsub <url> -f srt -l fr,en\n"
        "  ytsub --langs <url>\n"
        "  ytsub <url-playlist> -o transcripts/ --limit 10",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("url", nargs="?", help="URL YouTube (video ou playlist) ou ID de video")
    p.add_argument("-f", "--format", choices=sorted(core.FORMATS), default="text", help="format de sortie (defaut: text)")
    p.add_argument("-l", "--lang", default="fr,en", help="langues preferees par ordre, separees par des virgules (defaut: fr,en)")
    p.add_argument("-o", "--output", help="fichier de sortie (video) ou dossier (playlist); sinon affiche dans le terminal")
    p.add_argument("-j", "--join", action="store_true", help="format text: regroupe en paragraphes au lieu d'une ligne par sous-titre")
    p.add_argument("--langs", action="store_true", help="liste les langues de sous-titres disponibles et quitte")
    p.add_argument("-p", "--playlist", action="store_true", help="traite l'URL comme une playlist (automatique si l'URL ne contient que list=)")
    p.add_argument("--limit", type=int, default=50, help="nombre maximum de videos pour une playlist (defaut: 50)")
    p.add_argument("-V", "--version", action="version", version=f"ytsub {__version__}")
    return p


def _err(msg: str) -> None:
    print(f"ytsub: {msg}", file=sys.stderr)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")


def _run_playlist(args, langs) -> int:
    videos = core.playlist_videos(args.url)[: max(1, args.limit)]
    if not args.output:
        _err("une playlist demande -o <dossier>")
        return 2
    out_dir = Path(args.output).expanduser()
    ext = core.EXTENSIONS[args.format]
    failures = 0
    for i, video in enumerate(videos, 1):
        name = f"{i:02d}-{core.slugify(video['title'])}.{ext}"
        try:
            text = core.fetch(video["id"], args.format, langs, args.join)
        except core.YtsubError as exc:
            failures += 1
            _err(f"[{i}/{len(videos)}] {video['id']}: {exc}")
            continue
        _write(out_dir / name, text)
        print(f"[{i}/{len(videos)}] {out_dir / name}", file=sys.stderr)
    return 1 if failures == len(videos) else 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.url:
        parser.print_usage(sys.stderr)
        return 2
    langs = [c.strip() for c in args.lang.split(",") if c.strip()]
    try:
        if args.langs:
            for lang in core.list_languages(args.url):
                kind = "auto" if lang["generated"] else "manuel"
                print(f"{lang['code']:8} {lang['language']} ({kind})")
            return 0
        if args.playlist or core.is_playlist_only(args.url):
            return _run_playlist(args, langs)
        text = core.fetch(args.url, args.format, langs, args.join)
    except core.YtsubError as exc:
        _err(str(exc))
        return 1
    except KeyboardInterrupt:
        return 130
    if args.output:
        path = Path(args.output).expanduser()
        _write(path, text)
        print(path, file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
