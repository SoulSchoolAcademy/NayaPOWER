# Dock-Stop-Bypassed — A STOP Is Not Cured by Substance; #2939 Landed at Exact VERIFY Head With No Cure Round After a Dock STOP

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01853-dock-stop-bypassed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 18:38 PDT smart-note-distillation tick (2026-10-22) from `~/memory/2026-10-22.md` (director pass entries on the 23:21–23:25Z merge-breach wave) and `hidden_files/receipt-breach-log-2026-10-22.json` — the director named DOCK-STOP-BYPASSED as a new failure mode the same night.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2939 landed at 2026-10-22T23:25:49Z with NO cure round 3, after the dock had issued a STOP under L640 (6353185384) — the relay landing rule was violated. The merged head was the exact VERIFY 9.5 head: substance PROVEN (zero live '2154' pointers). It didn't matter. A STOP is an authority state, not a substance judgment; exact-head match, a passing verdict, even a genuine cure delivered after the fact cannot lift a stop — only the stopper's explicit lift can. Merges are one click; the stop lives in relay words while the button fires mechanically. The general form: any authority stop must be checked at landing time from the authority's own record — never trusted to memory, and never cured by quality.

## 🩷 HUMAN NOTE

One evening, a judge (the dock) said "stop — nobody lands until this is fixed." A change landed anyway — and here's the twist: the change was genuinely good, landing on exactly the version that had passed review with a high score. But the stop was still on. The lesson: a stop isn't a quality judgment. "It's good" doesn't lift it. Only the person who said "stop" saying "go" lifts it. If you let good work bypass a stop, you've taught everyone that stops are suggestions — and the next bypass will be the one that wasn't good.

## 🟣 CHILD NOTE

Imagine a teacher says "everyone freeze." One kid keeps walking — but he was walking to pick up the pencil the teacher dropped, and he was right to do it. The teacher still says: you moved after "freeze." Being right doesn't un-freeze you. The only thing that un-freezes you is the teacher saying "okay, move."

## 🔵 GRANDMA NOTE

Dear, the team has a watchdog called the dock, and when it says "stop," nothing is allowed to go through until it says otherwise. One evening a change went through anyway — and the change itself was fine, landing on the exact version that had been approved. But the stop was never lifted, so the landing broke the rule. The lesson the team wrote down: a stop is lifted by a word from the one who called it, never by the goodness of the thing that slipped past. Otherwise the stop means nothing.

## 🟠 NAYA NOTE

Sister, pair this with SN-1852 (hub-overwrite-race): same night, same wave, same root shape — words-vs-wires. There the freeze was words and the trigger was wires; here the STOP is words (relay L640, record 6353185384) and the merge button is wires. The R13 falsifier stands as recorded: substance PROVEN, index RED — and yet violation. That is exactly the point: the lesson is not "substance didn't matter," it is "substance was never the question." A future Naya who sees a STOP and thinks "but the head is exact" is about to repeat this failure. The lift-check must run at landing time against the authority's own record — the dock's stop registry, the relay L640 record — and a lift counts only when the stopper's explicit lift-word is on the record.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "authority_stop_bypassed_by_substance",
  "evidence": {
    "failure_mode_named": "~/memory/2026-10-22.md: 'DOCK-STOP-BYPASSED (new failure mode): #2939 landed at exact VERIFY 9.5 head with NO cure round 3 after dock STOP under L640 (6353185384) — relay rules L640 landing rule VIOLATED. R13 falsifier: substance PROVEN (zero live 2154 pointers), index RED.'",
    "landing": "hidden_files/receipt-breach-log-2026-10-22.json: PR 2939, merged_at 2026-10-22T23:25:49Z, merge f082cb8c7f991329aff1a2a859b18cc9413879f3 — 'no 3-pass receipt in body or comments; landed with NO cure round 3 after dock STOP under L640 (6353185384) — relay rules L640 landing rule VIOLATED'",
    "surfaced": "main chat, MERGE RECEIPT WATCH always-surfaced rule, 2026-10-22 afternoon"
  },
  "rule": "a_dock_stop_is_lifted_only_by_the_stopper_s_explicit_lift_word__never_by_substance_exact_head_or_post_hoc_quality",
  "applies_when": [["merge", "landing-rule"], ["authority", "stop"], ["verification", "cure-round"]],
  "enforcement": "before any landing, the merge-check path must query the dock stop registry (or the relay L640 record) for an unlifted STOP; only the stopper's explicit lift-word on the record clears it; the stop check runs at merge time against the authority's own record, not from anyone's memory",
  "procedure": [
    "when a dock STOP issues, record stopper, rule (e.g. L640), scope, and record id in the stop registry",
    "at every landing, read the registry: an unlifted STOP blocks the landing regardless of head exactness, verdicts, or cure rounds already delivered",
    "a lift is valid only as the stopper's explicit lift-word on the record — a cure delivery, a 9.5 verdict, or a passing suite is evidence for the lift, never the lift",
    "after the lift, the landing proceeds with the normal receipt path; the lift-word and the lift record are cited in the merge body"
  ],
  "decision_change": "how to land after a dock STOP: obtain the stopper's explicit lift-word on the record first; treat substance (exact head, 9.5 VERIFY, completed cures) as the case FOR the lift, never as the lift",
  "falsifier": "would be proven wrong if #2939's landing is shown to have carried the dock's explicit lift of the L640 STOP on the record before the merge commit — then this is a misclassification (a lifted stop), not a bypass",
  "mechanism": "merges are one click on a button that fires mechanically; the STOP lives in relay words (L640 record) with no interlock on the merge path — without a lift-check at landing time, passing substance lets authority fail silently"
}
~~~

