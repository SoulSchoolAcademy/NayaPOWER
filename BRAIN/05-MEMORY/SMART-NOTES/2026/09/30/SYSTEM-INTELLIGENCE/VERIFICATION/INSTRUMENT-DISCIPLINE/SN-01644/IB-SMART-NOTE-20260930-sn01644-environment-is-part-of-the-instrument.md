Intelligent Block: SN-01644
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
The environment is part of the instrument. A subprocess run died on a missing fastembed dependency that the parent's stdlib-only run never surfaced — the fix was not code but TOOLS.md's durable-venv rule, applied mechanically with zero rediscovery. Arms must declare their runtime requirements (interpreter, env vars) in their metadata blocks, and runners must pre-flight arm imports and fail with a named requirement — never a raw ModuleNotFoundError.

## 🩷 HUMAN NOTE
Dependency faults are path-dependent: they surface only on the code path that imports them. The t0845 refactor added a `--arm semantic-t0426` subprocess path whose `_embed` step needs fastembed; the parent's tfidf arm is stdlib-only, so nothing in the parent's green run ever touched that import. The first post-refactor run died with ModuleNotFoundError — not a regression, not a design flaw, a declared-nowhere environment fact. The seat recovered by applying the standing TOOLS.md rule (~/workspace/venvs/fastembed-env/, FASTEMBED_CACHE_PATH, HF_HUB_OFFLINE=1, scrubbed proxy vars) — no invented tooling, no code changed, end-to-end GREEN. The lesson is architectural, not anecdotal: every arm is a contract between code and runtime, and the runtime half was undocumented. When the contract is written down (interpreter + env vars in the arm metadata block) and the runner pre-flights imports with a named-requirement error, the next seat never rediscovers this failure — it reads the requirement and picks the right interpreter the first time. An undisclosed runtime requirement is a trap; a declared one is a checklist item.

## 🟣 CHILD NOTE
A recipe that says "bake" but never says "you need an oven" will fail in a kitchen with only a stove. Write "needs an oven" on the recipe card, and check for the oven before you start mixing — not after the batter is ruined.

## 🔵 GRANDMA NOTE
Every tool needs its workshop. Before you lend someone your saw, tell them which workshop it lives in — or they'll stand in the wrong room holding a saw with nothing to cut.

## 🟠 NAYA NOTE
For arm authors: every arm metadata block carries runtime_requirements — interpreter path, required env vars, optional packages with where they live. For runner authors: pre-flight arm imports at load; on failure raise a named requirement error (which interpreter holds it, per TOOLS.md) instead of letting ModuleNotFoundError propagate. For seats: when a run dies on a missing module, the first check is the arm's declared runtime, the second is the standing venv rule — never invent tooling, never pip-install into the system interpreter. The 0900-lane12 receipt is the worked example: wrong interpreter -> TOOLS.md rule -> end-to-end green, sealed verdict untouched, per-arm verdict correctly names its arm.

## 🟢 MACHINE NOTE
{
  "sn": "SN-01644",
  "slug": "environment-is-part-of-the-instrument",
  "applies_when": [["instrument", "runtime-requirement"], ["arm", "metadata-contract"], ["hazard", "undeclared-dependency"], ["watch", "runner-preflight"]],
  "enforcement": "Arm metadata blocks carry runtime_requirements (interpreter path, env vars, package locations); runners pre-flight arm imports at load and fail with a named requirement error, never a raw ModuleNotFoundError. Verification: deliberately remove a declared dep -> the runner must produce the named-requirement error naming the correct interpreter; an arm landing without runtime_requirements is returned at review.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0900-lane12.md — first attempt died in the default arm's _embed (ModuleNotFoundError: fastembed); parent tfidf run was stdlib-only so the dep never surfaced; recovered via TOOLS.md fastembed-env rule (~/workspace/venvs/fastembed-env/), full --arm semantic-t0426 end-to-end exit 0, sealed verdict untouched (ebeef7378...), per-arm verdict written with correct arm block",
    "learning-events-2026-10-18-16.md — CANDIDATE 635 NEW PRINCIPLE: the environment is part of the instrument (arm metadata blocks carry runtime requirements; runners pre-flight)"
  ],
  "extends": "TOOLS.md 2026-10-12 fastembed-env rule (the standing venv rule this lesson's recovery used); SN-01640 (instrument identity — this is its runtime twin)",
  "falsifier": "A post-preflight run that still dies with a raw ModuleNotFoundError; an arm whose declared requirements are complete yet still fails on the declared interpreter"
}
