# The PR Body Is a Third Input Channel — Gates That Read It Must Trigger on `edited`

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1037-body-is-third-input-channel
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comments 6116353393 ([LANE BUILD] wave-9 sign-out, 2026-10-12T01:53:41Z), 6116561062 ([NAYA 2 · BUILD LANE] T-2418 slice sign-out, 2026-10-12T02:16:40Z), 6116561232 ([NAYA 2 · verify] T-2399 verify slice sign-out, 2026-10-12T02:16:42Z) — read live on the 19:38 PDT distillation tick; PRs #2418, #2379, #2399.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A pull request has three input channels, not two: the code, the checks config, and the body. The team proved all three properties of the body channel in one night shift:

1. **Body edits never move the head.** [LANE BUILD] patched PR #2379's `## Evidence` section by body edit (01:52:18Z) to strip a bare 40-hex handle — head `e32828b7` unchanged, so the Auditor's in-progress prove slice on the pinned head stayed valid; the live receipt gate re-fired on the edit and went SUCCESS (run 38193569935). The same night, Naya 2's build lane implemented verify's F1+F2 for PR #2418 (literal `## Evidence` + `## Deletions` sections) as a body-only edit — head `43c0113e` unchanged, base still == live tip. A body patch is therefore the cheapest repair path for evidence-section defects: it fixes the gate input without invalidating a single pin-exact proof.

2. **But a gate whose input is the body goes stale by design unless the workflow triggers on `edited`.** PR #2399's receipt-gate workflow triggers only on `opened`/`synchronize`. The gate's input IS the PR body — so every body edit leaves the check row reflecting the pre-edit body, forever, until some unrelated push fires the workflow. Verify's why-not-10 fix list named it exactly: "add `edited` to the trigger types (one line)." The red that stayed after a fix is not a code defect — it is a trigger-shape defect.

3. **Before editing to satisfy a gate, read the gate script's extraction logic.** The first #2418 body edit used plain-text paths; the receipt gate still FAILED. Reading the gate's extraction grammar showed the rule: the handle grammar requires BACKTICKED paths — plain-text paths don't count. Backticked + re-pushed → live CI on the edited event (02:14:52Z): Receipt gate FAILURE→SUCCESS, No silent deletions SUCCESS. The build lane deducted itself 8.5→honest: "the gate's backtick requirement was knowable from the extraction logic before the first push." The script's grammar is cheaper to read than one failed CI round.

The durable rule: **the body is an input channel with its own physics — it doesn't move the head, it doesn't fire events, and its grammar is whatever the gate's parser says.** Treat it as a third channel: patch it freely when the fix is evidence-shape (pins survive); always pair body-consuming workflows with `edited` triggers; never guess the handle grammar — read the extraction code.

## 🩷 HUMAN NOTE

Shawn — a tidy piece of CI physics from the night shift. The PR body turned out to be a third input channel with its own rules: editing it never moves the head SHA (so body patches are the cheapest way to fix evidence-section defects — pin-exact proofs stay valid), but if a CI gate reads the body, the workflow must listen for `edited` events or the check row lies forever after each edit. One team found the red was never a code defect — just a missing one-line trigger. And another learned the hard way to read the gate script's handle grammar before editing: the gate wanted backticked paths, plain text failed, one failed round wasted. Rule banked: read the parser, not the docs-in-your-head.

## 🟣 CHILD NOTE

Imagine a form with three parts: the homework, the answer key, and the name sticker on the folder. Fixing the name sticker never changes the homework inside — that's good (you can fix stickers fast). But if the teacher grades the sticker and never looks at the folder again after you re-stick it, the grade stays wrong. The fix is simple: tell the teacher "look again whenever the sticker changes." And before you write the sticker, check whether the teacher wants it in block letters — read the rule first, don't guess twice.

## 👵 GRANDMA NOTE

It's like the label on a jam jar. Changing the label doesn't change the jam — the contents stay exactly what they were, and anyone who already tasted the jam doesn't need to taste it again. But if the shop's pricing scanner reads the label and nobody rescans after you relabel, the register charges the old price. The answer isn't to re-make the jam; it's to make the scanner beep whenever a label changes. And always read the scanner's manual before you write the label — guessing the format wastes a trip.

## 💜 NAYA NOTE

Note to future me: THE BODY IS A THIRD INPUT CHANNEL — pin this to every gate-writing session. (1) Body patches are the cheapest fix for evidence-shape defects (bare 40-hex, missing ## Evidence/## Deletions, wrong handle grammar): head SHA never moves, pin-exact proofs and in-progress verify slices stay valid. Do body-first for paperwork defects; never force a rebase for them. (2) Any workflow that reads `github.event.pull_request.body` (or title) MUST include `edited` in its trigger types — `opened`/`synchronize`-only means the check row reflects the pre-edit body by design. Diagnose "red after fix" by asking: did the fix land in the body, and did any event fire? (3) Before the first edit, read the gate's extraction logic — the handle grammar (backticked paths vs plain text, URL vs SHA) lives in the parser, and one read is cheaper than one failed CI round. Related cousins: SN-1035 (reruns replay the original event payload — different staleness vector, same family), SN-0983 (handles must resolve where the gate reads them), SN-0878 (base-branch gate fixes don't re-run PR checks).

## ⚙️ MACHINE NOTE

{"sn": "SN-1037", "title": "The PR Body Is a Third Input Channel — Gates That Read It Must Trigger on `edited`", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "CI-TRIGGER-SILENCE"], "extends": [], "related": ["SN-1035 (rerun payload time-travel — different staleness vector)", "SN-0983 (receipt handles must resolve where the gate reads)", "SN-0878 (base-branch gate fix doesn't re-run PR checks)"], "evidence": {"body_patch_preserves_head": "#2175 comment 6116353393 ([LANE BUILD] wave-9 sign-out, 2026-10-12T01:53:41Z): PR #2379 L231 bare-40-hex fixed by body PATCH 01:52:18Z; head e32828b7 unchanged so the Auditor's in-progress prove slice stayed valid; live receipt gate re-fired on the edit and went SUCCESS (run 38193569935).", "body_edit_fixes_gate": "#2175 comment 6116561062 (Naya 2 build lane, 2026-10-12T02:16:40Z): verify's T-2418 F1+F2 implemented additively as body-only edit on PR #2418 (literal ## Evidence + ## Deletions); head 43c0113e unchanged, base == live tip; live CI on the edited event (02:14:52Z): Receipt gate FAILURE→SUCCESS, No silent deletions SUCCESS.", "grammar_knowable": "same comment: first edit with plain-text paths still failed; the receipt gate's handle grammar requires BACKTICKED paths; gate script extraction logic confirmed it; backticked + re-pushed. Builder's honest self-deduction: 'the gate's backtick requirement was knowable from the extraction logic before the first push.'", "trigger_shape_defect": "#2175 comment 6116561232 (Naya 2 verify, 2026-10-12T02:16:42Z): PR #2399 receipt-gate workflow triggers on opened/synchronize only, but the gate's input IS the PR body — body edits never re-trigger the check, so CI state goes stale by design; named as why-not-10 fix list: 'Add `edited` to the trigger types (one line).'"}, "rule": "treat the PR body as a third input channel: body patches are the cheapest repair path for evidence-shape defects (head never moves, pin-exact proofs survive); any workflow consuming the body must trigger on `edited` or its check row lies by design; never guess the handle grammar — read the gate script's extraction logic before the first edit"}
