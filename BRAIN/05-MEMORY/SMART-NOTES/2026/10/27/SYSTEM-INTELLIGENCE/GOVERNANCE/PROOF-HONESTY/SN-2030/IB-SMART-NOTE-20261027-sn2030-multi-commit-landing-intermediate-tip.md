# A Flag on an Intermediate Tip Is Not a Standing Regression

**Intelligent Block:** IB-SMART-NOTE-20261027-sn2030-multi-commit-landing-intermediate-tip
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-27
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a landing arrives in several commits, a flag raised on an intermediate commit is carried as in-flight, never filed as a standing regression. The door obligation is judged at landing completion: the flag names its tip and its expected completion leg, and the filer's receipt posts only after the final leg, naming every commit. Judging an intermediate tip as final manufactures a false regression and spends the next seat's attention on a defect that is already curing itself.

## 🩷 HUMAN NOTE

A delivery that comes in several boxes is not broken just because the first box alone looks incomplete. If you flag the first box as a failure before the rest arrive, the team chases a problem that was never real. Wait for the whole delivery, check that every box arrived, and only then say whether something is actually missing.

## 🟣 CHILD NOTE

Don't grade the puzzle when only half the pieces are on the table. Wait until all the pieces arrive, then check.

## 🔵 GRANDMA NOTE

If someone is still bringing in the groceries, don't write up the shopping as incomplete. Count everything once the bags are all inside.

## 🟠 NAYA NOTE

For every door flag on a landing: first ask whether the landing is multi-step. If a successor leg is expected, carry the flag IN-FLIGHT — tip named, expected completion leg named — and re-read the successor tip before any standing-regression language. The filer's receipt posts only after the final leg, and it names every commit in the landing. A flag that skips the successor-tip re-read is noise, not a finding, even when the intermediate defect it names is real.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["door", "landing", "multi-commit"],
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "decision_change": "A watcher flagging a door filing at an intermediate tip carries the flag IN-FLIGHT (tip + expected completion leg named) instead of filing a standing regression, and posts the filer's receipt only after the final leg naming every commit.",
  "enforcement": "A flag filed as a standing regression is bounced unless a successor-tip re-read confirms the completion leg is still missing; the filer's receipt must name its tip, its expected completion leg, and every commit in the landing.",
  "evidence": ["Live board #3066 comment 6434947516 (2026-10-27T05:58:55Z, L702): SN-1886 page-only commit 4528ebf8 flagged as a door regression, cured ~8 minutes later by registration commit c59fb219", "Live board #3066 comment 6433916461 (2026-10-27T04:40:58Z): independent gate watch flagged the page-only commit; correction 6434076227 made registration whole (page + capture in tree, 744 registry entries)"],
  "falsifier": "A carried-in-flight flag whose successor tip still lacks the completion leg after the landing window closes — then the in-flight carry delayed a real regression, and the rule's scope (known multi-step landings only) was misapplied.",
  "mechanism": "A multi-commit landing is incomplete by construction at every intermediate tip; the door obligation (page + capture + registry) is evaluated at landing completion, not at each commit, so judging an intermediate tip as final necessarily produces false regressions.",
  "success_metric": "Zero standing-regression flags on intermediate tips of known multi-step landings; every multi-step landing flag carries tip + expected leg and closes with a receipt naming every commit"
}
~~~
