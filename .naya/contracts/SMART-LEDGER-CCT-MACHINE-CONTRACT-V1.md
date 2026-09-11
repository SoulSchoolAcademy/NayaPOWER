# Smart Ledger / CCT Machine Contract V1

Status: CONTRACT DEFINED — RUNTIME NOT YET VERIFIED

## Purpose
This document defines the machine-facing contract boundary for Smart Ledger and Collective Chain Technology (CCT). JSON schemas define event shapes; this contract defines behavior that code must implement and tests must prove.

## Governing pipeline
`ACTION → LEDGER EVENT → EVIDENCE → VERIFICATION → VALUE → POINTS → LEVEL → CCT RELATIONSHIP → LEARNING`

## Invariants
1. A ledger event records that an event occurred; it does not claim that the event is valuable or true.
2. Evidence must precede `verified` state.
3. Value must reference a ledger event and its verification state.
4. Points are calculated from verified value events, never from raw activity alone.
5. Historical ledger events are not rewritten to change scoring rules.
6. Corrections and supersession are new events/relations.
7. Harm is a constitutional boundary and is not offset by positive points elsewhere.
8. Displayed member points use the V1 zero floor: `MAX(0, cumulative_calculated_points)`.
9. Member level is derived from verified contribution points and the locked V1 thresholds.
10. Smart Links expose a safe human-facing route to verified objects without exposing protected provenance.
11. Collective Chain connections do not imply truth; contradiction, uncertainty, and supersession remain representable.
12. CCT is not blockchain technology.

## Required machine components
- Smart Ledger Event Schema V1
- Verification Receipt Schema V1
- Value Event Schema V1
- Member Level Contract V1
- Smart Link Contract V1
- deterministic point calculation implementation
- deterministic level calculation implementation
- integrity/chaining implementation
- automated tests

## V1 level thresholds
1 Awakening Member: 0–49
2 Emerging Member: 50–149
3 Developing Member: 150–399
4 Advancing Member: 400–999
5 Five-Star Member: 1,000–2,499
6 Mastering Member: 2,500–5,999
7 Catalyst Member: 6,000–14,999
8 Luminary Member: 15,000–34,999
9 Visionary Member: 35,000–74,999
10 Ten-Star Member: 75,000+

## V1 value-event inputs
Meaningful Like +1; Helpful reaction +1; Save useful intelligence +2; Helpful Connection action +2; Useful comment +3; Meaningful Smart Space participation +3; High-quality reply +5; Useful Share +5; Smart Note +5; Smart List +5; Valuable curation +5; valuable Smart Space +10; exceptionally valuable Smart Note +10; verified downstream application +5 to +10; verified positive outcome +10 to +25; verified new Collective Intelligence +25 to +100+; exceptional verified collective breakthrough +100+.

These values are engine inputs, not immutable ledger facts. The calculation version must be recorded so future weighting changes do not rewrite history.

## Integrity contract
Each event may reference the previous event in its applicable chain and may carry an integrity hash or equivalent cryptographic proof. The implementation must make tampering detectable. The exact cryptographic mechanism remains an implementation decision and must be independently tested before being marked VERIFIED.

## Privacy contract
Protected actor references and internal provenance may exist for authorization, audit, abuse prevention, and revocation. They must not be exposed in collective intelligence objects or public Smart Links unless explicitly authorized by the privacy contract.

## Verification contract
`recorded` means only that the system recorded an event. `evidence_available` means evidence is attached/retrievable. `verified` means the verification rules accepted the evidence. `valued` means a value event was calculated from verified evidence. `applied` means downstream use was observed. `outcome_verified` means the claimed outcome itself has evidence.

## Test gate
No component is considered implemented merely because its source exists in GitHub. The implementation is complete only when tests pass and the exact runtime behavior is independently observed. Documentation and schemas establish the contract; they do not constitute runtime proof.
