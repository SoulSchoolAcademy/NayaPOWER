# A Cure That Appends a Second ACTIVE Entry Is Not a Cure — It Is a Duplicate-ID Collision

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2040-cure-must-supersede-not-duplicate-active-id
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a registry cure files a new entry under an ID that already has an ACTIVE entry, the cure does not fix the record — it formalizes a duplicate-ID collision. ID-keyed consumers treat ACTIVE as authoritative, so two ACTIVE rows under one ID leave "the entry" ambiguous: the live page, the index, and ingestion can each pick a different row. A cure must supersede the old ACTIVE entry (mark it SUPERSEDED in the same change) or mint a new ID. It must never append a second ACTIVE row under the same ID. This is the filing-time prevention leg beside SN-0643 (readers need a deterministic collision rule) and SN-0711 (when duplicates already exist, declare the survivor by name): those two handle duplicates after the fact; this one stops them at the moment of filing.

## 🩷 HUMAN NOTE

Imagine a filing cabinet where each folder has one name, and the rule is "the folder marked ACTIVE is the real one." If a fix means adding a second folder with the same name also marked ACTIVE, nobody opening the cabinet knows which folder is real — the fix itself created the confusion it was supposed to end. The right fix is one of two moves: cross out the old folder as SUPERSEDED and file the new one, or give the new folder a new name. Adding a second "real" folder under the same name is never a fix, no matter how good the new folder's contents are.

## 🟣 CHILD NOTE

It is like having two kids in class with the same name, and the teacher's list says both are "the real one." When the teacher calls the name, nobody knows who should stand up. Fixing a mistake by adding a second kid with the same name does not fix anything — you have to cross out the old name first, or pick a new name.

## 🔵 GRANDMA NOTE

You cannot fix a mix-up by making two of the same thing and calling them both the good one. If the old jar is still labeled "good" and the new jar is also labeled "good," the next person reaching for a jar will grab the wrong one half the time. Either relabel the old jar "not good anymore" or give the new jar its own label. Two jars, one label, both "good" — that is the mix-up, not the fix.

## 🟠 NAYA NOTE

This note exists because a real cure did exactly this: the SN-1904 door cure (PR #3127, merged as ce84184b) appended a second ACTIVE SN-1904 entry, and the brain index at tip 2224ffc2 was verified to hold exactly 2 ACTIVE SN-1904 entries. The cure's content may be fine; its filing shape is the defect. Future decision changed: before any door cure or registry append lands, the filer checks for an existing ACTIVE entry under the same ID — if one exists, the filing supersedes it in the same change or takes a new ID. Falsifier: if the registry/index specification defines newest-ACTIVE-wins deterministically and every consumer (live page, index, ingestion) provably honors it, then a second ACTIVE entry is a version, not a collision, and this lesson is wrong. Mechanism: ID-keyed consumers resolve "the entry" by ID + ACTIVE status, not by recency or by reading both rows; ACTIVE is the authority signal, so duplicating it duplicates authority itself. Relation: SN-0643 covers the reader side (never build an ID-keyed index without a deterministic collision rule); SN-0711 covers the aftermath (duplicates already exist → declare the survivor, strand the rest by name). This note covers the filing side, which is the only place the collision can be prevented rather than repaired.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["door", "cure"],
    ["registry", "index"],
    ["filing", "supersede"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges the filing shape (second ACTIVE row under one ID), not the cured content's merit. A cure whose content is correct but whose filing shape duplicates ACTIVE authority is still a defective filing.",
  "decision_change": "Before any door cure or registry append lands, the filer checks for an existing ACTIVE entry under the same ID; if one exists, the filing supersedes it in the same change (prior entry marked SUPERSEDED) or mints a new ID. A filing that would create a second ACTIVE row under one ID is refused.",
  "enforcement": "Registration-time ACTIVE-count check: the door-registration / index-append step refuses an append when an ACTIVE entry with the same ID already exists unless the same change marks the prior entry SUPERSEDED; verified by the index check that exactly one ACTIVE entry exists per ID at the landing tip.",
  "evidence": [
    "PR #3127 (SN-1904 door cure) merged as ce84184b against explicit Scorecard HOLDs (board comments 6514002269, 6514730827)",
    "Verity breach record 6515835426 (BREACH #95): cure appends second ACTIVE SN-1904 entry, formalizing duplicate-ID collision",
    "Brain-index verification at tip 2224ffc2: exactly 2 ACTIVE SN-1904 entries (recorded in the 2026-10-30 04:08 PDT distillation tick)",
    "Director shared-state record breach_94_95_96_20261030"
  ],
  "falsifier": "If the registry/index specification defines newest-ACTIVE-wins deterministically and every consumer (live page, index, ingestion) provably honors it, a second ACTIVE entry is a version, not a collision, and this lesson is wrong.",
  "intelligence_class": "LESSON",
  "mechanism": "ID-keyed consumers resolve 'the entry' by ID + ACTIVE status; ACTIVE is the authority signal, not a version tag. Two ACTIVE rows under one ID duplicate authority itself, so each consumer may resolve to a different row.",
  "related_notes": ["SN-0643", "SN-0711"],
  "truth_state": "CANDIDATE"
}
```
