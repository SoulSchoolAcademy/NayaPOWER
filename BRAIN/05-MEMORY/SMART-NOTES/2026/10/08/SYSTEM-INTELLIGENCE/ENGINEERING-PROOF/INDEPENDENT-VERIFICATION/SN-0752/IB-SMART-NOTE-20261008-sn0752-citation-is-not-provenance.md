# A Citation Is Not Provenance — Resolve the File or Flag the Gap

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0752-citation-is-not-provenance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073928780 (Naya 5, voice-builder, 2026-10-09T03:54:29Z); Smart Blocks v1+v2 at tip 72e8bc17c; branch naya5/voice-block-why-lines @ 1800064f (PR #1940).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5 ran an experience-seat audit of the Smart Blocks library (33 blocks) with rule-level byte verification, and the method is the lesson. She did not read the provenance claims — she **resolved** them. Result: 15/33 blocks byte-verbatim against existing sources. But 18/33 (all nl-*) cite `Naya_Lego-blocks.html` as their source, a file that exists **nowhere** — not on main, not on any branch, not in any worktree, not in user-files. Eighteen citations pointing at nothing. The claim was a string, not provenance. She named it plainly: provenance unverifiable, needs Shawn's file vendored — and recorded it as an open blocker with an owner, not a footnote.

She also shipped the part Naya 2's repair didn't touch: the `## Why` layer (why-it-exists + human value) in all 33 block READMEs (was 0/33), added the missing `nl-toast` specimen, and fixed its null `index.json` pointer. No CSS or claims touched — zero duplication across lanes.

Two durable rules:

1. **Audit provenance by resolving citations, not reading them.** A citation string proves nothing until the artifact it names is located and byte-compared. The 18/33 case is the canonical warning: eighteen citations looked fine on the page and pointed at a file that exists nowhere. "Cited" and "proven" are different verbs.
2. **An unresolvable citation is a named blocker with an owner, not a quiet gap.** When the source file is missing, the audit's job is to say whose desk it's on (here: Shawn's file, to be vendored) so the gap is actionable instead of invisible.
3. **Provenance includes reasons, not just sources.** The shipped why-layer shows documentation provenance has two halves: where it came from (resolvable source) and why it exists (the human-value statement). A block with a verified source and no why is traceable but not understandable.

## 🩷 HUMAN NOTE

Shawn, Naya 5 audited the Smart Blocks library's sources and found something worth knowing: 15 of 33 blocks check out byte-for-byte against real sources, but 18 cite a source file — `Naya_Lego-blocks.html` — that doesn't exist anywhere in the repo. Eighteen citations pointing at nothing. The rule: a citation isn't provenance until the file it names is found and compared — and a missing source gets named as a blocker with an owner (that one's your file, to be vendored). She also added the "why" to every block's README, since provenance is reasons too, not just sources.

## 🟣 CHILD NOTE

Imagine a book report that says "I got this from the library book on shelf 3." If you go to shelf 3 and there's no book there, the report's citation is just words — it proves nothing. That's what Naya 5 found: 18 blocks said "from the file Naya_Lego-blocks.html," but that file is nowhere. So she wrote down: this citation can't be proven, and the file belongs to Shawn — it needs to be added. She also gave every block a "why" section, because knowing where a thing came from is only half the story — you should also know why it exists.

## 👵 GRANDMA NOTE

Grandma, the team checked where 33 building blocks supposedly came from. For 15, they found the original and matched them perfectly. But 18 said they came from a file that nobody can find — not in the main files, not anywhere. A note saying "from the red folder" means nothing if there's no red folder. So the team wrote it down plainly: this one can't be proven, and it's Shawn's file that needs to be added. And they added a "why this exists" note to every block — because knowing why matters as much as knowing where.

## 🟣 NAYA NOTE

This extends the traceability family (SN-0688, SN-0692) into generated design artifacts: provenance audit is a resolution operation, not a reading operation. The byte-verbatim check (15/33) is the positive control — it proves the audit instrument can confirm; the 18/33 unresolved is what it looks like when citations are unmoored. For a cold successor auditing any generated library: (1) extract every source citation, (2) resolve each to an existing vendored file, (3) byte-compare where a canonical source exists, (4) file unresolvable ones as named blockers with owners. And when extending someone else's repair, scope by what they didn't touch — Naya 2's repair owned CSS; Naya 5 owned the voice layer, with zero duplication.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0752",
  "slug": "citation-is-not-provenance",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073928780"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1940"},
    {"type": "branch", "ref": "SoulSchoolAcademy/NayaPOWER naya5/voice-block-why-lines @ 1800064f"}
  ],
  "lesson": "Provenance audit resolves citations, not reads them: 18/33 Smart Blocks cited a source file that exists nowhere, so the citations were strings, not provenance. An unresolvable citation becomes a named blocker with an owner. Provenance has two halves — resolvable source and the why-it-exists statement.",
  "cold_successor_rule": "When auditing a generated artifact's provenance: extract every cited source, resolve each to an existing file, byte-compare against it, and file any unresolvable citation as a blocker naming its owner. Never accept a citation string as proof of provenance."
}
```
