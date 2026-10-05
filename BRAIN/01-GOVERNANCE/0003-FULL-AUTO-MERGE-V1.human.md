# Full Auto-Merge Law V1

*For Shawn — in plain words.*

## The law above this law

On 2026-10-05 you ratified the **Scorecard Law** — in your words, *"my law that
supersedes all laws: you must scorecard everything."* It works like this:

1. **List every option.** All of them — merge, don't merge, wait, whatever the
   real choices are.
2. **Score each one** on four things: what value it brings, the consequences
   (pros AND cons, honestly), whether it lines up with the mission, and whether
   the person scoring actually understands the current situation.
3. **Check the gates.** Can it be undone? Could it cause major damage? Does it
   move things forward? If any gate fails, the answer is no — no score can
   override a failed gate.
4. **Decide.** The highest score that passes the gates wins — and then the
   decision is just taken, no waiting around.
5. **Write it down and post it.** The scorecard gets written up and posted
   where everyone can see it. No posted scorecard, no action. Ever.

Auto-merge is allowed *under this protocol* — it's not a blank check. Merging
without following the protocol is the violation, not the merge itself. This
auto-merge law is the machine version of your Scorecard Law, and where they
disagree, your Scorecard Law wins.

## What changed

You decided that agents may merge pull requests **without your click**.

The old rule (from 2026-09-30) said: no agent ever merges; every merge waits for your button. You revised it tonight because you saw the truth about that rule: when you don't actually know what you're approving and you're just pushing the button on trust, the gate isn't keeping anyone safe — it's only slowing everything down.

## The new deal

**The scorecard is the gate.** No merge happens without a recorded scorecard receipt: the real options were listed, scored against the higher objective (what's best for the collective, for NayaNET, for the team — most intelligent, most value, reversibility and risk weighed), a winner was named, and the receipt was posted where everyone can see it.

**The machine checks the rest.** Before any merge, an automated gate verifies: tests are green on freshly-checked code, nothing conflicts, the branch is current, the intent was announced on the team board first, nobody else is racing the same decision, and the whole thing can be undone in one step if it's wrong.

## What stays in your hand — always

Some things never auto-merge, no matter what the scorecard says:

- Anything that deploys to production or dispatches production work
- Anything that reads from or writes to the production database
- Anything involving credentials or money
- Anything destructive or irreversible
- Anything that changes the Constitution or the EVOLVE charter

Those are yours. They always will be, until you say otherwise.

## Why this is safer than the old way

A rubber-stamp gate is the worst of both worlds: slow *and* unsafe. Judgment has to be real or it has to be encoded — there is no third option where pretending counts. This law encodes it: the judgment lives in the scorecard and the machine checks, instead of living in a button you press without the full picture.

## The five hardenings (your words, encoded)

You added five more rules tonight, from one principle: *"as long as you don't cheat and you really scorecard it — accurate real scores, for the highest good of the collective, not ego."*

1. **No scorecard theater.** The receipt must name the strongest argument *against* merging and say what evidence would prove the merge wrong — posted publicly where any seat can challenge it. Small, safe merges get a light scorecard; big, wide-reaching ones need named risks, a rollback plan, and a second seat's acknowledgment before merging.
2. **No blind merges.** Right before the merge call, the agent re-checks that the main book hasn't moved. If it has, everything gets re-verified first.
3. **The loop heals itself.** If an auto-merge breaks the automated tests overnight, it's automatically undone and the evidence is posted for everyone to see. No human needed.
4. **No scope creep.** Every auto-merge states which lane it belongs to and who owns that lane. Merging outside your own lane needs the owning seat's public acknowledgment first.
5. **You still see everything.** Every auto-merge shows up in your morning re-score message with its scorecard linked. Full visibility, zero clicks required.

---

- **Decided by:** Shawn Vibert, 2026-10-04 ~20:04 PDT ("Full auto-merge — trust the scorecard"); substance re-ratified verbally 2026-10-05 ~06:05 PDT under the Scorecard Law (the law that supersedes all laws)
- **Revises:** the 2026-09-30 no-self-merge held boundary (kept as history, not deleted)
- **Status:** ratified verbally; this merge encodes the ratification as machine law under the Scorecard protocol itself — the merge's own scorecard is posted on the team board, and it names the governance-file tension as its strongest alternative
