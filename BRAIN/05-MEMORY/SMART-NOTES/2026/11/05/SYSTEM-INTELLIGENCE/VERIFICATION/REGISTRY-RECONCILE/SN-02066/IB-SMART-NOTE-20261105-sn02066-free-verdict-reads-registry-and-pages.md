# INTELLIGENT BLOCK — SN-2066

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02066-free-verdict-reads-registry-and-pages
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Main-seat verification ~12:58 PST 2026-11-05 (tip 27debfba; ~/memory/2026-11-05.md): PR #3207 "SN-2059: The Structure Decides" (merged 20:26:19Z) body claimed "Number verified free before writing: hub [] + repo search total_count 0 for sn2059" — FALSE as a numbering claim: SN-2059 was already registered on main via #3202 ("Structure Beats Personality"); #3207 added a second SN-2059 page at a different path. Registry at 27debfba held SN-2059 once ACTIVE under the #3202 title. Fresh census this tick at live tip 486a381d: registry 1,123 entries, max SN-2065; SN-2066 absent from the registry with zero pages on main — the number for this note, chosen by registry + page census, not by the counter file (counter last line 2065; sequence_policy.next_sequence still 2053, stale per SN-2003).

## ✦ IN A NUTSHELL

A number is not free because the hub is empty and a repo search returns zero. The filer of PR #3207 ran exactly those two checks, declared SN-2059 free, and filed a second SN-2059 page — while the registry already held SN-2059 ACTIVE from PR #3202. The hub and the search index are derived views: the hub mirrors pages and lags main, and repo search is a text index with its own staleness and scope gaps (why #3207's search missed the registered page is unverified — the search may have run before #3202 landed or against a stale scope; the lesson does not depend on which). A derived view cannot prove a negative about its source. The durable rule: **a number is free only when the registry index AND the main-tree page census both read absent at the live tip; hub-empty plus search-zero is not a free verdict.** This is the pre-write arm of SN-2064 (page census before calling a filing landed) and the converse of SN-2065 (hub presence is not filing proof). Cousins: SN-0115 (three-layer claim registry), SN-0171 (scan every claim branch), SN-0184 (a registry read expires — re-scan at claim time).

## 🩷 HUMAN NOTE

Shawn — a filer checked two places, found nothing, and wrote "verified free" in the PR body. Both places were wrong: the number was already taken, filed by an earlier PR and sitting in the registry. The two places she checked — the Hub and a repo search — are copies that lag behind the real record; an empty copy doesn't mean the original is empty. From now on, "free" means two checks against the real thing, at the live tip: the number is absent from the registry index, and no page on main carries it. Anything less is a guess with a citation.

## 🟣 CHILD NOTE

Imagine a library where the catalog book says which numbers are taken, and a poster on the wall lists some of the books. A new librarian looks at the poster, doesn't see number 2059, and shelves a second book with that number — but the catalog book already had 2059 written in it. The poster is a copy, and copies can be out of date. The new rule: before you shelve a book, you check the catalog book itself AND you walk the shelves to count — both must say the number is free. The poster alone never decides.

## 🔵 GRANDMA NOTE

Dear, it's like checking whether a recipe number is taken by looking at the shop window and asking a neighbor — the window shows what's on display, the neighbor remembers what she saw, but neither of them is the recipe box. The number was already in the box, written in ink, and the window just hadn't caught up. From now on, before anyone takes a number, they open the box itself and fan through the cards — the box and the cards both have to say "free." The window and the neighbor are never the answer.

## 🟠 NAYA NOTE

For every seat that takes a number: never clear a number from hub rows or repo search. The hub mirrors pages and lags main; repo search is a text index with staleness and scope gaps — both can read empty while the registry holds the number, as PR #3207 proved on SN-2059. The free check is the registry index plus the main-tree page census at the live tip, both absent, read seconds before the write (SN-0184: the read expires). A PR body that asserts "verified free" must cite the registry + page-census result; a free claim citing only hub or search is void, and the filing is held for renumbering until the census is shown. This is the prevention arm — SN-2064 catches the double-file after landing; this note stops it before writing.

## 🟢 MACHINE NOTE

```json
{
  "slug": "free-verdict-reads-registry-and-pages",
  "sn": "SN-2066",
  "title": "A Free Verdict Reads the Registry — Hub-Empty Plus Search-Zero Is Not Free",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["claim", "registry", "number-free-check"],
  "enforcement": "Before writing under a number, the filer runs the registry + page census at the live tip — grep the registry index (.naya/memory/smart-notes/index.json) for the number AND list main-tree page paths carrying it; both must read absent. A PR body or staging claim asserting 'verified free' must cite the registry + page-census result; a free claim citing only hub rows or repo search is void and the filing is held for renumbering until the census is shown.",
  "falsifier": "A number cleared by registry-index + page-census at the live tip that still collides would falsify the census as sufficient — the miss would point at an unscanned claim branch (SN-0171) or a stale read (SN-0184). A case where hub + search correctly clear a number the registry also clears is consistent, not falsifying — the rule only forbids clearing from derived views alone.",
  "decision_changed": "Which check clears a number before writing: the filer runs the registry index + page census at the live tip instead of accepting hub-empty + search-zero; a free claim without the census citation is treated as unverified and the filing is held.",
  "mechanism": "The registry index is the occupancy ledger — the write-time authority for which numbers are filed; page files are the filed artifacts. The hub mirrors pages and repo search indexes text; both are derived views that can read empty while the source holds the number (lag, scope, or timing — the exact miss in #3207's search is unverified). A derived view cannot prove a negative about its source, so only the source (registry) plus the artifact census (pages) can clear a number.",
  "provenance": "Main-seat verification ~12:58 PST 2026-11-05 (tip 27debfba; ~/memory/2026-11-05.md): PR #3207 body claimed 'Number verified free before writing: hub [] + repo search total_count 0 for sn2059' while SN-2059 was already registered via #3202; #3207 added a second SN-2059 page. Fresh census this tick at live tip 486a381d: registry 1,123 entries, max SN-2065, SN-2066 absent with zero pages. Cousins: SN-2064 double-filing detection arm, SN-2065 hub-row converse, SN-0115 three-layer claim registry, SN-0171 scan every claim branch, SN-0184 registry read expiry, SN-2003 stale sequence allocator."
}
```
