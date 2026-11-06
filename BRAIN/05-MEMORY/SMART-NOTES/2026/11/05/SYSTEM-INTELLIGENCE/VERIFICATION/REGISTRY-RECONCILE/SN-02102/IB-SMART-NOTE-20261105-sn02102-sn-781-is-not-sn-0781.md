# INTELLIGENT BLOCK — SN-2102

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02102-sn-781-is-not-sn-0781
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** PR #3245 ("Distillation oct-2 landing", merged 2026-11-06T04:05:16Z by nayanet[bot], squash fee04460) claimed "SN-0781 exists twice in the registry". PR #3246 ("Distillation oct-3 landing", merged 04:12:35Z, squash ed455b73) corrected it within seven minutes: SN-781 ("The Relay Opener Recuses From Review") is a DISTINCT note from SN-0781 ("Scorecard Must Run the Gate"). Main-seat verification at ed455b73 (registry index, 1,215 entries): SN-781 x1 RETIRED by SN-2170; SN-0781 x1 RETIRED by SN-2157 — separate entries, separate titles, separate retiring essences. Eighth bot self-cure pair. The 2026-10-13 collision-registry draft read this backwards, listing the relay-opener note as a "stale variant" of SN-0781; it was never a variant, it was the other note. Number for this note, SN-2102, verified free by live tree+registry census at tip 7f70bc79 (04:32:16Z): absent from the main tree, the branch tree, and the registry (max 2174 at ed455b73; oct-4/5 essences SN-2175–SN-2201 in .naya/capture), and no open PR claims it (#3251 is a learning-event report, 1 file). Chosen as a gap below the campaign frontier (oct-5 took SN-2190–SN-2201) so it survives the staging-to-landing window SN-2077 describes. Branch counter reconciled: it ended at 2099 while the live max is 2201 (lag 102).

## ✦ IN A NUTSHELL

SN-781 and SN-0781 are two different notes, not one note written twice. The registry keys on the exact string, so zero-padding creates a distinct identity: "781" and "0781" are different keys that were allocated to different notes at different times, and both stand. The adjudication rule: compare exact strings first, then content — a padded variant with different content is a different note, never a duplicate to merge or retire. The contrast that keeps the rule honest: branch SN-02099 vs main SN-2099 IS a true collision — one numeric slot claimed twice because the branch counter lags the registry — and there the branch claim renumbers (SN-2077). Same digits, different content, different verdicts: the registry decides, not the shape of the number. And the boundary with SN-1631: normalize zero-padded ids at JOINS across representations, but never collapse distinct registry keys — a join canonicalizes, the registry does not.

## 🩷 HUMAN NOTE

Shawn — a bot claimed one of our notes existed twice because its number looked like a padded copy of another number: SN-0781 vs SN-781. A second bot corrected it seven minutes later, and the registry proves the correction: they are two different notes with different titles, retired by two different essences. The number's shape fooled the first check; the content tells the truth. From here on, when two note numbers differ only by a leading zero, we check the content before calling it a duplicate — different content means two notes, full stop. The one exception is the branch counter falling behind main: when the branch files a number main already took, that IS a collision and the branch renumbers. The registry is the judge of which case it is.

## 🟣 CHILD NOTE

Imagine two kids in school: one is named "781" and the other is named "0781". They look almost the same on paper, but they are two different kids with different stories. You would never say one of them is a copy of the other — you would look at their faces. Note numbers are like that: if the words inside are different, they are two different notes, even if the numbers look like twins. The only time it is really a double is when the branch writes a number main already used — then it is the same seat taken twice, and the branch picks a new seat.

## 🔵 GRANDMA NOTE

Dear, it's like two library cards: one says 781 and one says 0781. The numbers look like the same card with an extra zero, but they belong to two different books with different titles on different shelves. You don't throw one away for being a copy — you read the title first. If the titles are different, keep both cards. The only real double is when two people try to check out the very same book — then the second one waits and picks another. Read the title, not just the number.

## 🟠 NAYA NOTE

