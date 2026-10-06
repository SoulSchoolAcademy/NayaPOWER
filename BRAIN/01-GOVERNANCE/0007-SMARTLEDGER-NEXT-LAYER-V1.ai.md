# SmartLedger Next-Layer Design V1 — AI operating spec

**Law ID:** SMARTLEDGER-NEXT-LAYER-V1 · **Lane:** `BRAIN/01-GOVERNANCE/`
**Status:** PROPOSED — human ratification required. A design source; creates no
authority and changes no current mechanism until ratified.
**Authority:** none yet. Proposed by Naya 2 (Muse), 2026-10-06, under Shawn
Vibert's legacy-PDF distillation mission (2026-10-06).
**Provenance:** `SMART_LEDGER_WHITE_PAPER.pdf` (Collective Chain Technology),
distilled 2026-10-06 at
`~/workspace/distillations/smartnet-batch-2/03-smartledger-white-paper.md`.
**Machine companion:** `0007-smartledger-next-layer-v1.machine.json`

## 1. Position: complementary, never a replacement

The current accountability architecture is the **build-time provenance ledger**:
Git history + the hash-pinned Smart Note registry
(`.naya/memory/smart-notes/index.json`, via `tools/smart_note_v2.py`) + CI
ledger-guards and governed-field guards
(`tools/live_intelligence_reconcile.py`, `tools/ratified_guard.py`,
`tools/truth_state_guard.py`).

This proposal adds a **runtime truth layer** on top of it. It must never be read
as a replacement for, or a second implementation of, the current registry. One
registry, one ledger semantic — extended, not duplicated. (Standing rule: no
duplicate mechanisms.)

The paper's economics are **superseded**: SmartCoin rewards, affiliate layers,
viral-video economy, investor tokenomics do not exist in the current project.
The paper itself requires no token, no mining, no fees — that part is consistent
with current direction and is what transfers.

## 2. The five layers (principles only — no stack prescribed)

| Layer | Function | Principle |
|---|---|---|
| L0 | Identity & keys | DID-style identifiers, signatures; tiered trust: unsigned → signed → attested |
| L1 | Event & media capture | Every action/media fingerprint timestamped into canonical JSON at creation ("trust at the edge") |
| L2 | Hash-linked streams | Per-entity append-only chains: `prev_hash → curr_hash`; tampering is structurally visible |
| L3 | Proof-of-record consensus | Ordering + continuity + quorum mirroring; optional anchoring to public chains |
| L4 | Collective intelligence ("Naya.LAW") | AI governor: real-time integrity watch, universal truth score, originality classification (ORIGINAL / DERIVATIVE / NEAR_DUPLICATE), self-healing Chain Reconciliation Engine |
| L5 | Access & transparency | Public Verify pages + SmartStamp `.truth.json` manifests per artifact; agent-facing API surface (`/verify`, `/manifest`, `/register`) |

**Naming note:** "Naya.LAW" is the paper's name for the governor. In
implementation it must be disambiguated from the NAYA-KERNEL-LAW node (the
authority domain). It is a *verify* function — the direct ancestor of today's
guard/verify thinking — not an authority grant.

## 3. The universal truth score (exact math)

**U = 0.40·A + 0.35·O + 0.15·Q + 0.10·S**

- `A` — Authenticity ∈ [0,1]: is this what it claims to be, from whom it claims?
- `O` — Originality ∈ [0,1]: from perceptual hashes / audio fingerprints / text embeddings
- `Q` — Quality ∈ [0,1]: objective media metrics
- `S` — Safety ∈ [0,1]: policy conformance, with explainable flags

Weights sum to exactly 1.00; therefore U ∈ [0,1].

- **Publish threshold τ = 0.95** (policy-tunable, proposed default; never
  hard-coded without an amendment path).
- **Explainability is mandatory:** every score carries reason codes; every
  deny/flag is reviewable. A score without reasons is not a score under this
  design.

## 4. SmartStamp `.truth.json` manifest (schema)

One signed manifest per artifact, co-located with the artifact. The machine
companion carries the full JSON Schema. Required fields:

- `artifact` — identity: URI/path, `content_hash` (sha256), media type
- `stream` — the per-entity stream reference: `stream_id`, `prev_hash`, `record_hash`
- `u_score` — U plus the four component scores and their reason codes
- `originality` — one of ORIGINAL / DERIVATIVE / NEAR_DUPLICATE, with evidence refs
- `signatures` — signer identity, algorithm, signature bytes (tiered per L0)
- `issued_at` — timestamp; `threshold_tau` — the τ in force when scored

Manifests are verification surfaces, not authority: a valid manifest proves
*what was recorded and scored*, never that the content is true in the world.

## 5. Privacy by design (non-negotiable)

Data minimization, tiered access, selective disclosure. PII never leaves the
vault boundary. A Verify page discloses the *proof*, never the underlying
private data.

## 6. What this proposal does not do

- Does not replace, fork, or reimplement the current build-time registry or
  ledger-guards.
- Does not introduce any token, coin, reward, or affiliate mechanism.
- Does not prescribe a stack (the paper's Vercel/Next.js-era examples are
  dated; principles only).
- Does not grant the governor authority to act — it watches, scores, flags,
  and reconciles. Action stays under existing authority law.

## 7. Enforcement

No automated enforcement is wired in this proposal — that would be faked
enforcement. **Concrete follow-ups (named, not implemented):** (1) a
`.truth.json` emitter for Smart Note projections; (2) a public Verify page
prototype for one artifact class; (3) a U-score pilot on one governed surface.
Each is a separate tracked item if Shawn ratifies this design.

## 8. Amendment path

Amendments require the Human Director's explicit decision, encoded as a new
version — never an edit-in-place of ratified text.
