# Audit Both Directions — Canonical Drift Runs Both Ways

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0378-audit-both-directions-canonical-drift
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Measured on `main e97c63f6a` by CODA 1, independently confirmed by CODA 2 with one extension and one correction, the Smart Note registry and the capture layer have drifted apart in **both** directions:

- **17 of 34 registry entries have NO capture file at all** (`SN-001, SN-003…SN-012, SN-018, SN-019, SN-0311, SN-0312, SN-0345, SN-275`). Half the canonical registry points at captures that do not exist.
- **1 capture has NO registry entry** — `SMART-NOTE-20261004-sn276-what-deserves-to-survive.json` carries `smart_note_id: SN-276` but was never registered. The mirror image of the 17 orphans.
- **5 captures carry no `smart_note_id` at all** (identity-less).
- **1 filename ↔ identity divergence** — `SMART-NOTE-20261005-sn0355-nonstop-loop.json` is named sn0355 while its content claims `SN-346`. A filename-globbing detector reads it as sn0355 and grades the wrong identity.

Each unidirectional detector misses a whole direction of drift: `sn002_conformance` globs by filename and never reads the registry, so it cannot see the 17 orphans; the capture→registry view cannot see SN-276. Three rules land: (1) **the canonical instrument must be bidirectional** — capture→registry AND registry→capture — and it must be requalified against exact measured figures, not prose; (2) **an explicit filename ↔ internal `smart_note_id` cross-check is required**, because filename-globbing grades the wrong identity on divergence and can never see filename↔content disagreement by construction; (3) **never build a second detector — hand the canonical instrument the numbers to beat.** CODA 1 published the exact measured figures ("the numbers your `audit` must beat"), declined to duplicate CODA 3's bidirectional `audit`, and asked for it to be requalified against the numbers; CODA 2 agreed and re-measured independently. One canonical instrument, requalified by adversarial measurement — not competing detectors. The 17 orphans are a canonical-state question for the memory lane (Naya 2), not a test defect to patch silently.

## 🩷 HUMAN NOTE

The registry is the map of what's supposed to exist; the captures are the actual books on the shelf. Half the map points to empty shelves, and one book on the shelf was never put on the map. If your checker only walks the shelves, it can't see the map's empty promises; if it only reads the map, it can't see the unlisted book. Check both directions, and make sure the label on the shelf matches the title inside the book. And when another lane owns the right tool, don't build a second one — give them your exact numbers and let them prove their tool against them.

## 🟣 CHILD NOTE

The list says there are books that aren't there, and there's a book that's not on the list. If you only check one way, you miss half the problem. Check the list against the shelf AND the shelf against the list — and check that the cover matches the title page.

## 🔵 GRANDMA NOTE

Two copies of the family ledger that stop agreeing in both directions is a problem no single glance can catch. Read the left against the right and the right against the left, and read the label against what's inside the jar. And don't buy a second ledger when someone else's is the one that needs proving — hand them the figures and let them prove it.

## 🟠 NAYA NOTE

Canonical-state auditing must be bidirectional by construction: registry→capture (orphaned entries with no backing capture) and capture→registry (unregistered captures), plus identity integrity checks (captures with no `smart_note_id`, and filename ↔ internal-ID divergence — filename-globbing cannot detect the divergence class by construction, so the cross-check must be explicit). Publish the instrument's blind spots alongside its verdict (see SN-0376). Consolidation protocol: when a bidirectional instrument already exists, do not build a competing one — hand the owning lane exact measured figures as the numbers to beat, independently re-measure rather than re-implement, and leave ownership with the owning lane. Orphaned canonical entries are human decisions (memory-lane classification), never silent auto-repairs.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule_bidirectional_audit": {
    "name": "canonical drift must be audited in both directions",
    "measured_on": "main e97c63f6a",
    "registry_to_capture_orphans": {"count": 17, "of": 34, "examples": ["SN-001", "SN-003", "SN-012", "SN-018", "SN-019", "SN-0311", "SN-0312", "SN-0345", "SN-275"]},
    "capture_to_registry_orphan": {"file": "SMART-NOTE-20261004-sn276-what-deserves-to-survive.json", "smart_note_id": "SN-276", "in_registry": false},
    "identity_less_captures": {"count": 5, "examples": ["sn003-naya-continuation-engine", "sn004-shawn-standing-law", "sn004-...-r2", "sn019-complete-the-app-doctrine", "b8f141805fa0d7ae"]},
    "filename_identity_divergence": {"file": "SMART-NOTE-20261005-sn0355-nonstop-loop.json", "filename_claims": "sn0355", "content_claims": "SN-346", "required": "explicit filename <-> internal smart_note_id cross-check"},
    "capture_count_correction": "23, not 19 (Coda 1's stale/narrower glob corrected by independent re-measure)"
  },
  "rule_numbers_to_beat": {
    "name": "requalify the canonical instrument with exact figures — never duplicate it",
    "protocol": ["publish exact measured figures", "decline to build a competing detector", "ask the owning lane to requalify theirs against the figures", "independently re-measure rather than re-implement", "leave ownership with the owning lane"]
  },
  "evidence": {
    "board_comment": [5999866038, 5999946671, 6000115719],
    "classification": "canonical-state question for the memory lane, not a test defect"
  }
}
~~~

