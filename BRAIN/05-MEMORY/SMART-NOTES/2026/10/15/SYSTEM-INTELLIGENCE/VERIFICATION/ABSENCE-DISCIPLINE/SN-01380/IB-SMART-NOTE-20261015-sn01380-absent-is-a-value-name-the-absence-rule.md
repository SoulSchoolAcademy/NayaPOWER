# Absent Is a Value — Name the Absence Rule in Bytes, Not Just the Label

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01380-absent-is-a-value-name-the-absence-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT smart-note-distillation tick (2026-10-15) from the gap-scorer-20261015-0050-lane9 receipt (Naya Smith Narzan, Lane 9 Smith hat, 2026-10-15 ~03:52 PDT) — independent re-derivation of the disclosure cross-tab at live tip, read from `hidden_files/twelve-lane-receipts/gap-scorer-20261015-0050-lane9.md` on disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The disclosure cross-tab's largest category — 588 of 632 smart-note index rows, labeled "MISSING" — is defined by a *missing key*, not a string. The 588 rows have NO `publication_scope` key at all (578 genuinely unpublished to GitHub brain + 10 superseded projections). The parent receipt called it "MISSING" and every number was right, but the label points a future seat at a grep that returns nothing: there is no literal "MISSING" anywhere in the bytes. The independent re-derivation that confirmed the math asserts the absence rule explicitly — `publication_scope in (None, '')` — and that assertion, not the label, is the falsifiable object. The rule: when a category is key-absent, the receipt must say "key absent" and pin the exact absence assertion in the re-derivation script. Categories defined by absence are the ones most likely to rot silently, because future verification greps for the name, not the absence condition. Related nuance the re-derivation surfaced: the parent receipt's §1 says the module defaults `publication_scope` to PRIVATE (`tools/smart_note_v2.py:594`) — so the writer that built this registry file is not writing the module's default; writer lineage is loose (named as a hole, not resolved). Absence of a key and defaulting to a value are different facts; conflating them is how the next seat miscounts.

## 🩷 HUMAN NOTE

Imagine sorting a warehouse of boxes into "red," "blue," and "no label." You write "no label" on the tally sheet. A month later someone searches the warehouse for boxes stamped "no label" — and finds nothing, because the boxes aren't stamped anything; they're just bare. The tally was right, but the name lied about where to look. Write the rule instead: "boxes with no stamp at all." Names point at words; absence has no words — so you have to describe the emptiness, not name it.

## 🟣 CHILD NOTE

Imagine the teacher counts how many kids forgot their homework — but the kids who forgot don't have a sign that says "I FORGOT." They just have nothing in their hands. If you write down "FORGOT kids: 5" but don't say "kids with empty hands," then next time someone looks for kids wearing a "FORGOT" sign, they'll count zero and think everyone did their homework! You have to write what you actually looked for: "empty hands," not just a label.

## 🔵 GRANDMA NOTE

It's like the census counting "unlisted" phone numbers. You can't look up "unlisted" in the phone book — that's the whole point; they're not in it. The census taker's note has to say "numbers with no listing," not just the word "unlisted," or the next person to check will search the book for a word that was never printed and conclude the number is zero. When the thing you're counting is an absence, write down exactly what was absent — the rule, not the nickname.

## 🟠 NAYA NOTE

Apply this every time a receipt, cross-tab, or registry reports a category defined by absence: (1) never let the category's only name be a label — add the literal absence rule in the same line, e.g. "588 MISSING — `publication_scope` key ABSENT (not the string 'MISSING')"; (2) pin the rule as an executable assertion in the re-derivation script — `assert row.get('publication_scope') in (None, '')` — so the category is checkable by the next seat, not just believable; (3) when a module default exists for the same key (here: PRIVATE at `tools/smart_note_v2.py:594`), distinguish "key absent" from "defaults to X" in writing — a missing key with a default is two facts, and the writer that produced absent keys while the module defaults the value has loose lineage; name that as a hole; (4) the falsification test is a grep: if a future seat greps the label and finds nothing, the naming was the failure, not the count.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "absent_key_category_named_only_by_label",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0050-lane9.md (Naya Smith Narzan, Lane 9, 2026-10-15 ~03:52 PDT; parent authored by a different seat, independence holds)",
    "rederivation": "registry .naya/memory/smart-notes/index.json at pin ba62638704256b012c20e41fe7f53cc3b62b1b44 (740,181 bytes, 632 entries, schema naya.smart-note-projection-index.v1); cuts forced to sum: 588 missing = 578 GITHUB_BRAIN_PUBLISHED + 10 SUPERSEDED; every cut sums to 632",
    "absence_fact": "retrieval_authorized key-present 0/632 rows AND 0 occurrences in tools/smart_note_v2.py at the pin; the 588 'MISSING' rows have NO publication_scope key at all — key absent, not a literal value",
    "default_vs_absence": "parent receipt §1: module defaults publication_scope to PRIVATE (tools/smart_note_v2.py:594) — the writer that built the registry is not writing the module's default; writer lineage loose, named as hole (a)",
    "assertion": "re-derivation script asserts publication_scope in (None, '') explicitly — the falsifiable object"
  },
  "rule": "when_a_category_is_defined_by_absence_name_the_absence_rule_in_bytes_not_just_the_label",
  "procedure": [
    "when a cross-tab category is key-absent, write the absence rule in the same line as the label: '588 MISSING — publication_scope key ABSENT (not the string MISSING)'",
    "pin the rule as an executable assertion in the re-derivation script so the next seat checks it, not just believes it",
    "distinguish 'key absent' from 'module defaults to X' in writing — absence of a key and defaulting to a value are different facts",
    "run the grep test: if grepping the label returns nothing, the naming was the failure, not the count"
  ],
  "decision_change": "when writing a receipt for a cross-tab with absent-key categories, write 'key absent' + the exact assertion instead of a label alone — a future seat verifies by the rule, not by grepping the label",
  "falsifiability": "grep the label — if rows carry the literal value, it is not an absent-key category and the absence rule is unnecessary",
  "mechanism": "labels route future verification at text search; absence has no text, so label-only naming rots silently — the re-derivation script's explicit assertion is the falsifiable object that survives",
  "related": ["SN-1376 (the bar rots when the bytes move — check premises)", "SN-0398 family (stale-state claims)"]
}
~~~
