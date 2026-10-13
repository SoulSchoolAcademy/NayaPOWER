# Score the Wait Option on Information Gain — a Check That Fails on the Base Cannot Turn Green on the Head

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0798-score-the-wait-option-on-information-gain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6084869931 ([NAYA 2 — BRAIN-BUILD LOOP] SCORECARD (Scorecard Law): merge PR #1997, 2026-10-09T16:22:15Z). Source: SoulSchoolAcademy (Naya 2 lane).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's scorecard for merging PR #1997 (brain-index regen) priced three options: A merge now (9.0), B wait for CI to go green (6.0), C do nothing (3.0). Option B lost on one argument: **CI cannot change the classification.** The `test` check fails at Python collection on the base SHA `c791b779` too (`ModuleNotFoundError: engineering_gates`, exit 2) — so no head built on that base can ever turn it green. "Waiting extends the drift window with zero information gain."

The general rule: **a wait option must be scored on the information it could produce, not on the comfort of waiting.** Before pricing "wait," ask: what verdict could the future possibly return that the present cannot? If the failing check fails identically on the base (collection error), the rejection is deterministic on the request shape (SN-0439 family), or the environment cannot produce the evidence at all (SN-0755), then the future verdict is already known — waiting buys exactly zero information and costs drift. Waiting in that state is not diligence; it is drift at compound interest.

The corollary: a check whose verdict is predetermined belongs in the scorecard as a *classification* (pre-existing, owned by another lane — here #1840), not as a gate. Once classified, merge the green parts on their own merits: the index regen merged 9.0 with byte-verified blobs, `--check` exit 0, and all 3 remaining failures reproduced on the pristine base.

## 🩷 HUMAN NOTE

Shawn — a scoring lesson worth locking in. When Naya 2 priced "wait for CI to go green" on the index-regen merge, she didn't score it as the safe option — she scored it 6.0 because CI *couldn't* go green. The failing check dies at collection on the base SHA too, so waiting would only stretch the drift window with zero new information. The rule she applied: a wait option is only worth what the waiting can teach you. If the answer is nothing — the verdict is already determined by the base, the shape, or the environment — then waiting is drift, not diligence, and the right move is to classify the red as pre-existing and merge the green work on its own merits. That's how the regen merged 9.0 instead of sitting red for days.

## 🟣 CHILD NOTE

Imagine you're waiting for a light to turn green, but someone painted over the green bulb — it will never turn green, no matter how long you wait. That's what happened here: the team was offered the option of "wait until the tests turn green," but the test was broken in a way that had nothing to do with their change — it fails on the old code too, before their work even starts. Waiting would have taught them nothing and only let more changes pile up behind it. Moral: only wait when waiting can teach you something. If the answer is already known, waiting is just standing still while the world moves past you.

## 👵 GRANDMA NOTE

The team had a choice: merge a fix now, wait for the automated tests to turn green, or do nothing. Waiting *felt* safest, but they discovered the failing test was broken in the old code too — it could never turn green on their change. Waiting would have produced zero new information while letting the backlog grow. So they recorded the test failure as a known, separate problem owned by someone else, and merged the good work on its own merits. The lesson: when deciding whether to wait, ask what the waiting could possibly teach you. If the answer is nothing, don't wait — name the known problem, handle it separately, and keep moving.

## 🟠 NAYA NOTE

Before you price a "wait for X" option in any scorecard or gate decision, run the information-gain test: *what verdict could the future return that the present cannot?* If the answer is none, the option scores low regardless of how safe it feels. Failure classes that make a wait zero-information: (1) the check fails identically on the base SHA (collection/import errors, exit-2-style failures — re-run on a pristine base worktree to prove it); (2) the rejection is deterministic on the request shape (SN-0439: HTTP 400; SN-0485: verify the mechanism); (3) the environment cannot produce the required evidence (SN-0755: waiting is indefinite blocking, not diligence). When all three are excluded but the check is still red, *then* waiting may have information value. Once the red is classified as pre-existing, record the owning lane/repair, and score the work on its own merits — never let a predetermined verdict veto an independent green.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0798",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-RUN-DIAGNOSIS",
  "doctrine": "score-the-wait-option-on-information-gain",
  "rule": "A wait option is priced on the information the wait could produce. A check that fails identically on the base SHA, a deterministic rejection of the request shape, or evidence the environment cannot produce yields zero information — classify the red as pre-existing (named owning lane) and score the work on its own merits; waiting is drift, not diligence.",
  "failure_mode": "\"wait for CI to go green\" scored as the safe default when CI green is impossible — the drift window extends while nothing new is learned; a predetermined verdict vetoing an independent green",
  "mechanism": {
    "observed_case": "Naya 2 scorecard for merge PR #1997: A=9.0 merge now, B=6.0 wait for CI green, C=3.0 do nothing. B priced at 6.0 because `test` check fails at collection on base `c791b779` (ModuleNotFoundError: engineering_gates, exit 2) — reproducible on pristine base worktree; same-class repair lane #1840 open",
    "verdict": "merge now; receipt posted BEFORE merge; post-merge faithfulness proof followed",
    "information_gain_test": "what verdict could the future return that the present cannot? if none, wait option scores low"
  },
  "related": ["SN-0439", "SN-0440", "SN-0485", "SN-0755", "SN-0236"],
  "provenance": ["#1354 comment 6084869931"]
}
