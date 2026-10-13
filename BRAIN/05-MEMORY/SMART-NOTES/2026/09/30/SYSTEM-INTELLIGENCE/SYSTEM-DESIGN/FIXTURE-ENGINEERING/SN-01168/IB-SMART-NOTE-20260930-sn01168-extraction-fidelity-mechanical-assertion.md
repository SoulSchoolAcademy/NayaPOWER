# Extraction fidelity is a mechanical assertion

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1168-extraction-fidelity-mechanical-assertion
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:38 PDT distillation tick (2026-10-13) from the t0593-lane10 receipt (`hidden_files/twelve-lane-receipts/t0593-lane10.md`, Naya Librarian, mirror lesson, self 9.0/10), read from local files.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Building a 50-doc fixture corpus, the lane's "verbatim" extractions weren't verbatim: the instrument's own `sentences()` splitter splits on hyphens and newlines, so "Self-validation is…" and the B2 parenthetical fractured across sentence boundaries. Byte-comparing each extraction span against the source document's actual `sentences()` output caught two defects her eyes had approved — DA2's source bytes carry a literal newline mid-sentence (preserved verbatim), and DC1's extraction string had dropped an apostrophe (byte-compared against source, corrected). The rule: extraction fidelity is a mechanical assertion — every extraction span must satisfy span ∈ doc bytes AND span == source sentences() output — and it belongs in code (`build_fixture_checks`), not in design-time intention. The check compares bytes, not memory of what the sentence "says."

## 🩷 HUMAN NOTE

She was copying "exact quotes" into her test set — and her quotes were wrong in ways her eyes couldn't see. One source sentence had an invisible line break in the middle of it; another lost an apostrophe. The machine she trusted to split sentences split them in places a human never would (on hyphens, on line breaks). The fix: don't trust your eyes or your memory of what the sentence says — write a check that compares the actual bytes, character by character, against the source. Two catches, fixed before anything was sealed. That's the standard: fidelity lives in an assertion, not in your good intentions.

## 🟣 CHILD NOTE

Imagine you're copying lines from a book for a spelling test. You think you copied them perfectly — but the page had a line that wrapped in a weird spot, and you accidentally dropped a letter. Your eyes say "looks right." The only way to be sure is to put your copy next to the book and check every single letter, one by one. That's what she did with the computer's help: a byte-by-byte comparison against the real source. It found two mistakes her eyes had missed. The lesson: "I was careful" is not a check. The computer comparing bytes IS the check.

## 🔵 GRANDMA NOTE

It's like proofreading a recipe you've copied by hand — you read it over and it looks fine, but you've dropped a word somewhere without noticing. The reliable way is to have someone read the original out loud while you follow your copy word for word. She did the computer version of that: every copied sentence was matched character-by-character against the original document. Two slips caught — one invisible line break, one missing apostrophe — before anything was finalized. Careful intentions don't catch errors; mechanical checking does.

## 🟠 NAYA NOTE

Apply this every time you build fixtures with extracted claims: (1) every extraction span is asserted in code, never claimed in prose: `span ∈ doc bytes` AND `span == source sentences() output` — the source's real splitter output, not your memory of sentence boundaries; (2) split defensively: `sentences()`-style splitters fracture on hyphens and newlines, so mid-sentence newlines are preserved verbatim, not normalized away; (3) catch them in `build_fixture_checks` at fixture-build time — pre-seal, not receipt-time; (4) when your eyes approve and the bytes disagree, the bytes win — twice this tick (DA2's literal newline, DC1's dropped apostrophe); (5) ship the assertion with the fixture set so every future regeneration re-proves fidelity. Cousin map: SN-1160 (read the gate before writing the body — here, read the splitter before extracting from it); the t0591 Herald recompute-before-reading rule (bytes over memory, same family).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "extraction_fidelity_claimed_not_asserted",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0593-lane10.md — Naya Librarian, t0593 lane 10 (mirror, third fixture hard-class, self 9.0/10)",
    "fixture_builder": "fixture_t0593.py, sha16 0f83599db111ba8b — fresh 50-doc corpus; in-code integrity via build_fixture_checks (≥48 docs, zero t0432 whole-doc reuse, extraction spans verbatim in docs, hard-class discipline n_claims ≥ 1 ∧ fired == 0 vs all 3 tasks)",
    "two_catches": "DA2's source bytes carry a literal newline mid-sentence (preserved verbatim); DC1's extraction string dropped an apostrophe (byte-compared against source, corrected) — both fixed pre-seal",
    "root_cause": "the instrument's own splitter almost made her a planter — sentences() splits on hyphens and newlines, so \"Self-validation is…\" and the B2 parenthetical fractured across sentence boundaries; fidelity check compared bytes against the source doc's actual sentences() output, not memory of what the sentence \"says\"",
    "carrier": "the assertion now lives in build_fixture_checks; the sentences()-equality check joins the fixture assertions next fixture"
  },
  "rule": "extraction_spans_must_satisfy_span_in_doc_bytes_and_span_equals_source_splitter_output_in_code",
  "procedure": [
    "assert every extraction span in code: span ∈ doc bytes AND span == source sentences() output",
    "treat mid-sentence newlines and hyphen-splits as verbatim content — never normalize away what the splitter preserves",
    "run the fidelity assertion at fixture-build time (build_fixture_checks), pre-seal",
    "when eyes approve and bytes disagree, bytes win — record both catches, fix, re-run",
    "ship the assertion with the fixture set so regeneration re-proves fidelity"
  ],
  "related": ["SN-1160 (read the gate before writing the body — read the splitter before extracting from it)"]
}
~~~
