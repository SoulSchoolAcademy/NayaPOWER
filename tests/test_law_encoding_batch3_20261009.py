"""Tests for the 2026-10-09 law-encoding BATCH 3.

Every law encoded this batch gets the same proof contract:
  - a VIOLATING fixture makes the check FAIL (the encoding fires), and
  - an HONORING fixture makes the check PASS (the encoding stays quiet).

Runnable with plain python3 (no pytest required):
    python3 tests/test_law_encoding_batch3_20261009.py
Also pytest-compatible (plain assert functions).

Re-validator: `python3 -m pytest tests/test_law_encoding_batch3_20261009.py -v`
runs this file blind — no fixtures outside this file.

Covers:
  - decision_receipt.py (The Decision Receipt Law)
  - wisest_choice.py    (The Wisest Choice Law — Shawn's standing command)
  - merge_authority.py  (Delegated Merge Authority — the 5-condition gate)

Note on overlap: decision_log.py and scorecard.py (on main) hold the
decision MATH; this batch holds the decision RECEIPT (the report), the
JUDGMENT contract (objective + named basis + justified questions), and
the merge packet gate. No law is encoded twice.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / "tools" / "protocol" / "checks"
sys.path.insert(0, str(CHECKS.parent))

from checks import decision_receipt, merge_authority, wisest_choice  # noqa: E402


# ================================================================ fixtures

def _good_receipt():
    return {
        "decision": "batch-3 law selection",
        "chosen": "opt-c",
        "alternatives": [
            {"id": "opt-a", "description": "Decision Receipt Law"},
            {"id": "opt-b", "description": "Wisest Choice Law"},
            {"id": "opt-c", "description": "Delegated Merge Authority"},
            {"id": "opt-d", "description": "SN-0575 Fix It First"},
        ],
        "winning_evidence": "scorecard 8.5/8.0/8.3 vs 7.2; A+B cover SN-0522's remaining slice",
        "receipt": ("I chose opt-c. I looked at opt-a, opt-b, opt-c, opt-d. "
                    "opt-c won because its scorecard beat opt-d's 7.2 and "
                    "A+B already cover D's slice. This is what I did."),
        "seat": "naya-5",
        "close_call": False,
        "uncertainty_declared": False,
    }


def _good_wisest():
    return {
        "decision": "batch-3 branch base",
        "objective": "keep the law-encoding lane moving with independent re-validation",
        "options_analyzed": ["stack on 8c9a44ab", "fresh off main @ 45f0ed26c"],
        "basis": {"type": "law", "ref": "DECISION-RECEIPT-LAW"},
        "question_asked": False,
        "close_call": False,
        "uncertainty_declared": False,
    }


def _good_merge_packet():
    return {
        "target": "main",
        "branch": "naya5/law-encoding-batch3",
        "seat": "naya-5",
        "tests_green": True,
        "test_evidence": "pytest 61/61 green, CI workflow run #...", 
        "self_scorecard": {"score": 9.1, "evidence_backed": True,
                           "value_calculus_run": True},
        "independent_validator": "naya-1",
        "posted_to_1354": True,
        "team_objections": 0,
        "post_merge_report_planned": True,
    }


# ======================================================== decision_receipt

def test_receipt_honoring_passes():
    r = decision_receipt.check(_good_receipt())
    assert r["pass"], r["reasons"]


def test_receipt_fires_when_alternatives_missing():
    rec = _good_receipt()
    del rec["alternatives"]
    r = decision_receipt.check(rec)
    assert not r["pass"], "absence of alternatives must fail closed"


def test_receipt_fires_when_single_alternative():
    rec = _good_receipt()
    rec["alternatives"] = [{"id": "opt-c", "description": "Delegated Merge Authority"}]
    r = decision_receipt.check(rec)
    assert not r["pass"], "one option is not a decision"


def test_receipt_fires_when_chosen_not_in_field():
    rec = _good_receipt()
    rec["chosen"] = "z"
    r = decision_receipt.check(rec)
    assert not r["pass"], "choosing what was never looked at is guessing"


def test_receipt_fires_when_winning_evidence_missing():
    rec = _good_receipt()
    rec["winning_evidence"] = ""
    r = decision_receipt.check(rec)
    assert not r["pass"], "'X won because [evidence]' is load-bearing"


def test_receipt_fires_when_receipt_names_no_choice():
    rec = _good_receipt()
    rec["receipt"] = "We considered some options and picked the best one."
    r = decision_receipt.check(rec)
    assert not r["pass"], "the receipt must name the choice"


def test_receipt_fires_when_receipt_omits_an_alternative():
    rec = _good_receipt()
    rec["receipt"] = ("I chose opt-c. I looked at opt-a, opt-b, opt-c. "
                      "opt-c won because evidence.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "'I looked at A, B, C' must name the field"


def test_receipt_fires_when_close_call_not_declared():
    rec = _good_receipt()
    rec["close_call"] = True
    rec["uncertainty_declared"] = False
    r = decision_receipt.check(rec)
    assert not r["pass"], "honest on close calls"


def test_receipt_passes_when_close_call_declared_honestly():
    rec = _good_receipt()
    rec["close_call"] = True
    rec["uncertainty_declared"] = True
    r = decision_receipt.check(rec)
    assert r["pass"], r["reasons"]


def test_receipt_fires_when_seat_anonymous():
    rec = _good_receipt()
    rec["seat"] = ""
    r = decision_receipt.check(rec)
    assert not r["pass"], "anonymous decisions are void"


# =========================================================== wisest_choice

def test_wisest_honoring_passes():
    r = wisest_choice.check(_good_wisest())
    assert r["pass"], r["reasons"]


def test_wisest_fires_when_objective_missing():
    rec = _good_wisest()
    rec["objective"] = ""
    r = wisest_choice.check(rec)
    assert not r["pass"], "objective-less decisions cannot be wisest"


def test_wisest_fires_when_basis_unadmitted():
    rec = _good_wisest()
    rec["basis"] = {"type": "vibes", "ref": "felt right"}
    r = wisest_choice.check(rec)
    assert not r["pass"], "opinion is not authority"


def test_wisest_fires_when_basis_ref_missing():
    rec = _good_wisest()
    rec["basis"] = {"type": "protocol", "ref": ""}
    r = wisest_choice.check(rec)
    assert not r["pass"], "authority theater — name the source"


def test_wisest_fires_when_basis_absent():
    rec = _good_wisest()
    del rec["basis"]
    r = wisest_choice.check(rec)
    assert not r["pass"], "missing basis fails closed"


def test_wisest_fires_on_unjustified_question():
    rec = _good_wisest()
    rec["question_asked"] = True
    r = wisest_choice.check(rec)
    assert not r["pass"], "'A, B, or C?' without naming the gate is a violation"


def test_wisest_passes_on_justified_question():
    rec = _good_wisest()
    rec["question_asked"] = True
    rec["protected_gate"] = "production deploys need Shawn's word"
    r = wisest_choice.check(rec)
    assert r["pass"], r["reasons"]


def test_wisest_passes_on_genuine_ambiguity_question():
    rec = _good_wisest()
    rec["question_asked"] = True
    rec["genuine_ambiguity"] = "protocol admits two readings; only Shawn's intent resolves it"
    r = wisest_choice.check(rec)
    assert r["pass"], r["reasons"]


def test_wisest_fires_when_close_call_not_declared():
    rec = _good_wisest()
    rec["close_call"] = True
    r = wisest_choice.check(rec)
    assert not r["pass"], "decisive on clear winners, honest on close calls"


def test_wisest_fires_when_single_option_analyzed():
    rec = _good_wisest()
    rec["options_analyzed"] = ["fresh off main @ 45f0ed26c"]
    r = wisest_choice.check(rec)
    assert not r["pass"], "the wisest choice among one option is a ceremony"


# ========================================================= merge_authority

def test_merge_honoring_passes():
    r = merge_authority.check(_good_merge_packet())
    assert r["pass"], r["reasons"]


def test_merge_fires_when_tests_not_green():
    rec = _good_merge_packet()
    rec["tests_green"] = False
    r = merge_authority.check(rec)
    assert not r["pass"], "condition (1) not met"


def test_merge_fires_when_score_below_nine():
    rec = _good_merge_packet()
    rec["self_scorecard"]["score"] = 8.9
    r = merge_authority.check(rec)
    assert not r["pass"], "below 9.0 still needs Shawn's word"


def test_merge_fires_when_score_not_evidence_backed():
    rec = _good_merge_packet()
    rec["self_scorecard"]["evidence_backed"] = False
    r = merge_authority.check(rec)
    assert not r["pass"], "scores move only on evidence"


def test_merge_fires_when_value_calculus_not_run():
    rec = _good_merge_packet()
    rec["self_scorecard"]["value_calculus_run"] = False
    r = merge_authority.check(rec)
    assert not r["pass"], "'most intelligent thing wins' requires the math"


def test_merge_fires_when_validator_is_self():
    rec = _good_merge_packet()
    rec["independent_validator"] = "naya-5"
    r = merge_authority.check(rec)
    assert not r["pass"], "self-validation is not independent validation"


def test_merge_fires_when_validator_unnamed():
    rec = _good_merge_packet()
    rec["independent_validator"] = ""
    r = merge_authority.check(rec)
    assert not r["pass"], "absence fails closed"


def test_merge_fires_when_not_posted_to_1354():
    rec = _good_merge_packet()
    rec["posted_to_1354"] = False
    r = merge_authority.check(rec)
    assert not r["pass"], "unposted intent is not team consensus"


def test_merge_fires_when_team_objects():
    rec = _good_merge_packet()
    rec["team_objections"] = 1
    r = merge_authority.check(rec)
    assert not r["pass"], "a seat objects — still needs Shawn's word"


def test_merge_fires_when_no_post_merge_report():
    rec = _good_merge_packet()
    rec["post_merge_report_planned"] = False
    r = merge_authority.check(rec)
    assert not r["pass"], "merge, THEN report after"


def test_merge_passes_by_scope_for_non_main_target():
    rec = _good_merge_packet()
    rec["target"] = "feature-branch"
    rec["tests_green"] = False  # even a red packet passes: law not applicable
    r = merge_authority.check(rec)
    assert r["pass"], "delegation covers merges to main only"


# ================================================================== CLI

def _cli(mod, record):
    p = subprocess.run(
        [sys.executable, str(CHECKS / mod), "--record",
         __import__("json").dumps(record)],
        capture_output=True, text=True, timeout=30,
    )
    return p.returncode


def test_cli_decision_receipt_fires_and_silences():
    assert _cli("decision_receipt.py", _good_receipt()) == 0
    bad = _good_receipt()
    bad["winning_evidence"] = ""
    assert _cli("decision_receipt.py", bad) == 1


def test_cli_wisest_choice_fires_and_silences():
    assert _cli("wisest_choice.py", _good_wisest()) == 0
    bad = _good_wisest()
    bad["basis"] = {"type": "instinct", "ref": ""}
    assert _cli("wisest_choice.py", bad) == 1


def test_cli_merge_authority_fires_and_silences():
    assert _cli("merge_authority.py", _good_merge_packet()) == 0
    bad = _good_merge_packet()
    bad["team_objections"] = 2
    assert _cli("merge_authority.py", bad) == 1


# ================================================== gap closures (batch-3 re-validator)

def test_receipt_fires_on_article_id_exploit():
    # The re-validator's gap 1: id "a" passed as the English word "a" in
    # prose — the receipt never names the alternative, yet the name-check
    # passed on articles.
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "a", "description": "plan alpha"},
        {"id": "the", "description": "plan beta"},
    ]
    rec["chosen"] = "a"
    rec["receipt"] = ("I chose the best option after a thorough review. "
                      "a won because the evidence favored a.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "dictionary-word ids must fail closed (article exploit)"


def test_receipt_fires_on_common_word_id_case_insensitive():
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "This", "description": "plan alpha"},
        {"id": "opt-2", "description": "plan beta"},
    ]
    rec["chosen"] = "This"
    rec["receipt"] = ("I chose This. I looked at This and opt-2. "
                      "This won because evidence.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "'This' is an ordinary word even capitalized"


def test_receipt_fires_on_template_placeholder_letter_id():
    # "b" is template vocabulary now: the law's own template writes
    # "I looked at A, B, C" in every receipt, so a bare "b" id can never
    # be genuinely named — it fails closed exactly like "a".
    rec = {
        "decision": "tiny pick",
        "chosen": "b",
        "alternatives": [
            {"id": "b", "description": "plan beta"},
            {"id": "opt-2", "description": "plan gamma"},
        ],
        "winning_evidence": "b scored 9.1 vs 7.0",
        "receipt": ("I chose b. I looked at b and opt-2. b won because its "
                    "score beat opt-2. This is what I did."),
        "seat": "naya-5",
        "close_call": False,
        "uncertainty_declared": False,
    }
    r = decision_receipt.check(rec)
    assert not r["pass"], "template placeholder letters must fail closed as ids"


def test_wisest_fires_on_fabricated_law_ref():
    # The re-validator's gap 2: {"type": "law", "ref": "SN-9999 ..."} was
    # verified against nothing.
    rec = _good_wisest()
    rec["basis"] = {"type": "law", "ref": "SN-9999 the law I just made up"}
    r = wisest_choice.check(rec)
    assert not r["pass"], "fabricated law refs must fail"


def test_wisest_fires_on_nonexistent_sn_number():
    rec = _good_wisest()
    rec["basis"] = {"type": "law", "ref": "SN-0000"}
    r = wisest_choice.check(rec)
    assert not r["pass"], "nonexistent SN numbers must fail"


def test_wisest_passes_on_real_law_id():
    rec = _good_wisest()
    rec["basis"] = {"type": "law", "ref": "WISEST-CHOICE-LAW"}
    r = wisest_choice.check(rec)
    assert r["pass"], r["reasons"]


def test_wisest_passes_on_sn_number_inside_prose_ref():
    rec = _good_wisest()
    rec["basis"] = {"type": "law", "ref": "SN-0522 Self-Governing Intelligence"}
    r = wisest_choice.check(rec)
    assert r["pass"], r["reasons"]


def test_wisest_passes_on_law_name():
    rec = _good_wisest()
    rec["basis"] = {"type": "law", "ref": "The Decision Receipt Law"}
    r = wisest_choice.check(rec)
    assert r["pass"], r["reasons"]


def test_merge_fires_when_validator_is_alias_of_seat():
    # The re-validator's gap 3: "naya5" vs "naya-5" passed as "different";
    # string inequality is not identity.
    rec = _good_merge_packet()
    rec["independent_validator"] = "naya5"  # seat is "naya-5"
    r = merge_authority.check(rec)
    assert not r["pass"], "alias evasion: naya5 == naya-5"


def test_merge_fires_when_validator_differs_only_by_case_and_spaces():
    rec = _good_merge_packet()
    rec["independent_validator"] = "NAYA 5"
    r = merge_authority.check(rec)
    assert not r["pass"], "case/separator variants are the same seat"


def test_merge_fires_when_validator_is_fullwidth_alias_of_seat():
    # The NFKC hole: fullwidth "ｎａｙａ５" stripped to "" which matched
    # nothing, so self-validation sailed through as "different".
    # Normalization must translate before it compares, never erase.
    rec = _good_merge_packet()
    rec["independent_validator"] = "ｎａｙａ５"  # seat is "naya-5"
    r = merge_authority.check(rec)
    assert not r["pass"], "fullwidth self-validation is not independent validation"


def test_seat_key_nfkc_folds_fullwidth_to_ascii():
    assert merge_authority._seat_key("ｎａｙａ５") == merge_authority._seat_key("naya-5") == "naya5"
    assert merge_authority._seat_key("ｎａｙａ４") == "naya4"


def test_merge_passes_for_fullwidth_of_a_different_seat():
    # The fix must not glue distinct seats together: fullwidth naya-4 is
    # still a different seat from naya-5.
    rec = _good_merge_packet()
    rec["independent_validator"] = "ｎａｙａ４"
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]


def test_merge_passes_for_genuinely_distinct_seats():
    rec = _good_merge_packet()
    rec["independent_validator"] = "naya-4"
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]


# --------------------------------- confusables class (batch-3 lane fixer)
# The parked watch-list class: Cyrillic/Greek/Armenian homoglyph smuggling.
# NFKC cannot fold U+0430 CYRILLIC SMALL LETTER A -- it is a distinct
# letter, not a compatibility form -- so the NFKC micro-fix leaves this
# class wide open. Policy: normalize-and-flag (fold to canonical ASCII
# per Unicode confusables.txt before comparing; record the fold in the
# details). Reject-on-mixed-script was measured and rejected: a fully
# Cyrillic "naya-5" (every letter Cyrillic; digits/hyphen are
# Script=Common) is single-script and would sail past it. Folding is
# script-agnostic. Non-ASCII is written as \u escapes here on purpose:
# invisible homoglyphs in source are a maintenance hazard.
# ---

def test_merge_fires_when_validator_is_cyrillic_a_alias_of_seat():
    # The original instance: "nаya-5" with U+0430 CYRILLIC SMALL LETTER A.
    rec = _good_merge_packet()
    rec["independent_validator"] = "n\u0430ya-5"  # seat is "naya-5"
    r = merge_authority.check(rec)
    assert not r["pass"], "cyrillic-a self-validation is not independent validation"
    assert r["details"].get("confusables_folded") is True


def test_merge_fires_on_fresh_mixed_script_variants():
    # Six fresh single-char swaps across Cyrillic/Greek/Armenian, all must
    # fold to the seat and fire. Class-first: not the one instance, the
    # whole family.
    variants = [
        "n\u03b1ya-5",   # GREEK SMALL LETTER ALPHA for a
        "na\u0443a-5",   # CYRILLIC SMALL LETTER U for y
        "\u039daya-5",   # GREEK CAPITAL LETTER NU for n
        "\u0578aya-5",   # ARMENIAN SMALL LETTER VO for n
        "n\u0430y\u0430-5",  # two Cyrillic swaps at once
        "n\u03b1y\u03b1-5",  # two Greek swaps at once
    ]
    for v in variants:
        rec = _good_merge_packet()
        rec["independent_validator"] = v
        r = merge_authority.check(rec)
        assert not r["pass"], f"smuggled variant {v!r} passed as a different seat"
        assert merge_authority._seat_key(v) == "naya5", f"{v!r} did not fold to naya5"
    # Different seat family, same class:
    rec = _good_merge_packet()
    rec["seat"] = "coda-1"
    rec["independent_validator"] = "\u0441oda-1"  # CYRILLIC SMALL LETTER ES for c
    r = merge_authority.check(rec)
    assert not r["pass"], "cyrillic-es self-validation is not independent validation"


def test_merge_fires_on_full_cyrillic_homoglyph_string():
    # Every LETTER Cyrillic: "\u0441\u043e\u0501\u0430" (es, o, komi de,
    # a) + "-1" is visually "coda-1". Digits and the hyphen are
    # Script=Common, so this is single-script -- a reject-on-mixed-script
    # policy is blind to it. Folding is script-agnostic, not fooled.
    # (Note: Cyrillic \u043d looks like 'h', not 'n' -- a "fully Cyrillic
    # naya-5" is not a visual twin at all. The honest twin is coda-1's.)
    rec = _good_merge_packet()
    rec["seat"] = "coda-1"
    rec["independent_validator"] = "\u0441\u043e\u0501\u0430-1"
    r = merge_authority.check(rec)
    assert not r["pass"], "single-script cyrillic self-validation must not pass"
    assert merge_authority._seat_key("\u0441\u043e\u0501\u0430-1") == "coda1"


def test_seat_key_folds_confusables_to_ascii():
    assert merge_authority._seat_key("n\u0430ya-5") == "naya5"
    assert merge_authority._seat_key("n\u03b1ya-5") == "naya5"
    assert merge_authority._seat_key("\u0578aya-5") == "naya5"
    assert merge_authority._seat_key("\u0441oda-1") == "coda1"
    # provenance flag: clean text folds nothing, smuggled text folds
    key, folded = merge_authority._seat_key_folded("naya-5")
    assert (key, folded) == ("naya5", False)
    key, folded = merge_authority._seat_key_folded("n\u0430ya-5")
    assert (key, folded) == ("naya5", True)


def test_merge_flags_confusables_in_details():
    rec = _good_merge_packet()
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]
    assert r["details"].get("confusables_folded") is False
    rec = _good_merge_packet()
    rec["independent_validator"] = "n\u0430ya-5"
    r = merge_authority.check(rec)
    assert not r["pass"]
    assert r["details"]["seat_key"] == r["details"]["validator_key"] == "naya5"
    assert r["details"]["confusables_folded"] is True


def test_merge_passes_for_confusable_fold_of_a_different_seat():
    # The fold must not glue distinct seats together: the Cyrillic twin of
    # "coda-2" folds to coda2, still a different seat from coda-1.
    rec = _good_merge_packet()
    rec["seat"] = "coda-1"
    rec["independent_validator"] = "\u0441\u043e\u0501\u0430-2"
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]


def test_merge_passes_with_multiscript_prose_in_evidence():
    # Honest multi-script prose must NOT false-positive: the fold only
    # touches seat identity comparison, never the evidence field.
    rec = _good_merge_packet()
    rec["test_evidence"] = ("pytest 61/61 green, CI run 42; notes: "
                            "проверка системы, δοκιμή, համակարգ")
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]


def test_merge_fires_on_infinite_score():
    # The re-validator's gap 4: score Infinity passed the 9.0 bar.
    rec = _good_merge_packet()
    rec["self_scorecard"]["score"] = float("inf")
    r = merge_authority.check(rec)
    assert not r["pass"], "Infinity is not a score"


def test_merge_fires_on_nan_score():
    rec = _good_merge_packet()
    rec["self_scorecard"]["score"] = float("nan")
    r = merge_authority.check(rec)
    assert not r["pass"], "NaN is not a score"


def test_merge_fires_on_score_above_ten():
    rec = _good_merge_packet()
    rec["self_scorecard"]["score"] = 11.0
    r = merge_authority.check(rec)
    assert not r["pass"], "scores live on the 0-10 scale"


def test_merge_passes_on_boundary_scores():
    # Honoring side: the bar's own edges stay legal.
    for s in (9.0, 10.0):
        rec = _good_merge_packet()
        rec["self_scorecard"]["score"] = s
        r = merge_authority.check(rec)
        assert r["pass"], (s, r["reasons"])


def test_merge_fires_on_claim_shaped_evidence():
    # The re-validator's residual risk: "trust me, green" is unfalsifiable,
    # not proof.
    rec = _good_merge_packet()
    rec["test_evidence"] = "trust me, green"
    r = merge_authority.check(rec)
    assert not r["pass"], "'trust me, green' is unfalsifiable, not proof"


def test_merge_passes_on_url_shaped_evidence():
    rec = _good_merge_packet()
    rec["test_evidence"] = ("https://github.com/SoulSchoolAcademy/NayaPOWER/"
                            "actions/runs/4821 — 61/61 green")
    r = merge_authority.check(rec)
    assert r["pass"], r["reasons"]


# ================= template-vocabulary ghost ids (re-validator's residual hole)

def test_receipt_fires_on_ghost_ids_chose_looked_end_to_end():
    # The re-validator's demonstrated exploit, locked in as a regression:
    # ghost options with ids "chose"/"looked" and a receipt written in the
    # law's own template that never names either option PASSED the full
    # check pre-fix. The template writes those words by construction.
    rec = {
        "decision": "revalidator demo",
        "chosen": "chose",
        "alternatives": [
            {"id": "chose", "description": "ghost option one"},
            {"id": "looked", "description": "ghost option two"},
        ],
        "winning_evidence": "it scored well",
        "receipt": ("I chose the winner. I looked at every option carefully. "
                    "The winner won because evidence showed it was best. "
                    "This is what I did."),
        "seat": "naya-5",
        "close_call": False,
        "uncertainty_declared": False,
    }
    r = decision_receipt.check(rec)
    assert not r["pass"], "ghost ids from the template vocabulary must fail closed"


def _ghost_verbfamily_rec(ghost_id, receipt):
    # Ghost is an unchosen alternative; the receipt is natural prose that
    # only ever mentions the ghost word BY ACCIDENT ("had to choose",
    # "one hard look"). Pre-fix every such record PASSED end-to-end —
    # the word was not banned, so step 2 let it through and the
    # bounded-token name-check in step 5 matched the accidental token.
    return {
        "decision": "verb-family ghost demo",
        "chosen": "opt-a",
        "alternatives": [
            {"id": ghost_id, "description": "ghost option"},
            {"id": "opt-a", "description": "plan alpha"},
        ],
        "winning_evidence": "measured faster in the field trial",
        "receipt": receipt,
        "seat": "naya-5",
        "close_call": False,
        "uncertainty_declared": False,
    }


def test_receipt_fires_on_ghost_id_choose():
    # Verb-family closure (class-fix): the template writes "chose", but the
    # same past-tense idea arrives in receipts as "choose" — the ban must
    # cover the family, exactly as ORDINARY_WORDS already covers full
    # conjugations for every other verb in the list.
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "choose",
        "I chose opt-a. I looked at opt-a and the other plan. opt-a won "
        "because the measured score was higher, and honestly I had to "
        "choose fast."))
    assert not r["pass"], "ghost id 'choose' must fail closed"


def test_receipt_fires_on_ghost_id_chosen():
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "chosen",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because the "
        "field data favored it; I have chosen the safer plan."))
    assert not r["pass"], "ghost id 'chosen' must fail closed"


def test_receipt_fires_on_ghost_id_chooses():
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "chooses",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because the "
        "protocol chooses the measured winner, and that was opt-a."))
    assert not r["pass"], "ghost id 'chooses' must fail closed"


def test_receipt_fires_on_ghost_id_choosing():
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "choosing",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because "
        "choosing on evidence instead of vibes is the law."))
    assert not r["pass"], "ghost id 'choosing' must fail closed"


def test_receipt_fires_on_ghost_id_look():
    # The template's "looked" is banned; its bare-stem sibling "look" is
    # equally accidental in prose ("one hard look"). Bounded-token matching
    # means banning "look" never collides with "looked" — the honest
    # template token — anywhere else.
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "look",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because one "
        "hard look at opt-b showed weaker evidence."))
    assert not r["pass"], "ghost id 'look' must fail closed"


def test_receipt_fires_on_ghost_id_looks():
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "looks",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because it "
        "looks stronger on every measure."))
    assert not r["pass"], "ghost id 'looks' must fail closed"


def test_receipt_fires_on_ghost_id_looking():
    r = decision_receipt.check(_ghost_verbfamily_rec(
        "looking",
        "I chose opt-a. I looked at opt-a, opt-b. opt-a won because I "
        "kept looking at opt-b and the numbers never moved."))
    assert not r["pass"], "ghost id 'looking' must fail closed"


def test_receipt_fires_on_ghost_id_evidence():
    # "[evidence]" is the template's own evidence slot — the word appears
    # naturally in every template receipt, so it can never name an option.
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "evidence", "description": "ghost option"},
        {"id": "opt-2", "description": "plan beta"},
    ]
    rec["chosen"] = "opt-2"
    rec["receipt"] = ("I chose opt-2. I looked at opt-2 and the evidence. "
                      "opt-2 won because the evidence was strong. "
                      "This is what I did.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "'evidence' is template vocabulary, not an id"


def test_receipt_fires_on_ghost_id_x():
    # "X" is the template's chosen placeholder ("I chose X ... X won") —
    # every template receipt writes it without naming any option.
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "x", "description": "ghost option"},
        {"id": "opt-2", "description": "plan beta"},
    ]
    rec["chosen"] = "x"
    rec["receipt"] = ("I chose X. I looked at X and opt-2. X won because of "
                      "scoring. This is what I did.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "'x' is the template's placeholder, not an id"


def test_receipt_fires_on_ghost_id_c():
    # "C" is the template's third-placeholder letter ("A, B, C") — same
    # class as "b", which fails closed above.
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "c", "description": "ghost option"},
        {"id": "opt-2", "description": "plan beta"},
    ]
    rec["chosen"] = "c"
    rec["receipt"] = ("I chose X. I looked at A, B, C. X won because it "
                      "scored 9.1. This is what I did.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "template placeholder letters must fail closed as ids"


def test_receipt_passes_with_honest_identifiers():
    # Honoring side for the closure: real identifiers that a receipt must
    # deliberately write stay legal. The dictionary check is full-string
    # equality, so "opt-a" never collides with the banned bare letter "a".
    rec = {
        "decision": "honest pick",
        "chosen": "opt-alpha",
        "alternatives": [
            {"id": "opt-a", "description": "plan alpha"},
            {"id": "plan-2", "description": "plan beta"},
            {"id": "opt-alpha", "description": "plan gamma"},
        ],
        "winning_evidence": "opt-alpha scored 9.1 vs 7.0 and 6.5",
        "receipt": ("I chose opt-alpha. I looked at opt-a, plan-2, "
                    "opt-alpha. opt-alpha won because it scored 9.1. "
                    "This is what I did."),
        "seat": "naya-5",
        "close_call": False,
        "uncertainty_declared": False,
    }
    r = decision_receipt.check(rec)
    assert r["pass"], r["reasons"]



# ------------------------------------------------- fix2: dead-entry lane
# Re-validator's D1-D3: U+03F2 in "coda-1" sailed through end-to-end --
# NFKC mapped it to U+03C2 first, the table never saw U+03C2, the strip
# deleted it: "oda1" vs "coda1" -> PASSED as a different seat. The
# fixpoint fold (NFKC-after-fold, iterated) plus the 2 NFKC-closure
# entries (U+03C2/U+03A3 -> 'c') close this lane. Non-ASCII is written
# as \u escapes here on purpose: invisible homoglyphs in source are a
# maintenance hazard.
# ---

def test_merge_fires_on_lunate_sigma_dead_entries():
    # The exact re-validator probes: U+03F2, U+03F9, and the direct
    # NFKC-output attacks U+03C2 / U+03A3 typed by hand.
    twins = (
        "\u03f2oda-1",  # GREEK LUNATE SIGMA SYMBOL
        "\u03f9oda-1",  # GREEK CAPITAL LUNATE SIGMA SYMBOL
        "\u03c2oda-1",  # GREEK SMALL LETTER FINAL SIGMA (direct)
        "\u03a3oda-1",  # GREEK CAPITAL LETTER SIGMA (direct)
    )
    for twin in twins:
        rec = _good_merge_packet()
        rec["seat"] = "coda-1"
        rec["independent_validator"] = twin
        r = merge_authority.check(rec)
        assert not r["pass"], f"dead-entry twin {twin!r} passed as a different seat"
    assert merge_authority._seat_key("\u03f2oda-1") == "coda1"
    assert merge_authority._seat_key("\u03c2oda-1") == "coda1"


def test_merge_fires_on_nfkc_retargeted_variants():
    # NFKC-retargeted entries (2026-10-09, re-grounded -- was
    # test_merge_fires_on_fresh_dead_entry_variants): the table now folds
    # these to their NFKC behavior, not confusables.txt's MA mapping. A
    # human reading "\u017fin-1" reads "sin-1", not "fin-1"; the old
    # assertions encoded the defeated MA judgment. The gate is unchanged
    # in form: the twin is caught against its HONEST canonical, and it
    # must NOT collide with the defeated MA canonical (no false merge of
    # seats a human reads as different).
    twins = [
        # (twin, honest_seat, honest_key, defeated_ma_seat)
        ("\u017fin-1", "sin-1", "sin1", "fin-1"),      # LONG S -> 's'
        ("\u2110ook-1", "iook-1", "iook1", "look-1"),   # SCRIPT CAPITAL I -> 'i'
        ("\u2160ook-1", "iook-1", "iook1", "look-1"),   # ROMAN NUMERAL ONE -> 'i'
        ("\uff29ook-1", "iook-1", "iook1", "look-1"),   # FULLWIDTH CAPITAL I -> 'i'
        ("\u2119in-1", "pin-1", "pin1", None),          # DOUBLE-STRUCK P -> 'p'
    ]
    for twin, seat, key, defeated in twins:
        rec = _good_merge_packet()
        rec["seat"] = seat
        rec["independent_validator"] = twin
        r = merge_authority.check(rec)
        assert not r["pass"], f"retargeted twin {twin!r} passed as {seat!r}"
        assert merge_authority._seat_key(twin) == key
        if defeated is not None:
            assert merge_authority._seat_key(twin) != \
                merge_authority._seat_key(defeated), \
                f"twin {twin!r} still collides with defeated {defeated!r}"
    # Stylistic digit forms stay digits in the seat key (digit/letter
    # non-fold policy, now honored in this lane too):
    assert merge_authority._seat_key("naya-\U0001d7ce") == "naya0"
    assert merge_authority._seat_key("naya-\U0001d7cf") == "naya1"
    # The 45-char residual a single-pass reorder misses: NFKC output IS
    # a table source (U+02E0 -> U+0263 -> 'y').
    assert merge_authority._seat_key("\u02e0") == "y"


def test_confusable_fold_closes_every_enumerated_pair():
    # The class property, not instances: for ALL 1455 table sources,
    # the fixpoint fold must equal the enumerated target.
    import re as _re
    from checks import confusables_table
    bad = []
    for s, tgt in zip(confusables_table._SRC, confusables_table._DST):
        got = _re.sub(r"[^a-z0-9]", "",
                      confusables_table.fold_to_ascii_fixpoint(s).lower())
        if got != tgt:
            bad.append((hex(ord(s)), tgt, got))
    assert not bad, f"{len(bad)} enumerated pairs do not close: {bad[:5]}"


def test_receipt_fires_on_confusable_ghost_word():
    # Re-validator's cross-lane probe: "ch\u043e\u043ese" (2x CYRILLIC
    # SMALL LETTER O) is visually "choose" -- an ordinary word -- but the
    # ban compared raw codepoints and let it through.
    ghost = "ch\u043e\u043ese"
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": ghost, "description": "the familiar option"},
        {"id": "opt-b", "description": "the new option"},
    ]
    rec["chosen"] = ghost
    rec["receipt"] = (f"I chose {ghost}. I looked at {ghost}, opt-b. "
                      f"{ghost} won because it is familiar. This is what I did.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "cyrillic-o ghost word passed the dictionary ban"
    assert decision_receipt._is_dictionary_word(ghost)
    assert decision_receipt._is_dictionary_word("choose")


def test_receipt_fires_on_fresh_ghost_word_variants():
    # Fresh ghost words, not the re-validator's instance: "l\u043e\u043ek"
    # and "ev\u0456dence" (U+0456 CYRILLIC SMALL LETTER
    # BYELORUSSIAN-UKRAINIAN I).
    for ghost in ("l\u043e\u043ek", "ev\u0456dence"):
        assert decision_receipt._is_dictionary_word(ghost), repr(ghost)
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "l\u043e\u043ek", "description": "glance option"},
        {"id": "opt-b", "description": "stare option"},
    ]
    rec["chosen"] = "l\u043e\u043ek"
    rec["receipt"] = ("I chose l\u043e\u043ek. I looked at l\u043e\u043ek, opt-b. "
                      "l\u043e\u043ek won because it is quick. This is what I did.")
    r = decision_receipt.check(rec)
    assert not r["pass"], "cyrillic-o ghost word passed the dictionary ban"


def test_receipt_passes_with_multiscript_prose_and_folded_nonword_id():
    # Honest controls for the cross-lane fix: multi-script prose in the
    # receipt must not false-positive, and a folded id that is NOT a word
    # ("opt-\u03b1" -> "opta") must stay legal.
    rec = _good_receipt()
    rec["alternatives"] = [
        {"id": "opt-\u03b1", "description": "greek-suffixed option"},
        {"id": "plan-2", "description": "second option"},
    ]
    rec["chosen"] = "opt-\u03b1"
    rec["receipt"] = ("I chose opt-\u03b1. I looked at opt-\u03b1, plan-2. "
                      "opt-\u03b1 won because "
                      "\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 "
                      "\u03b4\u03bf\u03ba\u03b9\u03bc\u03ae. "
                      "This is what I did.")
    r = decision_receipt.check(rec)
    assert r["pass"], r["reasons"]
    assert not decision_receipt._is_dictionary_word("opt-\u03b1")
    assert not decision_receipt._is_dictionary_word("naya-5")


if __name__ == "__main__":
    tests = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    print(f"{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(1 if failed else 0)
