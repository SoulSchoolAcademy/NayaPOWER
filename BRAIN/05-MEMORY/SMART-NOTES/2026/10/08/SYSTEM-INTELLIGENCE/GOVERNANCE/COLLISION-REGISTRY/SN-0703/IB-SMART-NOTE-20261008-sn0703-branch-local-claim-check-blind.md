# A Branch-Local Claim Check Is Blind to Cross-Branch Collisions

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0703-branch-local-claim-check-blind
**Smart Note:** SN-0703
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6065378806 (Naya 2 claims SN-0699 "connection bottleneck", 2026-10-08T17:25:47Z, staged on PR #1906 branch brain-build/smart-note-sn0699-connection-bottleneck), 6065548556 (Naya 4 stages SN-0699 "TEN STAR SERVICE", 17:35:41Z, staged on naya4/smart-notes-2026-09-30 feeding PR #1825). `stage_smart_note.py` claim check (header cites the SN-0449/0455/0457 collision class). SN-0171 (registry scans every branch carrying live claims). Renumber repair commit b847dc3b.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes claimed SN-0699 within ten minutes — Naya 2's "connection bottleneck" (PR #1906's branch) and Naya 4's "TEN STAR SERVICE" (the smart-notes staging branch). The collision should have been impossible: `stage_smart_note.py` carries a mechanical claim check written after the SN-0449/0455/0457 collisions. But the check scans only the staging branch's own tree — it is blind to claims living on other open Smart Note PR branches. Doctrine SN-0171 already says the registry's layer 2 is every branch tree carrying live claims, not just the staging branch — the mechanical gate was weaker than the doctrine it cited. Repair: first claim stands (Naya 2's, 17:25:47Z); TEN STAR SERVICE was renumbered SN-0699→SN-0700 in one atomic commit (b847dc3b; new path present, old path gone). The standing lesson: a mechanical gate must be at least as strong as the doctrine it cites — until the script's check is extended to enumerate open Smart Note PR head trees, check the board (#1354) and open Smart Note PRs by hand before taking a number.

## 🩷 HUMAN NOTE

Shawn — a small numbering collision happened today, and it's worth knowing about because it exposed a gap in the machinery. Two of your seats both filed Smart Notes as SN-0699 within ten minutes of each other — one on each of two different branches. There's a script whose whole job is to prevent exactly this, and it has the check in it — but the check only looks at one branch, so it couldn't see the other claim. The rule your team already ratified says the check must cover every branch with live claims; the tool just hadn't caught up to the rule. It's fixed: the first claim kept the number, the second note was renumbered to SN-0700, and the lesson is now written down so the next staging tool gets the check right from the start.

## 🧒 CHILD NOTE

Imagine two kids both writing their name on the same locker — but they're in different hallways, and the hall monitor only checks one hallway. The monitor has a rule to stop double names, but the rule doesn't work if it only looks in one place. That's what happened: two notes got the same number because the checker only looked at one branch. Fix: the checker has to look at ALL the branches, and until it does, you check by hand. First one to claim the number keeps it.

## 👵 GRANDMA NOTE

Dear — the team files lessons with numbers, like library books. Today two lessons accidentally got the same number because they were filed from two different desks, and the automatic checker only watched one desk. Nobody's fault, really — the rulebook already said to watch every desk, but the tool hadn't been updated to do it. It's corrected now: the first one keeps its number, the second got a new one, and the lesson is written into the record so the tool gets fixed properly.

## 🤖 NAYA NOTE

Future Naya: this is the instrument-parity family applied to your own tooling. (1) The failure: `stage_smart_note.py`'s CLAIM CHECK greps `/SN-<n>/` only in the staging branch's recursive tree (`base_tree` = staging tip). A claim on any other open Smart Note PR branch (here: PR #1906's `brain-build/smart-note-sn0699-connection-bottleneck`) is invisible to it — a false green on a real collision. (2) The doctrine already knew: SN-0171 defines registry layer 2 as every branch tree carrying live claims, and SN-0115's three-layer registry is board / open Smart-Note PR heads / commit-graph search. The gate was weaker than the law. (3) The repair direction: extend the script's claim check to enumerate open Smart Note PRs (title/head-ref scan), fetch their head trees, and refuse staging on any number claimed on any of them; keep the board (#1354) as the manual fallback until the script does this. (4) The protocol when a collision is found live: first claim stands, renumber yours — executed here as one atomic git-data commit (add new path + delete old path, parents=[tip], ref PATCH after tip re-verification): TEN STAR SERVICE SN-0699→SN-0700, commit b847dc3b on naya4/smart-notes-2026-09-30. (5) Ten minutes separated the two claims and both were on the same feed this loop reads — the in-flight claim was visible; the lane that took the second number checked the counter file but not the board's last ten minutes. Recency matters: check the board's newest comments, not just the counter.

## ⚙️ MACHINE NOTE

```json
{
  "note": "SN-0703",
  "type": "INSTRUMENT_PARITY_LAW",
  "name": "branch-local claim check blind to cross-branch collisions",
  "status": "CANDIDATE",
  "rule": "a mechanical gate must be at least as strong as the doctrine it cites; a claim check that cannot see cross-branch claims gives false greens",
  "finding": "stage_smart_note.py CLAIM CHECK scans only the staging branch tree; SN-0699 was double-claimed across PR #1906's branch and naya4/smart-notes-2026-09-30 (10 minutes apart), invisible to the check",
  "doctrine": "SN-0171 (registry layer 2 = every branch tree carrying live claims); SN-0115 (three-layer registry: board / open Smart-Note PR heads / commit-graph search)",
  "repair": "first claim stands (Naya 2, 17:25:47Z, PR #1906); TEN STAR SERVICE renumbered SN-0699->SN-0700, atomic commit b847dc3b (new path present, old path gone, tip re-verified before ref PATCH)",
  "prescription": "extend the script's claim check to enumerate open Smart Note PR head trees; until then, check #1354 newest comments + open Smart Note PRs by hand before taking a number — the counter file alone is a single-writer resource two lanes can race",
  "evidence": ["#1354:6065378806", "#1354:6065548556", "PR #1906 files", "commit b847dc3b"]
}
```
