import json

from tools.closed_loop_executor import ClosedLoopExecutor, Task, independently_recheck


def test_closed_loop_runs_ready_work_in_parallel_with_capacity():
    seen = []

    def make(name):
        def run():
            seen.append(name)
            return {"name": name, "status": "DONE"}
        return run

    executor = ClosedLoopExecutor(capacity=2)
    receipt = executor.run([Task("A", make("A")), Task("B", make("B"))])

    assert receipt["status"] == "VERIFIED"
    assert receipt["parallel"]["capacity"] == 2
    assert receipt["parallel"]["dispatched"] == 2
    assert set(seen) == {"A", "B"}


def test_failed_work_creates_durable_learning_and_changes_next_dispatch():
    calls = []

    def fail_once():
        calls.append("unsafe")
        raise RuntimeError("capacity-bound external lane unavailable")

    def safe():
        calls.append("safe")
        return {"status": "DONE"}

    executor = ClosedLoopExecutor(capacity=1)
    first = executor.run([Task("unsafe", fail_once), Task("safe", safe)])

    assert first["status"] == "VERIFIED"
    assert first["learning"]["lesson"] == "failed capacity-bound work must be bypassed and the next reversible ready task executed"
    assert first["learning"]["reusable"] is True
    assert calls == ["unsafe", "safe"]

    second = executor.run([Task("unsafe", fail_once), Task("safe", safe)])
    assert second["reuse"]["lesson_applied"] is True
    assert calls == ["unsafe", "safe", "safe"]
    assert second["status"] == "VERIFIED"


def test_receipt_is_self_contained_and_reconstructable():
    executor = ClosedLoopExecutor(capacity=1)
    receipt = executor.run([Task("one", lambda: {"status": "DONE"})])

    raw = json.dumps(receipt)
    restored = json.loads(raw)
    assert restored["verification"]["independent_recheck"] is True
    assert restored["verification"]["claim_matched_evidence"] is True
    assert restored["learning"]["reusable"] is True


def test_independent_recheck_accepts_a_persisted_experiment_wrapper(tmp_path):
    executor = ClosedLoopExecutor(capacity=1, state_path=tmp_path / "state.json")
    tick = executor.run([Task("one", lambda: {"status": "DONE"})])
    wrapper = {
        "schema": "NAYAPOWER_CLOSED_LOOP_EXPERIMENT_V1",
        "status": "VERIFIED",
        "first_tick": tick,
        "second_tick": tick,
        "verification": {
            "independent_recheck": True,
            "claim_matched_evidence": True,
            "receipt_reconstructed_after_write": True,
        },
    }
    path = tmp_path / "experiment.json"
    path.write_text(json.dumps(wrapper), encoding="utf-8")
    assert independently_recheck(path)["status"] == "VERIFIED"
