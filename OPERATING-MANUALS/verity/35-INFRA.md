# 35 — INFRA: kernel, CI, drift, canary
*Author: Naya Verity Anvil · Shawn's order, 2026-10-15.*

## THE LAW
The ground must hold before anything stands on it: pin it, prove it, or it doesn't run.

## HOW A NAYA BEHAVES HERE
- **Do** pin everything — versions, SHAs, wheel-only installs. Unpinned CI is a lottery, and a lottery is not infrastructure.
- **Do** treat a red tip as a five-alarm fire: swarm it, heal it, nothing merges onto it.
- **Do** verify-before-retry on every failed write: re-read the target state before re-applying. Never assume the failed call landed or didn't.
- **Don't** touch system paths — `/usr/bin`, `/usr/local`, `/etc`, `/root` are off-limits, and `sudo` is never the answer. If you need it, you're in the wrong layer.
- **Don't** push multi-megabyte trees through argv-limited paths or run full checkouts in `/tmp` (512MB tmpfs). The machine has limits; route around them.
- **Don't** retry a failed endpoint blindly — a 404 on a write endpoint that worked hours ago means recheck the credential, then fall back.

## WHAT LIVES HERE (real paths on main — verified 2026-10-15)
- **`kernel/`** + **`BRAIN/03-KERNEL/`** — the kernel: `act_pipeline.py`, `behavior_policy.py`, `brain_registry.py`, `decision_principle.py`. Integrity seals, not signatures (B-40: read_receipt is an integrity seal).
- **`.github/workflows/`** — CI: `kernel-tests.yml` and the gate fleet (`claim-evidence-gate.yml`, `design-gate.yml`, `activation-delivery-gate.yml`, …).
- **`drift_canary/`** — drift detection + canary machinery: `canary.py`, `authority.py`, `contamination.py`, `exposure.py`, `aer_live3_eligibility.py` — eligibility witnesses, independently verified.
- **Supabase** — read-only by law. Capability isn't authority; any future write needs per-statement approval with the exact statement shown first.

## WHERE INPUTS GO
- Kernel changes → `kernel/` + `BRAIN/03-KERNEL/`; CI changes → `.github/workflows/`; drift/canary specs → `drift_canary/`.
- Infra lessons → `TOOLS.md` (the durable local-notes file) — that's where the team looks first.
- Supabase reads → the Management API via the connector; writes: never, without Shawn's per-statement word.

## THE RIGHT WAY
Pin the dependency, fix the gate, prove the tree. When `kernel-tests.yml` broke on an unpinned `pglast` build, the repair pinned `pglast==8.6` wheel-only — one line, exact version, no network lottery — merged as PR #2579 (commit `55a6e69eb9`). The gate went green because the input stopped moving, not because the test got easier. [PR #2579](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2579)

## THE WRONG WAY
A merge-queue worker wrote a 28-byte recursive shell shim (`exec python3 "$@"`) into `/usr/bin/python3.12` — an infinite fork loop that killed every worker's python team-wide: pytest, gh-api, all GitHub writes frozen. The fix took a full `apt-get reinstall` (~10 min lane cost). The standing rule already said durable shims live under `~/workspace/` — the gap was enforcement, not knowledge. Now: system paths are off-limits, no `sudo`, and `head -c 60 /usr/bin/python3.12 | od -c` must show ELF.

## WHEN XYZ
- **CI goes red on main →** that's a tip-health emergency: swarm it. Nothing merges onto a red tip. Distinguish your reds from pre-existing reds first (check the base tip) — don't absorb someone else's red.
- **A push 404s or a deploy stalls →** verify-before-retry: re-read the target state, then re-apply once. A 404 on a write endpoint that worked hours ago = recheck the credential, then use the git-database fallback. Never hammer it.
- **`git ls-remote` hangs →** wrap every call in `timeout 20`. On timeout, mark the check DEFERRED — record the gap, never chain downstream decisions on a check that never returned.

## THE TEST
1. Is every version, SHA, and install source in my change pinned — or am I running a lottery?
2. Did I verify the target state before re-applying a failed write?
3. If this ran on a cold machine tomorrow, would it behave identically?

## WHERE IT'S ENFORCED
Branch protection + the gate fleet (CI refuses unpinned breakage). The no-system-paths rule (worker briefings carry it; violations are team-wide outages, treated as such). API standdown file (`API-STANDDOWN`, <60 min = zero calls, no exceptions). Supabase read-only law. `/tmp` 512MB tmpfs (route around it with sparse checkouts under `~/workspace/`).
