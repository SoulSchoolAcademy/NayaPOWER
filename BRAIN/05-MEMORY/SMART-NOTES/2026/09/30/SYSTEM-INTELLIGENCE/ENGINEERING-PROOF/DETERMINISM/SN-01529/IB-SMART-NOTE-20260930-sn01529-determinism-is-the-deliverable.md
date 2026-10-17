# Determinism Is the Deliverable: Two Seeds Before the Pin

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01529-determinism-is-the-deliverable
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-gap-t0907-lane5 mirror receipt (Lane 5, 2026-10-17 ~00:15 UTC) — the merge script joined multi-source `notes` from a Python `set`; three seeds produced three different SHAs; CORE-PRINCIPLES.md CANDIDATE 514; LEARNING event in learning-events-2026-10-16-17.md. Applied live in the 18:00-hour receipts ("determinism gate re-run twice before the boost (CANDIDATE 514 applied)").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A merge script committed a sha256 pin of its output — and the pin was a lottery draw. The script joined multi-source `notes` from a Python `set`, and set iteration order depends on PYTHONHASHSEED: three seeds produced three different SHAs (d30fe73c / 3a111649 / 4c841974). The committed bytes were whatever seed happened to be in the environment — a cold successor re-running the script could never reproduce them. The root fix was `sorted()` at both join sites in the branch and workspace scripts; post-fix, seeds 0/1/42/99 all produce identical `89bfc298a791c371` (459 records). The durable rule: any script whose output gets sha-pinned runs twice under different seeds before the pin counts — the pin certifies determinism, not just bytes. A pin on a non-deterministic script is a souvenir of one run, not evidence.

## 🩷 HUMAN NOTE

Imagine a notary stamping a document, but the document re-rolls its own words every time the room temperature changes. The stamp is real, the seal is genuine — and the stamped version never existed twice. That's a hash pin on a script with hidden randomness: Python's `set` ordering shifts with an environment seed nobody sees, so the same code produces different files on different runs. The committed number was whichever roll happened to be showing. The fix is a one-word discipline: sort before you join, then prove it by running twice under different seeds. Two matching stamps mean the process is stable; one stamp means you got lucky once.

## 🟣 CHILD NOTE

Imagine you write a recipe and the steps shuffle every time you read it — sometimes sugar first, sometimes flour first. You take a photo of one version and say "this is THE recipe." But nobody can bake from the photo, because next time the steps will be different. The fix: number the steps (sort them!) so they're always in the same order — then take the photo twice to prove it stays put. A photo of something that keeps changing is just a picture, not a promise.

## 🔵 GRANDMA NOTE

Dear, this one is about promises that hold still. We had a machine that stamped a fingerprint on its work — but the work quietly rearranged itself each time, like chairs moved in the night, because of a hidden seed in the room. So the fingerprint was different every morning, and the stamped copy could never be made again. We taught the machine to line everything up in order first (sorted, dear, like books on a shelf), then we asked it to stamp twice under different seeds — and both stamps matched. The wisdom, dear: never trust a single fingerprint on something that might move. Ask for two, and make them agree.

## 🟠 NAYA NOTE

Apply this before any sha gets committed or quoted as a pin: (1) audit the script for order-dependent iteration — Python `set` of strings, dict iteration where insertion order isn't guaranteed, any unsorted join of multi-source fields; (2) insert `sorted()` (or an explicit canonical ordering) at every such site, in both the branch script and any workspace copy — the 514 incident needed the fix in both; (3) run the script under at least two different PYTHONHASHSEED values and require byte-identical output SHAs before the pin is recorded — seeds 0/1/42/99 were used post-fix; (4) if any two seeds diverge, the pin is VOID and the script is not shippable — a diverging pin is a seed-lottery draw, and committing it fabricates reproducibility; (5) document the seed-check in the receipt next to the pin, so a cold successor knows the pin was earned, not drawn. Cousin map: CANDIDATE 504 (hash before place — this is the output side, 504 is the ingest side); CANDIDATE 524 (a pin needs its address — this note says the pin must also be deterministic); SN-1528 (addressability — same family, orthogonal dimension).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1529,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "two_seed_determinism_check_before_any_sha_pin",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gap-t0907-lane5 mirror (2026-10-17 ~00:15 UTC)",
    "violation": "merge script joined multi-source notes from a Python set; three PYTHONHASHSEED values produced three different output SHAs (d30fe73c / 3a111649 / 4c841974); the committed bytes were a seed-lottery draw",
    "root_fix": "sorted() inserted at both join sites in branch and workspace scripts",
    "post_fix_proof": "seeds 0/1/42/99 all produce identical sha 89bfc298a791c371 (459 records)",
    "live_application": "18:00-hour receipts record 'determinism gate re-run twice before the boost (CANDIDATE 514 applied)'"
  },
  "procedure": [
    "audit any script for order-dependent iteration (str sets, unsorted multi-source joins) before its output is sha-pinned",
    "insert an explicit canonical ordering (sorted()) at every such site, in every copy of the script",
    "run the script under at least two different PYTHONHASHSEED values and require byte-identical output SHAs before recording the pin",
    "any seed divergence voids the pin; the script is not shippable until seeds agree",
    "record the seed-check beside the pin in the receipt"
  ],
  "applies_when": ["sha-pin", "merge-script", "dedup", "evidence-discipline", "reproducibility", "lane-executor"],
  "enforcement": "the named determinism gate: any script whose output gets sha-pinned must pass the two-seed byte-check (run under at least two different PYTHONHASHSEED values, require identical output SHAs) before the pin is recorded or committed; a diverging pin is void and blocks the receipt — precedent: gap-gap-t0907-lane5 post-fix seeds 0/1/42/99 identical, and 18:00-hour receipts gate boosts on the determinism re-run",
  "cousins": ["CANDIDATE 504 (hash before place — ingest side of the same family)", "CANDIDATE 524 / SN-1528 (a pin needs its address — orthogonal dimension)", "CANDIDATE 125 (spec-true vs code-true)"],
  "decision_change": "whether a sha pin may be committed or quoted as evidence: no pin without the two-seed byte-check; pins on unchecked scripts are treated as unproven",
  "falsifier": "a script with provably order-independent iteration (no set/dict-order dependence anywhere) makes the check vacuous — the gate must name its scope; or two seeds agree but a third diverges, proving the gate needs more seeds",
  "mechanism": "PYTHONHASHSEED randomizes str-set iteration order per process, so the same code emits different byte sequences on different runs; a sha of such output certifies the accident, not the process. Sorting canonicalizes the order, making the bytes a function of the inputs alone",
  "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
~~~
