# Edge-function type-check gate

## Why this exists

Deno edge functions under `supabase/functions/**` are **never type-checked by any
existing gate**. They are only ever executed inside Supabase, where a runtime error
becomes an HTTP status code with no stack trace and no cause.

That is not theoretical. `nayanet-prove-runtime` shipped a `stableJson()` call in its
`inspect` branch that was never imported. At runtime that is a `ReferenceError`,
which the handler's outer `catch` converts into a generic **HTTP 400** —
indistinguishable from a client sending a bad request. It surfaced as
`live-prove-proof` run 37384065800 failing with a bare `curl: (22) error: 400` and
no explanation, and it stayed labelled "root cause unknown" across lanes for days.

Worse, the unit tests for that function were green. Every assertion on the failing
seam regex-matched the handler's **source text** rather than executing it, so a green
check meant "the code looks right", not "the code runs".

The three failure modes this gate catches, all of which have shipped or nearly
shipped here:

| Defect | Production symptom |
|---|---|
| Undefined identifier (missing import/export) | opaque HTTP 400/500 |
| Wrong arity on a called function | silent wrong argument / crash |
| Condition that can never be true | dead safety guard — a check that never fires |

## What it does

Runs a real `tsc --noEmit` over every `.ts` file in `supabase/functions/**`, using
`remote-module.d.ts` to stub the Deno global and the `https:`/`npm:`/`jsr:`
import specifiers that only Deno can resolve.

Current result across all 14 functions: **0 errors**.

## What it deliberately does NOT do

- It is **not** a Deno emulator. Remote imports are typed `any` on purpose. Asserting
  real library types would be a much larger project with a much larger maintenance
  burden, and it is not where the production failures came from.
- It does not type-check with `strict`. Non-strict keeps the gate focused on the
  mechanical defect classes above rather than churning unrelated code.
- It does not replace execution. A green type-check is **not** proof a handler works —
  see the honesty note below.

## Proving the gate still has teeth

A gate nobody has seen reject anything is not evidence of anything.
`tests/edge-typecheck-gate.test.mjs` compiles three mutants against this exact config
and asserts the gate reports each:

| Mutant | Error | The shipped bug it stands for |
|---|---|---|
| unbound identifier | TS2304 | PROVE `stableJson` — opaque HTTP 400, run 37384065800 |
| wrong arity | TS2554 | verified-ai-action `idempotency_key` — inert replay guard |
| impossible condition | TS2845 | know.ts `=== NaN` — dead authority-expiry guard |

The mutants live in a temp directory that `extends` the real config, so they compile
against the real stubs and real strictness, and the repository is never mutated. If a
future change makes the gate permissive, this test goes red.

## Honesty: what this gate is and is not

This is a **static** check. It proves the code is internally consistent — no unbound
identifiers, no arity mismatches, no impossible conditions. It does **not** prove:

- the handler returns correct results for real inputs,
- the database schema matches what the code assumes,
- the deployed function matches this source.

A type-check is a floor, not proof. Promoting "tsc passes" to "the edge function is
verified" would be exactly the collapse of `IMPLEMENTED` into `VERIFIED` that
AGENTS.md forbids. Where a runtime proof exists, use it; this gate exists to make sure
a function can *reach* that runtime proof instead of dying on a `ReferenceError` first.

## Wiring

The gate runs from `tests/edge-typecheck-gate.test.mjs`, which the existing
`node --test tests/*.test.mjs` step in `.github/workflows/kernel-tests.yml` already
executes on every push and PR. It needs no workflow edit, so it cannot be lost to a
CI-config change and it cannot be skipped by editing the node/pytest steps.

An earlier draft added a dedicated `edge-typecheck` job to `kernel-tests.yml`. That is
still the better long-term shape — a separate job makes the gate independently
required and independently visible — but wiring it requires write access to
`.github/workflows/`, which the token used to land the repair does not have (GitHub
refuses OAuth apps without the `workflow` scope). That is a credentials gate, so it
is left for a human rather than worked around by weakening the gate.

To add it later, append to `kernel-tests.yml`:

```yaml
  edge-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "24"
      - run: npm install --no-save --no-audit --no-fund typescript@5.7.2
      - run: npx tsc -p tools/edge-typecheck/tsconfig.json
```

Keep it as a separate job. Do not merge it into the `test` job's steps, or a later
edit to those steps can quietly drop the gate.

To run locally:

```bash
npm install --no-save typescript   # optional; the test fetches 5.7.2 if absent
npx tsc -p tools/edge-typecheck/tsconfig.json
```

## Adding a new remote import

If a future function imports a symbol this stub does not declare, tsc will report
`has no exported member`. Add the symbol to `remote-module.d.ts` with an `any`-shaped
signature. Do not add the real library types — see scope discipline above.
