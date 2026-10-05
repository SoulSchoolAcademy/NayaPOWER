#!/usr/bin/env python3
"""Naya Voice Renderer — canonical Intelligent Block text -> Chatterbox -> web audio.

Implements the renderer half of
BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md.

Pipeline:
    canonical text -> validate -> chunk (sentence-aware) ->
    synthesize (model loaded ONCE per process) -> PCM16 WAV ->
    MP3 (ffmpeg) -> content-hash cache -> path

Audio-key contract (Hub side, PR #1423):
    R2 naya-voice/<boardId-verbatim>.mp3
This renderer produces the .mp3 bytes. bake_naya_voice.py owns the
<boardId-verbatim>.mp3 naming. The browser never synthesizes; it just plays.

The model is loaded once per process (get_model singleton). bake_naya_voice.py
renders every block through one process — never one model load per block.

Heavy dependencies (torch, chatterbox, soundfile) are imported lazily inside
functions so the pure-logic surface (chunking, cache keys, naming) is importable
and testable without them.

Usage:
    python3 tools/render_naya_voice.py --text "Hello, I am Naya." --out /tmp/naya-hello.mp3
    python3 tools/render_naya_voice.py --text-file block.txt --cache-dir .naya/voice-cache
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "BRAIN" / "04-INTELLIGENCE" / "NAYA-VOICE-REGISTRY-V1.json"
DEFAULT_REF = REPO / "voices" / "naya_reference.wav"
DEFAULT_CACHE = REPO / ".naya" / "voice-cache"
LOCAL_CKPT = Path.home() / "workspace" / "naya" / "chatterbox-model"
CKPT_FILES = ["ve.safetensors", "t3_cfg.safetensors", "s3gen.safetensors",
              "tokenizer.json", "conds.pt"]

# Bump when the render pipeline changes; part of the cache key so a pipeline
# change can never silently serve stale audio.
RENDERER_VERSION = "2"
NATIVE_SR = 24000          # Chatterbox native sample rate
CHUNK_LIMIT = 240          # max chars per generate() call
SILENCE_BETWEEN_CHUNKS_S = 0.25
MP3_BITRATE = "128k"


@dataclass
class RenderResult:
    path: Path
    cache_key: str
    voice_version: str
    renderer_version: str
    duration_s: float
    chunks: int
    cached: bool
    encoding: str  # "mp3" | "wav"


def registry_voice_version() -> str:
    try:
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        return str(reg["voices"][0]["version"])
    except Exception:
        return "1"


def cache_key(text: str, voice_version: str,
              renderer_version: str = RENDERER_VERSION) -> str:
    """Deterministic content/voice/pipeline key. Same input -> same key, always."""
    return hashlib.sha256(
        f"{text}\nvoice_version={voice_version}\nrenderer={renderer_version}"
        .encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    """Collapse whitespace; keep sentence punctuation intact for chunking."""
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, limit: int = CHUNK_LIMIT) -> list[str]:
    """Sentence-aware chunking. Deterministic: same text -> same chunks.

    Sentences are greedily packed into chunks of at most `limit` chars.
    A single overlong sentence is hard-split at word boundaries. An overlong
    single word is hard-split at `limit`.
    """
    text = normalize_text(text)
    if not text:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""
    for sent in sentences:
        if not sent:
            continue
        # Hard-split an overlong sentence at word boundaries.
        words = sent.split(" ")
        piece = ""
        pieces: list[str] = []
        for w in words:
            if len(w) > limit:  # overlong word: hard-split the word itself
                if piece:
                    pieces.append(piece)
                    piece = ""
                for i in range(0, len(w), limit):
                    pieces.append(w[i:i + limit])
                continue
            candidate = (piece + " " + w).strip() if piece else w
            if len(candidate) <= limit:
                piece = candidate
            else:
                pieces.append(piece)
                piece = w
        if piece:
            pieces.append(piece)
        for p in pieces:
            candidate = (current + " " + p).strip() if current else p
            if len(candidate) <= limit:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = p
    if current:
        chunks.append(current)
    return chunks


# ---------------------------------------------------------------------------
# Model lifecycle — loaded ONCE per process. Never per block, never per chunk.
# ---------------------------------------------------------------------------
_model = None
_model_loads = 0


def load_model():
    """Load ChatterboxTTS (local checkpoint preferred). Counts loads for tests."""
    global _model_loads
    try:
        from chatterbox.tts import ChatterboxTTS
    except ImportError as e:
        raise RuntimeError(
            "chatterbox-tts is not installed. Install it with: pip install chatterbox-tts "
            "(needs torch; CPU works, GPU is faster)."
        ) from e
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if all((LOCAL_CKPT / f).exists() for f in CKPT_FILES):
        model = ChatterboxTTS.from_local(str(LOCAL_CKPT), device=device)
    else:
        model = ChatterboxTTS.from_pretrained(device=device)
    _model_loads += 1
    return model


def get_model():
    """Process-wide singleton. The bake lane renders every block through this."""
    global _model
    if _model is None:
        _model = load_model()
    return _model


def model_load_count() -> int:
    return _model_loads


def reset_model_singleton() -> None:
    """Test/CLI escape hatch only — lets a fresh process state be simulated."""
    global _model, _model_loads
    _model = None
    _model_loads = 0


def check_reference(ref_wav: Path) -> Path:
    if not ref_wav.exists():
        raise FileNotFoundError(
            f"Voice reference not found: {ref_wav}. "
            "Provide the Naya voice reference audio (see voices/ and "
            "BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md).")
    return ref_wav


def synthesize_chunks(chunks: list[str], ref_wav: Path, model) -> tuple[object, int]:
    """Run the model once per chunk; concatenate with inter-chunk silence.

    Returns (wav_tensor_1xN, sample_rate). `model` needs .generate(text,
    audio_prompt_path=...) and .sr — the real ChatterboxTTS or a test stub.
    """
    import torch
    sr = int(model.sr)
    parts = []
    silence = torch.zeros(1, int(sr * SILENCE_BETWEEN_CHUNKS_S))
    for i, chunk in enumerate(chunks):
        wav = model.generate(chunk, audio_prompt_path=str(ref_wav))
        wav = wav.cpu()
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        parts.append(wav[:, :])
        if i < len(chunks) - 1:
            parts.append(silence)
    full = torch.cat(parts, dim=1)
    return full, sr


def write_pcm16_wav(wav_tensor, sr: int, out_path: Path) -> Path:
    """Write 16-bit PCM WAV — the universally decodable intermediate."""
    try:
        import soundfile as sf
    except ImportError as e:
        raise RuntimeError(
            "soundfile is not installed (pip install soundfile). "
            "PCM16 WAV output requires it.") from e
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = wav_tensor.squeeze(0).cpu().numpy() if hasattr(wav_tensor, "cpu") else wav_tensor
    sf.write(str(out_path), data, sr, subtype="PCM_16")
    return out_path


def encode_mp3(wav_path: Path, mp3_path: Path, bitrate: str = MP3_BITRATE) -> Path:
    """ffmpeg PCM16 WAV -> MP3. Fails loudly; never silently keeps the WAV."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "ffmpeg not found on PATH. MP3 encoding requires ffmpeg; "
            "install it or render with --format wav.")
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [ffmpeg, "-y", "-v", "error", "-i", str(wav_path),
         "-codec:a", "libmp3lame", "-b:a", bitrate, str(mp3_path)],
        capture_output=True, text=True)
    if proc.returncode != 0 or not mp3_path.exists() or mp3_path.stat().st_size == 0:
        raise RuntimeError(f"ffmpeg MP3 encode failed: {proc.stderr[:300]}")
    return mp3_path


