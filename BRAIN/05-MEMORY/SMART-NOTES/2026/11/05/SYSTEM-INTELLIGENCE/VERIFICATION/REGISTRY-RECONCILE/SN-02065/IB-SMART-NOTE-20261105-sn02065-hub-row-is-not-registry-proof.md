# INTELLIGENT BLOCK — SN-2065

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02065-hub-row-is-not-registry-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat verification ~12:26 PST 2026-11-05 (tip 1ecfd925; ~/memory/2026-11-05.md): MIRROR VERIFIED via read-only sb-api — hub rows exist for SN-2055/2056/2057; ASYMMETRY: SN-2058 ALSO has a hub row (19:38:38Z) with no registry entry, no capture, page-only on main — "hub follows the page, not the registry." Fresh census this tick at tip 27debfba: SN-2062 and SN-2063 pages exist on main with no registry entry, so the page-only class keeps growing.

## ✦ IN A NUTSHELL

A hub row is not proof a note is filed. At 19:38:38Z on 2026-11-05, SN-2058 had a hub row while having no registry entry, no capture, and only a page on main — the hub mirror had picked the page up before any filing step had registered it. The hub sync follows page files; the registry follows the filing path (capture + index.json); the two writers are independent, so a page-only landing creates hub presence without registry presence. The class keeps growing: at tip 27debfba, SN-2062 and SN-2063 pages exist on main with no registry entry. The durable rule: **a landing is proven only by the four-way check — page + capture + registry entry + hub row — and a hub row alone proves only that a page file exists.**

## 🩷 HUMAN NOTE

Shawn — a note showed up in the Hub today with no registry entry and no saved capture behind it. It looked live and filed, but it was only a page sitting on main that the Hub's mirror picked up on its own. The Hub watches the pages; the registry watches the filings — and those are two different watchers that don't talk to each other. So "it's in the Hub" can never mean "it's filed." From now on, a landing counts only when all four things are shown together: the page, the saved capture, the registry entry, and the Hub row. Any one of them alone is just one quarter of the proof.

## 🟣 CHILD NOTE

Imagine a school bulletin board that copies whatever is pinned on the classroom wall, and a separate attendance book that only the teacher writes in. One day a drawing appears on the bulletin board — but the teacher never wrote it in the attendance book, because the drawing was pinned straight to the wall and skipped the teacher entirely. The board shows it, the book doesn't. The new rule: seeing it on the board doesn't mean it's counted. You check the board AND the book AND the drawer where the original is kept — all four — before you say it's really there.

## 🔵 GRANDMA NOTE

Dear, it's like a shop window and a stock ledger. The window displays whatever is placed on the shelf; the ledger records only what was properly received and written down. A parcel was put straight on the shelf, so it shows in the window — but nobody wrote it in the ledger, so as far as the books are concerned it was never received. The window is not the ledger. From now on, before anyone calls a delivery properly filed, they check the shelf, the receipt, the ledger, and the window — all four together. One alone is never enough.

## 🟠 NAYA NOTE

For every seat and every verifier: never cite a hub row as proof a note is filed or registered. The hub github-sync mirrors page files; the registry is written only by the filing path (capture JSON + index.json). A page-only landing therefore creates hub presence without registry presence, and the hub row silently outruns the filing. When you verify a landing, assert all four stores independently — page file, capture JSON, registry entry, hub row — and carry any note with a hub row but no registry entry as page-only, not filed. When you report a note as live in the Hub, say which of the four you actually checked; "hub row exists" is a serving claim, never a filing claim.

## 🟢 MACHINE NOTE

```json
{
  "slug": "hub-row-is-not-registry-proof",
  "sn": "SN-2065",
  "title": "A Hub Row Is Not Registry Proof — The Hub Follows the Page, Not the Registry",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["filing", "verification", "hub", "registry", "mirror"],
  "enforcement": "A filing-verification receipt must assert all four stores — page file, capture JSON, registry entry, hub row — before calling a note landed; a hub-row-only proof is rejected and the note is treated as unregistered until the registry entry is shown.",
  "falsifier": "A page-only note with no hub row would show the hub sync is selective rather than page-driven; a hub row that vanishes when its page is deleted would show the mirror tracks the registry after all — either would require revising the stated mechanism.",
  "decision_changed": "Whether a note is called filed or live: a hub row no longer counts as filing proof — the verifier checks the registry entry independently, and a note with a hub row but no registry entry is carried as page-only, not filed.",
  "mechanism": "The hub github-sync mirrors page files from the repo while the registry is written only by the filing path (capture JSON + index.json); the two writers are independent and keyed on different things, so a page-only landing creates hub presence without registry presence, and the hub row silently outruns the filing.",
  "provenance": "Main-seat verification ~12:26 PST 2026-11-05 (tip 1ecfd925; ~/memory/2026-11-05.md): MIRROR VERIFIED via read-only sb-api — hub rows exist for SN-2055/2056/2057; ASYMMETRY: SN-2058 ALSO has a hub row (19:38:38Z) with no registry entry, no capture, page-only on main — 'hub follows the page, not the registry.' Fresh census this tick at tip 27debfba: SN-2062 and SN-2063 pages exist on main with no registry entry. Cousins: SN-1891 door filings register on write, SN-01482 filing and registry one transaction, SN-0887 note and registry entry atomic — all state the filing obligation; this note states what a hub row does and does not prove."
}
```
