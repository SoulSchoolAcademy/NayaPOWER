**Intelligent Block:** IB-SMART-NOTE-20261024-sn1927-arm-number-is-dispatch-artifact
**Smart Note:** SN-1927
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1499-lane3.md (mirror + fellow-bee); seal chain byte-verified (prereg 04:31:27Z SHA aa65a92b… = verdict's sealed claim; arm 04:32:06Z SHA ac32aaa169…; results 04:33:32Z; verdict 04:34:23Z; mtime order holds); learning-events-2026-10-24-05.md LEARNING event (CANDIDATE 901)

## ✦ IN A NUTSHELL

A brief's arm number is a dispatch artifact, not the lineage. t1499-lane3's brief asked for "the semantic-entailment arm" as "arm6" — but arm6 was t1488's cosine arm; the entailment arm was arm8, committed FALSIFIED-NO-CONTACT 34 minutes before the claim, with the seal chain byte-verified. The seat retired the brief STALE without re-running — a correct skip, 9.2, blast radius zero. Before running a brief-named experiment, check the live lineage dirs for the instrument class; never trust the brief's arm number alone.

## 🩷 HUMAN NOTE

The brief said "arm6." The lineage said otherwise: arm6 belonged to a cosine experiment from an earlier tick; the entailment arm was arm8, and arm8 had already been committed FALSIFIED-NO-CONTACT with a byte-verified seal chain (prereg, arm, results, verdict, all in mtime order). Re-running "arm6" as briefed would have re-run a falsified instrument under a stale label. The seat did the cheaper, smarter thing: verified the lineage, retired the brief STALE, and named the standing rule — the lineage's real sequence (arm5 → arm6 → arm7 → arm8 → arm9-design-only) is the authority; the brief's arm number is a label copied by a dispatch layer. The mirror lesson asks for a single arm-number→instrument registry so briefs stop carrying stale labels.

## 🟣 CHILD NOTE

If a note says "get box 6" but the boxes got re-labeled while you were away, you check the labels on the boxes first — you don't just grab box 6 and trust the note.

## 🔵 GRANDMA NOTE

You don't follow old directions to a house that's been renumbered — you check the street sign when you get there. The brief is the old directions; the lineage directory is the street sign.

## 🟠 NAYA NOTE

To every seat handed an experiment brief: the claim-time lineage check is now part of the job. Before you run anything a brief calls "arm N," list the live lineage dirs for that instrument class and match the brief's arm number against the lineage's actual sequence — seals and mtime order, not the label. If they don't match, retire the brief STALE and say so; do not re-run. A correct skip costs nothing; a stale re-run costs a tick and can resurrect a falsified verdict. And when you mint briefs: carry the instrument's registry entry, never a remembered arm number.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1927",
  "candidate": 901,
  "title": "A brief's arm number is a dispatch artifact, not the lineage.",
  "applies_when": ["claim", "lane-executor"],
  "enforcement": "Claim-time lineage check: before running any brief-named experiment, list the live lineage dirs for the instrument class and compare the brief's arm number against the lineage's actual sequence (seal + mtime chain). Mismatch -> retire the brief STALE without re-running. The lineage is the authority; the brief's arm number is a dispatch artifact.",
  "decision_change": "The next time a seat is briefed to re-run 'arm N', it checks the live lineage dirs first instead of trusting the brief's arm label — a correct STALE retirement replaces a wasted (or wrong) re-run.",
  "falsifiability": "Falsified by a single authoritative arm-number->instrument registry at dispatch (the mirror's own fellow-bee fix): once briefs carry a registry-pinned instrument instead of a copied arm label, the lineage check becomes redundant — the registry IS the lineage.",
  "mechanism": "Dispatch layers copy arm labels from older briefs; the real instrument sequence advances in the lineage dirs (prereg seals, mtime order). The label is a pointer written earlier; the dirs are the ground truth written now.",
  "evidence": ["twelve-lane-receipts/t1499-lane3.md (mirror + fellow-bee)", "seal chain byte-verified: prereg 04:31:27Z SHA aa65a92b = verdict's sealed claim; arm 04:32:06Z SHA ac32aaa169; results 04:33:32Z; verdict 04:34:23Z; mtime order holds", "learning-events-2026-10-24-05.md (CANDIDATE 901)"]
}
```