def audio_duration_s(path: Path) -> float:
    """Duration via ffprobe; falls back to WAV header math."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        proc = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True)
        try:
            return float(proc.stdout.strip())
        except ValueError:
            pass
    # WAV fallback: 16-bit PCM
    import wave
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def render(text: str, cache_dir: Path = DEFAULT_CACHE,
           ref_wav: Path = DEFAULT_REF,
           voice_version: str | None = None,
           model=None,
           fmt: str = "mp3") -> RenderResult:
    """Render text to Naya-voiced web audio, using the content-hash cache.

    Cache hits need no model at all. Cache misses synthesize with `model`
    (or the process singleton), encode, and store under the cache key.
    """
    text = normalize_text(text or "")
    if not text:
        raise ValueError("empty text: nothing to render")
    if fmt not in ("mp3", "wav"):
        raise ValueError(f"unsupported format: {fmt!r} (want 'mp3' or 'wav')")
    version = voice_version or registry_voice_version()
    key = cache_key(text, version)
    ext = "mp3" if fmt == "mp3" else "wav"
    cached = cache_dir / f"{key}.{ext}"
    if cached.exists():
        return RenderResult(path=cached, cache_key=key, voice_version=version,
                            renderer_version=RENDERER_VERSION,
                            duration_s=audio_duration_s(cached),
                            chunks=len(chunk_text(text)), cached=True,
                            encoding=fmt)

    check_reference(ref_wav)
    m = model if model is not None else get_model()
    chunks = chunk_text(text)
    wav_tensor, sr = synthesize_chunks(chunks, ref_wav, m)

    cache_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_wav = Path(tmp) / "render.wav"
        write_pcm16_wav(wav_tensor, sr, tmp_wav)
        if fmt == "mp3":
            encode_mp3(tmp_wav, cached)
        else:
            shutil.copy2(tmp_wav, cached)
    duration = audio_duration_s(cached)
    return RenderResult(path=cached, cache_key=key, voice_version=version,
                        renderer_version=RENDERER_VERSION, duration_s=duration,
                        chunks=len(chunks), cached=False, encoding=fmt)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render Naya's voice for a text block.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Text to speak.")
    src.add_argument("--text-file", help="File containing text to speak.")
    ap.add_argument("--out", help="Copy the rendered audio here too (in addition to cache).")
    ap.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    ap.add_argument("--ref", default=str(DEFAULT_REF))
    ap.add_argument("--voice-version", default=None)
    ap.add_argument("--format", choices=["mp3", "wav"], default="mp3",
                    help="Web output format (default mp3, per the Hub audio-key contract).")
    args = ap.parse_args(argv)

    text = args.text if args.text else Path(args.text_file).read_text(encoding="utf-8")
    try:
        result = render(text, cache_dir=Path(args.cache_dir),
                        ref_wav=Path(args.ref), voice_version=args.voice_version,
                        fmt=args.format)
    except (RuntimeError, FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(str(result.path))
    print(f"cache_key={result.cache_key} duration_s={result.duration_s:.2f} "
          f"chunks={result.chunks} cached={result.cached} encoding={result.encoding}")
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(result.path.read_bytes())
        print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
