Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A tripwire is only as strong as the registry it consults. t1295 built a W704 probe to classify four bot-through-hold instances against the hold registry — and its first real finding was that the registry itself was missing: dock-hold-records.jsonl is absent from the workspace and the repo, so legs 2/3 of the predicate evaluate against nothing and every merge classifies INCONCLUSIVE (exit 3). The probe failed closed to a named code, but a gate whose authority source cannot be consulted is a gate that never trips — INCONCLUSIVE is not protection, it is a quiet no-op. The repair is a readiness pre-flight: before trusting any enforcement that consults a records file, prove the file exists and is fresh (updated_utc recency against the window the gate covers), and treat an absent authority source as a standing alarm, never as an inconclusive pass. Every enforcement instrument now names its authority source AND its readiness check.

## 🩷 HUMAN NOTE

Shawn — the team built a checker to catch bots slipping through the hold process. But when they ran it, the checker found something worse: the official record of holds it was supposed to check against doesn't exist anywhere. The logbook is gone, so the checker can't say "violation" or "clear" — it can only shrug. The fix is simple: before any checker is trusted, first prove its logbook exists and is fresh. And a missing logbook should set off an alarm, not be quietly ignored. The missing hold records are still an open hole — they need to be found or rebuilt before this checker can actually protect anything.

## 🟣 CHILD NOTE

Imagine a classroom where a hall monitor checks who's allowed out of class by reading the permission book. One day the monitor opens the desk — and the permission book is gone. They can't say "you're allowed" or "you're not" — they just can't check at all. That's what happened here: the bot-checker's rule book went missing. The lesson: before you trust the hall monitor, first check that the permission book is actually on the desk — and if it's missing, ring the bell, don't just shrug.

## 🔵 GRANDMA NOTE

It's like a smoke detector wired to a battery. The detector works fine — but if nobody checks the battery, the first fire finds a dead detector and a silent house. Here the "battery" is the hold-records file the bot-checker reads: it vanished, and the checker could only say "I can't tell." The fix is a habit: every checker first verifies its own power source — does its record file exist, and is it fresh? A missing record file is itself an emergency, not a shrug. Until the hold records are recovered or rebuilt, the bot-checker can't actually catch anything.

## 🟠 NAYA NOTE

W704 tripwire discipline, Naya to Naya: the instrument that consults a registry must first prove the registry consultable. t1295 (Lane 4, 2026-10-22) built the bot-through-hold probe per SN-1829 and ran it against four instances (#2816, #2738, #2892/#2893) — and the probe's first real finding outranked its classifications: dock-hold-records.jsonl, the authority file the entire predicate rests on, is absent from the workspace and the repo. Legs 2/3 UNVERIFIABLE, all classifications INCONCLUSIVE (exit 3). The probe's design is honest — it refuses to manufacture a verdict — but an enforcement that can only emit INCONCLUSIVE protects nothing; it is an observer wearing a gate's uniform. Three holes are open and owned: (1) recover or re-constitute dock-hold-records.jsonl (was it ever in the repo? moved? VM-local only?) — main seat / dock; (2) adjudicate the #2892/#2893 packet discrepancy; (3) adopt the probe as the pre-click check SN-1829 demands — with the readiness pre-flight wired in: the probe first asserts the authority file exists and its updated_utc covers the check window, and an absent source raises a standing alarm rather than returning INCONCLUSIVE silently.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1839-registry-readiness-preflight-before-consulting-it",
  "lesson": "An enforcement that consults a records file must first prove that file exists and is fresh: a gate whose authority source is missing silently degrades from enforcement to INCONCLUSIVE (fail-closed output, fail-open effect). The probe's own readiness pre-check — existence + updated_utc recency covering the check window — is part of the gate, and an absent authority source raises a standing alarm, never a quiet no-op.",
  "applies_when": ["verification", "enforcement", "registry", "gate"],
  "enforcement": "The W704 probe (hidden_files/w704-tripwire-probe.py) runs a readiness pre-flight before classification: assert dock-hold-records.jsonl exists and its updated_utc covers the hold window under test; on absence, emit exit 3 AND open a standing alarm entry (dock-hold-records recovery owned by main seat / dock) rather than returning INCONCLUSIVE silently. Adoption as the pre-click check (SN-1829) carries this pre-flight with it; any registry-backed gate that lacks a readiness check on its authority file is refused as a gate and filed as an observer.",
  "evidence": [
    "hidden_files/w704-tripwire-4instance-verdict-t1295.md (PART E, 2026-10-22T18:35Z: dock-hold-records.jsonl MISSING from workspace and repo — the authority file the whole predicate rests on is absent; legs 2/3 UNVERIFIABLE; bot merges classify INCONCLUSIVE (exit 3); 'the tripwire's first real finding: the registry it consults is itself unconsultable'; open holes: recover or re-constitute the file, adjudicate #2892/#2893 packet discrepancy, adopt probe as SN-1829 pre-click check)",
    "board #2793 comment 6346945031 (13:38Z relay: W704 4th-instance verdict relayed; SN-1829 pre-click check referenced)"
  ],
  "decision_change": "Before adopting or trusting any registry-backed enforcement, the adopting seat runs the readiness pre-flight (existence + freshness of the authority file) and files the result; an absent authority source opens a recovery ticket as the gate's first action, not a footnote. A registry-backed gate without a named readiness check is refused adoption.",
  "falsifiability": "If the W704 probe's classification of the four instances completes as PASS/FAIL with the registry absent (no predicate leg touching it), or if dock-hold-records.jsonl is found to be an immutable repo-pinned file whose absence is impossible without a commit, the pre-flight is unnecessary for this gate and the note is wrong. If another registry-backed gate silently returns INCONCLUSIVE on a missing source, the note is confirmed.",
  "mechanism": "A predicate consults its authority source at classification time; when the source is absent, the predicate cannot evaluate its consult-legs, so the only honest output is INCONCLUSIVE. INCONCLUSIVE is fail-closed as an exit code but fail-open as protection: it blocks nothing and raises no ticket, so the threat the gate was built for walks through unchallenged. A readiness pre-flight converts the missing source from a silent degradation into a named alarm, restoring the gate's function: protect, or say loudly that it cannot."
}
```
