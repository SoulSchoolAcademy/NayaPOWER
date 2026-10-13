"""Battery for the intelligence intake triage (Naya 5, 2026-10-13).

The battery IS the contract: these verdicts pin what "valuable
intelligence" means to the intake gate. v1 thresholds live here.
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "intake_triage", ROOT / "tools" / "intake_triage.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

MECHANISM_LESSON = (
    "When dispatching workers, always claim the lane in the truth file "
    "before spawning. A failed claim means the lane is taken. Enforcement: "
    "lane-state.py claim exits non-zero and the dispatcher aborts the spawn."
)


def test_exact_dupe_drops():
    v = mod.triage(MECHANISM_LESSON, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] == "DROP"
    assert "novelty" in v["reasons"][0]


def test_paraphrase_dupe_drops():
    near = ("Always claim the lane in the truth file before spawning workers, "
            "every time.")
    v = mod.triage(near, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] == "DROP", v


def test_novel_mechanism_with_teeth_promotes():
    v = mod.triage(MECHANISM_LESSON)
    assert v["verdict"] == "PROMOTE", v
    assert v["scores"]["novelty"] >= 6.0
    assert v["scores"]["durability"] >= 6.0
    assert v["scores"]["actionability"] >= 6.0


def test_novel_observation_without_teeth_logs():
    v = mod.triage(
        "Connection pooling shows higher latency under burst load in every "
        "benchmark we ran.")
    assert v["verdict"] == "LOG", v
    assert "actionability" in v["reasons"][0]


def test_transient_incident_with_teeth_logs_not_promotes():
    v = mod.triage(
        "Today's deploy failed because the migration ran twice. "
        "Check migration guards before deploying.")
    assert v["verdict"] == "LOG", v
    assert "durability" in v["reasons"][0]


def test_trivia_drops():
    v = mod.triage("Lunch was good.")
    assert v["verdict"] == "DROP", v


def test_empty_corpus_is_fully_novel():
    assert mod.novelty_score("anything at all") == 10.0


def test_scores_always_bounded():
    texts = [MECHANISM_LESSON, "Lunch was good.",
             "Today's deploy failed. Check guards before deploying.",
             "Connection pooling shows higher latency under burst load."]
    for t in texts:
        v = mod.triage(t, existing_lesson_texts=texts)
        for dim, s in v["scores"].items():
            assert 0.0 <= s <= 10.0, (dim, s, t)
        assert v["verdict"] in ("PROMOTE", "LOG", "DROP")
        assert v["reasons"], t


def test_enforcement_without_trigger_or_durability_does_not_promote():
    # Teeth alone are not a lesson: no trigger, no durability -> not PROMOTE.
    v = mod.triage("Enforcement: the gate blocks bad merges.")
    assert v["verdict"] in ("LOG", "DROP"), v


def test_repetition_does_not_game_durability():
    # "always" x3 scores the same as "always" x1 — markers count once.
    a = mod.durability_score("Always verify the lane claim.")
    b = mod.durability_score("Always always always verify the lane claim.")
    assert a == b


def test_negative_lesson_logs():
    # A "don't do X" lesson is real signal but weak as a Smart Note.
    v = mod.triage("Do not claim the lane before checking the truth file.")
    assert v["verdict"] in ("LOG", "DROP"), v


def test_cli_runs():
    import subprocess, json
    r = subprocess.run(
        ["python3", str(ROOT / "tools" / "intake_triage.py"),
         "--text", MECHANISM_LESSON],
        capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["verdict"] == "PROMOTE"
