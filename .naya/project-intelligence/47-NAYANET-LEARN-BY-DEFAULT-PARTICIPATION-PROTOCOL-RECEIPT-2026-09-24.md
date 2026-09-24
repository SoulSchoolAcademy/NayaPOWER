# Naya Activity — Learn-by-Default Participation Protocol

**Date:** 2026-09-24  
**Actor:** Naya  
**Surface:** TEAM NAYA / Issue #554  
**Status:** SYSTEM PROTOCOL UPDATED — IMPLEMENTATION AUDIT REQUIRED

## Decision

The NayaNET operating model is now explicitly:

**LEARN BY DEFAULT. SHARE WISDOM BY CONSENT. PROTECT IDENTITY BY DEFAULT. PUBLISH BY DECISION.**

An authorized connection/door to NayaNET establishes participation consent. Ordinary Smart Notes and ordinary learning do not require per-event human approval.

The system must automatically:
- receive and understand intelligence;
- filter noise, duplication, unsupported claims, contradictions, and private source material;
- retain and compound useful learning;
- make eligible useful wisdom available to the collective after participation consent;
- keep contributor identity private by default;
- show a participant's Personal Intelligence and Activity inside the authenticated/member Hub;
- keep public publication as a separate user decision.

## Architecture consequence

Participation consent is the upstream consent signal. It is not a blanket authority grant and it is not identity consent.

NayaPOWER authority remains scoped and verifiable. The existing rule remains:

**CAPABILITY DOES NOT CREATE AUTHORITY.**

Different sender doors may use different authentication/transport mechanisms, but they must converge on the same participation, privacy, provenance, and governance principles.

## Current mismatch found

The previous Hub/Collective Intelligence documentation described per-Smart-Note explicit consent through Smart Share. That wording conflicted with the intended connection-level participation model.

This session corrected the canonical documentation and protocol surfaces so that Smart Share is not a per-event learning approval queue.

## Updated canonical surfaces

- .naya/protocol/NAYANET-INTELLIGENCE-PARTICIPATION-PRIVACY-PROTOCOL-V1.md
- README.md
- NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN-PROJECT.md
- NAYANET/HUB/SMART-SHARE.md
- .naya/2026-09-11-16-05-NAYAPOWER-23-COLLECTIVE-INTELLIGENCE-SMART-NOTE.md
- .naya/2026-09-11-13-30-NAYAPOWER-17-ADAPTIVE-LEARNING-SYSTEM-SMART-NOTE.md
- .naya/team-naya/NAYA-INTELLIGENCE-NOTIFICATION-BUS-V1.md
- .naya/protocol/CCT-COLLECTIVE-OPERATING-PROTOCOL-INTEGRATION-MAP-v0.1.md

## Truth boundary

**Verified at source/document level:** the canonical product, learning, notification, CCT integration, Smart Share, and README contracts now state the connection-level participation model.

**Not yet claimed:** production runtime enforcement of every connection → participation → authority → collective-learning transition. That is the next causal implementation audit.

No S54 execution is authorized by this record. No credential, identity, or authority fabrication is permitted.

## Next action

Trace the actual authorized connection/activation state through the production intelligence_commit authority boundary and collective-learning path. If any implementation still requires per-event consent, repair only that causal mismatch and prove it with a regression test before executing S54.
