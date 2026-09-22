# 🔱 NayaNET Universal Agent Interface

STATUS: IMPLEMENTED / NOT YET LIVE-PROVEN
CONTRACT: ONE CANONICAL INTELLIGENCE CORE → MANY REPRESENTATIONS → ONE CANONICAL MEANING

This boundary exposes the existing NayaPOWER Project Intelligence runtime without creating another brain or event store.

Transports: REST/OpenAPI for deterministic application access; MCP for compatible agent clients.

Canonical operations: cold_restore, restore, retrieve, understand. `cold_restore` is the first-class 14-question Project Intelligence contract. Consequential UAI retrieve/understand actions perform `cold_restore` first, then delegate to the same authenticated `nayanet-compound-intelligence` runtime.

Security: incoming Bearer authorization is required and forwarded to the canonical runtime. Service-role credentials are never accepted from callers.

Proof required for production: transport → authentication → canonical runtime → persistence/retrieval → evidence/receipt → outcome. MCP additionally requires initialize → tools/list → tools/call → canonical result.


## Mandatory cold-start rule

Before a consequential Universal Agent Interface action, the adapter MUST resolve `NAYANET_COLD_NAYA_RESTORE_V1` and carry the resulting 14-question context into the proof record. A failed or incomplete cold restore blocks the action. This is a pre-action reconstruction boundary, not a second intelligence store.
