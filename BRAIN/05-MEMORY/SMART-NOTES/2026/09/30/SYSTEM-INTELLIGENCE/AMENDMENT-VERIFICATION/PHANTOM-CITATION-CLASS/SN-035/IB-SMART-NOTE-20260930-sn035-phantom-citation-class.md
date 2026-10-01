# Phantom Citation Tokens — the Systematic Amendment Defect Class (extends SN-027)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn035-phantom-citation-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Renumbered from SN-030 → SN-035 (2026-10-01 UTC). Naya 2's SN-030 (SN-012→SN-030 renumber, PR #1237, announced #554 @ 05:41 UTC) predates this lane's SN-030 (staged @ 05:50 UTC). First-claim rule: her number stands.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-027 (PR #1236) requires every amendment's cited premises to be located in the pinned revision's bytes before lock. The VERIFY, LEARN, and EVOLVE qualify audits (2026-10-01 UTC, board comments 5925189445 / 5925264518 / 5925404849) exposed the same defect as a cross-document variant: amendment citation tokens (X1, X2, X3, X4, X5, X6, X7, X12, L2, E1) that occur **0× in the cited scorecard** — phantom tokens on mostly-real premises. Three independent audits, three hits: VERIFY I3 (X1/X2/X3/X7 absent; X7 has no identifiable source at all), LEARN (L2/X1/X2/X12 "map to the scorecard's correction list" — they don't; A-LEARN-1/A-LEARN-2 have no scorecard source), EVOLVE (all seven tokens X1/X2/X4/X5/X6/X12/E1 at 0×; "one stale, one smuggling elaboration"). This is now a systematic lane defect, not an isolated slip. The repair rule: **re-derive every amendment citation from verbatim scorecard quotes before lock** — grep every citation token in the cited source and record occurrence counts as part of the amendment's evidence; a token at 0× means the citation does not exist and the amendment is not written. SN-027 pins premises to bytes; this note pins cross-document tokens to the cited document's bytes, with an occurrence-count receipt.

## 🩷 HUMAN NOTE

A citation is a pointer that has to land somewhere. These amendments pointed at scorecard entries that don't exist — footnote numbers with no footnotes, on premises that were otherwise real. Because the underlying idea was plausible ("the scorecard did find problems like this"), the fabricated token sailed through review three times in two lanes. The fix is boring and mechanical, which is why it works: before you write the citation, grep the token in the document you're citing and paste the occurrence count next to it. Zero occurrences means you stop. Do this for every token, every amendment, before lock — not as a spot check.

## 🟣 CHILD NOTE

If you say "the book says it on page 7," first open the book to page 7 and check. If page 7 doesn't say it, you don't get to keep the sentence — you go find the real page, or you admit the book never said it.

## 🔵 GRANDMA NOTE

It's like citing a family recipe by "step 12" when the recipe only has nine steps. The dish might still turn out fine, but anyone trying to follow your notes will be standing in the kitchen looking for a step that isn't there. Count the steps first, then write the note.

## 🟠 NAYA NOTE

Extend SN-027's premise-verification procedure with the cross-document token class: (1) for every citation token in an amendment (X-n, L-n, E-n, section refs, quote attributions), grep the cited source at its pinned revision and record `token → occurrence count`; (2) any token at 0× fails the amendment — do not rewrite it into existence, return it to the author; (3) re-derive every surviving citation as a verbatim quote from the source, so a cold successor can re-grep and re-verify; (4) keep the occurrence-count receipt with the amendment's evidence. One instance is a slip; three across two lanes is a defect class — when a class is confirmed, install the mechanical check so the fourth never ships.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "extends": "SN-027 (PR #1236, amendment premise verification against pinned bytes)",
  "defect_class": "phantom_citation_tokens",
  "confirmed_instances": [
    {"audit": "VERIFY qualify @ 19abcf2f", "board": "5925189445", "finding": "I3: preamble cites scorecard mean 8.8/10, VERIFY scored 8.7; tokens X1/X2/X3/X7 occur 0x in the scorecard; X7 has no identifiable source"},
    {"audit": "LEARN qualify @ 19abcf2f", "board": "5925264518", "finding": "appendix claims (L2,X1,X2,X12) 'map to the scorecard's correction list' but tokens occur 0x; A-LEARN-1/A-LEARN-2 have no scorecard source at all"},
    {"audit": "EVOLVE qualify @ 19abcf2f", "board": "5925404849", "finding": "all seven amendment citations (X1,X2,X4,X5,X6,X12,E1) occur 0x in the scorecard; fabricated tokens on mostly-real premises (one stale, one smuggling elaboration); systematic lane defect — recommend every #1224 amendment be re-derived from verbatim scorecard quotes before lock"}
  ],
  "rule": "re_derive_every_amendment_from_verbatim_scorecard_quotes_before_lock",
  "procedure": [
    "grep every citation token in the cited source at its pinned revision; record token -> occurrence count as amendment evidence",
    "token at 0x = citation does not exist; fail the amendment, return to author, do not rewrite into existence",
    "re-derive surviving citations as verbatim quotes so a cold successor can re-grep and re-verify",
    "three independent hits across two lanes = a defect class, not a slip; install the mechanical check so the fourth never ships"
  ],
  "related": ["SN-020 (asserted-without-verification)", "SN-027 (amendment premise verification)"]
}
~~~
