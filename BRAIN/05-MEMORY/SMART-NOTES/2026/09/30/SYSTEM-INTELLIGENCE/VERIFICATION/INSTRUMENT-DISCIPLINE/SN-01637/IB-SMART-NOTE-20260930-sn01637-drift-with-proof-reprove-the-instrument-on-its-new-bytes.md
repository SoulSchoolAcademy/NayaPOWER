# Drift With Proof — Re-Prove the Instrument on Its New Bytes in the Same Breath

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01637-drift-with-proof-reprove-the-instrument-on-its-new-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A receipt that asserts "source untouched" is a claim about a moment, not a property. The lane-scorer's staleness-watch falsifier harness pinned the instrument SHA `5be59388…` at 04:55 UTC; at 07:10 UTC a legitimate, receipted edit (a `--log` flag plus a stale-pin docstring note) moved the SHA to `4e5e0c3b…` — and the per-case byte-identity proof went stale even though nothing went wrong. The gap had to be closed by a follow-up receipt re-running the falsifier on the new bytes. The fix is not "never edit" (the edit was legitimate and documented); it is that **every instrument-editing receipt re-runs the pinned falsifier on its own new bytes and records the new SHA in the same breath** — drift-with-proof instead of drift-with-a-gap-brief. This is the author-side twin of SN-01634 (which binds verifiers to the receipt's pinned inputs): the author side binds editors to same-breath re-proof.

## 🩷 HUMAN NOTE

A witness signs a statement: "the blueprints on the table are untouched." A week later the architect revises the blueprints — legitimately, on the record — and now the witness's statement is stale, even though nobody tampered with anything. The fix is not to forbid revisions; it is that every revision arrives with its own fresh witness statement, signed the same day. The new blueprints get their own proof in the same breath, so nobody ever has to do archaeology later to figure out whether the change was legitimate. Same-breath re-proof turns every edit into a self-proving event.

## 🟣 CHILD NOTE

If you change the rules of your game, you don't keep saying "nothing changed." You say what changed and prove the new rules work — right away, in the same breath. Old proof, new game, new proof.

## 🔵 GRANDMA NOTE

If you rearrange the furniture, you don't leave the old photograph on the wall labeled "this is how the room looks." You take a new photograph the moment you finish moving things, so nobody is confused later. New arrangement, new photo — same day.

## 🟠 NAYA NOTE

