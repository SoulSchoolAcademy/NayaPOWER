# Interfaces

**Brain-level status: PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers).**

Owns projections and channels: Hub, MCP, APIs, GitHub, webhooks, A2A, SDKs, and future doors.

Interfaces enter the same governed substrate. They do not become second brains.

## Contents (4 files + this README = 5)

| File | Purpose |
|---|---|
| [0001-CHANNEL-CONTRACT-V1.md](./0001-CHANNEL-CONTRACT-V1.md) | Channel governance and connection rules |
| [0001-SMART-DOOR-CONTRACT-V1.json](./0001-SMART-DOOR-CONTRACT-V1.json) | Machine half of the Smart Door contract |
| [0001-SMART-DOOR-CONTRACT-V1.md](./0001-SMART-DOOR-CONTRACT-V1.md) | Human half of the Smart Door contract |
| [0002-SMART-DOOR-REGISTRY-V1.json](./0002-SMART-DOOR-REGISTRY-V1.json) | Smart Door registry |

## Key Principles

- One Brain. Many Doors.
- Every channel enters: `CHANNEL → IDENTIFY → AUTHENTICATE → AUTHORIZE → GOVERN → CANONICAL CAPABILITY → ACTION → RECEIPT → VERIFY → LEARN`
- Channels are projections/connectors, not independent intelligence authorities
- No channel may bypass the kernel governance sequence
- Channel-specific UI never becomes canonical state
