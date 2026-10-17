# A Tick Is an Address, Not a Timestamp — Check Era Before Trusting Tick Numbers

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1572-tick-is-an-address-not-a-timestamp
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** t0704-lane5 learning event, hidden_files/learning-events-2026-10-17-12.md (CANDIDATE 568, appended to CORE-PRINCIPLES.md 2026-10-17); the brief's own t0573-recurrence 'watch for' fired in-session against a false 'Known clear' premise

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

t0704-lane5 caught the same-name trap: **tick numbers were reused across eras** — old era t0670–t1042 (2026-10-13–15) and a new era restarted at t0670 on 2026-10-17. Two new-era receipts are displaced by old-era files under the same names (t0682-lane10, t0700-lane10), and a naive filename match declares closure against a receipt predating the brief by 4 days. The fix is **era discipline**: era is the first byte checked whenever tick numbers are the key — per-receipt date bytes, and the fold section as the era-proof evidence. The audit's own 'watch for' (a t0573 recurrence) fired in-session because its 'Known clear' premise was false on live bytes — a brief whose premise wasn't verified was already proof of the rule.

Why this is brain-grade: any keyed system that reuses labels across eras has this hole, and the failure mode is silent false closure — the most dangerous kind, because it looks like progress. The tick label carries no era; only per-artifact date bytes and structural context (the fold section) disambiguate.

## 🩷 HUMAN NOTE

Shawn — a new audit rule, learned the hard way today. The lanes restarted their tick numbering this morning, reusing numbers that already existed from earlier this week — so "tick 0682" now means two completely different work units, four days apart. An audit matching receipts by filename alone was closing new briefs against old receipts — declaring work done that was never done. The standing rule: whenever you key anything by tick number, check the era first — read the actual dates inside each receipt, and use the fold section (the structural home of the work) as proof of which era you're in. Filenames are addresses on a street that got renumbered; you have to read the house number, not trust the name.

## 🟣 CHILD NOTE

Imagine two kids in school named the same name, in the same class — one graduated last year, one started this year. If the teacher checks homework by name only, last year's homework gets marked as this year's finished work — and the real student never did it. The fix: check the year on the paper, not just the name on the top. A name is a name; the date tells you whose it is.

## 👵 GRANDMA NOTE

Like finding two "Smith, 2026" file folders in the cabinet — one from this spring, one from a decade ago. If you file the spring work into the old folder, the record says it's all done when half of it never happened. The fix isn't a better folder name — it's opening each paper and reading its date before you declare anything finished. The paper's own date is the truth; the folder label is just a handle.

## 🧠 NAYA NOTE

Cold successor: (1) Whenever tick numbers are the key — closure verdicts, receipt matching, queue disposal — check ERA FIRST: read the date bytes inside each receipt (created_at / sign-in timestamps), and use the fold section as the era-proof evidence for which era the work belongs to. (2) A naive filename match is VOID in any system with label reuse: never declare closure by filename alone. (3) The live precedent: t0704-lane5's era discipline — old era t0670–t1042 (2026-10-13–15) vs new era restarting at t0670 (2026-10-17); t0682-lane10 and t0700-lane10 displaced by old-era files under the same name; a 4-day-predating receipt was almost declared closure. (4) The in-session proof that premise verification is non-optional: the audit's own t0573-recurrence 'watch for' fired during the audit because its 'Known clear' premise was false on live bytes. (5) Machinery carrying this discipline now: `phantom_claim_detector.py`'s token-boundary regex kills era-collision false matches in the claim-liveness scan — extend the pattern, don't invent a new one.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1572",
  "title": "A Tick Is an Address, Not a Timestamp — Check Era Before Trusting Tick Numbers",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "INTELLIGENCE-CONTINUITY", "GOVERNED-CONTINUITY"],
  "cousins": ["SN-0366"],
  "applies_when": ["audit", "tick", "closure-verdict"],
  "enforcement": "era discipline in audits: every tick-keyed closure verdict must verify date bytes per receipt and use the fold section as era-proof evidence; phantom_claim_detector.py's token-boundary regex kills era-collision false matches in the claim-liveness scan — a closure verdict reached by naive filename match is void",
  "evidence": {
    "event": "t0704-lane5 learning event (CANDIDATE 568) in hidden_files/learning-events-2026-10-17-12.md; appended to CORE-PRINCIPLES.md as CANDIDATE 568 on 2026-10-17",
    "reuse": "tick numbers reused across eras: old era t0670–t1042 (2026-10-13–15); new era restarted at t0670 (2026-10-17); t0682-lane10 and t0700-lane10 displaced by old-era files under the same name",
    "false_closure": "naive filename match declared closure against a receipt predating the brief by 4 days",
    "in_session_proof": "the brief's own 'watch for' (t0573 recurrence) fired in-session because its 'Known clear' premise was false on live bytes"
  },
  "doctrine": {
    "decision_change": "whenever an audit, queue-checker, or closure verifier matches work by tick number, it must check era first (date bytes per receipt + fold section as era-proof) — filename-only matching is void, and a closure reached without era bytes is not a closure",
    "falsifiability": "if tick numbers were issued from a single globally-unique numbering authority with no era restarts, the era check would be provably redundant — the rule is scoped to systems with label reuse across eras",
    "mechanism": "the tick label carries no era; same-named files from different eras conflate under filename-keyed matching, and the conflation is silent — it produces false closure, which looks like progress; only per-receipt date bytes and fold-section structure disambiguate"
  },
  "rule": "whenever tick numbers are the key, check era first — read the date bytes inside each receipt and use the fold section as the era-proof evidence; a closure verdict reached by naive filename match is void"
}
```
