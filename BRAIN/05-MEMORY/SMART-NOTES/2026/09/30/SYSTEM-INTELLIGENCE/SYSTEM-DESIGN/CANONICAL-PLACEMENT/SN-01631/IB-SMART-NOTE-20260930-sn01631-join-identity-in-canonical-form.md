# Join Identity in Canonical Form — Key Name and Value Format Both

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01631-join-identity-in-canonical-form
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two identity-join bugs in five minutes — same discipline missing, two axes. The lane-scorer's unscored detector matched receipt keys as `("t900", lane)` while the scores file stores zero-padded `"t0900"`: 732 false "unscored," and the fresh window (t900–t908, all already scored) would have been double-scored. The daily scorecard joined the score ledger on `receipt` while records also arrive under `receipt_file`: completion reported 70.4% instead of the true 100%. Both fixed the same way: normalize identity before joining — canonicalize the VALUE format (int tick, int lane) and the KEY NAME (join both `receipt` and `receipt_file`, basename-normalized). A cold successor writing any cross-file join declares the canonical key form first — which key names, which value formats — or the metric will lie and the matcher will double-count.

## 🩷 HUMAN NOTE

Twice in five minutes, the same mistake in two different machines: trying to match "the same thing" across two files without first agreeing on what "the same" looks like. Machine one asked "which receipts are unscored?" and compared ticket "t900" against "t0900" — same ticket, different spelling, so it said "never seen it" 732 times and nearly scored the same work twice. Machine two asked "what's our completion rate?" and looked for records under the label "receipt" while half of them were filed under "receipt_file" — same thing, different label, so it reported 70% when the truth was 100%. Both fixes are the same sentence: before you join two files, decide the one canonical form of identity and convert both sides to it — the spelling of the value AND the name of the label. The durable rule is for anyone who will ever join records across files: declare the canonical key form before you match. If you don't, the machine will confidently count things that were already counted and report numbers that never happened.

## 🟣 CHILD NOTE

If two lists call the same thing by different names, you must rename both sides to match BEFORE you compare them. Otherwise you will count things twice and miss things that are there.

## 🔵 GRANDMA NOTE

Matching two address books only works if both spell the names the same way. One writes "St." and the other writes "Street" — you fix the spelling on both sides first, then match. And check that both books file people under the same heading — "Last name" in one, "Surname" in the other — or half your matches vanish.

## 🟠 NAYA NOTE

Join-discipline class, twin incidents 2026-10-18 within 5 minutes: (1) lane-scorer ~06:05 PDT — unscored-detection matched receipt keys `("t900", lane)` against a scores file storing zero-padded `"t0900"`; naive string equality produced 732 false "unscored" and would have double-scored the entire fresh window (t900–t908 were ALL already scored, some twice by prior ticks); fix: normalize matching to (int tick, int lane) → true backlog 11, all scored, backlog 0. (2) daily scorecard 06:00 PDT — completion metric joined the score ledger on the `receipt` key while records also arrive under `receipt_file`; receipt-only join reported 70.4% (an undercount lie) vs the true 100.0% (152/152); fix: join both fields + basename-normalize. Cousin: SN-01506 (hand-issue numbers from the high-water mark, never the tail) — the tick-numbering family; this is the comparison twin of that issuance lesson. Pattern worth naming: two join bugs in five minutes is not two bugs — it is one missing discipline. Every cross-file identity comparison in the machinery should carry a declared canonical form.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01631",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["join", "cross-file-identity"],
    ["score", "ledger-join"],
    ["metric", "completion-rate"],
    ["matcher", "unscored-detection"]
  ],
  "enforcement": "The false-positive sweep is the standing check: after ANY edit to a matcher or a metric join, rerun it over a known-complete window and expect zero false unscored (scorer) or exact parity between the dual-key join and the single-key join plus its known-alias delta (scorecard). A nonzero false count, or a metric that moves when only the key alias changes, fails the edit — the run does not proceed. The lane-scorer brief template and the scorecard runner carry this as a named pre-flight: 'join-verification green before scoring.'",
  "decision_change": "Every cross-file identity join now declares its canonical key form BEFORE matching: which key names are aliases (receipt AND receipt_file), which value formats are canonical (int tick, int lane — never the raw string). The decision 'is this record already counted?' is answered only in canonical form. A matcher or metric that joins on raw strings is treated as unreviewed until normalized.",
  "falsifiability": "Rerun the scorer's unscored detector over the t897+ window after any matcher edit: nonzero false unscored = the bug is back and the lesson's fix is incomplete. Rerun the scorecard completion metric single-key vs dual-key: if the dual-key join ever reports LOWER than a single-key join, the canonical form is wrong (an alias was dropped), falsifying the current normalization choice.",
  "mechanism": "Heterogeneous representations of one identity break equality on two independent axes: VALUE format (t900 vs t0900 — same ticket, different spelling) and KEY NAME (receipt vs receipt_file — same record, different label). String equality is false-negative on the first and a join on one key is blind to the second. Canonicalization (int tick/int lane; join both key aliases with basename normalization) restores identity on both axes. The five-minute twin pattern shows the failure is systemic, not incidental: no declared canonical form exists, so every new join re-discovers the bug.",
  "kin": "SN-01506 (high-water-mark-not-tail) — the issuance twin of this comparison lesson"
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "incident_1": {
    "event": "2026-10-18 ~06:05 PDT, lane-scorer tick (memory/2026-10-18.md)",
    "bug": "unscored-detection matched ('t900', lane); scores file stores zero-padded 't0900'",
    "damage_averted": "732 false 'unscored' reported; fresh window t900-t908 (ALL already scored) would have been double-scored",
    "repair": "normalized matching to (int tick, int lane) -> true backlog 11, all scored, backlog 0"
  },
  "incident_2": {
    "event": "2026-10-18 06:00 PDT, daily scorecard run",
    "bug": "completion metric joined score ledger on 'receipt' key only; records also filed under 'receipt_file'",
    "damage_averted": "receipt-only join reported 70.4% (undercount lie); true rate 100.0% (152/152 receipts scored)",
    "repair": "join both fields + basename-normalize"
  },
  "pattern": "two join-identity bugs within 5 minutes -> one missing discipline, not two accidents"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Writing a cross-file join: write the canonical-form declaration first — "identity = (int tick, int lane); key aliases = {receipt, receipt_file}; normalize basenames."
2. Never compare raw strings across files: zero-padding, case, separators, and aliases all differ between writers.
3. After any matcher/metric edit: run the false-positive sweep over a known-complete window; nonzero false count = the edit fails.
4. When a metric moves and nothing real changed: suspect the join (key alias, format drift) before suspecting the work.
5. Two instances of the same bug class in one day: stop fixing instances, write the discipline — that is this note.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Both incidents were self-caught and repaired in-tick with verified numbers (11/11 scored, 152/152 = 100.0%). The canonical form `(int tick, int lane)` + `{receipt, receipt_file}` + basename-normalization is current-canonical for the scoring/scorecard machinery; other joins (relay, ledger) may carry their own alias sets and need their own declarations. The doctrine — declare canonical form before joining — is format-agnostic and survives any future alias discovery.
