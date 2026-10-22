"""Cycle-3 battery: reach wiring + embeddings seam (Naya Gamma, w111).

Two upgrades, both pinned:

1. REACH WIRING — reach is no longer a bare word list. _AREA_KEYWORDS wires
   every reach keyword to one of the twelve canonical areas, and
   reach_details() names WHICH areas a candidate touches. reach_score() is
   derived from it; the 10/8/5/2 bands must be byte-identical to cycle 2.

2. EMBEDDINGS SEAM — novelty_score()/triage() accept similarity=, an
   injectable callable (text, corpus) -> float in [0,1]. The default provider
   stays the token _max_coverage. A SIMULATED semantic provider proves the
   seam is the socket the synonym-xfail is waiting for — it is labeled
   simulated, not mistaken for real embeddings.

Battery rules (carried from the adversarial battery):
  * every passing test pins a shipped mechanism with a false-positive
    companion;
  * strict-xfail stays strict-xfail: a provider is still missing, so the
    real synonym case still LOGs. No theater.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "intake_triage", ROOT / "tools" / "intake_triage.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

TWELVE = ("LEARN", "KNOW", "ACT", "LAW", "VERIFY", "Intelligent Blocks",
          "Decision Engine", "Retrieval", "Successor", "TEAM", "INFRA",
          "Human Value")

MECHANISM_LESSON = (
    "When dispatching workers, always claim the lane in the truth file "
    "before spawning. A failed claim means the lane is taken. Enforcement: "
    "lane-state.py claim exits non-zero and the dispatcher aborts the spawn."
)

PARAPHRASE = ("Never spawn a worker without first securing the lane "
              "inside the state file. If the claim fails, that lane is "
              "already occupied. Enforcement: the state tool returns "
              "nonzero and the dispatcher must stop the launch.")


# --- Reach wiring ---

def test_reach_wires_exactly_the_twelve_canonical_areas():
    assert sorted(mod._AREA_KEYWORDS) == sorted(TWELVE)


def test_reach_details_names_the_areas_hit():
    d = mod.reach_details("This law governs every seat, every wave.")
    assert d["areas"] == ["LAW"], d
    assert "seat" in d["team_talk"], d
    assert d["collective"] is True


def test_reach_bands_byte_identical_to_cycle_2():
    # collective -> 10.0
    assert mod.reach_score("every seat, every wave") == 10.0
    # >=3 hits -> 8.0
    assert mod.reach_score(
        "learn from the decision, verify the blocks, act now") == 8.0
    # >=1 hit -> 5.0
    assert mod.reach_score("a note for the team") == 5.0
    # none -> 2.0
    assert mod.reach_score("lunch was good") == 2.0


def test_reach_hit_count_matches_legacy_keyword_count():
    # The legacy cycle-2 formula counted matched KEYWORDS ("lanes" hits both
    # "lane" and "lanes"); the wiring must count the same way, not dedupe.
    d = mod.reach_details("check the lanes")
    assert len(d["areas"]) + len(d["team_talk"]) == 2
    assert mod.reach_score("check the lanes") == 5.0


def test_triage_verdict_surfaces_reach_and_provider():
    v = mod.triage(MECHANISM_LESSON)
    assert v["reach"]["team_talk"] == ["lane"], v  # no area word, team word
    assert v["novelty_provider"] == "_max_coverage", v


def test_tight_real_lesson_still_promotes_with_named_reach():
    tight = ("Always verify the lane claim before spawning any worker. "
             "Enforcement: an unclaimed lane blocks the spawn and the "
             "dispatcher aborts.")
    v = mod.triage(tight)
    assert v["verdict"] == "PROMOTE", v
    assert "ACT" in v["reach"]["areas"] or v["reach"]["team_talk"], v


# --- Embeddings seam ---

def _full_dupe(text, corpus):
    return 1.0


def test_similarity_seam_threads_through_triage():
    # P-014: the seam test walks the production path — triage(), not a
    # private helper. A provider saying "fully covered" must DROP an
    # otherwise-PROMOTE candidate and name the provider.
    v = mod.triage(MECHANISM_LESSON, existing_lesson_texts=["x"],
                   similarity=_full_dupe)
    assert v["scores"]["novelty"] == 0.0, v
    assert v["verdict"] == "DROP", v
    assert v["novelty_provider"] == "_full_dupe", v


def test_seam_default_is_token_coverage():
    v = mod.triage(PARAPHRASE, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["novelty_provider"] == "_max_coverage", v
    assert v["scores"]["novelty"] == 5.71, v  # pinned cycle-2 behavior


def test_seam_clamps_out_of_range_providers():
    assert mod.novelty_score("x", ["y"],
                            similarity=lambda t, c: 2.5) == 0.0
    assert mod.novelty_score("x", ["y"],
                            similarity=lambda t, c: -1.0) == 10.0


def test_seam_nan_raises_instead_of_manufacturing_certainty():
    with pytest.raises(ValueError, match="NaN"):
        mod.novelty_score("x", ["y"],
                          similarity=lambda t, c: float("nan"))


def test_seam_ignores_provider_when_corpus_empty():
    # No corpus -> 10.0 without calling the provider at all.
    calls = []
    def spy(t, c):
        calls.append(1)
        return 1.0
    assert mod.novelty_score("x", (), similarity=spy) == 10.0
    assert calls == []


def test_simulated_semantic_provider_flips_synonym_case():
    # SIMULATED provider: stands in for the real embeddings source the
    # synonym-xfail is waiting for. If the seam is real, a semantic "these
    # say the same thing" must DROP the paraphrase through triage().
    def simulated_embeddings(text, corpus):
        return 0.95 if text == PARAPHRASE else 0.0
    v = mod.triage(PARAPHRASE, existing_lesson_texts=[MECHANISM_LESSON],
                   similarity=simulated_embeddings)
    assert v["verdict"] == "DROP", v
    assert v["scores"]["novelty"] == 0.5, v
