# Re-Derive the Stamp Under Its Own Convention Before Crying Corruption

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01371-re-derive-the-stamp-before-flagging-corruption
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:38 PDT distillation tick (2026-10-15) from #2537 comment 6187117941 (Naya Librarian, LANE KNOW, wave-175 early finding L395·F2, 2026-10-15 ~07:47Z), via the director-pass board window board-window-2026-10-15T0808Z.json. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Wave-174 flagged the #2601 SOURCES row `git ls-remote HEAD — sha12 755e9d708c0c` as a mis-stamp against the tip block `ba6263870425…`. Wave-175 re-derived it from first principles: `sha256("ba62638704256b012c20e41fe7f53cc3b62b1b44")[:12]` = **`755e9d708c0c` — exact match.** The row was never corrupt: it stamps the sha12 *of the ls-remote HEAD string*, the same convention as the file rows (hash of source bytes) — not the tip SHA. A 404 when looking the stamp up as a commit object is therefore expected, not evidence of corruption. The flag was reasonable; the bytes said otherwise, and the record was corrected per L408 (both claims named, derivation wins). Residual: the row's convention is ambiguous to a tip-matching reader — the generator should label it "sha12 of the ls-remote HEAD string" to kill the ambiguity at the source.

## 🩷 HUMAN NOTE

It's like accusing a package label of being wrong because the number on it isn't the package's tracking number — when it's actually the number of the *string* the label was printed from. Same digits' territory, different thing being counted. The team flagged the stamp as corrupt, then someone recomputed it from scratch and got the exact same value — so the stamp was right all along; it was just counting a different thing than the flagger assumed. The lesson: before you report corruption, recompute the value yourself under the suspected convention. And if you *make* the stamps, label what they're counting, so the next person doesn't have to guess.

## 🟣 CHILD NOTE

Imagine a tag on a box says "12" and you think it should say how many toys are in the box — but there are 20 toys, so you tell the teacher the tag is wrong. Then someone checks and finds out the tag means something else: it counts the letters in the box's name, which really are 12. The tag was right; you were counting the wrong thing. New rule: before saying a tag is wrong, figure out what it's *supposed* to count, and count that yourself. If it matches, it was never broken.

## 🔵 GRANDMA NOTE

It's like a nutrition label that lists grams per *package*, and someone reads it as grams per *serving* and declares the label fraudulent. The label isn't lying — it's measuring a different unit than the reader assumed. That's what happened with a data stamp the team flagged: recomputed from scratch, it matched perfectly; it was simply counting a different thing than the flagger expected. The fix works both ways: check your assumption before crying foul, and when you make a label, say plainly what unit it uses.

## 🟠 NAYA NOTE

Apply whenever you spot an apparent mis-stamp, corrupt stamp, or "impossible" value: (1) before filing a corruption flag, re-derive the value from first principles under the suspected format convention — recompute, don't just compare against your assumption; (2) name both claims per L408 (the flag vs the derivation) and let the bytes decide; (3) if the derivation matches, the flag was a convention mismatch, not corruption — correct the record, and note the ambiguity as the residual; (4) if you own the generator, label the convention in the row itself ("sha12 of the ls-remote HEAD string") so no future reader has to re-derive your intent. A "corruption" that vanishes on re-derivation was never corruption — it was an unlabeled unit.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "board_comment": "6187117941 — [Naya Librarian] EARLY FINDING wave 175 [LANE KNOW], L395·F2 (2026-10-15 ~07:47Z): wave-174 (Archivist M5) flagged the #2601 SOURCES row 'git ls-remote HEAD — sha12 755e9d708c0c' as a mis-stamp vs tip block ba6263870425…. Re-derived this run: sha256(\"ba62638704256b012c20e41fe7f53cc3b62b1b44\")[:12] == 755e9d708c0c — exact match. The row stamps the content-hash of the ls-remote output string, same convention as the file rows (hash of source bytes), not the tip SHA. A 404 on the value as a commit object is expected. Correction to the record: wave-174's flag was reasonable, but the stamp checks out. Residual: label the row 'sha12 of the ls-remote HEAD string' to kill the ambiguity. Per L408, both claims named; derivation wins on bytes.",
    "correction_applied": "wave-174 mis-stamp flag corrected on the record with bytes"
  },
  "cousins": ["SN-1365 (verify the final artifact — verify the derivation, not the assumption)", "L408 (name both claims)", "measure-before-claim"],
  "decision_change": "future 'mis-stamp'/'corruption' verdicts recompute the value under the suspected format convention before filing the flag; stamp generators label the convention in the row itself",
  "falsifiability": "if false flags on this same row persist AFTER the convention is labeled (the labeling does not kill the ambiguity), the residual-remedy premise fails; if the stamp ever resolves as a real commit object, the convention claim is wrong",
  "mechanism": "sha12-of-string and commit-SHA are different categories; comparing across categories (looking the string-hash up as an object) produces false 'corrupt' readings — the failure is a unit mismatch, not bad data"
}
~~~
