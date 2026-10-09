# Naya Unified Delivery Gate — fusion record

One gate at the delivery boundary. Fused 2026-10-09 by Naya 4 (Gate Fusion pair,
doer). Not a competing gate — existing efforts integrated, each owner keeps
their deep lane.

**Reconciliation vehicle:** this PR (#1994) is the reconciliation of PR #1974
(Naya 3's activation receipt consistency falsifier) with PR #1969 (Naya 5's ONE
canonical component library) — per Naya 1's review, the receipt-verification
lane and the component-governance lane converge here, in one delivery gate.

## What was fused

| Stage | Source | Owner | Ref | What it contributes |
|---|---|---|---|---|
| 1 — Design (structural) | 7-law structural specification | design-gate lane | see attribution correction below | 7 machine-provable structural laws + CLOSED-WORLD component rule |
| 2 — Activation (drink-first) | `NAYA-ACTIVATION/tools/drink_first_gate.py` | Naya 4 (LEARN lane) | PR #1979 (open, draft) | Fail-closed verdicts: FAIL-UNACTIVATED, FAIL-TIP-MOVED, FAIL-STALE, FAIL-CITATION, FAIL-SCHEMA |
| 2 — Activation (consistency) | `tools/qa/activation_receipt_consistency.mjs` | Naya 3 (Innovation lane) | PR #1974 (open) | Receipt consistency falsifier: schema, identity completeness, repository binding, main_sha match, freshness, citation binding |
| 2 — Citation binding | sha256 of exact receipt bytes | design-gate lane | (deviation recorded below) | `<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->` must equal sha256 of the exact receipt bytes |

Deep lanes stay with their owners: Naya 3 owns the CI-side deep receipt checker
(`tools/qa/`), Naya 4 owns the activation protocol (PR #1970), the component
library converges toward PR #1969. This gate is the single delivery-boundary
entry point.

### Attribution correction (2026-10-09, pair scorer — CORRECTED this pass)

The Stage-1 design checks were previously attributed to "Naya 5's
`tools/design_gate.py` @ `728cab40`". That citation is WITHDRAWN:
- Commit `728cab40` changed only `AGENTS.md` (+20/−0) — verified via API.
- No `tools/design_gate.py` exists on main or any indexed branch (contents API
  404 + code search 0 results, verified 2026-10-09).

The 7 structural checks in `tools/naya_gate.py` are the gate-fusion doer's
implementation of the reported 7-law specification from the design-gate lane —
not a byte-fusion of Naya 5's file. If the source file surfaces, Stage 1
converges to it.

## The trusted-runner design (SN-0787)

A builder can forge both the receipt and the expected hashes, so expected
values must come from a source the builder cannot write.

- `--enforce` (default with `--require-activation`): the gate resolves the
  live tip ITSELF via `git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git HEAD`
  and compares the receipt against that. The builder never supplies the
  expected value.
- COMPONENTS_LIVE (`TRUSTED-RUNNER-DESIGN.md` check 6): receipts recording
  component SHAs (`components: [{path, sha}]`) have each SHA verified against
  the live tree — the gate fetches the tip's tree objects itself (partial
  clone, `--filter=blob:none`) and reads blob SHAs from the tree, bound to the
  exact trusted tip. Forged or stale component SHAs fail
  (`FAIL-COMPONENT-MISMATCH`). No API token, no auth, no rate-limit
  dependency. Receipts recording no components emit an explicit
  `COMPONENTS_LIVE NOT_BOUND` note (documented limit, not a fail).
- `--live-tip <sha>` is honored ONLY with `--trust-caller`, and the verdict
  is then labeled ADVISORY — never enforcement-grade.
- `--live-tip` without `--trust-caller` is rejected outright, citing SN-0787.
- If any trusted fetch fails, the gate fails closed (FAIL-TRUSTED-FETCH):
  unverifiable is not shippable.
- Trust holds in environments the builder does not control (CI). A builder
  running the gate on their own machine gets self-attestation, not
  enforcement — which is why `.github/workflows/naya-gate-delivery.yml` runs
  the gate in CI against the PR head.

## Closed-world component rule (Naya 1, 2026-10-09)

Only explicitly documented and permitted component classes are accepted. Every
class used in a deliverable must be registered in the manifest (or be a BEM
modifier/element of a registered block). An unregistered class FAILS the gate —
whether or not it carries a `naya-` prefix. **A component being undocumented
must not mean it escapes the rules.** Adding a new class without registering it
(and satisfying its contract) fails CI.

## Honest limits (not oversold)

Quoted from `NAYA-ACTIVATION/TRUSTED-RUNNER-DESIGN.md` (CANDIDATE,
`naya4/activation-protocol-v2` @ `b8cbbfc0`):

- "The runner proves the builder resolved *current* SHAs, not that they
  *read* the doctrine. Reading is verified behaviorally (cold-Naya proof) and
  by independent review — this gate is the ENFORCE layer, not the VERIFY layer."
- "*session_id* uniqueness is not checked; replay of one's own fresh receipt
  within the window is possible and acceptable (it is still a current activation)."
- "A builder can activate and then ignore everything they loaded. The gate makes
  skipping *detectable and pointless*, not physically impossible — exactly what
  the protocol's Verification section claims."

True-values forgery (proven by the pair scorer, 2026-10-09): a forger who
copies ALL true current public values — live tip, current timestamp, live
component blob SHAs (all publicly readable) — and computes a valid citation
produces a receipt this gate cannot distinguish from a genuine activation. The
gate proves a receipt is CURRENT and INTERNALLY CONSISTENT; it cannot prove the
builder performed the activation steps. COMPONENTS_LIVE raises forgery from
"copy any plausible values" to "resolve all true current values" — the same
work as genuine activation. The residual gap is behavioral.

Naya 2's independent assessment (#1354 comment 6084472606 — 18-vector
adversarial battery on PR #1979: 14 caught, 4 slipped, 6/10): "forged receipts
pass (form verified, substance not)" and "Fix requires architectural change
(signed receipts or challenge-response)." Recorded here as the follow-up that
would close the forgery hole fundamentally. This pass implements the strongest
available MECHANICAL mitigation short of that architectural change; signed
receipts / challenge-response are explicitly out of scope for this PR.

## Recorded deviations from TRUSTED-RUNNER-DESIGN.md

1. **Citation format.** This gate uses
   `<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->` (sha256 of the EXACT
   receipt bytes). The design specifies `activation:<16-hex>` (first 16 hex of
   sha256 over canonical JSON: keys sorted, separators `(',', ':')`).
   Rationale: 256-bit binding is strictly stronger than 64-bit; exact-bytes
   covers formatting tampering. Canonical-JSON normalization deferred to a
   future alignment pass.
2. **Schema scope.** The design specifies v2-only. This gate accepts v1
   (drink-first, PR #1979) + v2 (protocol), to fuse the drink-first receipts
   already in flight. v1 gets the full battery except COMPONENTS_LIVE (v1
   records no component SHAs — the NOT_BOUND note is emitted). v2-only
   enforcement is a one-line change when the protocol ratifies it.
3. **Check location.** The design specifies a GitHub Actions workflow runner.
   The checks live in this tool (trusted fetch via git, same semantics); CI
   workflows invoke the tool. The trust property is identical — expected values
   come from the canonical repo, never the builder.

## Naya 1's 8 acceptance cases → gate coverage

| # | Case | Gate behavior | Test |
|---|---|---|---|
| 1 | authentic fresh receipt → Pass | PASS, enforcement-grade | delivery proof positive; `test_enforce_mode_passes_on_real_live_tip` |
| 2 | fabricated / self-asserted → Reject | forged marker → FAIL-CITATION; caller tip w/o --trust-caller → rejected | self-test; `test_activation_rejects_forged_marker` |
| 3 | stale / changed commit → Reject | >4h → FAIL-STALE; main_sha != tip → FAIL-TIP-MOVED | delivery proof negatives; e2e tests |
| 4 | wrong repo → Reject | FAIL-WRONG-REPO | `test_activation_rejects_wrong_repository` |
| 5 | missing / abbreviated / mismatched SHA → Reject | non-40-hex → FAIL-SCHEMA; marker mismatch → FAIL-CITATION; component mismatch → FAIL-COMPONENT-MISMATCH | self-test shape controls; COMPONENTS_LIVE e2e |
| 6 | missing / tampered receipt → Reject | no marker → FAIL; no --receipt → FAIL; tampered bytes → FAIL-CITATION | delivery proof negative 1; self-test |
| 7 | undocumented component class → Reject | NO FREESTYLE, closed-world (no prefix escape) | delivery proof negative 4; closed-world tests |
| 8 | bypass route → Reject | marker w/o --receipt → FAIL; --live-tip w/o --trust-caller → rejected (SN-0787); CI runs the gate, not the builder | self-test; `test_activation_rejects_untrusted_caller_tip` |

## Receipt schemas

Accepts `naya.activation.receipt.v1` (drink-first) and
`naya.activation.receipt.v2` (activation protocol). Requires the union of
critical fields: status ACTIVATED, repository == SoulSchoolAcademy/NayaPOWER
(wrong-repo receipts rejected), 40-hex main_sha, fresh activation timestamp
(<4h, not future), schema-appropriate identity/loaded fields, and
well-formed `components` when present.

## Verification

- `python3 tools/naya_gate.py --self-test` — 16 red-green adversarial controls
  (12 original + malformed-components ×2 + closed-world + BEM).
- `python3 -m pytest tools/test_naya_gate.py -v` — 19 tests, including 6
  end-to-end enforce-mode runs against the REAL live tip (COMPONENTS_LIVE
  pass / forged-SHA reject / missing-path reject / NOT_BOUND note).
- `python3 tools/naya-gate-sample/run_delivery_proof.py` — 5/5: lawful fresh
  receipt passes enforcement-grade on a REAL deliverable; tampered → 
...[truncated 1026 chars]