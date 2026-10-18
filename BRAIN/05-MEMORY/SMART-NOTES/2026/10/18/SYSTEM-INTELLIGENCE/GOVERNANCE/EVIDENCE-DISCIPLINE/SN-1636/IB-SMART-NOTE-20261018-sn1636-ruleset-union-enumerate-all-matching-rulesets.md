# A Ruleset-Bypass Verdict Enumerates Every Matching Ruleset — GitHub Evaluates the Union

**Intelligent Block:** IB-SMART-NOTE-20261018-sn1636-ruleset-union-enumerate-all-matching-rulesets
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** shared-state.json director_tick_2026_10_17_2138 correction (2026-10-17 21:38Z): the 21:08Z "L495 settings arc CLOSED at live bytes" claim was FALSIFIED — director byte-read ruleset 24858146 (main-protection, ACTIVE, target ~DEFAULT_BRANCH) with `bypass_actors: []` and its pull_request rule live; the DeployKey bypass grants had been written to 24857158, 24857323, and 23853581 but NOT to 24858146, so the deploy-key push stayed structurally blocked and #2752's hold did not lift. Board #2721: comment 6245567148 (Resolve VERIFY — VERIFIED-WITH-BLOCKER, 24858146 empty bypass_actors), comment 6245986728 (Naya Clarity — 24858146 bypass written 21:44 PDT, re-verified 22:08 PDT, all 4 rulesets now carry the DeployKey bypass), comment 6246512807 (Resolve VERIFY — companion settings byte-verified, key 166807399 write-capable, ruleset 24857158 carries the bypass — the verification pass that kept missing the fourth).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A "cleared" verdict on a ruleset-bypass repair is not evidence unless it names **every** active ruleset whose target matches the ref. GitHub evaluates the union of all matching rulesets — a bypass granted on three of four leaves the fourth enforcing, and the push stays blocked exactly as before. The fourth ruleset is always the one the verdict forgot to enumerate.

## 🩷 HUMAN NOTE

Shawn — the #2752 arc taught a sharp one: the fix looked complete three times, but the push stayed blocked because one ruleset — the main-protection ruleset 24858146 — never got the DeployKey bypass grant. The new standing rule: no repair is declared "cleared" until the verifier has listed every active ruleset matching the target branch, read the bypass list on each one, and named all of them with their states in the verdict. Fixing N−1 of N is still blocked; the math is union, not majority.

## 🟣 CHILD NOTE

Imagine a hallway with four locked doors in a row and a key card that opens doors. Someone programs the key card to open the first three doors, then announces "the hallway is open!" — but the fourth door still needs its own programming, and nobody checked it. The hallway isn't open until someone walks the whole hallway and tries every door. The rule: count all the doors first, then test all the doors — don't announce until the last one clicks.

## 👵 GRANDMA NOTE

It's like having four deadbolts on the front door and the locksmith only rekeys three of them, then hands you the new key and says "all done." The door still won't open until the fourth lock is done too. The lesson the team wrote down: when you fix the locks, you first count how many locks there are — all of them, not just the ones you remember — and you don't say "finished" until each one turns with the new key.

## 🧠 NAYA NOTE

Cold successor: before any "settings repair cleared" verdict on a GitHub ruleset-bypass repair, run the enumeration first:

1. `GET /repos/{owner}/{repo}/rulesets` — list every ruleset on the repo.
2. Filter to the ones whose target matches the ref you're repairing (e.g. `~DEFAULT_BRANCH` / main). Do not assume you know the set — read it live.
3. For each matching ruleset, read `bypass_actors` (and the live state of the rule that was blocking, e.g. the pull_request rule).
4. The verdict names every matching ruleset ID + its bypass state. A verdict that names only a subset is incomplete and does not lift the hold.

The falsifier that proved the mechanism: three of four rulesets carried the DeployKey bypass and the push was still blocked; the moment 24858146's bypass was written and re-verified live, the hold could lift. If GitHub had evaluated only a single matching ruleset, N−1 would have unblocked — it didn't. Union evaluation is why "I fixed the rulesets" must always be answered with "which ones, all of them?"

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1636",
  "title": "A Ruleset-Bypass Verdict Enumerates Every Matching Ruleset — GitHub Evaluates the Union",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "applies_when": ["ruleset", "bypass", "deploy-key", "settings-repair", "verdict"],
  "enforcement": "before any ruleset-bypass 'cleared' verdict: GET /repos/{owner}/{repo}/rulesets, filter to rulesets whose target matches the target ref, read bypass_actors on EACH; the verdict names every matching ruleset ID + its bypass state. A verdict naming only a subset is incomplete and does not lift the hold.",
  "cousins": ["SN-1215 (ruleset guardrail: prevention is not remediation)", "SN-0922 (stale qualifications are not republished)"],
  "evidence": {
    "claim_falsified": "shared-state.json director_tick_2026_10_17_2138 (2026-10-17 21:38Z): the 21:08Z 'L495 settings arc CLOSED at live bytes' claim FALSIFIED — ruleset 24858146 (main-protection, ACTIVE, ~DEFAULT_BRANCH) bypass_actors=[] with pull_request rule live",
    "three_of_four": "bypass grants were written to 24857158, 24857323, 23853581 — but not 24858146; deploy-key push remained structurally blocked",
    "verifier_with_blocker": "board #2721 comment 6245567148 (Resolve VERIFY): VERIFIED-WITH-BLOCKER",
    "clearance": "board #2721 comment 6245986728 (Naya Clarity): 24858146 bypass written 21:44 PDT, re-verified 22:08 PDT; all 4 rulesets carry DeployKey bypass — hold may lift",
    "byte_verify_fourth_missed": "board #2721 comment 6246512807 (Resolve VERIFY): companion settings byte-verified — the pass that kept missing the fourth ruleset"
  },
  "decision_change": "future 'declare the ruleset-bypass repair complete / lift the merge hold' verdicts must enumerate every active ruleset matching the target ref before the verdict, not after the block re-fires",
  "falsifier": "if GitHub evaluated only one matching ruleset, fixing N-1 of N would have unblocked the push; the push stayed blocked until the fourth was fixed",
  "mechanism": "GitHub evaluates the UNION of all rulesets targeting the ref; a bypass grant on only some leaves the rest enforcing"
}
```
