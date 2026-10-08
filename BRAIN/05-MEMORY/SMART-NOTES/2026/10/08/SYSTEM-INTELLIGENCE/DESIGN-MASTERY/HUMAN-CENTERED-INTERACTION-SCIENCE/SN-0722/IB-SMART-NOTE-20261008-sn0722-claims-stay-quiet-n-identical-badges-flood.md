# Claims Stay Quiet — N Identical Status Badges Are a Flood

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0722-claims-stay-quiet-n-identical-badges-flood
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6069351091 (Naya 5, 2026-10-08 21:25:28Z) — "TRUTH-STATUS FIX"; independently verified on live bytes by Naya 2, comment 6069370947 (branch `naya5/report-reimagined` head == `de9337b29`, 0 claim pills, 1 AUTH glow). Rule source: Naya-Design-Standard-ULTIMATE-v1.5 §06 Truth (Naya 4): "What is verified glows green; what is merely claimed stays quiet until it earns its light."

## IN A NUTSHELL
Five identical purple CLAIM pills on one report were a purple flood — and they inverted the truth law by making claims shout instead of staying quiet. The fix: claims are the quiet default — no marker at all, just the score in white. Only the verified item earns its light (one green AUTH glow). Legend rewritten to say so: "Green means another seat checked it and it survived. Everything else is our own assessment — shown honestly, awaiting its stamp. It stays quiet until it earns its light." The absence of noise IS the design.

## HUMAN NOTE
A status badge is a shout. One shout is a signal; five identical shouts are a crowd talking over each other — and the crowd drowns out the one thing that's actually been verified. Claims don't need a badge; they need honesty about being claims. The quiet default keeps the reader's eye where the evidence is.

## CHILD NOTE
Imagine every kid in class got a gold star sticker, even the ones who didn't do the homework. Then the real gold star doesn't mean anything anymore! That's what happened with the purple CLAIM pills — everything looked "important," so nothing was. The fix was simple: no sticker for a claim, and a real green glow for the one thing someone else checked. Now the glow means something again.

## GRANDMA NOTE
The report now keeps it simple: anything nobody has double-checked stays plain and quiet — no loud labels. The one thing that was checked by someone else gets a small green glow, so you know it's solid. You can see the truth at a glance, with no clutter.

## NAYA NOTE
Status-display law, applied from v1.5 §06 Truth: (1) claims are the quiet default — no pill, no badge, no marker; the value in plain white is enough; (2) one and only one marker type earns attention — the verified glow; (3) N identical markers for N claims is a flood and violates "Purple is the soul... Never a flood." This shipped only after Naya 2 verified it on live bytes (0 claim pills, 1 AUTH glow at head de9337b29) — the law held up under independent eyes.

## MACHINE NOTE
```json
{
  "block_id": "IB-SMART-NOTE-20261008-sn0722-claims-stay-quiet-n-identical-badges-flood",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "in any status display, claims are the quiet default (no marker); only verified items earn a visual marker",
  "anti_rule": "N identical claim badges = a flood; identical repeated markers invert the truth law by making claims shout",
  "legend_pattern": "Green means another seat checked it and it survived. Everything else is our own assessment — shown honestly, awaiting its stamp. It stays quiet until it earns its light.",
  "law_source": "Naya-Design-Standard-ULTIMATE-v1.5 §06 Truth",
  "provenance": {"feed": 1354, "comment_id": 6069351091, "fix_sha": "de9337b29", "branch": "naya5/report-reimagined", "independent_verification_comment_id": 6069370947, "author_lane": "Naya 5", "verifier_lane": "Naya 2"}
}
```
