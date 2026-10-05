#!/usr/bin/env python3
"""Bake Naya voice audio for Intelligent Blocks — the canonical bake lane.

Implements the baker half of
BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md.

Reads a blocks manifest (block_id -> canonical text), renders every block
through ONE process (the model loads once), and writes per-block audio files
honoring the exact Hub audio-key contract (PR #1423):

    out_dir/<boardId-verbatim>.mp3   ->   R2 naya-voice/<boardId-verbatim>.mp3

The boardId is used VERBATIM — the string the board factory produced
(feed blocks: 'note-' + slug(...), 40 chars; queue/observer: 'board-' + slug(...),
40 chars). The baker never re-slugs or transforms the id; any transformation
would diverge from the factory key and cause permanent 404s. A block id that
cannot be a verbatim filename fails loudly for that block (bake never dies).

Usage:
    python3 tools/bake_naya_voice.py --blocks-json blocks.json --out-dir .naya/voice-baked --out-manifest audio-manifest.json
    python3 tools/bake_naya_voice.py --blocks-json blocks.json --out-dir out --dry-run

blocks.json shape: {"block_id": "canonical text", ...}
audio-manifest.json shape: {"block_id": {"audio": "<block_id>.mp3", "cache_key": ...,
    "voice_version": ..., "renderer_version": ..., "duration_s": ..., "status": ...}, ...}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_naya_voice import (
    render, cache_key, chunk_text, get_model,
    DEFAULT_CACHE, DEFAULT_REF, registry_voice_version, RENDERER_VERSION,
)

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[1] / ".naya" / "voice-baked"


def board_filename(block_id: str) -> str:
    """Mirror the Hub's audioUrl key derivation exactly (HUB/app/index.html):

        const key = String(boardId || '').trim() || 'block';

    The filename is the key VERBATIM + '.mp3'. Ids containing path separators
    cannot be verbatim filenames — fail loudly instead of transforming.
    """
    key = (block_id or "").strip() or "block"
    if "/" in key or "\\" in key or key in (".", "..") or key.startswith("."):
        raise ValueError(
            f"block id {block_id!r} cannot be a verbatim audio filename; "
            "the Hub audio-key contract requires the boardId verbatim.")
    return key + ".mp3"


def bake(blocks: dict, cache_dir: Path, out_dir: Path, ref_wav: Path,
         voice_version: str, model=None, dry_run: bool = False) -> dict:
    """Bake every block in one process. `model`, when given, is used for all
    renders (persistent-process inference); otherwise the process singleton
    loads once on first cache miss."""
    manifest: dict = {}
    m = model  # may be None -> render() uses the singleton (loads once)
    for block_id, text in blocks.items():
        text = ((text or "").strip())
        try:
            filename = board_filename(block_id)
        except ValueError as e:
            manifest[block_id] = {"status": "failed", "error": str(e)[:200]}
            continue
        if not text:
            manifest[block_id] = {"status": "skipped", "reason": "empty text"}
            continue
        key = cache_key(text, voice_version)
        if dry_run:
            manifest[block_id] = {"audio": filename, "cache_key": key,
                                  "voice_version": voice_version,
                                  "renderer_version": RENDERER_VERSION,
                                  "status": "would-render"}
            continue
        try:
            result = render(text, cache_dir=cache_dir, ref_wav=ref_wav,
                            voice_version=voice_version, model=m, fmt="mp3")
            if m is None and not result.cached:
                # render() loaded the process singleton for this cache miss;
                # reuse it so the model is never loaded twice in one bake.
                m = get_model()
            out_file = out_dir / filename
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(result.path.read_bytes())
            manifest[block_id] = {"audio": filename, "cache_key": key,
                                  "voice_version": voice_version,
                                  "renderer_version": result.renderer_version,
                                  "duration_s": round(result.duration_s, 2),
                                  "chunks": result.chunks,
                                  "status": "cached" if result.cached else "rendered"}
        except Exception as e:  # noqa: BLE001 — bake must never die on one block
            manifest[block_id] = {"audio": filename, "cache_key": key,
                                  "voice_version": voice_version,
                                  "renderer_version": RENDERER_VERSION,
                                  "status": "failed", "error": str(e)[:200]}
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Bake Naya voice audio for Intelligent Blocks.")
    ap.add_argument("--blocks-json", required=True, help="JSON: {block_id: canonical text}")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR),
                    help="Where <boardId-verbatim>.mp3 files are written.")
    ap.add_argument("--out-manifest", default=None,
                    help="Where to write the audio manifest JSON.")
    ap.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    ap.add_argument("--ref", default=str(DEFAULT_REF))
    ap.add_argument("--voice-version", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    blocks = json.loads(Path(args.blocks_json).read_text(encoding="utf-8"))
    version = args.voice_version or registry_voice_version()
    out_dir = Path(args.out_dir)
    manifest = bake(blocks, Path(args.cache_dir), out_dir, Path(args.ref),
                    version, dry_run=args.dry_run)

    if args.out_manifest:
        out = Path(args.out_manifest)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(str(out))

    n_ok = sum(1 for m in manifest.values() if m["status"] in ("cached", "rendered"))
    n_fail = sum(1 for m in manifest.values() if m["status"] == "failed")
    n_skip = sum(1 for m in manifest.values() if m["status"] == "skipped")
    print(f"blocks={len(manifest)} ok={n_ok} failed={n_fail} skipped={n_skip} dry_run={args.dry_run}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
