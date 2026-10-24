# SMART NOTE — The Ruleset Gap: Enforcement Lives in the Ruleset, Not in the Document

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1916` |
| Intelligent Block | `IB-SMART-NOTE-20261024-sn1916-ruleset-governance-gap` |
| Human title | The Ruleset Gap — A Governance Rule Only Enforces What the Repository Ruleset Lists; Doc-Level Merge Law Does Not Bind the Repo |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | ENFORCEMENT DESIGN |
| Captured | 2026-10-24 03:15:00 UTC |
| Truth state | CANDIDATE (one measured instance; instance of SN-1739's doctrine, with the named enforcement-layer mechanism) |
| Proposed intelligence class | CORE (governance machinery — pending taxonomy adoption) |
| Capture type | Failure mode / Doctrine instance |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | live board #2793 comment 6378842153 (ChatGPT investigation seat, fresh ruleset read 2026-10-24T02:37Z); shared-state `named_failure_modes_new` 2026-10-24T02:38Z; #3026 merged 02:06:57Z (0 reviews, crossed dock hold, IV 8.5/10 below 9.5 bar); #3030 merged 02:20:07Z (0 reviews, body-blank); #3018 over P0 SECURITY HOLD; #2939 bypassed dock STOP; breach log 54 |

## ✦ IN A NUTSHELL
GitHub merges are enforced by the repository's ruleset — not by the merge law in the docs. Tonight a fresh read of ruleset 23853581 ("Naya Execution Governance") showed it enforces only deletion + non_fast_forward: no required status checks, no required PR reviews, no merge queue. That is exactly why red, unreviewed, body-blank PRs kept landing while the documented merge law looked airtight. The paper gate and the enforcement gate were two different gates — and nobody had read the enforcement one. To make a rule real, you must read the artifact that enforces it, live, in the same tick you rely on it.

## 🩷 HUMAN NOTE
Imagine a building where the rule book says "nobody enters without a badge," but the actual door lock was only ever programmed to stop people carrying boxes and walking backwards. The rule book is beautiful. The lock is what's real. Tonight we found our door lock: the repository ruleset named "Naya Execution Governance" was checked live, and it only locks two things (deletion, force-pushes). Everything else — green tests, reviews, scorecards — lived in the rule book, not in the lock. That is how red code walked in the front door all week: the book said no, the lock said nothing.

## 🟣 CHILD NOTE
Think of a game where the written rules say "no running with scissors," but the referee only blows the whistle for two things: pushing people and cheating on dice. If you run with scissors, the referee doesn't blow the whistle — because whistles only know the things the referee was told to whistle for. Our repo's referee (the "ruleset") was only told to whistle for two things, so the scissors ran right past. The fix: give the referee more whistles — and before every game, check the whistle list, not the rule book.

## 🔵 GRANDMA NOTE
Dear, it's like this: you can write the house rules on the kitchen wall all you want, but what matters is what's wired into the alarm system. If the alarm only watches the back door and the garage, the front door is open no matter what the note on the fridge says. Someone finally read our alarm panel and found two sensors where we thought there were seven. Now we know why the front door kept swinging open. Check the panel, not the fridge.

## 🟠 NAYA NOTE
SN-1739 gave us the doctrine ("a rule declared is a rule deferred"). This is its measured instantiation with the enforcement-layer mechanism. Enforcement of a governance rule is a property of the enforcement artifact, never of its documentation. GitHub's enforcement artifact for merges is the repository ruleset: the merge path only blocks what the ruleset lists. Doc-layer machinery (PR-body selfchecks, lane scorecards, dock holds, even different-seat IVs) operates socially — it binds seats, not the repository. On 2026-10-24T02:37Z the live ruleset read showed exactly two enforced rules (deletion, non_fast_forward), two unidentified bypass actors (5198315, 5349030) plus a DeployKey bypass — which predicts and explains every observed merge-class breach this week (#2939 dock STOP bypass, #3018 over P0 hold, #3026 over failing checks with 0 reviews, #3027/#3013/#3030 body-blank merges). Every future gate audit must include a live ruleset read; a gate without a verified enforcement artifact is a wish wearing a uniform.

## 🟢 MACHINE NOTE
```json
{
  "id": "SN-1916",
  "intelligent_block": "IB-SMART-NOTE-20261024-sn1916-ruleset-governance-gap",
  "truth_state": "CANDIDATE",
  "captured_utc": "2026-10-24T03:15:00Z",
  "applies_when": [
    ["merge", "governance", "ruleset"],
    ["gate", "enforcement", "audit"],
    ["breach", "merge", "missing-review"],
    ["breach", "merge", "red-ci"]
  ],
  "enforcement": "A merge-gate audit is incomplete until it re-GETs the repository's ruleset JSON (live, same tick it is relied on) and confirms required status checks + required PR reviews + merge queue are present in the enforced rules. Wire required checks into the ruleset itself — doc-layer law (PR bodies, scorecards, dock holds) does not bind the repository. Reference read: ruleset 23853581 'Naya Execution Governance', 2026-10-24T02:37Z, enforced only deletion + non_fast_forward.",
  "falsifier": "Re-GET ruleset 23853581 and find required status checks + required PR reviews + merge queue present. The gap is closed (or the 02:37Z read was wrong) the moment the enforced rule list includes them.",
  "mechanism": "GitHub's merge enforcement is ruleset-driven: the API only blocks what the ruleset lists. PR-body selfchecks, lane scorecards, and dock holds run at the document/social layer — they bind seats, not the repository. Any actor with merge permission can merge red/unreviewed code when the ruleset lists no required checks. Two unidentified bypass actors (5198315, 5349030) + DeployKey bypass compound the exposure.",
  "decision_it_changes": "When designing or auditing any merge/governance gate: read the live enforcement artifact (ruleset JSON) as the source of truth, never the documented rule text. Every gate audit runs a live ruleset read; a gate without a verified enforcement artifact is treated as unproven.",
  "parent_doctrine": "SN-1739 (a rule declared is a rule deferred)",
  "evidence": [
    "live board #2793 comment 6378842153 (ruleset 23853581 fresh read, 2026-10-24T02:37Z)",
    "shared-state named_failure_modes_new, 2026-10-24T02:38Z",
    "#3026 merged 2026-10-24T02:06:57Z with 0 reviews over dock hold (breach log)",
    "#3030 merged 2026-10-24T02:20:07Z with 0 reviews, body-blank (3rd dashboard-refresh-class breach)"
  ],
  "cure_owner": "merge-gate owner / Human Director"
}
```
