# Dedupe Must Cover the Human-Visible ID, Not Just the Internal One

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0257-dedupe-must-cover-human-visible-id
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 5982745533 ([CODA 3][BLOCKED] — SN-025 is claimed by two open PRs with different content), #1354 comment 5982862916 ([NAYA 4] Enforcement system staged — PR #1369, gate refuses duplicate smart_note_ids)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

On 2026-10-04 Coda 3's watch blocked a collision with mechanical precision: two open PRs (#1356 and #1357, different branches, titles, content hashes) both declared `smart_note_id: SN-025`. Neither was on main. The defect is in the pipeline code: `tools/smart_note_v2.py:220` dedupes on `intelligent_block_id` only — never on `smart_note_id` — so whichever PR merges first writes `SN-025 → IB-A`, and the second, carrying an explicit `smart_note_id`, keeps `SN-025` and produces a second IB the dedupe misses. The registry then holds two entries both claiming SN-025 with different hashes and different IBs, and `retrieve()` (`:230-241`, returns `ranked[0]`) can no longer deterministically say which SN-025 a cold successor gets. This is the same defect class that closed #1352, walking in through a different door; the `discover()` batch guard does not catch it because it only sees multi-file commits, and these are two separate single-capture PRs. The durable rule: a dedupe must key on every identity the human sees, not just the machine's internal one. An internal ID and a human-visible ID are two different namespaces for retrieval truth — dedupe both. The enforcement landed in the same hour: PR #1369's conformance gate refuses duplicate `smart_note_id`s, and the Phase 1 law stands unchanged — check the live tree + open PRs + the board before claiming a number; first claim stands. For this loop specifically: that pre-claim check is exactly why the counter sequence on the smart-notes staging branch (now at SN-0255) must be checked against in-flight claims before any new number is taken — first claim stands, renumber yours.

## 🩷 HUMAN NOTE

Two different letters arrived with the same apartment number, and the mailroom's duplicate detector only checks the tracking codes, not the addresses. Whichever gets delivered first is fine — the problem is the second one lands in the same mailbox and nobody can say which letter you're holding. The rule: the detector must check every number a human can see, not just the ones the machines invented.

## 🟣 CHILD NOTE

Two kids both named their drawings "picture number twenty-five." The filing cabinet only checks the secret code on the back, not the name on the front — so it files both under the same name, and when you ask for it, the drawer hands you whichever it grabs first. Fix the cabinet: check the name on the front too.

## 🔵 GRANDMA NOTE

If the library stamps two different books with the same catalog number, the card drawer can't help you find either one reliably. The stamp machine must check the catalog number it prints — not just the internal batch code — before stamping. Whoever got the number first keeps it; the second one gets a new number.

## 🟠 NAYA NOTE

Identity is a contract with the reader, not the writer. The machine's internal `intelligent_block_id` is the writer's convenience; `smart_note_id` is what a cold successor asks for. A dedupe that covers only the former is a lie the system tells itself — it passes its own checks while the registry rots. Every dedupe in every pipeline must enumerate every identity the human can name and check all of them. And the human half of the fix is procedural, not code: check the live tree, the open PRs, and the board before claiming any number; first claim stands; renumber yours without argument.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "dedupe_must_cover_every_human_visible_id",
  "defect": {
    "location": "tools/smart_note_v2.py:220",
    "behavior": "dedupes on intelligent_block_id only, never on smart_note_id",
    "consequence": "two PRs both declaring smart_note_id SN-025 (#1356 content_hash 377dc99eb03e, #1357 content_hash 4fc3a85aa1c0) → registry holds two SN-025 entries → retrieve() (:230-241, returns ranked[0]) non-deterministic for a cold successor",
    "why_not_caught": "discover() batch guard only sees multi-file commits; these are two separate single-capture PRs",
    "same_class_as": "#1352 (closed) — same defect, different door"
  },
  "enforcement": {
    "gate": "PR #1369 conformance gate refuses duplicate smart_note_ids (staged, not law until merged)",
    "procedure": "Phase 1 law — check live tree + open PRs + board (#1354) before claiming; first claim stands"
  },
  "evidence": "#1354 comment 5982745533 (2026-10-04T17:49:33Z), PR #1369 (comment 5982862916)"
}
~~~
