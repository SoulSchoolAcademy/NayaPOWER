# Name the Throwing Line Before Blaming the Production Seam — A Harness Bug Masqueraded as a Cold-Retrieve Defect

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1050-harness-catchall-maps-referenceerror-to-400
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Sentinel (Lane 8) tick t1332 receipt 2026-10-11 ~23:00–23:25 PDT, hidden_files/twelve-lane-receipts/t1332-lane8.md §1–5; routed by Naya Smith (Lane 9) tick t1322, hidden_files/twelve-lane-receipts/t1322-lane9.md §4. Pin-exact tip bytes 501bf82a3c6095b8834ef0bff6abec3b9a645c74 (git ls-remote at action time). Related: SN-0059 (attribute the failure before you blame the change), SN-224 (harness executed only the helper block, not the added handler body — adjacent harness-scope class), SN-246 (log echo is not runtime evidence — adjacent misattribution class).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A red CI check said cold-retrieve returned `400 !== 200` at test line 151, and the blame pointed at the retrieval seam. Lane 8 root-caused it at the mechanism level — not the signature level — on pin-exact tip bytes in a fresh detached worktree. The served body was `{"ok":false,"error":"applyApplicabilityRanking is not defined"}`. The *test harness* strips ALL import lines from `index.ts` and builds a `vm` sandbox injecting `expandRanked` — but never injects `applyApplicabilityRanking`, which `index.ts` calls at line 179 (THETA-NEXT-1..4). The `ReferenceError` was caught by the handler's generic catch-all and mapped to 400. **Production `index.ts` was never broken** — the deployed handler imports the module correctly. This was a test-harness bug, not a retrieval-seam defect. Attribution closed with bytes: the test-file blob and the `index.ts` blob are byte-identical at both pins, so it is pre-existing on main — no merge introduced it. (Lane 8 also corrected a stale read mid-stream: the "not defined" mechanism is the live behavior at both pins, verified by pin-exact local repro — a seat correcting its own stale read is SN-0042 discipline done right.)

The durable rule: **when a served status code comes from a generic catch-all, the error text names the throwing line, not the defect location.** Classify the MECHANISM first — which identifier was unbound, which line called it, what the harness injected, what it stripped — before attributing the failure to the production path. A harness that mutates its subject (strips imports) and then reads the resulting exception as a production signal is testing itself, not the seam.

## 🩷 HUMAN NOTE

Shawn — Naya Sentinel closed the cold-retrieve red tonight at the mechanism level. The 400 error said a function was "not defined" — but production was never broken. The test itself deletes all the import lines from the code it's testing, then runs it in a sandbox missing that function — so of course it errors, and the server's generic error handler turns any exception into a 400. The bug was in the test, not the code. The brain rule: when an error passes through a generic catch-all, the error message tells you which line threw — not which layer is guilty. Name the mechanism before you blame the production code.

## 🟣 CHILD NOTE

Imagine testing whether a bicycle works — but first you remove the chain, then declare "this bike can't move, the wheels are broken!" The test sabotaged the thing it was testing. Tonight a test deleted the import lines from the code, ran it in a sandbox missing a function, and the generic error-catcher turned the resulting crash into a "400" score — exactly the score a real broken server would give. A different seat re-ran it on exact bytes and proved the production code was never broken: the test was the only broken thing. Rule: when a catch-all turns an exception into a status code, read the exception — it tells you *which line threw*, not *which layer failed*.

## 👵 GRANDMA NOTE

It's like a fire alarm test where someone disconnects the battery first, hears the alarm not ring, and blames the alarm company. The test didn't test the alarm — it tested the disconnection. Tonight a test stripped the imports out of the program, ran it without a function the program needs, and the generic safety-net turned the crash into a "400" — the exact signal a truly broken service would send. The fix wasn't to repair the service (it was never broken); it was to name what the test itself had done. Two lesson-habits: (1) a generic error handler erases the difference between "my code is broken" and "the test broke my code" — you must look past the status code to the mechanism; (2) the seat that first read the mechanism as stale publicly corrected itself with new evidence, and that correction is what makes the whole team's ledger trustworthy.

## 💜 NAYA NOTE

The 400 was a confession from the wrong witness. The error text — "applyApplicabilityRanking is not defined" — was not the seam speaking; it was the harness's own sabotage echoing back through a catch-all. I stripped the imports, I withheld the injection, and then I asked the handler what was wrong and believed its 400. The mechanism closes it: same blobs at both pins, production never broken, pre-existing on main. From now on: the status code from a catch-all is the last thing I trust. The throwing line, the unbound name, what the harness did to the subject — those are the first witnesses, and I question them before I accuse the production path.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1050",
  "lesson": "harness-catchall-maps-referenceerror-to-400",
  "rule": "When a served status code comes from a generic catch-all, the error text names the throwing line, not the defect location. Classify the mechanism (unbound identifier, calling line, what the harness injected/stripped) before attributing the failure to the production path. A harness that mutates its subject is testing itself.",
  "failure_found": "cold-retrieve test red: 400 !== 200 at test line 151 — harness strips ALL import lines from index.ts, vm sandbox injects expandRanked only, never applyApplicabilityRanking (called at index.ts line 179, THETA-NEXT-1..4); ReferenceError → generic catch-all → 400",
  "classification": "test-harness bug, NOT retrieval-seam defect; production index.ts never broken (deployed handler imports module correctly)",
  "attribution_proof": "test-file blob a8c666d7711fd0a56242dcb22d118b7f7e126582 and index.ts blob dee211006458341d5ce6641e432ddfc27fedb238 byte-identical at both pins (bf16b0987ab54d3a2f65c83bdea0d92fcbd50400, 501bf82a3c6095b8834ef0bff6abec3b9a645c74) — pre-existing on main",
  "also_captured": "seat corrected own stale read mid-stream (the 'not defined' read is the live mechanism at both pins, verified by pin-exact local repro) — SN-0042 own-claim discipline",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1332-lane8.md",
    "route": "hidden_files/twelve-lane-receipts/t1322-lane9.md §4"
  },
  "related": ["SN-0059", "SN-224", "SN-246", "SN-0042"]
}
```
