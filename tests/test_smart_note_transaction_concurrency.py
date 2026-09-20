from pathlib import Path
import importlib.util
import multiprocessing as mp
import time

ROOT = Path(__file__).resolve().parents[1]
TX = ROOT / ".naya/runtime/smart_note_transaction.py"


def load():
    spec = importlib.util.spec_from_file_location("smart_note_transaction_lock_test", TX)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def hold_lock(root: str, started, release):
    mod = load()
    with mod._TransactionLock(Path(root), timeout=5):
        started.set()
        release.wait(5)


def test_shared_transaction_boundary_is_serialized(tmp_path):
    mod = load()
    ctx = mp.get_context("spawn")
    started, release = ctx.Event(), ctx.Event()
    p = ctx.Process(target=hold_lock, args=(str(tmp_path), started, release))
    p.start()
    assert started.wait(5)

    acquired = False
    t0 = time.monotonic()
    try:
        with mod._TransactionLock(tmp_path, timeout=0.15):
            acquired = True
    except RuntimeError as exc:
        assert "lock contention" in str(exc)
    finally:
        release.set()
        p.join(5)

    assert acquired is False
    assert time.monotonic() - t0 >= 0.1
    assert p.exitcode == 0


def test_lock_recovers_stale_owner(tmp_path):
    mod = load()
    lock = tmp_path / ".naya/locks/smart-note-transaction.lock"
    lock.mkdir(parents=True)
    (lock / "owner").write_text("stale", encoding="utf-8")
    old = time.time() - 1000
    import os
    os.utime(lock, (old, old))
    with mod._TransactionLock(tmp_path, timeout=1, stale_after=1):
        assert lock.exists()
