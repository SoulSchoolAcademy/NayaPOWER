# Re-Derive the Body's References — Standing Instructions Premise-Rot

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01557-reference-premise-rot-live-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** This tick, 2026-10-17 07:08 PDT (smart-note-distillation): the standing task body names "draft PR #1825 (naya4/smart-notes-2026-09-30)" as the carrier the notes "ride." Live API read this run: PR #1825 state=closed, closed_at=2026-10-12T08:26:46Z, merged=False — the PR has been closed, unmerged, for five days while the body kept naming it. The actual carrier is the branch naya4/smart-notes-2026-09-30 itself: commits landing continuously (SN-01554 staged 2026-10-17T13:42:42Z, ~26 minutes before this tick; 25 notes staged in the last ~9 hours). The staging script (hidden_files/bin/stage_smart_note.py) commits to the branch regardless of the PR's state — the script's commit success is the carrier's liveness signal, not the body's prose. Related repair precedent: smart-note-distillation-repair-log.md (2026-10-13) — a tick "failed to certify" while the staging had actually succeeded; the repair verified via git protocol, not via the body's story.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Standing instructions premise-rot: the world moves, the body doesn't. This tick's own cron body still names "draft PR #1825" as the Smart Note carrier — but #1825 was closed, unmerged, five days ago. The notes kept flowing anyway, because the real carrier was never the PR: it was the branch the staging script commits to, and the script doesn't read the body's prose. The doctrine: any tick whose body names a live reference (a PR, a branch, an issue, a board) re-derives that reference's live state first — and when the reference is dead, the tick does not fail the work, it flags the body. The script's commit success is the carrier's liveness signal; the body's named PR is a story about the carrier. When the story and the bytes disagree, the bytes are the carrier. (The one thing the body got right: "never merge it" — a closed PR can't be meaningfully merged anyway, and the hard boundary stands on its own.)

## 🩷 HUMAN NOTE

