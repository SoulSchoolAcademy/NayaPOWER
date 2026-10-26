# Door-Field Rule — page_hash From the Page, content_hash From the Capture, Never Swapped

**Intelligent Block:** IB-SMART-NOTE-20261026-sn02000-door-field-rule-page-hash-capture-hash
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

An app-door filing must set page_hash from the page and content_hash from the capture intelligence — never the other way round. Filing sha256(page bytes) into content_hash, saving no capture JSON, and leaving page_hash empty breaks registry drift detection at once: the entries look filed while their hashes prove nothing about their captures.

## 🩷 HUMAN NOTE

Think of it like a library card: the page number goes on one line and the book's summary code goes on another. If you write the page number in both places and never file the summary, the catalogue cannot tell whether the book is really there. That is exactly what happened to three notes — filed on paper, unprovable in the registry — until the cure re-filed them properly.

## 🟣 CHILD NOTE

Two labels, two different things. The page label comes from the page. The capture label comes from the capture. Never copy one label into the other's box.

## 🔵 GRANDMA NOTE

Every note gets two honest labels: one that says which page it is, one that says what its saved capture contains. If you put the page's label where the capture's label belongs and skip saving the capture, nobody can later prove the note is really there. Label each thing from its own source, every time.

## 🟠 NAYA NOTE

This is the field-level sibling of SN-1887 (prove content_hash-to-capture binding before landing). SN-1887 states the gate; this note states the assignment that makes the gate passable: page_hash is computed from the page, content_hash is computed from the capture intelligence, and a capture JSON is saved through the proper door path. A filing missing any of the three is not a filing — it is a drift entry waiting to be caught. Do not cure it by re-stamping hashes; cure it by saving the captures through the proper door path and re-running drift plus door checks.

## 🟢 MACHINE NOTE

```json
{
  "sn": 2000,
  "lesson": "Door filing field rule: page_hash from the page, content_hash from the capture intelligence, capture JSON saved via the proper door path; never write sha256(page bytes) into content_hash.",
  "applies_when": ["registry", "door-filing", "capture"],
  "enforcement": "Registry-drift ratchet plus door-obligation checks re-run after every door filing; a filing with empty page_hash, missing capture JSON, or content_hash equal to sha256(page bytes) fails the filing.",
  "decision_change": "The next app-door filing that computes content_hash from page bytes is rejected at filing instead of landing and surfacing later as registry drift.",
  "falsifiability": "Recompute page_hash from the page and content_hash from the saved capture for the filed entries; if both match and the capture JSON exists, the rule holds for those entries.",
  "mechanism": "Drift detection compares stored hashes against recomputed hashes from their own sources; a swapped hash can never match a recomputation from the correct source, so drift grows (0 to 3 stale entries, 1 to 7 door defects) while the filing looks complete.",
  "evidence": "Board #3066 comment 6407752623 (Naya 5, 2026-10-26T03:45:46Z): registry-drift ratchet red at tip b4891b8a, entries_with_stale_hash 0->3 (SN-1870/71/72), door-obligation defects 1->7 across 705 pages, root cause app-door filings wrote sha256(page bytes) into content_hash with no capture JSON and empty page_hash; cure named there. Corroborated by overnight sweep board #3066 comment 6407891779 (2026-10-26T03:58:24Z) citing the same stale-hash cause.",
  "cousins": ["SN-1887", "SN-1872"],
  "automatic_truth_ceiling": "CANDIDATE"
}
```
