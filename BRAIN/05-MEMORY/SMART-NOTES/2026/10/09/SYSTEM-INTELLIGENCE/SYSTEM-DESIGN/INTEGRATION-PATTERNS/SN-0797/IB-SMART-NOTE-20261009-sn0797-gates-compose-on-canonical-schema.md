# Gates Compose on the Canonical Schema — Never Invent a Parallel One

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0797-gates-compose-on-canonical-schema
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6084482355 ([STRUCTURAL GATE SUPPORT] — Schema mismatch found between the two gates, 2026-10-09T15:58:51Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes built two gates that could not compose. Naya 4's drink-first gate validates `naya.activation.receipt.v1` — matching the canonical `NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json` on main. Naya 5's design gate (`--require-activation`) validated `naya.activation.receipt.v2` — requiring `session_id`, `human_authority`, `job`, `proof_plan`, `gates`, `activated_at` — a schema that exists nowhere on main. The mismatch was found the honest way: a unified pre-delivery runner (`tools/pre_delivery_gate.py`, running drink-first THEN the design gate) was tested against both gates on their branches, and it caught the integration hole mechanically. Verified on exact bytes: a lawful page with a valid v1 receipt → Stage 1 (drink-first) PASS → Stage 2 (design gate) FAIL with 8 schema violations. Two gates, one pipeline, mutually exclusive on schema alone.

The fix is not a compatibility shim — it's discipline: **the design gate's activation check must accept the canonical v1 schema.** A schema gets upgraded by upgrading the template itself through the proper channel; a lane never invents v2 in its own branch and silently forks the contract.

Why this is brain-grade: every lane invents its own schema for the same reason — the canonical one doesn't have the fields the builder wishes it had. But the moment two lanes disagree on the contract, every lawful input issued under the real contract becomes a false rejection, and the pipeline's enforcement is fiction. One canonical schema is what makes separately-built components compose. The composition test — actually running the components together on exact bytes — is what catches the fork before it ships.

Rule for a cold successor: **before validating a contract, read the canonical source first.** If the contract exists on main, you don't get to invent a parallel one — validate against the canonical schema, and route your upgrade proposal through the template itself. And build the composition runner: if two checks are supposed to run in sequence, test them in sequence on exact bytes; the schema fork hides until the components actually meet. Pairs with SN-0787 (receipts need a trusted runner — trusted state comes from the canonical source, never caller-supplied).

## 🩷 HUMAN NOTE

Shawn — a clean integration catch to bank. Two lanes built two gates for one pipeline: Naya 4's gate checks the canonical receipt schema (the real template on main), Naya 5's gate checked a v2 schema that exists nowhere on main. A builder with a perfectly valid receipt would pass gate one and fail gate two on schema alone — eight violations, nothing to do with the page. The honest fix isn't a shim between them; it's that the gate checks the canonical schema, and schemas get upgraded through the template itself, never by one lane forking its own version. The standing rule: read the canonical contract before you validate anything, and test components together before you claim they compose.

## 🟣 CHILD NOTE

Imagine two kids building one long train track. Kid A builds her half to match the official track piece in the box. Kid B decides the official piece isn't good enough and invents his own new connector — that doesn't exist in any box. When they join the halves, the trains can't cross: A's piece fits the box, B's piece fits only itself. The fix isn't a weird adapter — it's that B builds to the piece in the box, and if the box piece needs to change, the change goes through the box, not through B's bedroom. One canonical piece, or the track doesn't connect.

## 👵 GRANDMA NOTE

Grandma, think of two offices that share one form. Office A checks applications against the official form from headquarters. Office B quietly redesigns the form with new fields nobody else has. Every legitimate applicant who used the official form now fails at Office B — not because anything is wrong, but because the offices disagree on what the form is. The fix isn't a translator between the forms; it's that Office B uses the official one, and if the form needs new fields, headquarters issues them to everyone. One official form, or the offices can't work together.

## 🟣 NAYA NOTE

Mechanical rule for lane composition: (1) before validating any contract, read the canonical source on main — if it exists there, validate against it exactly; (2) never invent a parallel schema version in your own branch to get the fields you want — route the upgrade through the canonical template's own channel; (3) when two checks are designed to run in sequence, build the unified runner and test both against exact branch bytes before either claims composability — the fork is invisible until the components meet; (4) a schema violation on a lawful input is a contract defect, not an input defect — fix the contract, never shim the input. Do not solve composition by silently inventing a second receipt schema.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0797",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTEGRATION-PATTERNS",
  "doctrine": "gates-compose-on-canonical-schema",
  "rule": "Validate against the canonical schema on main; never invent a parallel schema in your own lane. Upgrade a schema by upgrading the canonical template through the proper channel. Test sequential components together on exact bytes (unified runner) before claiming composability.",
  "failure_mode": "lane invents v2 schema existing nowhere on main; lawful v1 inputs fail Stage 2 with schema violations; composition claimed without running the unified runner; compatibility shim hiding the fork instead of fixing the contract",
  "checks": [
    "validated schema matches the canonical template on main byte-for-byte (or a governed supersession of it)",
    "unified runner executes all sequential gates against exact branch bytes",
    "lawful canonical input passes every stage",
    "no invented schema version exists that main's template does not define"
  ],
  "pairs_with": ["SN-0787", "SN-063", "SN-0434"],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6084482355],
    "author": "SoulSchoolAcademy",
    "seat": "brain-build lane (structural gate support)",
    "timestamp": "2026-10-09T15:58Z"
  }
}
