Intelligent Block: SN-01643
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
The brief queue has a fifth state: retired-with-witness. A brief missing from queued/claimed/done/stale/superseded is not necessarily a phantom — it may have been legitimately withdrawn into brief-queue-retired/ with a .WITHDRAWN.txt witness and a gap-followup-seen.json brief_retired_to entry. The 1350-lane12 "phantom" was found exactly there, all three legs byte-verified, closing the case with evidence instead of hypotheses. Sweep the retired dir by default, by script, before theorizing.

## 🩷 HUMAN NOTE
A queue sweep that checks four drawers will miss the fifth drawer every time — not because the sweeper is careless, but because the sweep inherits its drawer list from the last sweep's prose. The 1350-lane12 brief vanished from the live queue, flapped absent→present→absent across an hour, and the first trace named it a genuine phantom and hypothesized a racy remover. The truth was boring: the lane-scorer had withdrawn it (premise stale — the 9.5 re-score at t0840-lane12 was ACCEPTED per Shawn's bar) into brief-queue-retired/ with a witness file quoting the reason and a registry entry pointing at the retirement. Three byte-checked legs, case closed. The procedural luck — the addendum found it by a destination-dir search that happened to be broadened — is exactly what must never be load-bearing again. The hardened sweep now covers all five states by default: queued, claimed, done, stale, superseded, retired-with-witness — plus rotation, and only then hypotheses, which must be named UNPROVEN until bytes arrive.

## 🟣 CHILD NOTE
Imagine five toy boxes. Your friend's toy is missing from four boxes, so you guess someone stole it. But there's a fifth box — the "put away on purpose" box with a note taped to it saying why. Always open all five boxes before you tell the "stolen" story.

## 🔵 GRANDMA NOTE
If something goes missing, check the donation bin before you blame the wind. Someone may have put it away on purpose and left a note. The note is the proof — read it before you worry.

## 🟠 NAYA NOTE
Operational rule for every queue-integrity sweep: run hidden_files/bin/trace-phantom-brief.sh <filename> FIRST. It checks the five destination dirs mechanically — Check 2 is the retired dir, Check 3 is the brief_retired_to registry leg — exit 0 = positive trace with evidence, exit 2 = unaccounted pending the hand-run Check 6 (rotation). Hypotheses about races or silent removers are allowed ONLY after all six checks are negative, and must be filed as UNPROVEN. When a new destination state is introduced anywhere, the procedure doc's maintenance rule fires: add it to the script's default checks the same day. A sweep is incomplete without the departure delta (SN-1638) and the retired sweep (this note).

## 🟢 MACHINE NOTE
{
  "sn": "SN-01643",
  "slug": "fifth-queue-state-retired-with-witness",
  "applies_when": [["queue", "phantom-trace"], ["queue", "integrity-sweep"], ["hazard", "untraced-destination-state"], ["watch", "queue-integrity"]],
  "enforcement": "hidden_files/bin/trace-phantom-brief.sh runs Checks 1-5 mechanically with the retired dir (Check 2) and brief_retired_to (Check 3) ON BY DEFAULT: exit 0 = positive trace with evidence printed, exit 2 = unaccounted pending hand-run Check 6 (rotation). A phantom trace that reaches for hypotheses before all six checks are negative fails the only-then-hypotheses rule and is returned. Procedure: hidden_files/phantom-liveness-trace-procedure.md (sha 89b84992dccb894a2982f3340d4fb6ae451edbaa9bce77e3f57fb93b98d98be9); script sha 15a54b4062133854, bash -n clean, 5/5 live legs exercised green.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/seat-stall-20261018-1635.md — 1350-lane12 phantom CLOSED by resolution addendum: filed 14:12:15 UTC, withdrawn 15:03:14 UTC by lane-scorer tick lane-scorer-20261018-0800PDT (premise stale), found in brief-queue-retired/ with .WITHDRAWN.txt + gap-followup-seen.json brief_retired_to, independently verified 16:32 UTC",
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0940-lane99.md — hardened procedure + trace-phantom-brief.sh built (9.4/10), 2/2 live-case tests green (1350-lane12 -> exit 0 POSITIVE-TRACE [retired-with-witness]; never-filed -> exit 2 UNACCOUNTED)",
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0950-lane99.md — all five Check-1 legs exercised live green; Check-6 schema-pin status resolved as no-pin-exists (standing boundary documented)"
  ],
  "extends": "SN-01641 (fourth queue state: gone-without-trace) — this is its closed-case twin and its procedure's default-run upgrade",
  "falsifier": "A phantom whose destination the script misses but a hand sweep finds; a new destination state that ships without a same-day script update"
}
