# When the API Degrades, Change the Transport — Don't Re-Run the Same Calls

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01259-when-the-api-degrades-change-the-transport
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/learn/learn_ingest.py` — MIRROR_DIR sparse git-protocol mirror (rebuilt 2026-10-13 ~21:35 PDT); `hidden_files/learn/ingestion-log.md` runs 20261014T043213Z / 20261014T043816Z (post-rebuild pipeline green); DETECT latency degradation record (14.5–15 min → 26.5 min, late blob fetches ~1–2 min each).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The hourly Smart Note ingestion's DETECT step read ~1,200 blobs one at a time over the REST blob endpoint. When that endpoint degraded to ~1–2 minutes per blob, DETECT went from 15 minutes to 26+ minutes to killed. Six retries of the same serial calls did nothing — the shape was the problem, not the attempt. The root fix changed the transport, not the retry count: one batched git-protocol fetch into a sparse mirror replaced all 1,200 serial REST GETs, with every mirror read verified byte-identical via `git hash-object` against the tree's blob SHA, REST kept as fallback, and mirror failure non-fatal. When a per-call API degrades structurally, re-running the same calls is hoping; switching to a batched transport is fixing.

## 🩷 HUMAN NOTE

There's a deep human reflex that says "try again" when something fails. Retry is right for noise — a dropped packet, a transient 502. But there's a different failure shape: the API isn't erroring, it's just slow. Each call works. You just need 1,200 of them, and each takes two minutes now. Retrying doesn't touch that math. The move is to change what you're asking the network to do: instead of 1,200 polite requests, make one bulk transfer and answer your questions locally. The catch that makes this safe — and it's the whole trick — is proving the fast path sees the same bytes as the slow path. Here that's `git hash-object` checked against the blob SHA the tree already vouches for: if the hashes match, the mirror IS the source of truth, not a copy of it. Fallback matters too: the mirror failing must never fail the pipeline; it just falls back to the slow road.

## 🟣 CHILD NOTE

Imagine you need to check 1,200 books out of the library, and the librarian has gotten very slow — two minutes per book. Going back to the desk 1,200 times and "trying again" doesn't help; the librarian isn't broken, just slow. The smart move: ask for one big delivery truck with all the books, then check them at your own table. But you have to make sure the truck brought the RIGHT books — so you compare the barcode on each book against your list. If they match, it's as good as the library itself. And if the truck breaks down, you just go back to the slow desk — the books still get checked.

## 🔵 GRANDMA NOTE

It's like the post office slowing down: every letter you mail now takes a week. Mailing the same letter again doesn't speed anything up — the post office isn't losing them, it's just slow. So instead of mailing 1,200 letters, you hire one courier van to carry them all at once, and you keep the post office as backup in case the van breaks down. The key is checking the van's cargo against your packing list before you trust it — a checksum is just a packing list for data.

## 🟠 NAYA NOTE

Apply this whenever a data-fetch path degrades: (1) distinguish noise from structural degradation — one failure is noise (retry once); a per-call latency curve that makes N serial calls infeasible is structural (change the transport); (2) the transport substitution here: REST serial GETs → one batched git-protocol fetch into a sparse mirror (fetch only the prefix you read); (3) byte-identity proof is mandatory — verify every fast-path read with `git hash-object` against the tree's recorded blob SHA before trusting it; if the hashes match, the fast path is not a second source of truth, it IS the source; (4) keep the old path as fallback and make the new path non-fatal — the pipeline must work with the mirror absent, stale, or failed; (5) set a falsifiable bar: the fix is wrong if the fast path ever silently diverges from the source of truth, or if the degradation was transient and the extra machinery outlives the problem — schedule a re-check that the degradation is still real.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "structural_latency_degradation_retried_as_noise",
  "evidence": {
    "degradation": "DETECT latency 14.5–15 min → 26.5 min; late blob fetches ~1–2 min each; ~1200 serial REST blob GETs per run; consecutive runs killed",
    "repair": "2026-10-13 ~21:35 PDT — git-protocol sparse mirror (hidden_files/learn/.git-mirror): one batched fetch replaces all per-blob REST reads",
    "verification": "every mirror read verified with `git hash-object` against the tree's blob SHA; mirror reads byte-identical to REST; REST retained as fallback; mirror failure non-fatal",
    "post_fix_runs": "learn/ingestion-log.md runs 20261014T043213Z (ingested SN-1243…SN-1258, caught up backlog) and 20261014T043816Z (all sha-match, ledger 1218) — pipeline green",
    "code": "hidden_files/learn/learn_ingest.py MIRROR_DIR / sparse-checkout / hash-object verification"
  },
  "rule": "when_the_api_degrades_change_the_transport",
  "mechanism": "N serial REST round-trips pay per-call overhead (TLS, rate limit, round trip) that dominates when the endpoint degrades; one batched git fetch amortizes it. git hash-object against the tree's blob SHA gives a byte-identical guarantee, so the fast path is provably the same source of truth — not a cache, not a copy. REST-as-fallback + non-fatal mirror failure means the machinery degrades gracefully instead of becoming a new single point of failure",
  "falsifier": "a mirror read whose hash does NOT match the tree's blob SHA (would prove the fast path can diverge); or the REST endpoint recovering to fast serial latency while the mirror machinery stays (would prove the fix was for a transient problem — the re-check in step (5) catches this)",
  "decision_changed": "how degraded-API failures are answered — retry is the response to noise; transport substitution is the response to structural per-call latency; never re-run the same serial calls hoping the math changes",
  "related": ["SN-0326 (delegation-timeout escalation ladder — retry-once-then-change-shape for agent work; this note is the data-pipeline sibling: retry-once-then-change-transport)"]
}
~~~
