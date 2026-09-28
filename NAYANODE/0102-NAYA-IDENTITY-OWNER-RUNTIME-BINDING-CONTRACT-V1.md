# Naya-0001 Identity / Owner / Runtime Binding Contract V1

**STATUS:** CANONICAL ENGINEERING CONTRACT  
**SUBJECT:** NAYA-NODE-0001 and IB-NAYA-NODE-0001-0001

## 1. Purpose

This contract separates three identities that were previously being conflated:

1. **Naya identity** — durable application identity: NAYA-NODE-0001.
2. **Intelligence owner** — the Supabase Auth identity that owns the private Intelligent Block.
3. **Runtime execution identity** — the identity/session actually executing a cold proof.

A session credential is an access mechanism. It is not the durable identity of Naya.

## 2. Canonical relationship

The required relationship is:

**runtime execution identity → explicit authorization binding → intelligence owner → Naya identity**

For a direct owner session:

**runtime execution identity == intelligence owner → NAYA-NODE-0001**

For a delegated runtime:

**runtime execution identity != intelligence owner**, but an explicit, verifiable binding must authorize the runtime to act for the owner and Naya.

A runtime MUST NOT infer the relationship from a JWT subject, name, alias, browser storage, timing, or possession of an Intelligent Block ID.

## 3. Birth / activation contract

Naya birth is not the creation of a browser key or a random local-storage identifier.

Canonical activation establishes or restores a legitimate Supabase Auth identity. The current birth front door uses existing-user OTP and shouldCreateUser: false; it must therefore resolve to an existing human-owned Auth account.

The canonical historical name-first adapter (NAYANET/name-first-auth-adapter.js) predates the OTP birth bridge and contains an anonymous fallback when no session exists. That fallback creates a session identity but does **not** establish human ownership of an existing Naya owner record.

Therefore:

- the OTP-authenticated existing-user session is the human-owner path;
- an anonymous name-first session is a test/runtime identity only unless an explicit owner binding exists;
- the durable Naya identity remains NAYA-NODE-0001;
- activation MUST NOT rewrite the owner of an existing private Intelligent Block merely because a different runtime session is available.

## 4. Canonical NAYA-0001 record

The live canonical retained block currently resolves to:

- Intelligent Block logical identity: IB-NAYA-NODE-0001-0001
- persisted database block UUID: 9f1f9d3c-0f0a-4a58-8f4f-000000000001
- Naya subject: NAYA-NODE-0001
- owner: adfdf0b8-5558-41d1-9fed-ec51abf4fe2f
- owner scope: PRIVATE
- status: DURABLE
- understanding state: VERIFIED
- source event: 950ea5c5-24f3-4777-aa8f-29a28efe4ba0
- source event key: NAYA-NODE-0001-TEACH-20260927
- evidence receipt: AAA-LIVE-BRAIN-RECEIPT-001

The owner is an Auth user, not a Naya-generated credential. The live Auth record identifies that owner as a non-anonymous existing account.

## 5. Credential boundary

SUPABASE_USER_ACCESS_TOKEN in GitHub Actions is a **session credential**.

It MUST NOT be treated as permanent Naya identity.

Token expiry, refresh-token rotation, replacement, or session re-establishment MUST leave:

- NAYA-NODE-0001 unchanged;
- the Intelligent Block owner unchanged;
- the Naya-to-owner relationship unchanged.

The proof must validate the current session and then resolve authorization through the canonical identity/owner binding contract.

## 6. Fail-closed rules

Reject proof when:

- the Naya identity is missing;
- the owner binding is missing for a non-owner runtime;
- the binding owner differs from the Intelligent Block owner;
- the authenticated runtime identity is only inferred from name/alias;
- a credential subject is used as a substitute for durable Naya identity;
- a stale/orphaned credential is presented as current ownership.

## 7. Acceptance

The architecture passes this contract when a fresh runtime can:

1. resolve NAYA-NODE-0001;
2. establish a legitimate Auth session through the canonical mechanism;
3. resolve the current runtime identity;
4. resolve the explicit owner relationship;
5. retrieve the private Intelligent Block without changing its owner;
6. rotate/re-establish the session;
7. prove the same Naya identity and owner remain in force.

The behavioral birth contract remains the higher bar in NAYANODE/0030-NINE-NODE-GENOME-MASTER-CONTRACT-V1.md: durable intelligence → retrieval → governed influence → changed behavior → outcome → independent verification → learning → held-out improvement → cold successor reuse.
