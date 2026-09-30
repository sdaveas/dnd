#!/usr/bin/env python3
"""Render audiobook MP3s for the Laynlindr backstory chapters using kokoro-mlx.

Detects chapters that changed in git and re-renders only those.

Usage:
  python3 render_audiobook.py                       # chapters changed vs HEAD (uncommitted)
  python3 render_audiobook.py --base main           # chapters changed vs a git ref
  python3 render_audiobook.py --all                 # every chapter
  python3 render_audiobook.py path/to/chapter-11-conspiracy.md

Voice, speed, and pronunciation respellings are configured below.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import soundfile as sf

try:
    from kokoro_mlx import KokoroTTS
    BACKEND = "mlx"
except ImportError:
    from kokoro import KPipeline
    BACKEND = "cpu"

ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / "characters/laynlindr-freth/backstory/book"
OUT = ROOT / "characters/laynlindr-freth/backstory/audiobook"
FRONT_MATTER = "chapter-00"

VOICE = "af_bella"
SPEED = 0.9
SAMPLE_RATE = 24000
PARAGRAPH_PAUSE = 0.4
CHUNK_PAUSE = 0.15
MAX_CHUNK_CHARS = 500

PRONUNCIATION: dict[str, str] = {}

CACHE = ROOT / "labs/audiobook/cache"

_tts = None


class MlxBackend:
    def __init__(self):
        self._tts = KokoroTTS.from_pretrained()

    def generate(self, text, voice, speed):
        return self._tts.generate(text, voice=voice, speed=speed).audio


class CpuBackend:
    def __init__(self):
        self._pipeline = KPipeline(lang_code="a")

    def generate(self, text, voice, speed):
        audio = [
            np.asarray(a, dtype="float32")
            for _, _, a in self._pipeline(text, voice=voice, speed=speed)
        ]
        if not audio:
            return np.zeros(int(0.3 * SAMPLE_RATE), dtype="float32")
        return np.concatenate(audio)


def _backend():
    global _tts
    if _tts is None:
        _tts = MlxBackend() if BACKEND == "mlx" else CpuBackend()
    return _tts


def _fragment(text):
    key = hashlib.sha256(f"{BACKEND}|{VOICE}|{SPEED}|{text}".encode()).hexdigest()[:16]
    return CACHE / f"{key}.wav"


def _get_or_render(text):
    path = _fragment(text)
    if path.exists():
        audio, _ = sf.read(path, dtype="float32")
        return audio
    audio = _backend().generate(text, voice=VOICE, speed=SPEED)
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    sf.write(tmp, audio, SAMPLE_RATE, format="WAV", subtype="PCM_16")
    tmp.rename(path)
    return audio


def changed_chapters(base):
    rel = str(BOOK.relative_to(ROOT))
    cmd = ["git", "diff", "--name-only", "--diff-filter=ACM", base or "HEAD", "--", rel]
    try:
        files = subprocess.run(
            cmd, capture_output=True, text=True, cwd=ROOT, check=True
        ).stdout.split()
    except subprocess.CalledProcessError:
        return all_chapters()
    return sorted(ROOT / f for f in files if f.endswith(".md"))


def all_chapters():
    return sorted(p for p in BOOK.glob("chapter-*.md") if not p.stem.startswith(FRONT_MATTER))


def plain_paragraphs(md):
    paras, current = [], []
    chapter_intro = None
    for line in md.splitlines():
        if line.lstrip().startswith("[^"):  # footnote definitions are not read
            continue
        if line.lstrip().startswith("#"):
            if chapter_intro is None:
                m = re.match(r"#+\s*(Chapter \d+)\s*[—–-]+\s*(.+?)\s*$", line.lstrip())
                if m:
                    chapter_intro = f"{m.group(1)}. {m.group(2)}."
            continue
        if not line.strip():
            if current:
                paras.append(" ".join(current))
                current = []
            continue
        current.append(line.strip())
    if current:
        paras.append(" ".join(current))

    out = []
    if chapter_intro:  # spoken "Chapter X. Title." opener
        out.extend(chunk_paragraph(chapter_intro))
    for p in paras:
        p = re.sub(r"\[\^\d+\]", "", p)  # inline footnote markers are not read
        p = re.sub(r"\*([^*]+)\*", r"\1", p)
        for name, say in PRONUNCIATION.items():
            p = p.replace(name, say)
        if not re.search(r"\w", p):  # scene breaks (---) and ornaments
            continue
        out.extend(chunk_paragraph(p))
    return out


def chunk_paragraph(p, limit=MAX_CHUNK_CHARS):
    if len(p) <= limit:
        return [p]
    sentences = re.split(r"(?<=[.!?\u201d]) +", p)
    chunks, cur = [], ""
    for s in sentences:
        if cur and len(cur) + len(s) + 1 > limit:
            chunks.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def render_chapter(path):
    paragraphs = plain_paragraphs(path.read_text())
    if not paragraphs:
        return None
    para_silence = np.zeros(int(PARAGRAPH_PAUSE * SAMPLE_RATE), dtype="float32")
    chunk_silence = np.zeros(int(CHUNK_PAUSE * SAMPLE_RATE), dtype="float32")
    audio = []
    for i, p in enumerate(paragraphs):
        chunk_audio = _get_or_render(p)
        audio.append(chunk_audio)
        if i < len(paragraphs) - 1:
            audio.append(chunk_silence if len(p) > MAX_CHUNK_CHARS else para_silence)
        print(f"  {path.stem}: paragraph {i + 1}/{len(paragraphs)} ({len(chunk_audio) / SAMPLE_RATE:.1f}s)")
    return np.concatenate(audio)


def _render_chapter(path_str):
    path = Path(path_str)
    out_path = OUT / f"{path.stem}.mp3"
    print(f"rendering {path.name} -> {out_path.name}")
    audio = render_chapter(path)
    if audio is None:
        print(f"  {path.name}: skipped, no readable text (front matter or headings only)")
        return
    sf.write(out_path, audio, SAMPLE_RATE, format="MP3")
    print(f"  wrote {out_path} ({len(audio) / SAMPLE_RATE / 60:.1f} min)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="explicit chapter md files")
    ap.add_argument("--base", help="git ref to diff changed chapters against")
    ap.add_argument("--all", action="store_true", help="render every chapter")
    ap.add_argument("--force", action="store_true", help="render even if the md file is unchanged")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1),
                    help="parallel chapter renders (default: min(4, cpu count))")
    args = ap.parse_args()

    if args.paths:
        chapters = [Path(p).resolve() for p in args.paths]
        if not args.force:
            changed = changed_chapters(args.base)
            skipped = [p.name for p in chapters if p not in changed]
            if skipped:
                print(f"skipped (unchanged in git): {', '.join(skipped)}")
            chapters = [p for p in chapters if p in changed]
    elif args.all:
        chapters = all_chapters()
    else:
        chapters = [p for p in changed_chapters(args.base) if not p.stem.startswith(FRONT_MATTER)]

    if not chapters:
        print("no changed chapters")
        return

    missing = [p for p in chapters if not p.is_file()]
    if missing:
        sys.exit(f"missing chapter files: {[str(p) for p in missing]}")

    OUT.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(_render_chapter, [str(p) for p in chapters]))


if __name__ == "__main__":
    main()
