# The Chain Tests a Step It Never Performs — CANDIDATE Has No Path to ACTIVE
SN-813 · SYSTEM-INTELLIGENCE / LEARNING-PIPELINE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

The T11 learning chain lost its first honest lesson at the final step, and the lesson itself was never broken: it arrived as CANDIDATE (honestly unverified), the chain saved it, checked it, filed it, and linked it — but nothing in the entire chain ever flips the label from CANDIDATE to ACTIVE, while the lookup step only accepts ACTIVE or SUPERSEDED. The first candidate to ever walk the whole chain was therefore guaranteed to fail at retrieval. The durable rule: **every lifecycle state your pipeline produces must have a named step that can leave it — if a gate tests a transition the chain never performs, the failure is in the chain's design, not in the item.** The diagnostician also recorded two honest side-findings: the SN-782 number collides with another claim (needs untangling — first claim stands), and the lesson's access-gated smart link is correct behavior for Scope PRIVATE, not a bug.

## HUMAN

Shawn — the lesson got saved perfectly, but a fresh mind couldn't read it back, and here's the honest root cause: the system files every new lesson as "unverified candidate," and the lookup only serves "active" lessons — but nobody, human or machine, was ever assigned the job of flipping that label after the checks pass. So the chain was testing a door nobody can ever open. It's not a broken lesson; it's a missing link in the chain. The fix (a real branch and draft PR, #2033) wires up that missing flip. Two side notes from the same report: the lesson's tracking number SN-782 got claimed twice by two different pipelines — that needs untangling, first claim wins — and the fact that its link is access-gated is correct, not a bug, because the lesson is private.

## CHILD

Imagine a library where every new book gets a red sticker that says "not checked yet." The librarians check each book carefully — read it, stamp it, put it on the right shelf, write down where it lives. But nobody has the job of peeling off the red sticker. And the front desk rule says "you can only borrow books without a red sticker." So no new book can ever be borrowed, even though every book was checked. The fix isn't a better sticker — it's giving someone the job of peeling it off after the check passes.

## GRANDMA

Sweetie, think of it like a passport office. You fill in the form, they check your papers, take your photo, file everything away — and then nobody ever stamps the passport. When you show up at the border, the guard says "no stamp, no entry." Your papers were perfect; the office just never had anyone whose job was the stamping. That's what happened here: the lesson passed every check, but the final stamp — the one that says "this one is verified and ready to use" — had no owner. Now someone is building that step.

## NAYA

When designing or auditing any capture→retrieval pipeline:

1. **Draw the lifecycle graph and name the owner of every transition.** CANDIDATE→ACTIVE, ACTIVE→SUPERSEDED — each arrow needs a step, a trigger, and an owner. An arrow with no owner is a guaranteed future failure at the gate that reads the target state.
2. **Never let a gate test a state the chain cannot produce.** The retrieval gate admitting only ACTIVE/SUPERSEDED while the chain only ever emits CANDIDATE is a design contradiction, not a data error. When a gate and a producer disagree on the state space, fix the chain, not the item.
3. **Distinguish three outcomes at retrieval failure:** broken item (fix or drop the item), missing transition (fix the chain — this case), correct denial (access-gated PRIVATE content staying gated is the system working). Misclassifying a missing transition as a broken item burns a good lesson.
4. **Treat number collisions as claims, not bugs in the content.** SN-782 was claimed by two pipelines; the fix is untangling the claim (first claim stands), not rewriting either note.

## MACHINE

```json
{
  "sn": "SN-0813",
  "class": "LEARNING-PIPELINE",
  "subcategory": "CAPTURE-DESIGN",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Every lifecycle state a pipeline produces must have a named step that can leave it: if a retrieval gate tests a transition the chain never performs, the failure is a missing link in the chain's design, not a broken item. Never gate on a state the producer cannot emit.",
  "worked_example": {
    "failure": "T11 canonical receiver run 37980089547: cold-successor-held-out FAILURE with AssertionError: CANDIDATE — workflow admits only ACTIVE or SUPERSEDED, contradicting lawful CANDIDATE capture",
    "root_cause": "no step anywhere in the chain flips CANDIDATE to ACTIVE after checks pass; the chain tests a step it never performs",
    "corrective": "draft PR #2033 (corrective branch, exact head 719adf6c8a02e149c8)",
    "side_findings": "SN-782 claimed twice (untangle; first claim stands); access-gated smart link on PRIVATE scope is correct behavior, not a bug",
    "board_comment": "#1354 6087997893"
  },
  "related": ["SN-782"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0813-migrated.*
