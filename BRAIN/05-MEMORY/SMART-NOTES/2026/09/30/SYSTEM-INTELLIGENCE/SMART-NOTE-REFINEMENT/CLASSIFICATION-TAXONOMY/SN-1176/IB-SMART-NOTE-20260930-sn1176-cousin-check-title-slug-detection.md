# SMART NOTE — Duplicate Detection Must Compare Titles and Slugs, Not Declared Cousins Fields

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1176` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1176-cousin-check-title-slug-detection` |
| Human title | Duplicate Detection Must Compare Titles and Slugs, Not Declared Cousins Fields |
| Category | SYSTEM INTELLIGENCE |
| Topic | SMART NOTE REFINEMENT |
| Subtopic | CLASSIFICATION TAXONOMY |
| Captured | 2026-10-13 09:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Capture type | Pipeline mechanism fix |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | `hidden_files/learning-events-2026-10-13-02.md` event 1 (02:20 PDT review); `learn/ledger.json` SN-1167/1168/1169 vs `CORE-PRINCIPLES.md` candidates 84/87/90 |

---

## ✦ IN A NUTSHELL

**The ingestion cousin-check must compare titles and slugs, not just the declared "Cousins:" field.** Three "new" ingested notes — SN-1167, SN-1168, SN-1169 — were title-identical restatements of existing candidates 84, 87, 90, all filed with "Cousins: none," so the check missed them and they were filed as new. They were caught and retroactively linked (SN-1167→84, SN-1168→87, SN-1169→90), but the mechanism gap stays open until the check compares title/slug similarity at ingest time.

---

## 🩷 HUMAN NOTE

The system asks every new note "who are your cousins?" and trusts the answer. Three notes answered "none" — and they were wrong; they were restating notes that already existed. The lesson: don't only ask the note. Read the title yourself. A duplicate detector that relies on self-declaration will always miss the duplicates that don't know they're duplicates. Compare the words on the cover, not just the family tree inside.

---

## 🟣 CHILD NOTE

Imagine three kids turn in homework with the exact same title as homework already on the shelf, but each writes "I copied from nobody." The teacher shouldn't just believe the note — she should look at the titles. That's the fix: check the titles, not just the "I didn't copy" checkbox.

---

## 🔵 GRANDMA NOTE

Dear, if someone hands you a recipe titled exactly like one already in your box but swears it's new, you check the title against your box — you don't just take their word for it. Our system learned that this morning: trust, but compare the labels.

---

## 🟠 NAYA NOTE

1. At ingest time, the cousin-check MUST run title/slug-level similarity against existing candidates — the declared "Cousins:" field is advisory, never sufficient. Self-declared "Cousins: none" is the exact shape the misses take.
2. The witnessed failure: SN-1167/1168/1169 (expected-fail-fixture-first, extraction-fidelity, blinding-protocol) were byte-similar in title/slug to candidates 84/87/90 (Shawn's 2026-09-30 BRAIN originals). Convergent rediscovery is good news (lanes independently re-derived the originals); the pipeline gap is the work item.
3. Retroactive linking (SN-1167→84, SN-1168→87, SN-1169→90) repaired the instance; the mechanism fix prevents the class. An honest ledger names the gap instead of hiding the duplicates.
4. When the similarity check fires, link — don't file a new candidate. Filing a near-duplicate as new is how the active brain bloats.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1176-cousin-check-title-slug-detection",
  "epistemic_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "ingest cousin-check MUST include title/slug similarity; declared Cousins field is advisory only",
  "witnessed_failure": "SN-1167/1168/1169 title-identical to candidates 84/87/90, all filed 'Cousins: none'",
  "repair_done": "retroactive links SN-1167->84, SN-1168->87, SN-1169->90",
  "repair_owed": "title/slug-level duplicate detection at ingest time",
  "evidence": "learning-events-2026-10-13-02.md event 1; learn/ledger.json"
}
```

---

## 🔗 HOW IT CONNECTS

- **Repairs** the ingestion pipeline gap witnessed 2026-10-13 02:20 PDT.
- **Supports** the anti-bloat rule: no hoarding in the active brain (repo AGENTS.md discernment law, rule 10).

## 🔬 EPISTEMIC STATE

**CANDIDATE.** The failure is witnessed and the instance repaired; the mechanism fix (title/slug detection at ingest) is named but not yet implemented — that is the owed work.

## 🌍 APPLICABILITY

- **Applies to:** every Smart Note / candidate ingest path, including lane-mirror and twelve-lane captures.
- **Does NOT apply to:** deliberate restatements that add new evidence — those link AND extend, with the delta named.

## 🧬 SUCCESSOR EFFECT

Future Naya: when you ingest, compare the covers, not just the family trees. A duplicate that doesn't know it's a duplicate is still a duplicate — and the check that catches it is mechanical, not confessional.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
