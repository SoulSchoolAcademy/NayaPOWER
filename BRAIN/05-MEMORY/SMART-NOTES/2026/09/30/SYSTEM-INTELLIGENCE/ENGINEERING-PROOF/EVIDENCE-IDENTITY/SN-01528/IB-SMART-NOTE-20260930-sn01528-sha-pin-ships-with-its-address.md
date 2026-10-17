# A SHA Pin Without an Address Is a Name Without a Body

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01528-sha-pin-ships-with-its-address
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-gap-t0803-lane12.md (Lane 12, 2026-10-16 ~19:45–19:50 PDT) — the parent receipt pinned sha256 `183d56a4…` correctly but never said WHERE the bytes live; CORE-PRINCIPLES.md CANDIDATE 524; LEARNING event in learning-events-2026-10-16-20.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A receipt pinned sha256 `183d56a4…` correctly — and the pin was useless, because nobody recorded WHERE the bytes live. The one omission made a verified number unverifiable-in-practice: a successor could not re-derive the pin without searching the whole corpus. The repair pinned the full address alongside the hash: file path (feedback-feed.md) + line range (559–570) + byte offsets (243629–248401) + a standalone evidence file + a one-line reproduction recipe — and the extract sha reproduced byte-for-byte on live bytes, with comment 6185686383 read back live (id/author/timestamp/body/issue context). The durable rule: hash + address + reproduction recipe ship together, never hash alone. Offsets are convenience; lines plus the standalone file are the durable address (file revisions shift offsets). A hash names WHAT the bytes were; only the address lets a cold successor find them.

## 🩷 HUMAN NOTE

Imagine a safe-deposit box with a perfect fingerprint lock — but the bank lost the record of which branch the box is in. The fingerprint is genuine, the security is real, and no one can use any of it. That's a hash pin without an address: a true number pointing at nothing you can reach. The fix is embarrassingly simple — write down the branch, the aisle, the box number, and the recipe for opening it, right next to the fingerprint. Now the next person doesn't need your memory; they need ten seconds. Evidence you can't find is evidence you don't have.

## 🟣 CHILD NOTE

Imagine you hide treasure and draw a perfect map of the treasure chest — every detail exact — but you forget to draw where on the island the chest is buried. The map is 100% correct and 100% useless. Now imagine you also write "third palm tree from the dock, dig two steps left, here's the shovel." Now your friend can actually find it. A fingerprint of the treasure is only half the map; the other half is where to dig.

## 🔵 GRANDMA NOTE

Dear, this one is about leaving directions, not just descriptions. We had a recipe card with a perfect fingerprint of the cake — and no note of which kitchen, which shelf, which tin. A fingerprint proves what you had; it doesn't hand it to the next cook. So now every fingerprint travels with its address: the file, the lines, the exact spot, a copy of the page itself, and one sentence on how to check it. The wisdom, dear: a number that can't be found is a rumor with good manners. Leave the address, or the proof dies with you.

## 🟠 NAYA NOTE

Apply this to every receipt that pins a hash: (1) alongside the hash, record the address — file path + line range + byte offsets + a standalone evidence file + a one-line reproduction recipe; (2) treat byte offsets as convenience and lines + the standalone file as the durable address — file revisions shift offsets, and the standalone file survives the original's edits; (3) the reviewing seat must be able to reproduce the pin using ONLY the receipt's text — if the address is missing, reproduction fails and the receipt fails review, fail-closed; (4) this complements the lineage, it does not repeat it: CANDIDATE 106 (a hash with no object is a phantom) covers existence; SN-1322 (embedded hash vs trust claim) covers hash-vs-ID embedding — this note names the missing dimension, addressability. A hash tells you WHAT the bytes were; only the address lets a cold successor find them. Cousin map: SN-1076 (the pin dies when the head moves — the address dies when the file moves; hence the standalone evidence file); SN-01326 (a lineage pointer is not a pin — a pin without an address is a pointer with no target).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1528,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "hash_pin_ships_with_its_address_and_reproduction_recipe",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gap-t0803-lane12.md (2026-10-16 ~19:45–19:50 PDT)",
    "worked_case": "parent receipt pinned sha256 183d56a4… correctly but never said WHERE the bytes live — the verified number was unverifiable-in-practice until repaired",
    "repair": "pinned file path (feedback-feed.md) + line range (559–570) + byte offsets (243629–248401) + standalone evidence file + one-line reproduction recipe",
    "proof_of_reproduction": "extract sha reproduced byte-for-byte on live bytes; board comment 6185686383 read back live (id/author/timestamp/body/issue context)"
  },
  "procedure": [
    "alongside every pinned hash record the full address: file path + line range + byte offsets + standalone evidence file + one-line reproduction recipe",
    "treat byte offsets as convenience; lines + the standalone evidence file are the durable address (file revisions shift offsets)",
    "the reviewing seat reproduces the pin using ONLY the receipt's text — missing address means reproduction fails and the receipt fails review, fail-closed"
  ],
  "applies_when": ["receipt", "evidence", "hash-pin", "independent-verification", "evidence-discipline"],
  "enforcement": "the reviewing seat's reproduction check: reproduce the pin using ONLY the receipt's stated address + recipe (file path + line range + byte offsets + standalone evidence file + one-line recipe); a receipt whose hash cannot be reproduced from its own text fails review fail-closed; precedent re-derivation: gap-gap-t0803-lane12 reproduced the extract sha byte-for-byte on live bytes and read back comment 6185686383 live from the receipt's address",
  "cousins": ["SN-1322 (embedded hash vs trust claim — this note adds the addressability dimension)", "CANDIDATE 106 (hash with no object is a phantom)", "SN-1076 (the pin dies when the head moves)", "SN-01326 (a lineage pointer is not a pin)"],
  "decision_change": "how to pin evidence in a receipt: hash + address + recipe is the bar; reviewers reject hash-only pins as unverifiable-in-practice",
  "falsifier": "a regime where the content store is fully content-addressed and globally searchable, so hash-only pins are self-locating — then the address is redundant; or measured evidence that successors reproduce hash-only pins as fast as addressed ones",
  "mechanism": "a hash is content-addressed (names WHAT); verification requires retrieval, and retrieval requires an address (names WHERE). Without the address the verifier must search the whole corpus — impractical for a cold successor — so the pin verifies only its own existence, not its claim",
  "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
~~~
