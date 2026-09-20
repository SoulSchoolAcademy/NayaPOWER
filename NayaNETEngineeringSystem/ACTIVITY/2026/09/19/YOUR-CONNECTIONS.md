# Your Connections — Readiness Review — 2026-09-19

## Mission

Establish Your Connections as the canonical human-facing relationship projection shared by Smart Spaces, Smart List and Smart Mail.

## Architecture decision

**One subsystem, four surfaces:**
- Your Connections = WHO
- Smart Spaces = WHERE
- Smart List = HOW I ORGANIZE
- Smart Mail = HOW I COMMUNICATE

Smart Share remains the cross-cutting controlled sharing boundary.

## Canonical lifecycle

DISCOVERY → SPACE → JOIN → MEMBERSHIP → CONNECTION → COMMUNICATION / LIST → ACTIVITY → LEDGER

Reversal:

LEAVE / REVOKE → RELATIONSHIP RECALCULATION → COMMUNICATION / ACCESS DENIAL

## Governing distinctions

Interest ≠ membership.
Membership ≠ connection.
Connection ≠ unrestricted communication.
Communication ≠ intelligence access.
Membership ≠ private-data access.
Connection ≠ sharing authority.

## Current evidence

Existing Smart Space, Smart Mail, Smart List and identity/privacy contracts already describe the participating boundaries. Current production audits identify live Space, profile/identity, Mail, event and authorization primitives, but the complete relationship lifecycle is **not yet proven at the deployed product surface**.

No canonical relationship/contact store has been declared by this review.

## Readiness

**Architecture: DEFINED**
**Implementation: UNKNOWN**
**Authenticated lifecycle: NOT PROVEN**
**Two-user isolation: NOT PROVEN**
**Cloudflare parity: NOT PROVEN**

## Required proof

Create Space → activity → discover → join → membership persistence → connection eligibility → connection projection → Mail/List use → activity/ledger consequence → leave/revoke → communication/access denial.

## Next action

Inspect the existing production identity/profile, Space membership, Mail eligibility, List membership and canonical event primitives and select the smallest existing substrate for the relationship lifecycle. Do not create a contact table until that inspection is complete.
