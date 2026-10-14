"""Padding-resistance adversarial battery (Naya Gamma, w110 — cycle 2).

The w106 battery proved the containment fix was a REAL upgrade: a dupe
diluted with filler drops. This battery asks the harder question: which
other attacks still get through, and which fixes are real vs theater?

Rules of this battery:
  * Every passing test pins a shipped mechanism (stemming, stuffing guard)
    with a false-positive companion proving the mechanism doesn't eat
    real lessons.
  * Every strict-xfail is an HONEST RED: a named gap with a named fix
    (embeddings seam, semantic judgment), not a hidden failure. When the
    fix lands, the xfail flips. Manufacturing green here would be theater.
"""

import importlib.util
from pathlib import Path

import pytest

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

SALAD = ("Always whenever every mechanism law principle protocol contract "
         "invariant the paradigm synergy leverage holistically. When actioning, "
         "claim use add remove run build fix measure score dispatch. "
         "Enforcement: enforce gate check fail verify prove refuse block "
         "abort test.")

FILLER_MARKERS = ("whenever always never enforce gate check fail verify prove "
                  "refuse block abort test claim use add remove run build fix "
                  "measure score dispatch")


# --- Real upgrade 1: stemming (morphological variants no longer dodge) ---

def test_synonym_paraphrase_does_not_promote():
    # A paraphrase that only rewords + changes word forms (spawn/spawning,
    # claim/claimed, worker/workers) must not PROMOTE. Stemming demotes it
    # to LOG (novelty 5.71 < 6.0); full DROP needs the embeddings seam.
    paraphrase = ("Never spawn a worker without first securing the lane "
                  "inside the state file. If the claim fails, that lane is "
                  "already occupied. Enforcement: the state tool returns "
                  "nonzero and the dispatcher must stop the launch.")
    v = mod.triage(paraphrase, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] != "PROMOTE", v
    assert v["scores"]["novelty"] < 6.0, v


@pytest.mark.xfail(strict=True, reason="needs an embeddings PROVIDER wired "
                   "to the similarity seam (seam landed w111: "
                   "test_simulated_semantic_provider_flips_synonym_case "
                   "proves the socket works); token overlap cannot see "
                   "synonym-level paraphrase; stemming only demotes to LOG")
def test_synonym_paraphrase_drops_with_embeddings():
    paraphrase = ("Never spawn a worker without first securing the lane "
                  "inside the state file. If the claim fails, that lane is "
                  "already occupied. Enforcement: the state tool returns "
                  "nonzero and the dispatcher must stop the launch.")
    v = mod.triage(paraphrase, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] == "DROP", v


def test_stemming_does_not_create_false_dupe():
    # False-positive companion: a genuine lesson that quotes an old phrase
    # must not be nuked by stemmed containment.
    new = ("Building on lane discipline, here is the deeper mechanism: when "
           "the dispatcher itself restarts mid-wave, in-flight claims persist "
           "in the truth file and must be reaped by the incoming dispatcher "
           "before any new spawn. Enforcement: the dispatcher boot sequence "
           "runs lane-state.py reap-or-abort, and a spawn with unreaped "
           "claims fails closed. This law governs every seat, every wave.")
    v = mod.triage(new, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] != "DROP" or "padded duplicate" not in v["reasons"][0], v


# --- Real upgrade 2: keyword-stuffing guard ---

def test_buzzword_salad_does_not_promote():
    # The naive attack: text that IS scoring markers. Marker density 0.58 >
    # 0.5 -> actionability capped at 5.9 -> cannot PROMOTE.
    v = mod.triage(SALAD)
    assert v["verdict"] != "PROMOTE", v
    assert v["scores"]["actionability"] <= 5.9, v
    assert any("keyword-stuffed" in r for r in v["reasons"]), v


def test_tight_real_lesson_still_promotes():
    # False-positive companion: a tight real lesson (density 0.40) must
    # still PROMOTE — the guard must not eat concise real lessons.
    tight = ("Always verify the lane claim before spawning any worker. "
             "Enforcement: an unclaimed lane blocks the spawn and the "
             "dispatcher aborts.")
    assert mod._marker_density(tight) <= 0.5
    v = mod.triage(tight)
    assert v["verdict"] == "PROMOTE", v


def test_short_teeth_fragment_unaffected():
    # The guard only caps; it must not change verdicts that were already
    # below the bar for other reasons.
    v = mod.triage("Enforcement: the gate blocks bad merges.")
    assert v["verdict"] in ("LOG", "DROP"), v


@pytest.mark.xfail(strict=True, reason="adaptive stuffing dilutes marker "
                   "density below 0.5 with filler nouns; the density guard "
                   "only stops the naive attack — needs semantic judgment")
def test_adaptive_salad_with_filler_nouns_does_not_promote():
    adaptive = ("The report about the quarterly planning session mentions "
                "several ordinary items. People discussed schedules, budgets, "
                "rooms, coffee, parking, laptops, cables, chairs, windows, "
                "doors, lights, folders, papers, pens, clocks. Always whenever "
                "every mechanism law principle protocol contract invariant "
                "paradigm synergy leverage. When actioning, claim use add "
                "remove run build fix measure score dispatch. Enforcement: "
                "enforce gate check fail verify prove refuse block abort test.")
    v = mod.triage(adaptive)
    assert v["verdict"] != "PROMOTE", v


# --- Honest reds: attacks that still get through ---

@pytest.mark.xfail(strict=True, reason="semantic vacuity: shape scorers "
                   "cannot read meaning — stuffed trivia has trigger, verb, "
                   "enforcement and 'always' but informs no hive decision; "
                   "needs semantic/hive-world judgment")
def test_stuffed_trivia_does_not_promote():
    trivia = ("Lunch was good. When you eat lunch, always verify the plate "
              "is empty before seconds. Enforcement: the plate blocks hunger "
              "and the cook refuses refills.")
    v = mod.triage(trivia)
    assert v["verdict"] != "PROMOTE", v


@pytest.mark.xfail(strict=True, reason="combined attack: synonym-reworded "
                   "dupe plus marker filler evades stemming (synonyms), "
                   "containment (reworded) and the density guard (diluted) — "
                   "needs embeddings + semantic judgment together")
def test_combined_synonym_filler_attack_does_not_promote():
    attack = ("Never launch an agent without first reserving the lane in the "
              "state record. A rejected reservation means the lane is "
              "occupied. Enforcement: the record tool exits nonzero and the "
              "dispatcher halts the launch. When the hive learns, every "
              "mechanism law principle protocol contract invariant whenever "
              "always never " + FILLER_MARKERS)
    v = mod.triage(attack, existing_lesson_texts=[MECHANISM_LESSON])
    assert v["verdict"] != "PROMOTE", v


# --- Containment edge: micro-lesson elaboration ---

def test_elaborated_micro_lesson_drops():
    # If the corpus holds "Check the lane first." and the candidate is a
    # long restatement containing it whole, DROP is correct: it adds no
    # signal, only words. Containment working as intended, not a false
    # positive.
    new = ("Checking the lane first remains the rule before anything else "
           "begins; every worker must check the lane first, always, because "
           "lane order governs dispatch and the truth file is the authority "
           "on lane state. Enforcement: unclaimed lanes block the spawn.")
    v = mod.triage(new, existing_lesson_texts=["Check the lane first."])
    assert v["verdict"] == "DROP", v
    assert "padded duplicate" in v["reasons"][0], v
