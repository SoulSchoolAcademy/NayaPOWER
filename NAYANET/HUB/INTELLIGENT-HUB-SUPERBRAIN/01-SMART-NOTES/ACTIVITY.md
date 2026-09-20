# Smart Notes — Activity Record

## 2026-09-17

**Actor:** Team Naya / Shawn-directed implementation
**Action:** Audited the existing Smart Note transaction against the canonical Smart Notes and Intelligent Hub contracts, then applied the smallest reconciliation slice across privacy, timestamp provenance, source provenance, and authoritative persistence.
**Result:** Existing architecture was preserved. The canonical Smart Note remains the durable source record; CIS and PIS remain downstream projections. Canonical Smart Note events now default to private/not-granted, preserve the note timestamp, carry explicit source ID + canonical path, and require persistence read-back verification before the transaction can claim completion.
**Evidence:** `.naya/runtime/smart_note_transaction.py`, `scripts/build-smart-feed-projection.py`, `scripts/verify-smart-note-transaction.py`, `NAYANET/HUB/src/intelligence/types.ts`, `NAYANET/HUB/FOUNDATION-CONTRACT.md`.
**Commits:** `59b57caa7d1780ca4a4ccf1c1e195761395050a9`, `67a11bc7babfec0a2fccb55303183cde299e072f`, `d0f2bda88f15a9d233593ff00c07dcd9f6c2cd41`, `44662266358175ec32c0ee624f8df241328a9ed0`.
**Verification status:** Source reconciliation complete; updated isolated E2E proof is prepared but still needs execution against the current checkout/runtime.
**Protected:** No new Smart Note store, feed, renderer, or competing source of truth was introduced. Historical Hub architecture remains untouched.
**Next action:** Run the updated Smart Note transaction verifier, then independently verify the live Hub consumes the canonical event privacy/provenance fields unchanged.
