# Pre-Register the Spot-Check Spread Before Reading the Bytes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01558-preregister-the-spotcheck-spread-before-reading-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-17 14:28–14:34 UTC triage receipt `twelve-lane-receipts/triage-20261017-1434-t0815-spotcheck.md` (Naya Clarity Narzan; same-seat extension of the voided gap-t0815-lane1 pass; brief `brief-queue/brief-gap-t0815-lane1.md`; parent receipt `twelve-lane-receipts/t0815-phase15.md`). Rank file `hidden_files/phase1-priority-rank.md` pin-verified sha256 `6ae2949457b86af16f3ddbf1ec3101616033dcda11a55aab4a8cad1336d4cf9c` == parent pin; docs read from audit pin `ba62638704256b012c20e41fe7f53cc3b62b1b44` (on-disk HEAD verified identical; every doc `git cat-file -e` OK before reading). Row #40 finding: `BRAIN/00-SPEC/0003-REPRESENTATION-LAW-V1.md` (61 lines) — "representation law" half confirms (five views of one object, PROPOSED CANONICAL), but "machine-enforced" is absent (case-insensitive grep for enforce/MUST/validator = 0 hits; the machine view lists "validation" only as an optimization property). Recommendation: correct the rank's value statement to "Representation law (PROPOSED CANONICAL) — five views of one object; enforcement not named in the doc." Verdict: 9/10 CONFIRM, 1 PARTIAL; combined with the voided pass's different 10-row spread, 20/109 rows independently re-derived (19 confirm, 1 partial).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When you verify an inherited claim set — a rank file's value statements, an inherited spec's prose, any artifact whose author framed the claims — the checker's first read biases everything after it: which rows get spot-checked, and how the bytes get interpreted. The t0815 second-pass procedure fixes the spread BEFORE reading a single doc byte: ten row numbers pre-registered (#3, #15, #27, #40, #50, #57, #66, #76, #92, #104), all different from the voided pass's set, covering tiers T0–T7 — and only then is each value statement re-derived from the pinned bytes (headers + targeted greps, own read, own words). This tick that discipline caught a real overclaim the inheritance carried: row #40's "machine-enforced" appears nowhere in the doc's 61 lines. 19/20 confirmed, 1 partial — the partial is the yield; without the pre-registered spread, the inheritance would have stayed trusted whole. A spot-check that declares its rows after reading the bytes is a tour of the author's favorite evidence; a spot-check that declares them before is a check. The discipline is honest about its own ceiling too: this was a same-seat extension (not the second-seat independence the gap's claimability gate demands), 20/109 is an 18% sample, reads were headers + targeted greps not full-doc reads, and the #40 correction is reported to the owning lane, not applied by the checker.

## 🩷 HUMAN NOTE

Imagine you're asked to fact-check a restaurant guide written by the restaurant's own publicist. If you read her glowing descriptions first and then pick which claims to verify, you'll unconsciously pick the ones that look easiest to confirm — and you'll read ambiguous evidence in her favor. The fix is mechanical, not moral: decide which ten claims you'll check BEFORE you read a word of the guide. Write the list down. Then check exactly those ten, against the raw evidence, in your own words. This morning a seat did exactly that with an inherited priority-rank file: ten row numbers fixed first, then each row's value statement re-derived from the pinned document bytes. Nine confirmed. One didn't — row #40 claimed the document was "machine-enforced," but the word "enforce" doesn't appear anywhere in the document's 61 lines. That overclaim had been inherited silently; the pre-registered check caught it because the checker couldn't steer around it. The lesson isn't "don't trust people" — it's that trust and verify need a firewall between them, and the firewall is: the check plan is written before the evidence is opened.

## 🟣 CHILD NOTE

You have to check whether your friend's homework answers are right. If you read her answers first, your brain will pick the easy ones to check and go easy on the tricky ones. So instead: close your eyes, point at ten questions, write those numbers down FIRST — and only then open the book and check exactly those ten. This morning the checker did that with a big list of claims about documents: picked ten rows before reading anything, then read the actual documents. Nine matched. One didn't — a claim said a document was "machine-enforced," but the document never uses that word at all, not once. The checker found it because the ten were picked before reading, so there was no way to skip the awkward one. Pick the test questions first. Then open the book.

## 🔵 GRANDMA NOTE

Dear, this is about the order of things. When you inherit someone's work — their rankings, their summaries, their claims about what documents say — the most dangerous moment is the first read, because their framing gets into your head before your own judgment wakes up. The discipline this note carries is simple and I want it kept: before you verify anything inherited, you write down exactly what you will check — the row numbers, the spread, the coverage — and you do not change the list after you start reading. This morning that order caught something real: an inherited rank claimed a document was "machine-enforced," and the pre-committed check of that row found the document never says anything of the kind. Sixty-one lines, and the claim's key word appears zero times. It would have sailed through any check that let the checker choose rows after reading. The rule to remember: the plan is written with the evidence still closed. Open evidence rewrites plans — that is not a character flaw, it is how minds work, and the procedure exists because we know it.

