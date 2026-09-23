# ACTION 06 — SMART LIST + SMART MAIL RELATIONSHIP BINDING

**Date:** 2026-09-19  
**Owner:** Lead Naya  
**Supabase:** dahisasgpfvziswqvmvm

## DONE

Reconciled the live List/Favorite/Saved/Collection/Group inventory. No existing person-organization List primitive was found.

Implemented:
- `nayanet_smart_lists`
- `nayanet_smart_list_members`
- owner-scoped RLS
- idempotent List create/add/remove RPCs
- canonical Connection references only
- Smart Mail relationship gate in `nayanet_send_smart_mail_authorized`

Direct Smart Mail now requires:
**authenticated sender → mutual active Connection → current authority grant → existing idempotency/receipt path**.

## PROOF

Live production:
- `nayanet_smart_lists` exists, 0 persistent rows after transactional testing.
- `nayanet_smart_list_members` exists, 0 persistent rows after transactional testing.
- owner-scoped RLS exists.
- `nayanet_send_smart_mail_authorized` remains SECURITY DEFINER and retains authority validation.
- transactional List add + duplicate add returned `ALREADY_IN_LIST`.
- transactional Mail attempt without mutual Connection returned `RELATIONSHIP_REQUIRED`.
- no synthetic test state persisted.

## NOT PROVEN

- current Hub Smart List UI
- browser-authenticated List CRUD
- browser-authenticated Connections
- two-real-user mutual connection lifecycle
- browser Smart Mail after mutual connection
- attachment authorization under the new relationship gate
- Activity/Smart Ledger projection for List/Connection lifecycle
- Cloudflare parity

## DECISION

Smart List is organization only; it does not own relationship truth.

Direct Smart Mail requires mutual active canonical Connections in addition to authority.

Connection remains distinct from authority.

## BLOCKERS

Current browser/Cloudflare wiring is the remaining product-surface boundary.

## NEXT

ACTION 07 — ACTIVITY + LEDGER BINDING FOR MEMBERSHIP, CONNECTION, LIST AND MAIL CONSEQUENCES.
