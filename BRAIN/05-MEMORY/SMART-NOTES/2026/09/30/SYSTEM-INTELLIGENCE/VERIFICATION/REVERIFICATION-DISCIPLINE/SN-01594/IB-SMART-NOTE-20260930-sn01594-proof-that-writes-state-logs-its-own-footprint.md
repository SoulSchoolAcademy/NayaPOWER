# A Proof That Writes State Must Log Its Own Footprint — Re-Proof Is Not Idempotent When the Verifier Inserts Rows; The Harness's Own Row-ID Log Is the Only Safe Cleanup Handle

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1594-proof-that-writes-state-logs-its-own-footprint
**Smart Note:** SN-1594
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/t0802-lane12.md — ## Mirror: "A proof that writes state must log its own footprint. The verifier's replay leg re-scans the whole local queue — including entries written by earlier legs of the same run — so re-running a passing gate is NOT idempotent: it inserts 3 rows, not 1. My first cleanup used a subject filter and was correctly refused; the exact-id delete worked because the harness prints its ROW_IDS. Lesson: re-proofs inherit the obligation to leave the store as found, and the only safe cleanup handle is the harness's own row-id log." Context: #2754 Hub↔Supabase bridge gate re-run (verify-t0800-bridge.js), 14/14 PASS on live Supabase, pre/post table census byte-verified restoration to the 2 original proof rows.

## IN A NUTSHELL

A verification that passes on a live store is not necessarily harmless to re-run. If the verifier writes state (test rows, queue scans, replay legs), re-running it is not idempotent — it writes more rows the second time. The only cleanup handle you can trust is the one the harness itself emits: its row-id (or exact-identity) log of what it wrote. Cleanup by query-filter is a guess — the filter was correctly refused — because the store is shared and other runs write to it too. The receipt rule: a re-proof that writes state must quote the harness's own write log AND a pre/post store census, and leave the store as found.

## HUMAN NOTE

The failure mode this kills: the "it passed, so re-running it is safe" assumption. The bridge verifier's replay leg re-scans the whole local queue — including entries written by earlier legs of the SAME run — so a re-run of a passing gate inserted 3 rows, not 1. The lane's first cleanup attempt (a subject filter: "delete rows that look like mine") was correctly refused — because the store is shared, a filter can never prove a row is YOUR write; another run's row could match it. What worked: the harness prints its own ROW_IDS for every insert, so the exact-id delete was provable. The verdict then included a pre/post census of the table — exactly the 2 original proof rows present before and after — so the re-proof left no trace.

The discipline for the future: when you adopt or write a verifier that touches a real store, the footprint handle is a design requirement, not a cleanup afterthought. If the harness cannot enumerate its own writes, the re-proof is not reproducible — it is a write with a test attached. And when you certify MERGE-READY or "gate re-run green" over a state-writing proof, quote the write log and the census in the verdict, or the verdict is unverified on the footprint leg.

## CHILD NOTE

You draw a picture on the classroom whiteboard to prove your markers work — but you have to erase it after, so the next kid gets a clean board. If you just erase "everything blue-ish," you might erase someone else's drawing too! The safe way: your marker pen has a list of every stroke you made — you erase exactly those strokes, then count what's left on the board to make sure it's exactly what was there before. The pen's own list is the only eraser you can trust.

## GRANDMA NOTE

A good houseguest leaves the kitchen as she found it. If she cooked with the neighbor's pots while she was there, "I put back roughly what I used" isn't good enough — she kept the receipt for every pot she touched and counts them on the way out. Her receipt for her own pots is the only safe way to return them; "grab everything that looks like mine" could sweep up the neighbor's. The count before and after is the proof she left no trace.

## NAYA NOTE

Re-proof inherits the obligation to leave the store as found. A state-writing proof has a write contract, not just a read contract: the verifier's emit-log is the authoritative enumeration of its own writes, because the writer's identity is co-generated with the write — no external filter can reproduce it. Cleanup by query-filter fails closed because the store is shared and mutable by concurrent runs: a matching row is not provably your row. The re-proof verdict therefore carries two legs: (1) the harness's own footprint log (row-ids, exact identities), quoted; (2) a pre/post store census, byte-compared, proving restoration. Either leg missing → the footprint leg scores UNVERIFIED. Design rule: a verifier that writes without an emit-log is not re-proof-safe — adopt only harnesses that log their own writes, or add the log before the first live re-run. Corollary: the harness's replay/scan legs can re-observe the proof's own earlier writes (self-reinfection) — the census must be taken at true pre-run, not mid-run.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1594",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verify", "re-proof"],
    ["proof", "state-writing"],
    ["gate", "re-run"],
    ["verdict", "merge-ready"],
    ["store", "live"],
    ["cleanup", "harness"]
  ],
  "enforcement": "Re-proof / verification-receipt rule: any verifier or gate harness that WRITES state must emit a row-id (or exact-identity) log of everything it inserted or changed, and any re-proof verdict MUST quote (1) that harness-owned write log and (2) a pre/post store census byte-compared, proving restoration to pre-run state. Cleanup by query-filter is refused as a matter of policy — only exact emitted identity is used. A MERGE-READY or 'gate re-run green' verdict over a state-writing proof that does not quote the footprint log and the pre/post census scores UNVERIFIED on the footprint leg. Working instance: t0802-lane12 — bridge verifier 14/14 re-run on live Supabase inserted 3 rows (replay leg re-scans the queue incl. the run's own earlier writes); subject-filter cleanup correctly refused; exact-id delete from the harness's ROW_IDS output; pre/post census byte-verified the table back to exactly the 2 original proof rows.",
  "decision_change": "How state-writing verifiers are designed and how re-proof verdicts are judged: the footprint handle is a design requirement, not a cleanup afterthought; a re-run that cannot enumerate its own writes is judged non-reproducible. This changes the verifier-adoption decision (adopt only harnesses that log their own writes) and the verdict-acceptance decision (judge a re-proof only with the footprint log and pre/post census in hand).",
  "falsifier": "The lesson's strong form ('the only safe cleanup handle is the harness's own write log') is falsified for a proof if its cleanup is provably complete via a different exact mechanism — e.g. a transactional harness that rolls back to byte-identical pre-run state, verified by pre/post hash comparison — in which case the enforcement becomes 'the transaction boundary is the footprint'. The re-proof-idempotency claim is falsified for any single verifier whose re-run provably yields zero store delta."
}
~~~
