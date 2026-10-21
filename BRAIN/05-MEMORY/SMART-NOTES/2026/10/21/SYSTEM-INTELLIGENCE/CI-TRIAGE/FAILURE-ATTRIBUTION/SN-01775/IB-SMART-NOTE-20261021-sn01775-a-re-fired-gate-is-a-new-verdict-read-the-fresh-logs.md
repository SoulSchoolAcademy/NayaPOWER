# A Re-fired Gate Is a New Verdict — Read the Fresh Logs, Never Re-apply the Old Fix

**Intelligent Block:** IB-SMART-NOTE-20261021-sn01775-a-re-fired-gate-is-a-new-verdict-read-the-fresh-logs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/shared-state.json `naya2_to_builder` entry (added_utc 2026-10-21T16:08:00Z; comment 6319991404, Naya Resolve Narzan, integration / evidence pass — "fresh consensus logs post-seat-correction - missing independent review, not a parser defect"; https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6319991404). Follows the seat-token corrections of comment 6319976042 (SN-1774).

## ✦ IN A NUTSHELL

The consensus gate fired red on #2835/#2834/#2832/#2829, the seat tokens were fixed, and the gate fired red again. The instinct is to re-fix the seats — but the fresh consensus logs said something different: the gate now recognized the author seats and was correctly blocking on the next control — an INDEPENDENT review from a seat other than the author. "Not a parser defect." The re-fire was not confirming the old diagnosis; it was delivering a new verdict. A gate evaluates a conjunction of conditions and reports the first failing one: fixing condition A unmasks condition B. Cause-sticking — treating the second red as the first red, re-applying the old fix — is the failure mode. The ordered procedure after any gate fix: re-pull the exact-head log, quote the current blocking condition, fix THAT.

## 🩷 HUMAN NOTE

Shawn — quick one from the merge lanes: after the seat names on four PRs were corrected, the consensus gate went red again. Nobody re-edited the seats — Naya Resolve read the fresh logs first, and the gate was now asking for something else entirely: an independent review from a different seat than the author. That's not the same problem twice; it's the gate walking down its checklist. New rule: after any fix, a re-fired red gets read fresh — quote what the gate says now, then fix that. Re-applying yesterday's fix to today's red is chasing a ghost.

## 🟣 CHILD NOTE

Imagine a teacher checking your homework with a checklist: name on top, answers done, work shown. You forgot your name, so she hands it back: "name missing." You write your name and hand it back — and she hands it back again. Does that mean your name is still wrong? No — it means she's moved to the next box: "work not shown." If you keep rewriting your name, you'll never finish. The smart move: read what she's pointing at NOW, and fix that box. Gates work exactly like the teacher's checklist — one failing box at a time, in order.

## 🔵 GRANDMA NOTE

It's like the car failing inspection: first visit, the brake light is out — you fix the bulb. Second visit, it fails again — do you change the bulb a second time? No, you read the new report: this time it's the tires. The inspection station checks everything in order and only tells you the first thing wrong. Fixing the bulb twice doesn't help the tires. Rule of the garage: every failed visit gets read from the new slip, never from memory of the old one.

## 🟠 NAYA NOTE

Gates are conjunction checkers with first-failure reporting. tools/check_merge_consensus.py evaluates a sequence of conditions (registry-recognized author seat, independent review from a different seat, remaining per-PR gates) and reports the first one that fails. A fix that satisfies condition k promotes the report to condition k+1 — the second red is definitionally a different verdict than the first. Cause-sticking (re-applying fix k because "the gate is still red") wastes the repair budget on a satisfied condition and — worse — can manufacture a bypass (self-approval, fabricated verdict) where the gate now demands an independent seat. The discipline: (1) after any gate change, re-pull the exact-head gate log; (2) quote the current blocking condition verbatim on the record; (3) route that condition to its real owner (here: a real independent verifier with seat-tagged verdicts on exact head/diff/tests — not self-approval, not a fabricated verdict); (4) wait for the conclusion before further edits. Related: SN-1660 (name the gate's read surface before re-fire vs fix — read surface first, then adjudicate; this note is the post-fix corollary: re-read the surface after every fix); SN-1650 (exact-head pinning — the re-pulled log must be the exact head); SN-1774 (seat-token registry key — the condition-k fix whose re-fire produced this lesson's condition k+1).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1775",
  "title": "A Re-fired Gate Is a New Verdict — Read the Fresh Logs, Never Re-apply the Old Fix",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"],
  "applies_when": ["merge", "gate", "consensus-gate", "ci", "re-fire", "independent-review"],
  "enforcement": "After any gate fix, the next workflow run must re-pull the exact-head gate log and quote the current blocking condition verbatim on the record before any further edit (named verification step in the claim/IV flow; the scorer bounces gate-fix claims that do not quote the fresh blocking condition). A re-fire that names the identical condition is diagnosed as 'fix did not land' (re-apply or re-diagnose the fix); a re-fire that names a new condition is a new verdict and routes to that condition's owner. Self-approval or fabricated verdicts in response to an independent-review condition are bypasses, not fixes.",
  "cousins": ["SN-1660 (name the gate's read surface before choosing re-fire vs fix — the pre-fix order-of-operations; this note is the post-fix corollary)", "SN-1650 (exact-head pinning — the re-pulled log must be the exact head, or the 'fresh' verdict is stale)", "SN-1774 (seat-token registry key — the condition-k fix whose re-fire produced this lesson's condition k+1)"],
  "evidence": {
    "fresh_verdict_comment": "board #2793 comment 6319991404 (2026-10-21T16:08Z, Naya Resolve Narzan, integration / evidence pass): 'Fresh consensus logs after the seat-tag corrections: gate now recognizes author seats and correctly blocks on the next required control - an INDEPENDENT review from a seat other than the author. Latest exact-head consensus failures for #2835/#2834/#2832/#2829 name the missing different-seat review.'",
    "condition_k_fix": "comment 6319976042 (seat-token corrections on #2835/#2832/#2834/#2829) — the satisfied condition",
    "correct_routing": "route each PR to a real independent verifier (seat-tagged verdicts on exact head/diff/tests); do not bypass by self-approval or fabricate a verdict; remaining required gates owed per PR (incl. #2835 kernel registry drift, #2832 spec/kernel failures)",
    "patience": "Worker Protocol runs in progress for the four PRs; wait for final conclusions"
  },
  "falsifiability": "The fresh log is the falsifier: if the re-pulled exact-head log names the identical blocking condition (the fix did not land), the correct action IS to re-apply/re-diagnose the fix — the rule self-limits to changed conditions. The note is wrong only if a changed-condition re-fire is correctly fixed by re-applying the old fix.",
  "mechanism": "A gate evaluates a conjunction of conditions and reports the first failing one; fixing condition k unmasks condition k+1. Cause-sticking treats the gate as a single-cause machine, so it re-applies a satisfied fix while the real blocker advances.",
  "decision_change": "After any gate fix, the next red is read from the fresh exact-head log and the quoted current blocking condition is fixed; the old fix is never re-applied on assumption. When the new condition is 'independent review', the PR is routed to a real independent verifier — never self-approved or verdict-fabricated."
}
```
