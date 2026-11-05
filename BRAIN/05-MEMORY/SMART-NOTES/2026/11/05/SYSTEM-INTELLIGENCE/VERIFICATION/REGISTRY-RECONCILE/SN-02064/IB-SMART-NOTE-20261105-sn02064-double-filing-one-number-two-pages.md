# INTELLIGENT BLOCK — SN-2064

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02064-double-filing-one-number-two-pages
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director pass 12:08 PST 2026-11-05 (shared-state merge_watch_latest; ~/memory/2026-11-05.md) named NEW FAILURE MODE DOUBLE-FILING-VIA-DIRECT-PUSH-PLUS-PR on commit 82fc1c6e (SN-2060 page direct-pushed, ULTIMATE-AI-TEAM). Main-seat verification ~12:26 PST (tip 1ecfd925) confirmed SN-2060 has TWO pages on main — the direct-push ULTIMATE-AI-TEAM page and PR #3204's MULTI-AGENT page — the same pattern as SN-2055 (two pages: #3196 PRODUCT/SMART-ACCESS + #3197 SYSTEM/marketplace). Fresh tree census this tick at tip 27debfba: SN-2059 x2 pages, SN-2060 x2 pages, SN-2061 x2 pages; the registry holds each number once.

## ✦ IN A NUTSHELL

One Smart Note number, two different pages on main. A direct push filed the SN-2060 page under ULTIMATE-AI-TEAM (commit 82fc1c6e); PR #3204 then filed SN-2060 again under MULTI-AGENT — and both landed, because no check ever lists all the paths for one number. The registry holds SN-2060 once, so a registry-once check calls the filing clean while the tree holds it twice. A fresh census at tip 27debfba shows the pattern is not a one-off: SN-2059, SN-2060, and SN-2061 each have two pages on main. The durable rule: **a filing is not landed until a page-path census for its number returns exactly one path** — registry-once is necessary and not sufficient, and a direct-push page for a number blocks any PR filing of the same number until the push is reconciled.

## 🩷 HUMAN NOTE

Shawn — the same note number now lives in two places on main. One copy arrived by direct push, another by a pull request, in different folders — and both landed because every check looked at the number in the registry (where it appears once) and nobody listed the actual files (where it appears twice). Three numbers are double-filed now, not one. From here on, calling a filing "landed" means counting the files for that number on main, not just checking the registry. If the count is two, it isn't landed — it's a double-file waiting for a renumber or a cure.

## 🟣 CHILD NOTE

Imagine a library where every book gets a number, and the catalog says each number appears once. But two different shelves each hold a different book with the same number on the spine — because one person put a book on the shelf directly, and another person filed a second book through the front desk, and nobody ever walked the shelves to count. The catalog says "one," the shelves say "two." The new rule: before you say a book is shelved, walk the shelves and count how many books carry that number. If it's two, it's not shelved — it's doubled.

## 🔵 GRANDMA NOTE

Dear, it's like a recipe box where every recipe has a number, and the index says each number appears once. But two different cards with the same number got filed in two different sections — one slipped in by hand, one through the proper drawer — and the index never noticed because it only counts numbers, not cards. Three recipes are doubled now. From now on, before anyone calls a recipe filed, they fan through the box and count the cards with that number. Two cards, one number — that's not filed, that's a mix-up to fix.

## 🟠 NAYA NOTE

For every seat, the dock, and merge watch: a registry-once check never proves a clean filing. Before any filing is called landed, census all page files matching the SN number on main (git tree listing for the number) and require exactly one path. If the census returns two or more paths, the filing is a double-file: hold it, renumber the second filing, or cure the duplicate — never let it stand on a registry-once reading. A direct-push page for a number blocks a PR filing of the same number until the push is reconciled; the PR author checks the tree, not just the registry, before filing. When you verify someone else's landing, quote the page count, not the registry count.

## 🟢 MACHINE NOTE

```json
{
  "slug": "double-filing-one-number-two-pages",
  "sn": "SN-2064",
  "title": "One Number, Two Pages — A Direct Push Plus a PR Filing Double-Files the Note",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["filing", "registry", "collision", "direct-push", "verification"],
  "enforcement": "The landing verification step must census all page files matching the SN number on main (git tree listing) before calling a filing landed; more than one path fails the landing and forces renumber or cure, and a registry-once check alone is never accepted as proof of a clean filing.",
  "falsifier": "A same-number direct-push plus PR pair that lands as exactly one page on main (for example the PR overwriting the pushed path) would bound this lesson to path-divergent pairs; a registry check that counts pages per number and fails on two would show the detector already exists and this lesson is the procedure for using it.",
  "decision_changed": "Whether a filing is called landed: the verifier now censuses page paths for the number instead of trusting registry-once, and a direct-push page for a number holds any PR filing of the same number until the push is reconciled — the double-file is cured by renumbering, not by trusting the registry.",
  "mechanism": "The registry's uniqueness is keyed on the SN number (one ACTIVE entry per number) while the filesystem has no uniqueness constraint across different category paths, so a direct push writing path A and a PR writing path B each pass their own check; no check ever lists all paths for the number, so the registry says 'once' while the tree says 'twice.'",
  "provenance": "Director pass 12:08 PST 2026-11-05 (shared-state merge_watch_latest; ~/memory/2026-11-05.md) named NEW FAILURE MODE DOUBLE-FILING-VIA-DIRECT-PUSH-PLUS-PR on commit 82fc1c6e (SN-2060 ULTIMATE-AI-TEAM page, direct push). Main-seat verification ~12:26 PST (tip 1ecfd925) confirmed SN-2060 two pages on main (ULTIMATE-AI-TEAM + PR #3204 MULTI-AGENT) and the same pattern for SN-2055 (#3196 PRODUCT/SMART-ACCESS + #3197 SYSTEM/marketplace). Fresh tree census this tick at tip 27debfba: SN-2059 x2 pages, SN-2060 x2 pages, SN-2061 x2 pages; registry holds each once. Cousins: SN-2053 bulk import bypasses filing path, SN-0115 three-layer collision registry, SN-0151 claim registry write first — none names the two-pages-one-number double-file."
}
```
