# Hub Room Registry

| Order | Room | Contract | Status | Freeze rule |
|---|---|---|---|---|
| 01 | Your Intelligence Today | 01-YOUR-INTELLIGENCE-TODAY.md | SPECIFIED | Preserve once proven |
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
