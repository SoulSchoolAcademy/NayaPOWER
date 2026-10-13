# The Live-Board Law: Machine Gates Must Point at the Live Board, Never a Fixed Artifact

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0947-live-board-law-machine-gates-point-live
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Night-shift deep-map t2232-a (2026-10-10 22:36 PDT, verified tip `62e59713`); receipt `hidden_files/night-shift-2026-10-10/receipts/deepmap-machine-gates.md`; morning-flags.md [t2232-a]; t2210-b protocol-governance flag; #1354 comment cap reached 2026-10-10 ~12:21 PDT.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t2232-a machine-gates deep map (verified tip `62e59713`, exact bytes, zero REST) found a live contradiction: the merge-safety machinery and the protocol machine law both still point at a dead board. `tools/auto_merge_gate.py` P5 and `tools/auto_merge_self_heal.py` still require and write merge-receipt traffic to issue #1354 — which GitHub hard-capped at 2,500 comments at ~12:21 PDT on 2026-10-10, so nothing can be posted there again; #1354 is the archive and #2175 is the live coordination board. In the same run, the protocol machine found `kernel/protocol/cold_start_gate.py` enforcing "#1354" as a `REQUIRED_TRUTH_MARKER`, and `kernel/protocol/protocol_manifest.json` pointing 11 checks at `tools/protocol/checks/...` while `MIGRATION.md` declares `tools/protocol/` superseded. So the doctrine this note banks is the LIVE-BOARD LAW: **machine law and machine gates must reference the live coordination surface through an indirection (a canonical "current board" constant), never a fixed artifact ID.** A fixed ID is a time bomb: any board can be archived, capped, renamed, or superseded, and when it happens every gate that hardcodes it silently stops enforcing — or worse, enforces against an artifact nobody reads. The repair is mechanical (repoint the gates to #2175 and re-run the affected gate tests), but it touches merge-safety machinery, so it was flagged for Shawn's eyes before dispatch — changing a gate is itself a gated action. This is the machine-law twin of SN-0435 ("the last mile of law is wired, not written") and SN-0794 (resolve by availability): a law that is written in a doc but wired to a dead board is a law that stopped being law the day the board died.

## 🩷 HUMAN NOTE

Shawn — from tonight's machine-gates deep map: our own merge-safety machinery is still writing its receipts to the old board. Issue #1354 hit GitHub's 2,500-comment hard cap around 12:21 today, so nothing can be posted there ever again; #2175 is the live board now. But `auto_merge_gate.py`, `auto_merge_self_heal.py`, and the protocol's cold-start gate all still hardcode #1354 — one of them treats #1354 as a required "truth marker." Any merge-receipt path that depends on writing to the old board is quietly broken. The rule banked: machine law must point at the *live* board through a name that moves when the board moves, never a hardcoded number. The fix itself is a code change to merge-safety machinery, so I flagged it for your eyes instead of dispatching it — same principle that says changing a gate is a gated action.

## 🟣 CHILD NOTE

Imagine a robot guard that was told "send every report to Locker #1354." One day Locker #1354 gets permanently sealed shut by the building. But nobody updated the robot's instructions — so it keeps trying to stuff reports into a sealed locker, and all its reports disappear. The fix: tell the robot "send reports to the *current* mailbox" and put a sign on the wall that says which mailbox is current. That way, when the mailbox changes again, you only update the sign — not the robot.

## 👵 GRANDMA NOTE

The church's emergency phone list told everyone to call the old landline — but the line was disconnected months ago. Calls kept going nowhere. Nobody would leave the wrong number printed there; they'd print "call the current number posted in the kitchen." Same thing here: our automated safety checks were sending their records to an address that no longer accepts mail. The lesson is to point everything at the *current* address, not the old one, and make the current address the one thing you ever have to update.

## 💜 NAYA NOTE

Future Naya: (1) Never hardcode a coordination surface (issue ID, board, channel) in machine law, gates, or tools — define ONE canonical "current board" constant and point everything at it. (2) When the board moves (cap, archive, rename, supersede), the migration is one edit to the constant plus a mechanical sweep; audit every reference. (3) A gate that writes to a dead endpoint is a gate that stopped enforcing — this is a machine-law failure, not a cosmetic one, and the vigilance law (SN-0923) requires you to surface it. (4) Repairing gate machinery is itself a gated action: repointing `auto_merge_gate.py`/`auto_merge_self_heal.py`/cold-start markers off #1354 to #2175 needs Shawn's eyes (merge-safety machinery), then re-run the affected gate tests. Evidence anchors: #1354 capped 2026-10-10 ~12:21 PDT (shared-state.json `issue_1354_comments_disabled`); dead references confirmed at tip `62e59713` in receipts/deepmap-machine-gates.md; cold_start_gate `REQUIRED_TRUTH_MARKER` per t2210-b flag in morning-flags.md.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0947",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LAW-IS-CODE"],
  "cousins": ["SN-0923", "SN-0435", "SN-0794", "SN-0342"],
  "rule": "Machine law and machine gates must reference the live coordination surface through a single canonical indirection (a 'current board' constant), never a fixed artifact ID. A fixed ID is a time bomb: when the surface is archived, capped, renamed, or superseded, every gate that hardcodes it silently stops enforcing or enforces against an artifact nobody reads. Changing gate machinery is itself a gated action: surface to the authority, then repair + re-run the affected gate tests.",
  "anti_rule": "Hardcoding an issue number, board ID, or channel in gate code; 'fixing' a dead endpoint reference without re-running the gate's tests; treating a reference-rotation as a cosmetic edit when it touches enforcement paths.",
  "evidence": {
    "deep_map": "t2232-a, 2026-10-10 22:36 PDT, verified tip 62e59713, 29 workflows inventoried, 1 REST call",
    "dead_refs": "tools/auto_merge_gate.py P5 + tools/auto_merge_self_heal.py require/write to #1354; kernel/protocol/cold_start_gate.py REQUIRED_TRUTH_MARKER='#1354'",
    "cap_event": "#1354 hit GitHub 2500-comment hard cap 2026-10-10 ~12:21 PDT; shared-state.json issue_1354_comments_disabled=true; live board is #2175",
    "receipt": "hidden_files/night-shift-2026-10-10/receipts/deepmap-machine-gates.md; morning-flags.md [t2232-a] and [t2210-b]",
    "status": "flagged for Shawn before dispatch — merge-gate machinery change is a protected gate"
  },
  "authority": "observed field finding — Naya 4 night-shift deep map, CANDIDATE (auto-capture, not ratified)"
}
```
