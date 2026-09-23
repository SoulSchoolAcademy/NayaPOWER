# Hub Room Registry

| Order | Room | Contract | Status | Freeze rule |
|---|---|---|---|---|
| 01 | Your Intelligence Today | 01-YOUR-INTELLIGENCE-TODAY.md | IMPLEMENTED | Preserve once proven |
| 02 | Your Reports | 02-YOUR-REPORTS.md | SPECIFIED | Preserve once proven |
| 03 | Intelligent Library | 03-INTELLIGENT-LIBRARY.md | SPECIFIED | Preserve once proven |
| 04 | Smart Connect | 04-SMART-CONNECT.md | SPECIFIED | Preserve once proven |
| 05 | Smart Ledger | 05-SMART-LEDGER.md | SPECIFIED | Preserve once proven |
| 06 | Your Connections | 06-YOUR-CONNECTIONS.md | SPECIFIED | Preserve once proven |
| 07 | Smart Lists | 07-SMART-LISTS.md | SPECIFIED | Preserve once proven |
| 08 | Smart Mail | 08-SMART-MAIL.md | SPECIFIED | Preserve once proven |
| 09 | Smart Spaces | 09-SMART-SPACES.md | SPECIFIED | Preserve once proven |
| 10 | Settings | 10-SETTINGS.md | SPECIFIED | Preserve once proven |

## Current implementation checkpoint
The canonical Hub source is NAYANET/HUB/index.html on main.

Current source inspection confirms the Hub already contains a middle-workspace mechanism named nayaIntelligenceWorkspace and room routing hooks. This registry defines the durable product contract that future implementations must obey rather than improvising new page architecture.

## Change control
Before changing an existing room:
1. Read the registry and target room contract.
2. Read the current implementation and current proof.
3. Make the smallest causal change.
4. Re-run Hub regression/proof gates.
5. Update room status only with observed truth.
6. Never use a later room as justification for deleting or weakening an earlier room.


### Room 01 implementation checkpoint — 2026-09-23

Observed implementation checkpoint:
- Canonical source: `NAYANET/HUB/index.html`
- GitHub implementation commit before main merge: `fcc454be72e26d5f295927520eee5c6c2e994f0a`
- Main merge commit: `74884cb69badf54fee2bff0398a3f452c6c74384`
- PR: #530
- Implementation state: **IMPLEMENTED, NOT YET PROVEN/FROZEN**
- Room 01 now renders a daily cockpit inside `nayaIntelligenceWorkspace` with Room Header, Today Pulse, What Changed, What Did I Learn?, What Matters Now?, What Should I Remember?, What Am I Missing?, Naya's View, and high-value actions.
- The implementation deliberately marks daily comparison, daily learning-event retrieval, governed priority, memory recommendations, and verified daily activity retrieval as NOT VERIFIED rather than fabricating them.
- No shell/right-rail redesign was bundled.
- Next evidence boundary: deploy this exact main source and run live browser proof before changing Room 01 status again.
