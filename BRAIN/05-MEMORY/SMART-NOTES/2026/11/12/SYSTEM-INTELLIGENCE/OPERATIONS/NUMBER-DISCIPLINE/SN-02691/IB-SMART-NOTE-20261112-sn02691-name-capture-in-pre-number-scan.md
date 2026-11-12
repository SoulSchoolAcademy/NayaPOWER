**Intelligent Block:** IB-SMART-NOTE-20261112-sn02691-name-capture-in-pre-number-scan
**Smart Note:** SN-2691
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 00:38 PST. Evidence read first-hand from the local git mirror (git protocol, zero REST quota) — #1354 capped at 2500, commenting disabled 2026-10-10, no GitHub fetch. Pre-number check (this tick, full-domain): main tip 50adb4cda — .naya/capture holds SN-2685..SN-2690, BRAIN tree holds SN-2685..SN-2689, ledger max SN-2678, branch max SN-02686, registry next_sequence 2691 (display-only). SN-2691 free in every domain; SN-2692 likewise. The staged SN-2685/SN-2686 on the branch must renumber to 2693+ before landing (2690 taken by capture; 2691/2692 taken this tick).

## ✦ IN A NUTSHELL

First-claim-stands is old doctrine — SN-0022, SN-0151, SN-1372 already say a number is computed against merged main plus every open Smart Note PR, registry and ledger. What today's collision proved is that the scan's domain list is incomplete: it names the page tree, the registry, the ledger and the PRs, but never names `.naya/capture` — the place where numbers are claimed FIRST. Captures landed 07:34:35Z claiming SN-2685..SN-2689; the pages did not land until 08:24:56–08:36:46Z, fifty minutes later; SN-2690 has a capture and no page at all. The 00:08 PST tick read merged main and still collided, because "merged main" was read as "the page tree." Name `.naya/capture` in the scan, or the next check will make the same confident wrong answer.

## 🩷 HUMAN NOTE

Shawn — we already have the rule that the first claim stands and numbers are checked against main, the registry and the ledger. This morning a seat followed that rule and still took two numbers that were already taken — because the numbers were claimed in the capture files, a place the rule never names. Captures claim a number before the note page even exists, so checking only the pages misses them. The fix is one line added to the checklist: the scan must read the capture files' number field too.

## 🟣 CHILD NOTE

Imagine you have a rule: before you pick a number, check the big book of numbers. But there is a second, smaller book where numbers get written first — and your rule never mentions it. So you check the big book, pick a number, and find out later it was already written in the small book. The fix is simple: add the small book to the rule.

## 🔵 GRANDMA NOTE

Dear, we already had the rule — first claim stands, check everywhere before you pick a number. But this morning the helper checked everywhere the rule names, and still picked numbers that were taken — because the numbers were written first in the capture files, love, a list the rule never mentions. Captures claim a number before the note page is even made. The repair is one line: the rule must name the capture files too.

## 🟠 NAYA NOTE

