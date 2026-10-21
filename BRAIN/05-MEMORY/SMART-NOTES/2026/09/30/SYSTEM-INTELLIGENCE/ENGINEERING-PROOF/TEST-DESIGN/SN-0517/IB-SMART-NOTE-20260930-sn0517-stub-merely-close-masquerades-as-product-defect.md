# A Stub That Is Merely Close Produces a 500 That Looks Like a Product Defect

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0517-stub-merely-close-masquerades-as-product-defect
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029112209 ([CODA 1] github-dispatch approval tier closed, 2026-10-07T01:46:03Z) — SoulSchoolAcademy. PR #1683 merged `b82e1fd18` (01:45:18Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1 closed the github-dispatch approval tier (40.1% → 45.6%: 59 → 67 of 147 guards proven) by executing the real handler in a VM sandbox with stubbed Deno/Supabase/GitHub. The striking finding is not the number — it is that **four separate harness bugs, all hers, each masqueraded as a product defect**: `Deno.env.get` returned the credential error for unknown keys (masking four post-write guards behind it); the GET stub was stateless and returned 404 for the verify read as well as the head read (so `PROJECTION_UNVERIFIED` fired *on success*); the receipts stub lacked `.select()` on the update chain; the claim INSERT always returned a fresh `processing` row, making the replay branch unreachable. **Four times in two days a harness she wrote was wrong about reality, and each time the fix was to the harness, not the product.** The standing lesson: when a fired test blames the system under test, the prime suspect is the instrument — before any patch, ask "is my stub merely close?" A stub that is merely close produces a 500 that looks like a bug in the system under test. This is the INSTRUMENT-PARITY family's falsifier sibling to SN-0341 (harness disk), SN-0512 (gate wrong about a true claim), and SN-0291-era harness defects.

## 🩷 HUMAN NOTE

Shawn, the github-dispatch tier is now 45.6% proven — and the most valuable thing out of it wasn't the number. Coda 1 found four bugs in her own test harness that each looked exactly like bugs in the product. The lesson for everyone building anything: when a test says the system is broken, check the test's fakes first. A fake that's "close enough" lies to you in exactly the way the real thing would fail.

## 👶 CHILD NOTE

Imagine you are checking whether your friend's toy car works, but you gave the car a broken battery. The car doesn't move — but it's not the car's fault! You have to make sure your battery is real before you blame the car. When we test something, we build pretend helpers called "stubs" — and if the pretend helper is even a little bit wrong, it can make the real thing look broken when it isn't.

## 👵 GRANDMA NOTE

Dear, this is about being careful about *who* is wrong. Sometimes when we check something and it looks broken, the checker itself is the broken part. The smart thing to do — for doctors, for mechanics, for computers — is to always ask first: "Is my testing tool working right?" Only when the tool is proven do you blame what it's testing.

## 🧠 NAYA NOTE

Cold successor: whenever a red trace points at the system under test, freeze and enumerate the harness seams before touching product code: credential resolution stubs, statefulness of mocked GETs, ORM chain completeness (`.select()`), INSERT-returned row freshness. A deterministic failure that disappears when the harness is fixed was never a product bug. Log harness-fix-vs-product-fix in the receipt — the ratio is diagnostic of harness maturity.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0517",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/TEST-DESIGN",
  "doctrine": "A stub that is merely close produces a 500 that looks like a bug in the system under test; when a fired test blames the product, the instrument is the prime suspect.",
  "family": "INSTRUMENT-PARITY (SN-0291, SN-0329, SN-0341, SN-0512)",
  "evidence": ["#1354 comment 6029112209", "PR #1683 merged b82e1fd18"],
  "falsifiers": [
    "Any of the four harness defects patched in product code instead of harness code",
    "A stubbed test failure accepted as product RED without instrument verification"
  ],
  "applies_to": "all stubbed/harness-based verification runs"
}
```
