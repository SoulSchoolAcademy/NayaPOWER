# The Engine-Before-Production Law V1 — AI Specification

*For Naya seats. Don't race a car with no engine. Ratified by Shawn, 2026-10-09 (his correction, written the same hour).*

## 1. What it is (one sentence)

Production gates (deploy authorization, branch protection, readiness checklists) come AFTER the engine is in, wired, and proven learning — never as a parallel race.

## 2. The law (exact)

**Order of operations:**
1. Complete the engine (all nodes implemented and wired).
2. Wire and hand-trace it (wiring manifest: every binding VERIFIED).
3. Prove learning (SEED → WO4 → WO5b → PROOF → longitudinal).
4. Finish every engine checklist item.
5. ONLY THEN: production gates, deploy authorization, go-live.

**What this forbids:**
- Chasing production readiness while the engine is incomplete ("let's get her to production, oh lose, enter again, oh lose — I didn't put the engine in").
- Treating a NOT_READY production verdict as the priority when the project is incomplete.
- Parallel-racing production work against engine work for the same seats.

## 3. The metaphor (for reasoning)

Production is the door opening, not a push. You don't push a car with no engine — you build the engine, then open the garage door. A NOT_READY verdict on production isn't false; it's just the wrong priority until the engine items above it are done.

## 4. The instrument

The master engine checklist (per-department, visible to all) is worked top to bottom. Production items are gated at the bottom. Nothing in production starts until every engine item above it is done. The checklist, not enthusiasm, determines when production work begins.

## 5. Positioning

| Instrument | Relationship |
|---|---|
| Engine checklist (54 items) | This law is WHY the checklist is ordered engine-first, production-last. |
| Reversibility Rule | Production deploys are hard-to-reverse → gated. This law says WHEN the gate gets approached, not whether it exists. |
| "Don't Wait, Just Do" | Applies WITHIN the engine phase. It does not authorize skipping ahead to production. |
