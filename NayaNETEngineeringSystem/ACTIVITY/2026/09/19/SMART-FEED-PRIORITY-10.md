# SMART FEED — PRIORITY-10 EXECUTION PLAN — 2026-09-19

**Owner:** Smart Feed Naya  
**Objective today:** move Smart Feed from the pre-closure baseline to a fully operational, production-proven, visually finished feature without creating a second intelligence/event system.

## Execution command

> **Take Smart Feed to 10/10 today. Work back-to-back through the highest-value closure actions. Inspect source truth and live runtime before changing anything. Reuse the canonical cognition/intelligence/event substrate. Build capability first, prove it second. Never convert unknown to pass. After every action: record what changed, evidence, current score, remaining gap, and exactly one successor action. Do not stop at documentation, mock data, or code-complete.**

## Priority order

| # | Highest-value action | Completion proof |
|---|---|---|
| 1 | **Deploy the real `/feed` application surface and runtime bridge.** | Cloudflare production artifact serves `smart-feed.js`; source/build/runtime parity passes; desktop/mobile baseline passes. |
| 2 | **Execute authenticated Activity retrieval.** | Real authenticated member receives canonical events; unauthorized/no-session receives no data. |
| 3 | **Execute authenticated Personal retrieval.** | Owner-scoped intelligence is retrieved after authentication; private data never crosses the owner boundary. |
| 4 | **Establish explicit Collective publication and retrieval.** | One real owner publishes one owned cognition event by explicit consent; Collective retrieves only published intelligence; revoke removes it. |
| 5 | **Prove pagination and duplicate prevention.** | Page 1/page 2 have deterministic cursor progression and no duplicate canonical source IDs. |
| 6 | **Prove provenance/source drill-down.** | Every rendered item exposes canonical source ID, event lineage, classification/truth state, timestamp and source metadata. |
| 7 | **Prove authorized actions create canonical consequences.** | Save/favorite/like/love/publish produce durable canonical cognition/receipt evidence and survive refresh. |
| 8 | **Run two-user privacy denial.** | A→A allowed; B→B allowed; A→B denied; B→A denied, using legitimate authenticated users and server enforcement. |
| 9 | **Close every UI state.** | Auth blocked, loading, empty, stale/degraded, error, pagination end, action success/failure, mobile and reduced-motion states are truthful and polished. |
| 10 | **Final 10/10 closure audit.** | Source→build→deploy→runtime→human-use chain proven; no demo/local production path remains; scorecard reaches 10 only where evidence supports it. |

## Current execution state

### Completed today
- Real `naya-smart-feed` Edge Function deployed as **v2**, JWT verification enabled.
- Canonical Personal/Activity retrieval, Collective publication boundary, pagination, and governed interaction path exist.
- Production `nayanet_intelligence_publications` table created with explicit-consent publication and owner RLS.
- Dedicated `smart-feed.js` production surface created.
- Hub mounts the dedicated feed surface.
- Cloudflare release workflow now packages and verifies `smart-feed.js`.
- Production Cloudflare release **35453966388** passed:
  - exact artifact deployment
  - exact source/runtime parity
  - desktop baseline
  - mobile baseline
  - final runtime proof
- Live runtime parity is therefore proven for the deployed feed asset.

### Not yet proven
- Real authenticated browser/session execution of Activity, Personal and Collective.
- Two-real-user denial.
- Real Collective publication row and retrieval.
- Interaction receipt/ledger consequence observed end-to-end.
- No-duplicate pagination against real authenticated data.
- Final human visual approval.

## Score discipline

The earlier 3.2 score was the pre-backend-v1 audit. The current feature report had already moved to **4.7/10** after the real backend v1 existed. Today's deployment/parity closure materially improves the implementation state, but **does not justify 10/10** until the authenticated transaction proofs above pass.

**Rule:** score rises only from evidence, not from code volume.

## Success condition

`AUTHENTICATE → RETRIEVE → UNDERSTAND → AUTHORIZE → ACT → OBSERVE → VERIFY → RECORD → PRESENT → CONTINUE`

must work for all three Smart Feed streams while preserving one canonical intelligence/event substrate and the existing Intelligent Board visual language.
