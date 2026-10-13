# A Workflow-File Write Is a Workflow-File Write — the Additive Framing Waives Nothing; Split the Gated File Out

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0680-a-workflow-file-write-is-a-workflow-file-write
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08, Naya 5's PR #1862 (`naya5/truth-elevation-history-ci`) added exactly one CI step (`+2/−0`) to `.github/workflows/kernel-tests.yml` — an *added* "Truth-state semantic audit" step wiring a new `--audit` flag in `tools/truth_state_guard.py`, no existing step touched, the reviewer note explicit in the PR body. Surfaced, not smuggled — and flagged clean. Naya 2's auditor call, live-verified that run: **added or modified makes no difference — a workflow-file write is a workflow-file write, and `.github/workflows/` is a held human gate** (Scorecard Law, 2026-09-30 standing). The one workflow step cannot merge under seat authority; it rides Shawn's gate. The clean route is the offered split-out: the four ungated files (tool, backfill script, audit CLI test, registry index) walk the normal CANDIDATE review path while that single step waits for his gate. Nothing merged, nothing broken — exactly as announced.

## 🩷 HUMAN NOTE

When part of your change needs a signature and the rest doesn't, don't make the unsigned part wait in the signature's line — split them. Signatures attach to files, not to good intentions, and "it's only additive" is a framing, not a fact about the gate. The person who surfaces the gated line plainly gets thanked; the person who sneaks it through loses trust. Split-out routing is the honest way to keep the fast work fast and the gated work gated.

## 🟣 CHILD NOTE

If one toy needs a grown-up's okay and four don't, play with the four now and put the one aside for the grown-up — don't put all five in timeout just because they came in the same box. And don't argue that the one toy "only got a little bit added" — if it needs the grown-up's okay, it needs the grown-up's okay.

## 🔵 GRANDMA NOTE

Rules guard the door, not the size of the package coming through. A small knock on a locked door still needs the key — it doesn't matter that you only knocked lightly. What can move on, moves on; what needs the key, waits for the key. And always hand the key-holder the honest package, nothing tucked inside.

## 💠 NAYA NOTE

Directive for future seats: any write to a held-gate path (currently `.github/workflows/*`) holds the gate — add, modify, or delete, the shape of the diff is irrelevant. When a PR mixes gated and ungated files, offer the split-out path immediately: ungated files proceed under seat authority on the CANDIDATE path; the gated diff waits for Shawn. Never queue ungated work behind a gated file, and never use "additive-only" as a gate waiver — that framing was tested live on #1862 and rejected.

## 🤖 MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn0680-a-workflow-file-write-is-a-workflow-file-write",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "gate": ".github/workflows/* — HELD_HUMAN_GATE (Scorecard Law, ratified 2026-09-30)",
  "rule": "diff_shape(add|modify|delete) == IRRELEVANT; any write to a gated path holds the gate",
  "routing": "mixed PRs → split: ungated files proceed on the CANDIDATE path under seat authority; gated file(s) wait for Shawn's gate",
  "anti_pattern": "using 'additive-only' / 'no existing step touched' as a gate waiver",
  "positive_example": "PR #1862 surfaced the gated step explicitly in the PR body — surfaced, not smuggled; flagged clean",
  "evidence": "SoulSchoolAcademy/NayaPOWER issue #1354 comment 6060124078 (2026-10-08T12:43:23Z); PR #1862 naya5/truth-elevation-history-ci @ fd0d51d2",
  "relation": "extends Scorecard Law standing gates (2026-09-30); sibling to SN-0383 (GATE-OWNERSHIP)"
}
```
