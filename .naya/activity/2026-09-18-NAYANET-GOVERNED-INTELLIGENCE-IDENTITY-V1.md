# 2026-09-18 — Governed Intelligence Identity Protocol V1

## Result

Built the first executable 13-question identity/provenance envelope for NayaNET intelligence actors.

### Machine fields

WHO ARE YOU? → identity_id  
WHAT ARE YOU? → actor_class  
WHO CREATED / DELEGATED YOU? → who_created_or_delegated  
WHAT DO YOU KNOW? → knowledge  
WHAT CAN YOU DO? → capabilities  
WHAT ARE YOU AUTHORIZED TO DO? → authority  
WHO AUTHORIZED THAT? → authorized_by  
WHAT DID YOU RECEIVE? → received_artifacts  
WHAT PROVENANCE CAME WITH IT? → provenance  
WHAT CAN YOU DELEGATE? → delegation  
WHAT DID YOU ACTUALLY DO? → actual_actions  
WHAT HAPPENED? → outcomes  
WHAT DID YOU LEARN? → learning

## Safety properties

- UNKNOWN actors are blocked for consequential activity.
- Delegation requires explicit authority and a chain.
- Knowledge claims require source references.
- Received artifacts require source provenance.
- Actual actions require execution receipts.
- Outcomes require evidence.
- Learning requires identifiable sources.
- Capability without explicit authority is invalid.
- The envelope has a deterministic SHA-256 identity fingerprint.

## Architectural boundary

This does not replace:
- NayaNET account identity;
- the canonical identity registry;
- NayaPOWER Authority Registry;
- Smart Ledger;
- PIS.

It is the connective governance envelope between those systems.

## Next action

Bind this envelope into the existing Universal Execution Gate and persist the full governed identity fingerprint in Smart Ledger execution receipts.
