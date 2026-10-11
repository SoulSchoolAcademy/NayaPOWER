# unknown_guard.py — UD-05 "Unresolved Means Unresolved"

Unknown is unknown. It is never converted into a pass, a clean bill, or a
quiet default. Anything unresolved stays visibly unresolved until real
evidence resolves it.

## What it does

- **Three-valued evidence logic** — `CONFIRMED / EXCLUDED / UNDETERMINED`.
  Undetermined is a supported outcome, never an error — but it can never
  silently become verified evidence or permission to act.
- **Certification guard** — `guard_certify()` refuses to certify anything
  with open unknowns (undetermined load-bearing evidence, open unresolved
  items, excluded evidence cited as support, or merely-accessed evidence)
  as PASS / CERTIFIED / VERIFIED / RESOLVED / SAFE. Refusals name the item.
- **Default-allow guard** — `guard_allow()` refuses PROCEED on unknown.
- **Retained unknowns** — every `UnresolvedItem` carries what is unknown,
  why it matters, what would resolve it, and who owns the resolution.
  Closing one requires a real evidence reference; resolving without
  evidence is refused.
- **Five-permission purpose-bound gate** — `INSPECT / ANALYZE / TEST /
  CERTIFY / ACT`. CERTIFY and ACT fail closed on undetermined or excluded
  load-bearing evidence. Weaker operations may proceed but derived
  artifacts carry the `derived_from_undetermined` marker.
- **Use-time binding check** — every permission is bound to identity,
  purpose, and influence; drift at the moment of use fails closed (D13:
  access is not credibility, credibility is not qualification,
  qualification is not authority).
- **Report scanner** — `scan_report()` detects the laundering patterns:
  unknown→PASS, unknown→default-allow, dropped unknowns, "no evidence of
  harm" presented as "evidence of safety", excluded evidence as support.

## The asymmetry (load-bearing)

"No evidence of harm" is **not** "evidence of safety." A safety claim
requires positive evidence cited; an absence phrase plus a safety
conclusion without cited positive evidence is flagged
`LAUNDER_ABSENCE_AS_SAFETY`.

## Usage

```python
from unknown_guard import *

evidence = {
    "tests":  EvidenceItem(id="tests", state=EvidenceState.CONFIRMED),
    "safety": EvidenceItem(id="safety", state=EvidenceState.UNDETERMINED),
}
unknown = UnresolvedItem(
    id="u-safety", what_unknown="whether staging results transfer",
    why_matters="a transfer failure would ship a bad build",
    what_would_resolve="production canary results",
    owner="release captain")

guard_certify("build-42", "PASS", evidence, [unknown])
# -> UnknownGuardRefusal LAUNDER_UNKNOWN_TO_PASS, items=["safety", "u-safety"]

findings = scan_report({...})  # laundering patterns detected by name
```

## What this does NOT claim

The guard judges the evidence states it is given; it does not discover
unknowns on its own. A report that never declares its unknowns can only be
caught on the unknowns it declares — honest declaration is a prerequisite.