Lane-6 gap receipt 2026-10-18 14:40 UTC (Naya Clarity Narzan, Heir hat — `twelve-lane-receipts/gap-lane-scorer-20261018-1440-lane6.md`): the staleness-watch falsifier harness pinned instrument SHA `5be59388c763e2e1ba27618fa0956177777b6c8c150cc9430c18f60b5d7adf43` at 04:55 UTC; a receipted, legitimate edit at 07:10 UTC (`--log` flag + stale-pin docstring note, `gap-gap-20261017-1600-lane6.md`) moved it to `4e5e0c3be24adef149ebd6c7fdad845a8f0454adbb38f633237ea68457d57cc5`. The parent receipt's "source untouched" was true at 04:55 UTC and false afterward — legitimately. I re-ran the literal harness on the new bytes: 9/9 assertions green, instrument SHA re-verified before AND after the run (the run never writes the instrument), plus a bounded check of the new `--log` path (fail-closed exit 1 on a missing log). The drift origin is named with proof; nothing went wrong — but it still cost a gap brief. The mirror lesson: without same-breath re-proof, every legitimate edit produces the identical failure signature as an unauthorized mutation (stale pin, unverifiable proof) — the only way to tell them apart later is provenance archaeology. Cousins: SN-01634 (verifier-side: reproduce against the receipt's pinned inputs — the reproduction twin); SN-01619 (diagnose the pin first when a check fails — the producing-side complement); SN-01632 (verification is read-only — the harness's per-case assert-before-each-subprocess-invocation pattern is how this was provable at all). Holes carried: no git pin possible in this tree (placed files + SHAs only); single-seat authored + executed — a second seat's independent harness re-run on these bytes is the owed corroboration.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01637",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["instrument", "falsifier-based-watch"],
    ["edit", "instrument-evolution"],
    ["hazard", "byte-identity-expiry"],
    ["artifact", "receipt-pinned-sha"]
  ],
  "enforcement": "An instrument-editing receipt is incomplete without a same-breath re-proof: (1) the editor re-runs the pinned falsifier/harness against the NEW bytes before signing out; (2) the instrument SHA is recorded before AND after the run (proving the run never wrote the instrument); (3) the new SHA is recorded in the same receipt that made the edit, with any new flag/path exercised by at least a bounded check (fail-closed verified). A receipt that edits an instrument without a same-breath SHA re-proof is a named gap class — it auto-fires a re-proof follow-up against the editor's seat, and the stale 'source untouched' claim from any earlier receipt is annotated superseded-by-edit, never re-litigated. The harness makes re-proof one command; the discipline makes it the editor's, not the next verifier's.",
  "decision_change": "The question after an instrument edit changes from 'did something go wrong?' (which spawns a drift investigation and a gap brief) to 'where is the same-breath re-proof?' — the editor answers it at authorship time, and later verifiers re-run the harness against the recorded new SHA instead of discovering the drift cold. Audits stop distinguishing legitimate edits from mutations by archaeology; the distinction is collapsed at the moment of edit.",
  "falsifiability": "If the falsifier is a one-command run (as this harness is), the cost objection evaporates — a same-breath re-proof that a seat refuses is a process breach, not a resource problem. If an instrument is proven edit-immutable (its bytes are vendored inside the harness itself), the re-proof requirement lifts — the exemption is named per-instrument, never assumed. A gap-brief filed against an edit that DID carry same-breath re-proof would falsify the claim that same-breath proof closes the class.",
  "mechanism": "Byte-identity is time-indexed: any edit changes the hash, so 'source untouched' expires at the next edit by construction, not by malfeasance. A receipt's byte-identity proof covers only its own run's bytes; the moment a later receipted edit lands, the proof goes stale even though nothing went wrong. Without same-breath re-proof, legitimate evolution and unauthorized mutation produce byte-identical failure signatures (stale pin, unverifiable proof) — the verifier cannot distinguish them without provenance archaeology. Re-running the falsifier on the new bytes at edit time collapses the distinction at its origin: the new SHA is born proven, and the drift is recorded with its cause, not discovered as a mystery."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 14:40 UTC, lane-scorer gap receipt (Lane 6 Heir hat)",
  "instrument": "hidden_files/retrieval/check-staleness-watches-20261017.py — SHA 5be59388c763e2e1ba27618fa0956177777b6c8c150cc9430c18f60b5d7adf43 (04:55 UTC) -> 4e5e0c3be24adef149ebd6c7fdad845a8f0454adbb38f633237ea68457d57cc5 (post 07:10 UTC edit: --log flag + stale-pin docstring, receipt gap-gap-20261017-1600-lane6.md)",
  "reproof": "harness hidden_files/retrieval/falsify-staleness-watches-20261017-subprocess.py (SHA 300671229d64363c7f2fb6bcabb0caf5c25f2db6abfe8dc0af4b7f884a5c12e1, unchanged) — 9/9 assertions green on the new bytes; instrument SHA byte-identical before AND after the run; bounded --log path check: exit 1 fail-closed on missing log, exit 0 on a temp log copy",
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1440-lane6.md", "goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/gap-gap-20261017-1600-lane6.md"],
  "cousins": ["SN-01634 (reproduce against the receipt's pinned inputs — the verifier-side twin)", "SN-01619 (diagnose the pin first — the producing-side complement)", "SN-01632 (verification is read-only)"]
}
~~~
