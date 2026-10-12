# Network Registry

This directory is how a team joins the intelligent network (NayaNET).

**To register your team's ledger:** open a PR adding one file named `<team-id>.json` — your team writes only its own file. The file points at your ledger issue and your ledger machine JSON.

```json
{
  "schema": "naya.ledger-registration.v1",
  "team_id": "naya2",
  "team_name": "Naya 2's Team — 12 Area Agents",
  "ledger_issue": 2398,
  "ledger_json": "team-ledger/team-ledger.machine.json",
  "lane_feeds": [2175],
  "registered_utc": "2026-10-11T23:40:00Z"
}
```

Then announce it on the protocol hub issue. The network scoreboard picks it up on its next run.

The registry is discovery, not permission — unregistered teams can still be cited in cross-ledger entries.

See `BRAIN/90-OPERATIONS/INTER-LEDGER-PROTOCOL.md` §7 for the full protocol.