The verified facts: (1) Commit 59780c04, 2026-11-12 07:34:35Z, landed `.naya/capture` JSONs with `smart_note_id` SN-2685..SN-2689 (welcome, pricing, invite/ambassador, Auto-Match, Dashboard). (2) Main tip at the 00:08 PST tick was c450908f (08:01:29Z); 59780c04 is its ancestor — the captures were on main before the staging check ran. The check read the counter (last line 2684), the BRAIN tree (SN-2679–SN-2684), the ledger (max SN-2678) and the branch (max SN-02678), and concluded SN-2685/2686 were free. It never read `.naya/capture`. (3) Branch commits 76a93330 (SN-2685, relayed-ruling note) and 9652de52 (SN-2686, edit-anchor note) staged at 08:08Z — both numbers already claimed in the capture domain. (4) The collision compounded after staging: SN-2690 capture landed 08:19:29Z (d35d6fdd3), and BRAIN pages SN-2685..SN-2689 landed on main 08:24:56–08:36:46Z (f115b3abe, 9ef311f6d, e1f53c030, c63846d2b, 4802cef43). (5) Captures claim first: the SN-2685..2689 captures precede their pages by ~50 minutes, and SN-2690 has a capture with no page at all — a page-tree-only scan cannot see it. (6) The registry at main tip 50adb4cda says `next_sequence` 2691, and says it is display-only, `counter_role` advisory, allocation authority `tools/sn_claims.py` claim-before-author on the sn-claims branch — the local counter file is not the authority and lags main. (7) This tick's full-domain scan verified SN-2691 and SN-2692 free in every domain (capture, BRAIN tree, ledger, branch, registry) by first-hand git-protocol reads of the local mirror. The staged SN-2685/SN-2686 must renumber to 2693+ before landing. (8) Mechanism: each domain looks complete on its own, so a partial check returns a confident wrong answer with no error — the miss is silent. The failure is a coverage failure, not a race: the claims predated the check by 34 minutes. (9) What is NOT new here: first-claim-stands and "next free against merged main + open PRs" (SN-0022, 2026-10-07); claim-before-stage (SN-0151); check registry + ledger + open SN PRs (SN-1372). What IS new: the capture domain is missing from every one of those lists, and it is the domain where numbers are claimed first.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2691",
  "slug": "name-capture-in-pre-number-scan",
  "title": "Name .naya/capture in the pre-number scan: captures claim numbers before pages exist",
  "observation": false,
  "applies_when": [["claim", "sn-number"], ["staging", "collision"], ["number", "pre-number-check"]],
  "enforcement": "The pre-number check runs the full-domain scan before any number is taken, with .naya/capture named as a mandatory domain: (1) git grep smart_note_id across main's .naya/capture/, (2) git ls-tree of main's BRAIN/05-MEMORY/SMART-NOTES tree, (3) learn ledger max + registry next_sequence, (4) the staging branch's max, (5) open Smart Note PRs, (6) the local counter — and takes NO number when any domain cannot be read (fail closed). A number is taken only if it is above every domain's max; the tick report lists each domain's max.",
  "evidence": "Commit 59780c04 (2026-11-12 07:34:35Z) landed .naya/capture JSONs claiming SN-2685..SN-2689; main tip c450908f (08:01:29Z) contains it as an ancestor. Branch commits 76a93330/9652de52 staged SN-2685/SN-2686 at 08:08Z after a check that read counter (2684), BRAIN tree (SN-2679–SN-2684), ledger (max SN-2678) and branch (max SN-02678) but never read .naya/capture. SN-2690 capture landed 08:19:29Z (d35d6fdd3, no page); BRAIN pages SN-2685..SN-2689 landed 08:24:56–08:36:46Z (f115b3abe, 9ef311f6d, e1f53c030, c63846d2b, 4802cef43). Registry at tip 50adb4cda: next_sequence 2691, display-only, counter_role advisory. This tick verified SN-2691/SN-2692 free in every domain by first-hand git-protocol reads of the local mirror. Existing doctrine checked and NOT duplicated: SN-0022 (next free against merged main + open PRs), SN-0151 (claim-before-stage), SN-1372 (check registry + ledger + open SN PRs) — none names .naya/capture as a scan domain.",
  "decision_change": "Every future pre-number check names .naya/capture's smart_note_id as a mandatory scan domain; a number free in the page tree but claimed in a capture is never taken.",
  "falsifier": "If a collision occurs after a scan that included .naya/capture at the taking tip, coverage was not the gap — the gap is then a race (a claim landing between scan and stage) or a domain nobody knew existed, and the scan must name the race window or the new domain.",
  "cousins": ["SN-0022 (Shared Number Registry — next free against merged main + open PRs; this note patches its domain list)", "SN-0151 (No Number Without a Registry Entry — Claim-Before-Stage)", "SN-1372 (Staged Captures Aren't Indexed — check registry + ledger + open SN PRs)", "SN-1650 (pin the PR's state before pinning its head — same check-live-state family)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```