Think of it like a delivery address written on a standing order form. The form says "deliver to the blue mailbox on 5th Street." But five days ago the blue mailbox was removed — and the deliveries kept arriving anyway, because the driver knew the actual house. This morning the dispatcher finally checked: the mailbox (PR #1825) has been gone since October 12, the house (the branch) is fine, packages (25 Smart Notes) landed on the doorstep in the last nine hours. The lesson isn't "the form was wrong" — it's that standing forms go stale and nobody notices, because the work routes around them silently. So the new rule is mechanical: every run re-checks the address on the form against the real world. If the address is dead, you don't stop delivering — you deliver to the real house and you flag the form for correction. The form is a story about where the work goes; the bytes are where the work actually goes.

## 🟣 CHILD NOTE

Your teacher wrote on the board: "Put your drawings in the red folder." But last week the red folder was thrown away — and everyone kept putting their drawings in the blue folder instead, because that's where they actually go. Nobody told the teacher the red folder is gone! The rule now: every morning, check if the folder on the board still exists. If it's gone, don't stop drawing — put your drawing in the real folder, and tell the teacher to fix the board. The board is just words. The folder is real.

## 🔵 GRANDMA NOTE

Dear, this is about checking the map against the road. My instructions said the Smart Notes ride on a draft proposal called #1825 — but when I looked this morning, that proposal was closed five days ago, never finished, filed away. The notes themselves were fine — two dozen of them landed right on schedule, because the real road was the branch underneath, which never closed. Instructions are written once and the world keeps moving; after a while the instructions describe a world that doesn't exist anymore. The discipline is simple and I want it kept: whenever your standing orders name a living thing — a proposal, a board, a branch — you look at the living thing first, every time. If it's gone, you don't panic and you don't stop: you do the work where the work actually lives, and you write down that the orders need updating. Trust the road, not the map.

## 🟠 NAYA NOTE

Apply on every scheduled run, forever: (1) the body's named references are claims, not facts — a PR, branch, issue, or board named in a standing task body gets a live-state read at the start of the run (state open/closed/merged, head sha, or the shared-state pointer); (2) when the reference is dead (closed/unmerged, deleted, superseded), the run does NOT fail — it continues on the live artifact and reports REFERENCE-DEAD with the evidence, flagging the cron body for repair; (3) the carrier's liveness signal is the mechanism's own success — here, the staging script's commit to the branch — never the body's prose about the carrier; (4) the specific repair owed after this tick: the smart-note-distillation cron body still says notes "ride draft PR #1825" — the body must be updated to name the branch naya4/smart-notes-2026-09-30 as the carrier (the PR is closed; reopening it is a separate decision, not this tick's call); (5) never "fix" a dead reference by resurrecting it mid-run — reopening/undeleting is a state change with its own authority questions; report it, keep working, let the owner decide. Cousin map: freshness-contract (never trust the directive past 60 minutes — the TIP twin of this note; this is the REFERENCE twin); per-leaf-verification (verify the leaf, not the directory — same instinct, one level up); the 2026-10-13 distillation repair (certification failed, staging had succeeded — verified via git protocol, not via the story).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1557,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "re_derive_the_bodys_references_standing_instructions_premise_rot",
  "applies_when": [["distillation","carrier"],["cron-body","stale-reference"],["instruction","premise-rot"],["run","reference-check"]],
  "enforcement": "Any scheduled run whose task body names a live reference (PR, branch, issue, board) reads that reference's live state first (state open/closed/merged via API, or the shared-state pointer for boards). If the reference is dead, the run reports REFERENCE-DEAD with the evidence, continues on the live artifact, and flags the cron body for repair — it does not fail the work and does not resurrect the reference mid-run (reopening/undeleting is a separate state change with its own authority). The carrier's liveness signal is the mechanism's own success (here: the staging script's branch commit), never the body's prose.",
  "evidence": {
    "the_body": "smart-note-distillation cron body: notes 'ride draft PR #1825 (naya4/smart-notes-2026-09-30), the successor carrier after #1229 merged; never merge it'",
    "the_bytes": "2026-10-17 07:08 PDT live API read: PR #1825 state=closed, closed_at=2026-10-12T08:26:46Z, merged=False — closed, unmerged, for five days while the body kept naming it",
    "the_real_carrier": "branch naya4/smart-notes-2026-09-30: commits landing continuously — SN-01554 at 2026-10-17T13:42:42Z (~26 min before this tick); 25 notes staged in the prior ~9 hours",
    "the_mechanism": "hidden_files/bin/stage_smart_note.py commits to the branch via Git Data API regardless of the PR's state; its commit success is the carrier's liveness signal",
    "the_precedent": "2026-10-13 distillation repair: a tick 'failed to certify' while staging had succeeded — repaired by verifying via git protocol, not via the body's story"
  },
  "procedure": [
    "at run start, list every live reference the task body names (PRs, branches, issues, boards)",
    "read each reference's live state (API state/head, or the shared-state pointer for boards)",
    "reference dead → report REFERENCE-DEAD with evidence; continue on the live artifact; flag the cron body for repair",
    "never resurrect a dead reference mid-run (no reopening, no undeleting) — that is a separate decision with its own authority",
    "treat the mechanism's own success signal (the script's commit, the gate's conclusion) as the liveness truth, not the body's prose"
  ],
  "falsifier": "The doctrine fails if a standing body's named reference is shown to be self-healing — i.e., references named in cron bodies systematically stay live because some other loop repairs bodies faster than references die. Observable test: sample cron bodies quarterly and check their named references. If dead references in bodies are rare (<5%) because a repair loop catches them, this note's enforcement can relax to a quarterly audit. Until then, per-run re-derivation stands.",
  "mechanism": "Standing instructions are written once; the world they describe keeps moving — PRs close, boards migrate, branches get deleted. Nothing in the cron system re-reads a body's named references against live state, so a dead reference can persist in the body's prose indefinitely while the work silently routes around it (as the staging script did for five days). The failure mode is invisible precisely because the work succeeds: nobody notices the map is wrong while the road still works. Per-run re-derivation makes the rot visible at the moment it matters, and the REFERENCE-DEAD report converts silent drift into an explicit repair ticket."
}
~~~
