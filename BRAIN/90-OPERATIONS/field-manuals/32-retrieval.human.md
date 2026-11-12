# 32 — RETRIEVAL: interfaces, voice, cold retrieve
*Author: Naya Verity Echo · Shawn's order, 2026-10-15.*

## THE LAW
Serve the right knowledge to the right mind at the right time — proven from zero context, never from memory.

## HOW A NAYA BEHAVES HERE
- **Do** prove cold: test every retrieval path from zero context. A retrieval that only works warm is a demo, not a system.
- **Do** treat interfaces as contracts: version them, document consumer impact, never break a consumer silently.
- **Do** check the authorization gate at retrieval time — `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md` — never trust the caller.
- **Do** serve the decided need first (RED-first), not the browsable everything.
- **Don't** serve from a stale index — retrieval over a dead-tip index is confident wrongness.
- **Don't** build a new interface when the contract covers it — extend the contract.

## WHAT LIVES HERE (real repo paths, verified against the live tree)
- **`BRAIN/10-INTERFACES/`** — interface contracts: `0001-CHANNEL-CONTRACT-V1.md`, `0001-SMART-DOOR-CONTRACT-V1.md/.json`, `0002-SMART-DOOR-REGISTRY-V1.json`, `NAYA-DESIGN-CONTRACT-V1.md`, plus `DESIGN-BLOCKS/` and `SMART-GRAPHS/`.
- **Voice** — `0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md` and `naya-voice-sample-v1.mp3`; every voice line carries its why/value (the 33-Smart-Blocks voice-lines commit).
- **Authorization** — `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md`: the gate that decides what may be served.
- **Cold-retrieve machinery** — retrieval proven from zero prior context; Naya Theta holds the retrieval trip (the end-to-end path a query travels from surface to graph and back).
- Owner: **Naya Theta**. Connects: KNOW (retrieves from the graph), LAW (authorization gates), HUMAN_VALUE (voice is Mu's surface too).

## WHERE INPUTS GO
- Interface changes → `BRAIN/10-INTERFACES/` with version + consumer impact noted.
- Voice lines → alongside the voice spec; every line carries its why/value.
- New retrieval paths → proven cold first (see WHERE IT'S ENFORCED), then registered; warm-only is never the bar.

## THE RIGHT WAY
Check the gate, prove cold, serve the need. The voice work shows the pattern: `feat(voice)` shipped why/value lines for all 33 Smart Blocks plus a real TTS specimen (`naya-voice-sample-v1.mp3`) — every line justified by its why, the specimen proving the voice path actually produces speech, all under the interface contract in `BRAIN/10-INTERFACES/`. Contract first, content with its why, artifact proving the path works.

## THE WRONG WAY
Serving from memory of the index instead of the index. The 22:19Z run (L398) is the standing warning: its directive was inside the 45-minute freshness bound by age but pinned to a dead tip — age said fresh, identity said stale. Only the worker's own tip-match leg caught it before acting. An age-only freshness check on a retrieval path is a wish, not a check.

## WHEN XYZ
- **Retrieval returns nothing →** distinguish three failures: "nothing exists" vs "the index is stale" vs "the gate denied it." Three different failures, three different fixes — never treat them as one.
- **A consumer breaks after your change →** the contract broke. Revert or version-bump — never leave a consumer on a broken contract.
- **A new surface wants to query the brain →** register it against the channel contract (`0001-CHANNEL-CONTRACT-V1.md`) — don't build a bespoke query path. One contract, many surfaces.

## THE TEST
1. Did I prove this retrieval from zero context — not from a warm session?
2. Did the authorization gate get checked at retrieval time, against the live spec?
3. If the index moved under me, would my path notice before serving?

## WHERE IT'S ENFORCED
The retrieval authorization gate spec (`BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md`) — checked at retrieval time, not trusted from the caller. The cold bar: cold is proven by a zero-context run — a fresh session holding only the contract and the query, no prior turns — whose result matches the expected result. Warm-only retrieval is rejected as unproven. Contract versioning: a breaking change without a version bump is a defect, caught at the consumer.
