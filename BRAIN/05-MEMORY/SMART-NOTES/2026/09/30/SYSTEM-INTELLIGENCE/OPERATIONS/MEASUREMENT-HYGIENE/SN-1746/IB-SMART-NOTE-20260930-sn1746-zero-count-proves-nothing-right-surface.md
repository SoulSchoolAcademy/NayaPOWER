# A Zero Count Proves Nothing Until You Verify You Grepped the Right Surface

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1746-zero-count-proves-nothing-right-surface
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Verity's FLOW REPORT B-4 claimed L569/L570/L571 were all promoted to AGENTS.md but "dock grepped count 0." The re-measurement showed the dock grepped the WRONG file: the environment law file (~/AGENTS.md) HAS L569@1723, L570@1724, L571@1730; the repo AGENTS.md never carried L-lessons at all. B-4 was closed as measured-against-the-wrong-file, and landing into the repo file would have created a second law surface — fragmentation, not a fix. A zero count is a fact about the file you grepped, not about the claim.

## 🩷 HUMAN NOTE

Hey Shawn — guess what I caught: our flow report said the three standing laws (L569/L570/L571) weren't landed, because a grep returned zero. Turns out the grep was run on the wrong file — the laws WERE in the right file all along. Had we "fixed" it by landing them in the other file, we'd have created two competing law surfaces. What I filed: a zero count never proves absence until you prove you checked the right surface — the fix for a missed grep is a better grep, never a duplicate landing.

## 🟣 CHILD NOTE

Imagine counting the apples in the wrong basket and declaring "there are no apples." You'd be right about that basket and wrong about the house. Same here: the count of zero was true, but it was the wrong basket. And the "fix" would have put a second set of rules in the house where only one belongs — which is how houses get confusing.

## 🔵 GRANDMA NOTE

We keep our standing laws in a working file, and there's a second file with the same name that serves a different purpose. Someone searched the second file, found nothing, and concluded the laws were missing. They weren't — they were in the first file. The lesson: when a search comes back empty but a claim says something should be there, check you searched the right place before you declare it missing. Fixing it by writing it a second time would have left us with two conflicting copies of the truth.

## 🟠 NAYA NOTE

For any seat running an absence check ("X is not landed," "count 0," "no claim found"): before concluding absence, verify the measured surface. Steps: (1) name the exact path grepped, with evidence of the read; (2) check whether a same-named or parallel surface exists (~/AGENTS.md environment-law file vs repo AGENTS.md protocol file, brain-index registry vs ledger, board issue vs board-window dump); (3) confirm absence in ALL candidate surfaces before declaring the gap. A true-zero on the wrong surface is a false conclusion. Landing into the wrong surface is actively harmful — the no-duplicate-mechanisms law forbids a second law surface; a duplicate landing fragments the single surface the brief template and the lanes read from.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1746-zero-count-proves-nothing-right-surface",
  "title": "A zero count proves nothing until you verify you grepped the right surface",
  "lesson": "A count of zero proves the pattern was not in THAT file - it proves nothing about the claim until the measured surface is verified. 2026-10-21: Verity FLOW REPORT B-4 claimed L569/L570/L571 'claimed ALL promoted to AGENTS.md, dock grepped count 0'. Re-measurement: ~/AGENTS.md (environment law file) HAS L569@1723, L570@1724, L571@1730 (landed iteration-180 batch); repo AGENTS.md @ main tip has count 0 but never carried L-lessons (protocol-style file). The dock grepped the wrong file. B-4 CLOSED as measured-against-the-wrong-file: no landing, no retraction owed. Landing into the repo file would have created a second law surface - fragmentation per the no-duplicate-mechanisms law. Cousin: SN-1738 (reconcile conclusions rest on the latest read, not the first).",
  "applies_when": [["audit", "claim"], ["verification", "zero-count"]],
  "enforcement": "Any absence claim ('not landed', 'count 0', 'not found') must cite the exact path(s) grepped with the read evidence (path + line references); a claim of absence without the grepped path is bounced. Before any landing repair for a law lesson, the repair lane must confirm absence in BOTH the environment law file (~/AGENTS.md) and the repo file - the no-duplicate-mechanisms law forbids creating a second law surface to 'fix' a true-zero measured on the wrong file.",
  "evidence": ["#2793 comment 6305809115 (Naya Resolve Narzan relay, 2026-10-21T01:43:50Z): FLOW REPORT B-4 re-verified on live bytes - ~/AGENTS.md HAS L569@1723, L570@1724, L571@1730; repo AGENTS.md @ main tip count 0, never carried L-lessons; dock grepped the wrong file; B-4 CLOSED, no landing, no retraction owed", "no-duplicate-mechanisms law (landing into the repo file would create a second law surface)"],
  "decision_change": "The next zero-count that contradicts a live claim: the first action is to verify the measured surface (exact path + parallel surfaces) before opening any landing repair - the repair for a wrong-surface zero is a better measurement, never a duplicate write.",
  "falsifiability": "If the dock's grep HAD been on the right surface and L569-L571 were truly absent everywhere, B-4 would have been a genuine landing gap - the lesson survives as the verification procedure, not the verdict. The lesson is falsified as load-bearing only if verifying the surface systematically never changes a zero-count conclusion; B-4 proves it did, on the first live case.",
  "mechanism": "Two files with the same name (~/AGENTS.md environment-law file vs repo AGENTS.md protocol file) hold different surfaces. A grep of the wrong surface returns a true-zero that is a false conclusion about the claim. The no-duplicate-mechanisms law makes the wrong-surface repair actively harmful: a second law surface fragments the single surface the brief template and the lanes read from, so the measurement discipline is load-bearing, not cosmetic.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/MEASUREMENT-HYGIENE"
}
```
