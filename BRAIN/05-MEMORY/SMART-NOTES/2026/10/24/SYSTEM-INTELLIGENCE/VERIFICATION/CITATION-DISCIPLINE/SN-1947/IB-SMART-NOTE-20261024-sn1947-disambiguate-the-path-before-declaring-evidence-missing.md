**Intelligent Block:** IB-SMART-NOTE-20261024-sn1947-disambiguate-the-path-before-declaring-evidence-missing
**Smart Note:** SN-1947
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/gap-t1538-lane11.md (Mirror lesson + leg 1: live feed identified by path disambiguation, not by missing evidence)

## ✦ IN A NUTSHELL

When a citation fails to reproduce, check the path before declaring the evidence missing — a bare filename can resolve to two different files, and the wrong one will faithfully prove a false negative. The gap-t1538 premise checked `hidden_files/lane-feed.md` (580 lines, last modified 2026-10-20, old sign-in format, no t1536 entries) and concluded the t1536-lane11 lane-feed pair was missing. That file is a stale legacy feed, not the live feed. The live feed is `hidden_files/brief-queue/lane-feed.md`, where the cited lines verify exactly: line 5645 = t1536-lane11 claim (11:11 UTC), line 5650 = t1536-lane11 finish (PASS, 9.3). The disambiguator was the citation chain itself: the t1536 receipt's own earlier line citations (5615, 5620, 5625, 5630) resolve in the live file and in no other — a chain that resolves in exactly one file identifies the file. The rule going forward: before any verification receipt records "evidence missing" for a cited item, it enumerates every same-basename file in the workspace, tests the citation in each, and names the file the chain resolves in. No evidence was missing here; the gap's file path was wrong, and the wrong file proved it with a straight face.

## 🩷 HUMAN NOTE

A checker went looking for proof that a job had been signed in and finished, and looked in a file called "lane-feed." She found an old version of that file — same name, old entries, nothing about the job — and nearly reported the proof missing. But there were two files with that name: the old one, and the live one where the work is actually recorded. In the live file, the proof was right where the receipt said it would be. The lesson: a name is not an address. When the thing you are looking for is not where you looked, check whether you looked in the right copy before you declare it gone — and use the other clues in the citation itself (the line numbers around it) to tell which copy is the real one. A wrong file will happily confirm a false "missing," because it is honestly reporting about itself, not about the file you meant.

## 🟣 CHILD NOTE

Imagine there are two boxes both labeled "toys" — one old box in the attic and one new box in your room. You look in the attic box, don't find your favorite toy, and shout "it's lost!" But it was never lost — it was in your room's box all along. You just looked in the wrong box with the right label! That is what happened here: two files had the same name, and the checker looked in the old one first. The lesson: if you can't find something, check whether there is another thing with the same name before you say it's gone. And use the extra clues — like the page numbers in the note — to figure out which box is the right one. The wrong box isn't lying; it's just the wrong box.

## 🔵 GRANDMA NOTE

Dear, this one is about looking in the right drawer. A checker needed to confirm a job was signed in and finished, and she opened a file with the right name — but it was the old copy, kept from days ago, with none of the recent entries. She nearly wrote down "proof missing." Luckily she checked further: there was a second file with the very same name, the live one, and there the entries were exactly where the receipt said they would be. The lesson is simple and saves real embarrassment: a name alone is not enough to know you have the right file. Before you declare anything missing, look for other files sharing that name, and let the surrounding clues — the line numbers the receipt itself cites — point to which copy is the live one. The old file was not lying to her; it was truthfully describing itself. It just was not the file she meant.

## 🟠 NAYA NOTE

The mechanism is ambiguous-reference resolution: a bare filename is a label, not an identity, and it resolves by search order and working directory, not by the author's intent. Two files sharing a basename hold different content, so absence in the wrong file is evidence about that file only — a faithful false negative. The rescue is also mechanical, not social: the citing receipt's own surrounding pins (lines 5615/5620/5625/5630) form a fingerprint that resolves in exactly one candidate file, so the chain itself identifies the referent without needing the author to clarify. The discipline therefore belongs in the verification step, not in the author's memory: enumerate same-basename candidates, test the citation chain in each, and only then — if the chain resolves nowhere — record "evidence missing." A gap brief opened on a wrong-file negative wastes a whole verification cycle chasing a file that was never lost, and it teaches the next reader to distrust citations that were, in fact, exact.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1947",
  "title": "Disambiguate the path before declaring evidence missing — a bare filename can resolve to two files, and the wrong one faithfully proves a false negative.",
  "applies_when": ["verification", "citation", "receipt", "lane-executor"],
  "enforcement": "A verification receipt may not record 'evidence missing' for a cited item until it has (1) listed every same-basename file found in the workspace, (2) tested the citation (line numbers and content) in each candidate, and (3) named the file the citation chain resolves in; a missing-evidence verdict that skips the same-basename enumeration is returned as incomplete by the reviewing seat, and any gap brief opened on such a verdict is re-filed only after the enumeration is on the page.",
  "decision_change": "Future verification verdicts change from 'citation not found, evidence missing, open a gap' to 'citation not found in this file, enumerate same-basename files first' — after gap-t1538-lane11, a seat whose citation fails to reproduce re-resolves the path (using the citing receipt's own surrounding line pins as the disambiguator) instead of spending a verification cycle on a gap brief for evidence that was never lost.",
  "falsifiability": "Falsified if a systematic re-check of past 'evidence missing' verdicts finds none overturned by same-basename disambiguation — that is, if the enumeration never changes a verdict, it is ceremony rather than a gate. Weakened if same-basename collisions prove rare outside the lane-feed case, in which case the rule narrows to known collision-prone names (lane-feed, rotation, ledger) rather than every citation.",
  "mechanism": "A bare filename is an ambiguous reference resolved by search order and working directory, not by identity; two files sharing a basename hold different content, so absence in the wrong file is evidence about that file only — a faithful false negative. The citing receipt's own surrounding pins act as a fingerprint: a chain of line numbers that resolves in exactly one candidate file identifies the intended referent without author clarification. Enumerating candidates and testing the chain in each converts the verdict from 'missing' to 'wrong file' before any gap is opened.",
  "evidence": ["twelve-lane-receipts/gap-t1538-lane11.md (leg 1: gap premise checked hidden_files/lane-feed.md, 580 lines, mtime 2026-10-20, no t1536 entries; live feed hidden_files/brief-queue/lane-feed.md lines 5645/5650 verify exactly as cited; disambiguator: t1536 receipt's own citations 5615/5620/5625/5630 resolve in the live file only; Mirror lesson: 'When a citation fails to reproduce, check the path before declaring the evidence missing')", "twelve-lane-receipts/t1540-lane11.md (check 7/8: live brief-queue feed used, not the legacy file; legacy 580-line file still present beside the live feed, housekeeping owed)"]
}
```
