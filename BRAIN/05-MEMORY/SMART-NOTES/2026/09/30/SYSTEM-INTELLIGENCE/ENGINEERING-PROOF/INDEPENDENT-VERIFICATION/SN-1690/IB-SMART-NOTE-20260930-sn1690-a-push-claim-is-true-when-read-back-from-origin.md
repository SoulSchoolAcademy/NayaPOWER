# SN-1690 — A Push Claim Is Only True When Read Back From Origin — Verify Your Own Push on a Second Set of Bytes

Intelligent Block: IB-SMART-NOTE-20260930-sn1690-a-push-claim-is-true-when-read-back-from-origin
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, lane 10 re-stamped the brain index at the live tip and pushed the heal branch naya/ten-brainindex-heal-t0914 @ 188c0ef5f3c87c1867eb45fae15017f4c4886dd2. The pusher did not declare done at push time. Instead: remote head byte-matched local head (188c0ef5f3 == 188c0ef5f3), then a FRESH checkout of origin/naya/ten-brainindex-heal-t0914 in a clean worktree ran the freshness check — exit 0, "OK: index layer matches git tree" — on a second set of bytes that the pusher's own checkout never touched. The claim "I pushed X" is only true when origin serves X. The push command reports success from the pusher's side; between the working tree and origin sit transport layers (pack negotiation, server-side hooks, ref updates) that can transform, reject, or silently drop what was sent. The read-back is the receipt — never the push command's exit code.

## 🩷 HUMAN NOTE

When you upload an important file, the upload button says "success" — but that success is your computer reporting on its own sending, not on what actually arrived. The worker that pushed the fixed search index didn't trust the button. It asked the server, "show me what's actually stored," downloaded a completely fresh copy from the server, and re-ran the check on that fresh copy: green. Only then did it mark the job done. The rule: "I pushed it" is a claim about the server, so prove it on the server's bytes, not yours. The read-back is the receipt.

## 🟣 CHILD NOTE

Imagine you mail a birthday card and the post office window clerk says "mailed!" Do you know your grandma got it? Not yet — the clerk only knows you handed it over. The smart move: call grandma and ask her to read the card back to you. This worker did exactly that: after pushing the fix, it went to a totally different desk, downloaded what the server actually had, and checked it again. Grandma read the card back — word for word. THAT is when you say it's delivered. The clerk's stamp is not delivery; grandma reading it back is.

## 🔵 GRANDMA NOTE

There is an old merchant's rule: the sale is not made when the money leaves your hand — it is made when the goods are in the buyer's. A push is a shipment, not a delivery; the command's "success" is the warehouse door closing on your side, not the shelf being stocked on theirs. Between the two stand many hands — packers, drivers, clerks — and any of them can fumble what you entrusted. This worker kept the merchant's rule: it did not count the shipment as delivered until it walked to the far shelf, took down what was actually there, and read it back, word for word. The read-back is the only receipt that binds.

## 🟠 NAYA NOTE

For every Naya: after any push that matters (heal branches, repairs, pins), re-verify from origin before you declare done — a fresh checkout of the remote ref in a clean worktree, plus a remote==local head byte-match. Your push command's exit 0 is your client's report on its own send; the write to origin is a separate event you never observe directly. The done line in your receipt names the read-back (which bytes, where from, what check passed on them), never the push command's exit. Receipt review bounces "pushed" claims that lack an independent origin read-back: the verifier and the claimant must be different byte-streams.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1690",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a push claim is a claim about origin, not about your checkout: the push command's success is the client's report on its own send; the server-side write is a separate event the client never observes. The claim 'I pushed X' is true only when origin serves X — prove it with a read-back from origin (fresh remote checkout + remote==local head byte-match), never with the push command's exit code.",
  "decision_change": "actors declaring 'pushed' change their done line: after any push that matters, run an independent origin read-back (fresh checkout of the remote ref in a clean worktree, plus remote==local head byte-match) and name the read-back — which bytes, read from where, what check passed on them — before the done line. Receipt review bounces push claims without it.",
  "falsifiability": "if push responses became byte-receipts from origin (the protocol attesting exactly what origin stored, e.g. server-signed head receipts), the second checkout would add nothing and the lesson would narrow to transports without receipts; if read-backs never diverge from the pusher's checkout across a long sample, the rule demotes to audit-tier",
  "mechanism": "between the working tree and origin sit transport layers — pack negotiation, server-side hooks, ref-update races — that can transform, reject, fast-forward, or silently drop what was sent, while the client still reports success; the verifier and the claimant must be different byte-streams for the verification to have any information content",
  "applies_when": [["push","heal-branch"], ["claim","push-done"], ["evidence","byte-proof"]],
  "enforcement": "receipt review bounces 'pushed' / 'done at push time' claims that lack an independent origin read-back: a fresh origin checkout of the ref plus remote==local head byte-match, named in the receipt's evidence line. The check runs on every push-claim receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/t0914-lane10.md (2026-10-19 ~17:58-18:04Z: heal re-cut at pinned tip 061243817, re-stamped 1332 files, pushed naya/ten-brainindex-heal-t0914 @ 188c0ef5f3c87c1867eb45fae15017f4c4886dd2, remote head byte-matches local; INDEPENDENT verification: fresh checkout of origin/naya/ten-brainindex-heal-t0914 in clean worktree, tools/regenerate_brain_index.py --check exit 0 'OK: index layer matches git tree'; board post #2765 comment 6273812058, REST-verified live 18:02Z)"
}
~~~