For every seat adjudicating an apparent SN-number duplicate, and for every retirement pass: (1) compare SN IDs as exact strings — "SN-781" and "SN-0781" are different keys, and the registry holds both as separate entries; (2) compare content — if the two entries carry different titles and different retiring essences, they are two notes: keep both, retire each under its own essence, and never merge one into the other; (3) check the registry first — if both strings are registry keys with separate provenance, the duplicate claim is false on its face, and the claimer corrects the claim (as #3246 corrected #3245); (4) if only one string is a registry key and the other is a branch-only claim on the same numeric value, it is a true collision from a lagging branch counter — first claim stands, renumber the branch claim (SN-2077); (5) correct the 2026-10-13 collision-registry draft entry that listed the relay-opener note as a "stale variant" of SN-0781 — it is SN-781, a distinct note. Do not apply SN-1631's join normalization here: normalization belongs at joins across representations, never to registry keys. When taking a number while the distillation campaign is landing batches every few minutes, prefer a verified-free gap below the moving frontier over max-plus-one — a gap cannot be taken by the next sequential landing.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-781-is-not-sn-0781",
  "sn": "SN-2102",
  "title": "Zero-Padding Is an Identity, Not a Rendering — SN-781 Is Not SN-0781",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["registry", "numbering-collision", "distillation", "retirement", "collision-adjudication"],
  "enforcement": "Collision adjudication must compare SN IDs as exact strings AND compare content before declaring a duplicate: if both strings are registry keys with different titles and different retiring essences, the duplicate claim is rejected and the claimer corrects it (PR #3246 correcting PR #3245 is the template). The registry duplicate-ID scan counts only exact-string matches; a retirement pass that would retire SN-781 as a duplicate of SN-0781 fails closed. The 2026-10-13 collision-registry draft entry for SN-0781 is corrected to record SN-781 as a distinct note, not acted on as a collision. SN-1631 join normalization must never be applied to registry keys.",
  "falsifier": "A registry entry showing SN-781 and SN-0781 sharing one entry, one content blob, or one retiring essence would collapse the rule — they would be one note in two forms, not two notes. A future ingestion run that merges the two keys into one registry entry would falsify it the same way. Conversely, a third padded-variant pair found standing as two registry entries would strengthen it.",
  "decision_changed": "Whether an apparent SN-number duplicate is merged, retired, or kept: the adjudicator now compares exact strings first and then content, so a padded variant with different content is kept as a distinct note instead of being merged away — and the retirement pass retires each under its own essence (SN-781 by SN-2170, SN-0781 by SN-2157) instead of retiring one as a duplicate of the other. The same adjudication now also corrects the 2026-10-13 draft's misclassification instead of acting on it.",
  "mechanism": "The registry keys on the exact SN string, and its allocation sequence issued '781' and '0781' as two separate keys at different times to two different notes with different titles; nothing in the ingestion or registry path normalizes zero-padding, so the two keys never collapse. A duplicate claim arises only when a reader normalizes numerically (as PR #3245 did) and mistakes the shared digits for a shared note. The branch counter is a separate allocator that renders its numbers zero-padded ('SN-02099' for 2099) and lags the registry, so a branch claim on a numeric value main already holds is a true collision of one slot claimed twice — the opposite case, resolved by renumbering the branch claim (SN-2077). SN-1631's normalization rule governs joins across representations, where a canonical form must be named; the registry itself is not a join, so its keys stay exact.",
  "provenance": "PR #3245 body claimed 'SN-0781 exists twice in the registry' (merged 2026-11-06T04:05:16Z, squash fee04460); PR #3246 body corrected it (merged 04:12:35Z, squash ed455b73): SN-781 'The Relay Opener Recuses From Review' is DISTINCT from SN-0781 'Scorecard Must Run the Gate'. Main-seat verification at ed455b73 (registry index, 1,215 entries): SN-781 x1 RETIRED by SN-2170; SN-0781 x1 RETIRED by SN-2157. Eighth bot self-cure pair. Contrast case: branch SN-02099 'INDEX_CORRUPT:PATH_ESCAPE' (staged 19:38 PST, commit 38f03de8) vs main SN-2099 page 'Who I Am' (direct push a8b6fb48, 04:10:03Z) — 21st branch-vs-main collision, branch renumbers (SN-2077). Boundary cousin: SN-1631 (normalize zero-padded ids at joins) — this note states where that rule stops. Collision-registry draft: hidden_files/collision-registry-DRAFT-20261013.md ('1 true collision — SN-0781'). Number census for this note at live tip 7f70bc79 (04:32:16Z): SN-2102 absent from main tree, branch tree, registry index, and open PRs; gap below the oct-5 frontier (SN-2190–SN-2201)."
}
```
