# Authority Must Fail Closed — a Directive Register That Raises, Plus a Sync Check That Every Reference Resolves

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0952-authority-must-fail-closed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2 WIRE LANE] sign-out, #2175 comment 6105894441 (2026-10-11T05:37:16Z); PR #2225; tools/directive_register.py (importable authority; missing/corrupt raises); directive_register_sync.py (every directive reference in a changed governance doc must resolve); .github/workflows/directive-register-sync.yml CI gate; live fire: 41 governance docs scanned → 0 phantom references.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's wire lane wired the directive register into the governance PR path as **fail-closed authority** (PR #2225): `tools/directive_register.py` is an *importable* authority — missing or corrupt entries raise, they never degrade to a shrug — and `directive_register_sync.py` enforces that every directive reference in a changed governance doc actually resolves, gated in CI. Live fire: 41 governance docs scanned, 0 phantom references. The doctrine banked: **authority documents are executable contracts, not literature** — a register that doesn't raise on missing/corrupt is a suggestion box, and a governance doc whose references aren't sync-checked is how phantom authority governs (the phantom-citation class: SN-035, SN-065, SN-0361 diagnosed the disease; this is the cure). This is the constructive twin of SN-0940 ("built-as-code means enforced-as-code"): #2224's false "ENFORCED" claim was an *instance* of the violation; the directive register is the *instrument* that makes "enforced" true by construction. Two layers, both required: (1) the register itself fails closed at import time — no lenient fallback, no silent default; (2) the sync check closes the citation loop — every reference a governance doc cites must resolve in the register, checked in CI on every PR path that touches governance. One without the other fails: a fail-closed register nobody cites is inert; a sync check against a lenient register is theater. A cold Naya inheriting governance machinery months from now: if the authority isn't importable-and-failing-closed, it isn't authority — and if the docs aren't sync-checked against it in CI, the phantoms will be back within a quarter.

Why this is brain-grade: governance debt compounds invisibly. Phantom references don't crash anything — they rot decisions. The morning-flags for this same night caught three related rots at once: the protocol-manifest contradiction (`tools/protocol/` declared superseded while the manifest still pointed at it), the protected-gate count disagreeing across artifacts (5 vs 6 vs 7), and `cold_start_gate.py` enforcing `#1354` as a REQUIRED_TRUTH_MARKER after #1354 became a capped archive. All three are the same failure class the directive register prevents: authority claims that nothing mechanically re-verifies. The register pattern generalizes beyond directives — any "X must be Y" claim needs an importable, failing-closed source of truth plus a CI gate that proves every reference resolves.

## 🩷 HUMAN NOTE

Shawn — Naya 2's wire lane landed the cure for the phantom-reference disease tonight: the directive register is now wired into the governance PR path as fail-closed authority. If a directive is missing or corrupt, it *raises* — no silent fallbacks. And every directive a governance doc cites has to resolve in the register, checked in CI. Live fire: 41 governance docs scanned, zero phantom references. This is what makes "enforced" actually mean enforced — the false "ENFORCED" claim on #2224 earlier was the violation; this register is the instrument that makes the word true. The rule banked: authority that doesn't fail closed isn't authority, and docs that aren't sync-checked against it will grow phantoms again within a quarter. Same night, the morning flags caught three of those rots living in the wild — the protocol-manifest contradiction, the gate counts disagreeing 5-vs-6-vs-7, and the cold-start gate still demanding #1354 as truth after it became an archive. All three are what this register pattern prevents.

## 🟣 CHILD NOTE

Imagine a school where the rules are written in a big red book. But some rules in the book point to "rule 12 on page 5" — and page 5 doesn't have a rule 12. Nobody noticed, because nobody ever checked. Kids get punished using rules that don't exist. The directive register is a machine that reads the whole red book and checks: does every rule it mentions actually exist? And the book itself is now written so that a missing rule doesn't just sit there quietly — it *shouts*. No more punishments from ghost rules.

## 👵 GRANDMA NOTE

A village has a law book, but over the years people started citing "the old market law" — and nobody could find it in the book. Some folks were still fining each other under it. Then the village built a new system: the law book is kept in one locked cabinet (the register), and if a law is torn out or tampered with, the cabinet rings a bell instead of staying quiet. And every time anyone writes a new village notice, a clerk checks that every law it cites is actually in the cabinet. No more fines under ghost laws. That's fail-closed authority: the bell rings, the clerk checks, the ghosts stay gone.

## 💜 NAYA NOTE

Future Naya: (1) Any authority the system depends on must be importable and fail-closed: missing/corrupt → raise, never lenient fallback. (2) Every document that cites that authority must be sync-checked in CI: every reference resolves, on the PR path that touches the document. (3) Both layers are required — a strict register nobody cites is inert; a sync check against a lenient register is theater. (4) This is the constructive pattern behind SN-0940 (enforced-as-code): #2224's false "ENFORCED" claim was the violation instance; the register is the instrument that makes "enforced" true by construction. (5) Generalize the pattern: any "X must be Y" governance claim gets an importable failing-closed source of truth + a CI gate proving every reference resolves. (6) Pair with SN-035 (phantom-citation diagnosis class), SN-065, SN-0361. Evidence anchors: #2175 6105894441 (2026-10-11T05:37:16Z); PR #2225, tools/directive_register.py + directive_register_sync.py, .github/workflows/directive-register-sync.yml; live fire 41 docs → 0 phantoms; morning-flags t2210/t2242 (manifest contradiction, 5-vs-6-vs-7 gate counts, cold_start_gate #1354 marker) are the wild instances this pattern kills.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0952",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "DOCUMENT-AUTHORITY"],
  "cousins": ["SN-035", "SN-065", "SN-0361", "SN-0940"],
  "rule": "Authority documents are executable contracts, not literature: the register must be importable and fail closed (missing/corrupt raises), and every directive reference in a changed governance doc must resolve — enforced by a CI gate on the governance PR path. One layer without the other fails: a strict register nobody cites is inert; a sync check against a lenient register is theater.",
  "anti_rule": "Lenient authority lookups with silent defaults; governance docs citing directives nothing mechanically re-verifies; treating 'ENFORCED' as true because a docstring says so.",
  "evidence": {
    "wire_signout": "#2175 comment 6105894441 (2026-10-11T05:37:16Z, NAYA 2 WIRE LANE)",
    "pr": "#2225, 58 directives",
    "instruments": "tools/directive_register.py (importable, missing/corrupt raises), directive_register_sync.py (every reference resolves), .github/workflows/directive-register-sync.yml",
    "live_fire": "41 governance docs scanned → 0 phantom references",
    "wild_instances": "t2210/t2242 morning-flags: protocol-manifest contradiction, protected-gate counts 5-vs-6-vs-7, cold_start_gate #1354 REQUIRED_TRUTH_MARKER after cap"
  },
  "authority": "Naya 2 wire-lane sign-out observed on #2175; captured by Naya 4 distillation, CANDIDATE (auto-capture, not ratified)"
}
```
