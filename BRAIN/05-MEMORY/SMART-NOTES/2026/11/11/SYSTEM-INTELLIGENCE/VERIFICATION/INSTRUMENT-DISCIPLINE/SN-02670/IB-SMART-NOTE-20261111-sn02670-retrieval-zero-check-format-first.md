**Intelligent Block:** IB-SMART-NOTE-20261111-sn02670-retrieval-zero-check-format-first
**Smart Note:** SN-2670
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 10:38 PST. Evidence: self-build cycle W46-DRILLBANK-REPAIR (goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261111-0938-w46-drillbank-repair.md, PR #3347); mechanism verified first-hand in nayapower-hub/tools/smart_note_v2.py:661,989,995. Number census this tick: main registry max SN-2669 (door batch 2, verified at tip 7edcf2e4; later main commits e844bd06 HTML-only and 4260257c SN-2091-only, registry 1,737); open PRs #3347 (drill-bank repair) and #3345 (Smart Mail draft) hold no Smart Note claims; branch counter max SN-2661 — SN-2670 is the next free number.

## ✦ IN A NUTSHELL

The cold-retrieve relevance probe stayed red because no ACTIVE note carries "compounding proof" in title or nutshell — but the two closest carriers could not be served at all. SN-2200's `## In a Nutshell` lacks the blank line the retriever regex requires, and SN-2150 has no nutshell heading. An audit of 106 essence pages found 66 conformant, 12 missing the blank line, and 28 with no nutshell heading. The retriever regex demands heading, then a blank line, then content; without the blank line there is no extractable nutshell, and the winner fails with WINNER_EXPLANATION_EMPTY. A zero-result probe therefore proves nothing about whether the intelligence exists — it may prove only that the pages are unservable. The cure is format normalization (or a live servable carrier), never weakening the test or re-pointing the query to dodge the format. The cycle refused the re-point on exactly this ground.

## 🩷 HUMAN NOTE

Shawn — the retrieval test came back empty, and it looked like the intelligence just wasn't there. It was there. The two closest notes couldn't be read at all, because their pages were formatted a hair off — one was missing a blank line after its heading, the other had no heading. The test reads the heading plus a blank line; without it, the note is invisible to the machine. So an empty result doesn't mean "nothing to find." It can mean "the pages need fixing first." We fix the pages. We never bend the test to get a pass.

## 🟣 CHILD NOTE

Imagine a library where every book has its most important sentence on a special page, and the librarian only looks at that page if there is an empty line right under the title. Some books forgot the empty line, so the librarian says "this book has nothing important" — even though the sentence is right there. The books aren't empty; the librarian just can't see them. The fix is to add the empty line to those books, not to change what the librarian is looking for.

## 🔵 GRANDMA NOTE

Dear, the machine reads our notes by looking for a heading with an empty line beneath it, the way you'd look for a chapter title with space under it before the words begin. Twelve of our pages forgot that little space, and twenty-eight more never had the heading at all — so when the machine went looking for the answer, it came back empty-handed and we nearly believed the answer didn't exist. It did exist; the pages just weren't readable. We tidy the pages. We never pretend the test is wrong to make ourselves feel better.

## 🟠 NAYA NOTE

The verified facts: (1) The self-build cycle W46-DRILLBANK-REPAIR (2026-11-11, PR #3347, pin 7edcf2e4) left the relevance boundary test red: zero ACTIVE notes carry "compounding proof" in title/nutshell; closest live carriers SN-2200 (score 66.84) and SN-2150 (66.66) were unservable. (2) The mechanism, verified first-hand in nayapower-hub/tools/smart_note_v2.py: line 661 (`_nutshell_text`) and line 989 use the regex `##(?:\s+[^\n]*)?IN A NUTSHELL\n\n(.+?)(?:\n\n##|$)` — heading, then a mandatory blank line, then content. Line 995 raises `WINNER_EXPLANATION_EMPTY` when no explanation extracts. A page whose nutshell heading is immediately followed by content matches nothing; a page with no nutshell heading matches nothing. (3) The cycle's essence-page audit counted 106 pages: 66 conformant, 12 missing the blank line, 28 with no nutshell heading. (4) The cycle refused a test re-point on this ground: re-pointing would fail on the nutshell format, and tuning the query to dodge that would be gaming the gate. The cure named in the cycle is a live servable carrier or nutshell-format normalization plus registry re-hash — a distillation/MEMORY-lane job, not a test edit. (5) Honest scope: the audit counts (66/12/28) are worker-reported in the cycle file; the regex and the raise are verified in code. The lesson does not depend on the exact counts — one non-conformant page is enough to hide a carrier. (6) This is not SN-0718 (shallow-clone range math) or SN-1813 (shallow-clone ancestry void): those are about git history truncation, not extractor format gates. It is adjacent to SN-01168 (extraction fidelity) and SN-1283 (extraction is verbatim), which concern what extraction must preserve; this note names the specific format gate and the misreading a zero result invites.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2670",
  "slug": "retrieval-zero-check-format-first",
  "title": "A zero-result retrieval probe can mean unservable format, not absent intelligence — audit format conformance before re-pointing",
  "observation": false,
  "applies_when": [["retrieval", "cold-retrieve"], ["retrieval", "zero-result-probe"], ["format", "nutshell-heading"], ["test", "relevance-boundary"]],
  "enforcement": "Before any re-point of a relevance query or any weakening of a relevance test after a zero/no-carrier result, run the nutshell-conformance audit over the candidate pages (the retriever regex ##(?:\\s+[^\\n]*)?IN A NUTSHELL\\n\\n must match) and record conformant vs non-conformant counts; a non-zero non-conformant count blocks the re-point until the pages are normalized or a conformant live carrier is produced. The cold-start probe's WINNER_EXPLANATION_EMPTY names unservable format, not absent intelligence, and must be read that way in the receipt.",
  "evidence": "Self-build cycle W46-DRILLBANK-REPAIR 2026-11-11 (goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261111-0938-w46-drillbank-repair.md; PR #3347): relevance test stayed red; closest carriers SN-2200 (66.84) / SN-2150 (66.66) unservable — SN-2200's ## In a Nutshell lacks the blank line the retriever regex requires, SN-2150 has no nutshell heading; essence audit 106 pages: 66 conformant, 12 missing blank line, 28 no heading. Mechanism verified first-hand in nayapower-hub/tools/smart_note_v2.py:661,989 (regex requires IN A NUTSHELL followed by a blank line) and :995 (WINNER_EXPLANATION_EMPTY raise). Re-point refused in the cycle.",
  "decision_change": "A relevance probe returning no servable carrier must trigger a format-conformance audit before any conclusion that the intelligence is absent, before re-pointing the query, and before weakening the test. The next decision this changes is the relevance-boundary cure: normalize nutshell format (or produce a conformant live carrier) instead of re-pointing the query.",
  "falsifier": "Refuted if a page with a conformant nutshell (heading + blank line + content) still raises WINNER_EXPLANATION_EMPTY on retrieval — then the blank line is not the gate; or if adding the blank line to the 12 non-conformant pages does not make them extractable. Bounded: covers the smart_note_v2 retriever regex only; other extractors may have different format requirements.",
  "cousins": ["SN-01168 (extraction fidelity — mechanical assertion about extraction; this note names the specific blank-line format gate and the zero-result misreading)", "SN-1283 (extraction is verbatim — what extraction must preserve; this note is about when extraction finds nothing at all)", "SN-0718 (shallow-clone range math — different instrument, same shape: a tool silently returning a wrong empty answer because of an unseen precondition)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
