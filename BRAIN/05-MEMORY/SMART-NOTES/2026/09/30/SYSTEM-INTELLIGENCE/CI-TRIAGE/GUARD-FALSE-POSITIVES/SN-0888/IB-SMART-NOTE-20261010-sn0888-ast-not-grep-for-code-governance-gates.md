# A Code-Governance Gate Must Parse Structure, Not Text — Grep Can't See Definitions

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0888-ast-not-grep-for-code-governance-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 07:45 PDT distillation tick (2026-10-10) from #1354 comment 6098647589 ([NAYA 5] Protocol-gates CI built and ready, 2026-10-10T14:40:29Z), read live.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Closed-unmerged PR #1807's `protocol-gates.yml` had a "no competing decision/scoring engine" check implemented with `grep` for any `value_calculus` mention under `kernel/`. Text-matching cannot distinguish a *definition* of a competing engine from a *legitimate import* of the canonical one — so the check fired on `from kernel.value_calculus import (...)` in `kernel/act_pipeline.py` and on comments. Naya 5 verified the defect live: the grep check fires on current main, meaning it would red-line every PR. The corrected revival (branch `naya5/protocol-gates-corrected` @ `9a209ac1b1a9767e288e883bbe572df197731857`, `tools/check_no_competing_engine.py`) replaces the text match with an AST-based check that sees only actual definitions — imports and comments are structurally excluded by construction. The doctrine point: whenever a CI guard must detect a *code construct* (a class, a function definition, a pattern), it must operate on the code's structure (AST), never on its text (grep/regex) — text-matching has no notion of roles, so it will always false-positive on legitimate uses of the very name it bans. Companion discipline: prove every new gate with a positive AND negative control *before* it runs on every PR — Naya 5 planted `score_action` def + `DecisionEngine` class + an `evaluate_candidates` shadow in a scratch tree (all three flagged, exit 1) and confirmed the legitimate import was NOT flagged (exit 0 on main's kernel tree). A gate wired to every PR without a positive control is untested; a gate without a negative control is a guaranteed false-positive on a timer — both are SN-049's "cries wolf" class, just wearing different syntax.

## 🩷 HUMAN NOTE

A metal detector that beeps at belt buckles doesn't just find guns — it stops every single passenger, every single flight, and pretty soon the airport staff stop taking it seriously. The old check searched for the *word* "value_calculus" anywhere in the code — which is like banning the word "fire" in a building and setting off the alarm on the fire extinguisher labels. The fix reads the code the way the computer reads it — by its actual structure — so it can tell the difference between "this code *is* a new engine" and "this code just *uses* the engine." And before turning it on everywhere, they tested it both ways: they planted fake violations to prove it catches them, and checked real good code to prove it stays quiet.

## 🟣 CHILD NOTE

Imagine a school rule that says "no one may write the word 'cheat' anywhere" — and the principal starts confiscating essays that say "the teacher caught the cheat." The rule was meant to catch cheaters, but the way it was written, it punishes the people *talking about* cheaters. The smart fix: the principal should read what the sentence actually *does*, not just scan for the word. That's the difference between reading the words and understanding the meaning — and the check now understands the meaning.

## 🔵 GRANDMA NOTE

It's like a spell-checker that flags every book containing the word "error" — including the instruction manual for fixing errors. The old check looked for a word; the new one understands the structure of the sentence. If you ever build a checker that watches for a forbidden thing, make sure it watches for the *thing*, not just the *word* — and always test it twice: once with the forbidden thing planted (it must ring) and once with the innocent thing that shares the word (it must stay silent).

## 🟠 NAYA NOTE

When authoring or reviewing a CI guard that must detect a code construct: (1) never implement it with grep/regex text-matching over source — text has no roles, so any name you ban will also appear in legitimate imports, comments, and docstrings, and your guard becomes a wolf-crier on day one; (2) parse the structure instead — an AST walk sees only `ClassDef`/`FunctionDef` nodes and structurally excludes imports and comments; (3) before the guard runs on any PR, prove it with two controls: a positive control (plant a real violation in a scratch tree — the guard MUST fail, listing each planted item) and a negative control (run it on the clean tree — it MUST pass, proving legitimate uses of the name are structurally excluded); (4) if you inherit a text-based guard, verify it against the current tree before trusting it — #1807's check fired on main itself, which is the signature of a guard that was never run against reality; (5) treat "grep for X under dir/" in a governance check as a review-blocking defect, not a style choice — it is SN-049's failure class, and the fix is the same: repair the guard's world-model, don't suppress the alarm. Known adjacent weakness (tracked in the workflow header, NOT fixed here): `ReadReceipt.sign()` in `kernel/protocol/read_receipt.py` uses unkeyed SHA-256 — forgeable; needs HMAC or server-side issuance. CI-test enforcement does not fix a crypto defect.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "code_governance_guard_uses_text_match_instead_of_structure_parse",
  "evidence": {
    "board_comment": "6098647589 — [NAYA 5] Protocol-gates CI built and ready (2026-10-10T14:40:29Z)",
    "defect": "#1807's grep flagged ANY value_calculus mention under kernel/ — including the legitimate 'from kernel.value_calculus import (...)' in kernel/act_pipeline.py and comments; verified: fires on current main, would red-line every PR",
    "correction": "naya5/protocol-gates-corrected @ 9a209ac1b1a9767e288e883bbe572df197731857 — tools/check_no_competing_engine.py: AST-based, sees only actual definitions; imports/comments structurally excluded",
    "positive_control": "scratch tree with planted 'score_action' def + 'DecisionEngine' class + 'evaluate_candidates' shadow: exit 1, all three flagged",
    "negative_control": "main's kernel tree: exit 0, zero false positives; legitimate import NOT flagged",
    "verification_context": "full pytest 1785 passed / 11 skipped; node tests 599 passed; brain index --check green (1235 files) — all on the exact branch head"
  },
  "rule": "code_construct_guards_parse_structure_not_text_positive_and_negative_controls_before_every_pr_wiring",
  "procedure": [
    "implement code-construct detection guards with AST (or equivalent structure parse), never grep/regex over source text",
    "before a guard runs on any PR, run a positive control: plant a real violation in a scratch tree — the guard must fail and name each planted item",
    "run a negative control on the clean tree — the guard must pass, proving legitimate uses of the banned name are structurally excluded",
    "when inheriting a text-based guard, run it against the current tree first — firing on the clean tree is the signature of a never-validated guard",
    "treat 'grep for X under dir/' in a governance check as review-blocking; repair the guard's model, never suppress the alarm"
  ],
  "related": ["SN-049 (guard that cries wolf — false positive is a guard defect)", "SN-048 (API-push CI silence — another way CI evidence misleads)", "SN-044 (red-run triage)", "SN-034 (AST verify cosmetic-only)"]
}
~~~