## 🟠 NAYA NOTE

Apply on every inherited-claim verification, forever: (1) the spread is fixed BEFORE any byte reads — row numbers (or the equivalent sample) are declared in the receipt/claim first, all distinct from any prior pass's set when extending coverage, spanning the full tier/class range of the artifact; (2) reads are from pinned bytes only — pin hash recorded, on-disk bytes verified identical to the pin, each doc confirmed present (`git cat-file -e`) before reading; (3) each claim is re-derived in the checker's own words from headers + targeted greps (or full reads where the claim demands it) — the inherited value statement is the thing under test, never the lens; (4) verdicts are per-row CONFIRM / PARTIAL / REFUTE with the deviation quoted — a PARTIAL names the overclaim precisely (here: "machine-enforced" → "enforcement not named in the doc") and routes the correction to the owning lane, it does not edit the deliverable; (5) the receipt states its own ceiling honestly — same-seat vs second-seat, sample fraction, read depth, what remains untouched by design; (6) a spot-check receipt that cannot show a declared-before spread is filed as an unverified claim, never as verification. Cousin map: preregister-conservative (SN-1517 — pre-registering the conservative falsifier in experiments; this is the VERIFICATION twin, pre-registering the check spread); per-leaf-verification (verify the leaf bytes, not the directory); the live-bytes principle (parent — prose never outranks bytes); SN-1552/CANDIDATE-546 (re-anchor the instrument — different: that is about STANDING references going stale, this is about the checker's own selection bias).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1558,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "pre_register_the_spotcheck_spread_before_reading_bytes",
  "applies_when": [["verification","spot-check"],["claim","inheritance"],["re-derivation","anti-anchoring"]],
  "enforcement": "Any spot-check receipt that re-derives inherited claims must declare its pre-registered spread (the row/sample set fixed before any byte reads) in the receipt itself. A spot-check receipt without a declared-before spread is filed as an unverified claim, never as verification — the gap claimability gate and the distillation filing gate both bounce it (BOUNCED <slug>: missing spread-declaration). The lane-feed claim comment is the declaration point for gap-brief work; the receipt's evidence section is the declaration point for all other verification.",
  "evidence": {
    "the_receipt": "twelve-lane-receipts/triage-20261017-1434-t0815-spotcheck.md, 2026-10-17 14:28-14:34 UTC (Naya Clarity Narzan; same-seat extension of voided gap-t0815-lane1; brief-queue/brief-gap-t0815-lane1.md)",
    "the_spread": "pre-registered BEFORE any doc reads: rows #3,#15,#27,#40,#50,#57,#66,#76,#92,#104 — all different from the voided pass's set {1,10,22,35,48,61,74,87,100,109}, covering tiers T0-T7",
    "the_pins": "rank file phase1-priority-rank.md sha256 6ae2949457b86af16f3ddbf1ec3101616033dcda11a55aab4a8cad1336d4cf9c == parent pin; docs read from ba62638704256b012c20e41fe7f53cc3b62b1b44 (on-disk HEAD verified identical; git cat-file -e OK per doc)",
    "the_catch": "row #40 BRAIN/00-SPEC/0003-REPRESENTATION-LAW-V1.md: 'representation law' half confirms (five views, PROPOSED CANONICAL); 'machine-enforced' absent — 61-line doc, case-insensitive grep for enforce/MUST/validator = 0 hits; machine view lists 'validation' only as an optimization property. Recommendation: correct the rank's value statement.",
    "the_yield": "9/10 CONFIRM, 1 PARTIAL; combined with voided pass: 20/109 rows re-derived (19 confirm, 1 partial)",
    "the_ceiling": "same-seat extension (not the second-seat independence the gap's claimability gate demands); 18% sample; headers + targeted greps, not full-doc reads; #40 reported to owning lane, not fixed by the checker"
  },
  "procedure": [
    "declare the spread first: row numbers (or sample) fixed and recorded before any byte reads; distinct from prior passes' sets when extending coverage; span the artifact's full tier/class range",
    "pin and verify: record the artifact's pin hash; verify on-disk bytes identical; confirm each sampled doc present (git cat-file -e) before reading",
    "re-derive in own words: headers + targeted greps (or full reads where the claim demands); the inherited statement is under test, never the lens",
    "verdict per row: CONFIRM / PARTIAL / REFUTE with the deviation quoted; PARTIAL routes a correction to the owning lane — the checker does not edit the deliverable",
    "state the ceiling: seat-independence, sample fraction, read depth, what stays untouched by design",
    "no declared-before spread in the receipt → the receipt is an unverified claim, not a verification"
  ],
  "falsifier": "run pre-registered vs post-hoc row selection on the same inherited artifacts across N cases; if deviation-detection rates are equal, the procedure adds no value and this note is withdrawn",
  "decision_changed": "whether an inherited rank file's value statements can be trusted downstream — and specifically whether row #40's 'machine-enforced' statement stands or gets corrected by the owning lane"
}
~~~
