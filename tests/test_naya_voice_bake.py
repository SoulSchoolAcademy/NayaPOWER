"""Canonical voice bake lane tests — negative, cache, batch, and contract tests.

Pure-logic tests (chunking, cache keys, naming, error paths) run everywhere.
Audio-path tests skip cleanly when torch/soundfile/ffprobe are unavailable
(e.g. CI's repo venv); they run under the voice venv. The real-model test
only runs with NAYA_VOICE_REAL=1 and the local checkpoint + reference audio.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import render_naya_voice as R
from render_naya_voice import chunk_text, cache_key  # noqa: E402
from bake_naya_voice import bake, board_filename  # noqa: E402

HAS_FFPROBE = shutil.which("ffprobe") is not None
needs_ffprobe = pytest.mark.skipif(not HAS_FFPROBE, reason="ffprobe not available")


@pytest.fixture
def dirs(tmp_path):
    cache = tmp_path / "cache"
    out = tmp_path / "baked"
    cache.mkdir()
    out.mkdir()
    return cache, out


@pytest.fixture
def ref_wav(tmp_path):
    """Tiny valid WAV standing in for the voice reference.

    The stub model's generate() ignores the path, but the production
    check_reference() gate still runs — this keeps the strict gate while
    letting unit tests exercise the audio path. Written with stdlib `wave`
    so the suite gains no new third-party test dependency."""
    import struct
    import wave
    p = tmp_path / "ref.wav"
    n = 12000  # 0.5 s of silence at 24 kHz
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(struct.pack(f"<{n}h", *([0] * n)))
    return p


def stub_model(sr=24000):
    torch = pytest.importorskip("torch")
    pytest.importorskip("soundfile")

    class StubVoiceModel:
        def __init__(self):
            self.sr = sr
            self.generate_calls: list[str] = []

        def generate(self, text, audio_prompt_path=None):
            self.generate_calls.append(text)
            n = int(self.sr * 0.4)
            t = torch.arange(n, dtype=torch.float32) / self.sr
            return (0.25 * torch.sin(2 * torch.pi * 440 * t)).unsqueeze(0)

    return StubVoiceModel()


# ---------------------------------------------------------------------------
# Pure logic — no model, no audio libs
# ---------------------------------------------------------------------------

def test_empty_text_raises_value_error(tmp_path):
    with pytest.raises(ValueError, match="empty text"):
        R.render("", cache_dir=tmp_path)


def test_whitespace_only_text_raises(tmp_path):
    with pytest.raises(ValueError, match="empty text"):
        R.render("   \n\t  ", cache_dir=tmp_path)


def test_unsupported_format_raises(tmp_path):
    with pytest.raises(ValueError, match="unsupported format"):
        R.render("hello", cache_dir=tmp_path, fmt="ogg")


def test_missing_reference_fails_clearly(tmp_path):
    with pytest.raises(FileNotFoundError, match="Voice reference not found"):
        R.render("hello", cache_dir=tmp_path,
                 ref_wav=tmp_path / "nope.wav", model=object())


def test_chunk_short_text_single_chunk():
    assert chunk_text("Hello. I am Naya.") == ["Hello. I am Naya."]


def test_chunk_long_text_respects_limit_and_rejoins():
    text = " ".join(f"Sentence number {i} is here to talk." for i in range(30))
    chunks = chunk_text(text, limit=240)
    assert len(chunks) > 1
    assert all(len(c) <= 240 for c in chunks)
    assert " ".join(chunks) == " ".join(text.split())


def test_chunk_deterministic():
    text = "First. Second! Third? " * 20
    assert chunk_text(text) == chunk_text(text)


def test_chunk_unicode_no_crash_and_rejoins():
    text = ("Héllo wörld. " * 10 + "日本語のテスト。 " * 10
            + "🎉 emoji party time! " * 10)
    chunks = chunk_text(text, limit=120)
    assert chunks
    assert all(len(c) <= 120 for c in chunks)
    assert " ".join(chunks) == " ".join(text.split())


def test_chunk_overlong_word_hard_splits():
    word = "a" * 500
    chunks = chunk_text(word, limit=240)
    assert len(chunks) == 3
    assert "".join(chunks) == word


def test_cache_key_deterministic_and_versioned():
    k1 = cache_key("hello", "1")
    assert k1 == cache_key("hello", "1")
    assert k1 != cache_key("hello!", "1")
    assert k1 != cache_key("hello", "2")
    assert k1 != cache_key("hello", "1", renderer_version="99")
    assert len(k1) == 64


def test_board_filename_verbatim():
    assert board_filename("note-abc123") == "note-abc123.mp3"
    assert board_filename("  note-abc123  ") == "note-abc123.mp3"


def test_board_filename_empty_defaults_to_block():
    assert board_filename("") == "block.mp3"
    assert board_filename("   ") == "block.mp3"


def test_board_filename_rejects_path_separators():
    for bad in ("../evil", "a/b", "a\\b", ".hidden", ".", ".."):
        with pytest.raises(ValueError, match="[Vv]erbatim"):
            board_filename(bad)


def test_bake_empty_block_skipped(dirs):
    cache, out = dirs
    manifest = bake({"note-x": "   "}, cache, out, Path("/none"), "1", dry_run=True)
    assert manifest["note-x"]["status"] == "skipped"


def test_bake_dry_run_manifest_shape(dirs):
    cache, out = dirs
    manifest = bake({"note-a": "Hello world."}, cache, out, Path("/none"), "1",
                    dry_run=True)
    m = manifest["note-a"]
    assert m["status"] == "would-render"
    assert m["audio"] == "note-a.mp3"
    assert len(m["cache_key"]) == 64
    assert m["voice_version"] == "1"
    assert m["renderer_version"] == R.RENDERER_VERSION


def test_bake_bad_board_id_failed_not_dead(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    manifest = bake({"../evil": "Hello.", "note-ok": "Hi."}, cache, out,
                    ref_wav, "1", model=model)
    assert manifest["../evil"]["status"] == "failed"
    assert "verbatim" in manifest["../evil"]["error"].lower()
    assert manifest["note-ok"]["status"] == "rendered"
    assert (out / "note-ok.mp3").exists()


# ---------------------------------------------------------------------------
# Audio path — stub model (persistent-process batch semantics)
# ---------------------------------------------------------------------------

def test_persistent_process_single_model_instance(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    blocks = {f"note-{i}": f"Block number {i} speaking." for i in range(3)}
    manifest = bake(blocks, cache, out, ref_wav, "1", model=model)
    assert all(m["status"] == "rendered" for m in manifest.values())
    # One model object served all three blocks; one generate call per chunk.
    assert len(model.generate_calls) == 3
    assert all((out / f"note-{i}.mp3").exists() for i in range(3))


@needs_ffprobe
def test_cache_hit_second_bake_no_resynth(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    blocks = {"note-a": "Hello world."}
    first = bake(blocks, cache, out, ref_wav, "1", model=model)
    assert first["note-a"]["status"] == "rendered"
    calls_after_first = len(model.generate_calls)
    assert calls_after_first == 1
    second = bake(blocks, cache, out, ref_wav, "1", model=model)
    assert second["note-a"]["status"] == "cached"
    assert len(model.generate_calls) == calls_after_first  # no resynthesis
    assert second["note-a"]["cache_key"] == first["note-a"]["cache_key"]


@needs_ffprobe
def test_baked_mp3_decodes_to_audio(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    manifest = bake({"note-a": "Hello world."}, cache, out, ref_wav, "1",
                    model=model)
    mp3 = out / "note-a.mp3"
    assert mp3.exists() and mp3.stat().st_size > 1000
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,sample_rate:format=duration",
         "-of", "json", str(mp3)], capture_output=True, text=True)
    info = json.loads(proc.stdout)
    assert info["streams"][0]["codec_name"] == "mp3"
    assert float(info["format"]["duration"]) > 0.3


def test_mp3_magic_bytes(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    bake({"note-a": "Hello world."}, cache, out, ref_wav, "1", model=model)
    head = (out / "note-a.mp3").read_bytes()[:3]
    assert head[:3] == b"ID3" or head[:2] == b"\xff\xfb"


@needs_ffprobe
def test_manifest_full_shape(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    manifest = bake({"note-a": "Hello world."}, cache, out, ref_wav, "1",
                    model=model)
    m = manifest["note-a"]
    for field in ("audio", "cache_key", "voice_version", "renderer_version",
                  "duration_s", "chunks", "status"):
        assert field in m, f"missing manifest field: {field}"
    assert m["audio"] == "note-a.mp3"
    assert m["duration_s"] > 0
    assert m["chunks"] == 1


def test_long_unicode_text_renders_via_stub(dirs, ref_wav):
    cache, out = dirs
    model = stub_model()
    text = ("Héllo wörld, 日本語テスト。 " * 40).strip()
    manifest = bake({"note-u": text}, cache, out, ref_wav, "1", model=model)
    m = manifest["note-u"]
    assert m["status"] == "rendered"
    assert m["chunks"] > 1
    assert len(model.generate_calls) == m["chunks"]
    assert (out / "note-u.mp3").exists()


# ---------------------------------------------------------------------------
# Real model — only with NAYA_VOICE_REAL=1 and local assets present
# ---------------------------------------------------------------------------

@pytest.mark.skipif(os.environ.get("NAYA_VOICE_REAL") != "1",
                    reason="real-model render is slow; opt in with NAYA_VOICE_REAL=1")
def test_real_model_renders_playable_mp3(tmp_path):
    torch = pytest.importorskip("torch")
    pytest.importorskip("soundfile")
    pytest.importorskip("chatterbox")
    ckpt = Path.home() / "workspace" / "naya" / "chatterbox-model"
    ref = Path.home() / "workspace" / "naya" / "voices" / "naya_reference.wav"
    if not all((ckpt / f).exists() for f in R.CKPT_FILES) or not ref.exists():
        pytest.skip("local chatterbox checkpoint or reference audio missing")
    cache = tmp_path / "cache"
    result = R.render("Hello. I am Naya.", cache_dir=cache, ref_wav=ref,
                      voice_version="1", fmt="mp3")
    assert result.path.exists()
    assert result.duration_s > 1.0
    assert result.chunks == 1
    assert not result.cached
