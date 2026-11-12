# SN-2113 — Red Is Information: Attribute the Failure Before You Blame Anything

**Status: VERIFIED ESSENCE — VERIFIED-WITH-CORRECTIONS (verifier-sep-1).** Distilled from 11 raw notes by the sep-1 maker seat; independently verified by a different seat (verifier-sep-1, block verdict PASS). Verifier item C1 (name SN-048's license-limited drops in the receipt) is discharged in the campaign landing receipt: byte-search of SN-048's page at the live tip finds no D6 timestamp rule and no SN-145 reference — nothing was dropped, because nothing was there to drop; recorded there with the evidence. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

A red badge is a conclusion about a run, not a diagnosis of the thing the run was checking — so classify the failure and name its owner (code, dispatch, guard, environment, platform, harness) before any repair (SN-031, SN-044). CI-trigger claims are scoped by workflow event: SN-048's absolute ("API pushes never trigger Actions") was falsified and corrected by SN-074, while SN-051's remedy — local verification as the gate where the push path is genuinely CI-blind — survives (SN-048, SN-051, SN-074). Guards are judged on false positives (SN-049), proof environments are reset and the reset recorded (SN-087), no change is blamed without the clean-main control (SN-059), harnesses die under their own name (SN-097), and platform deltas are investigated to the byte while the untraced residue stays honestly UNKNOWN (SN-094, SN-098).

## Essence

A red badge is a conclusion about a run, not a diagnosis of the thing the run was checking. The first discipline is therefore **classify before code change**: read what actually failed, in which step, under which gate, before touching any code — and treat a scope 403 as a gate doing its job, not an obstacle to route around (SN-031). Its twin: a failed dispatch is not a failed action — read the failed step and name what moved and what didn't before acting on the red (SN-044).

The September corpus's largest CI lesson is a claim that had to be corrected in public. It was first recorded absolutely — pushes through the GitHub App API path never trigger GitHub Actions, so API-pushed commits sit CI-pending forever (SN-048) — and a remedy was built on it: when the push path is CI-blind, **local verification is the gate**, run with the same rigor CI would have applied (SN-051). The absolute was then falsified by an event the original claim hadn't scoped: the truth is per workflow event — the App-API push does not fire `push`-event runs, while `pull_request`-event runs do fire. The corrected law: scope every CI-trigger claim by workflow event; an unscoped trigger claim is an overgeneralization waiting for its counterexample (SN-074). Both notes stand in the record; the correction does not erase the original, it scopes it (SN-048, SN-074).

Guards and environments manufacture their own reds, and each class has an owner. A guard that false-positives on first-party imports will be ignored until it is useless — a guard that cries wolf about legitimate code trains the team to bypass it, so false-positive discipline is part of the guard's correctness (SN-049). A proof environment is part of the proof: a qualification runner executed twice against the same database failed 4 of 14 checks on leftover rows from prior runs and passed 14/14 after truncation — reset the environment (truncate, recreate, provision fresh), record the reset in the proof report, and ask "was the environment clean?" before ever "fixing" the subject for a defect it doesn't have (SN-087).

Attribution is the discipline that binds them. Before blaming a change for a failure, run the clean-main control: the same test against unmodified main — if it fails there too, the change is exonerated and the failure has another owner (SN-059). A harness that cannot make that distinction is worse than no harness: when the adversarial harness's own scratch clone died of /tmp exhaustion, it emitted per-case FAILs blaming the generator under test — a harness that reports its own death as the subject's failure manufactures evidence against an innocent component; harness deaths must exit as named environment fatals, distinct from any verdict (SN-097). And "it doesn't reproduce on my machine" is a hypothesis, not a verdict: a fresh clone made the failure count *worse* (32 → 36), proving the cause was the platform, not the workspace — files read without `encoding=` default to the OS codec (cp1252 on Windows) and die on UTF-8 bytes (SN-094). The completing discipline: investigate the other platform before dismissing it — reproduce the mechanism down to the byte (the `0x9d` smart-quote that decodes as UTF-8 and throws as cp1252), fix at the source (explicit `encoding="utf-8"` everywhere, `.gitattributes` enforcing `eol=lf` so hashes stop being hostage to checkout config), hand the proof back for requalification on the platform that failed, and own the earlier dismissal on the record when you made one (SN-098). What survives the proven fix stays explicitly UNRESOLVED and unattributed — never laundered into "probably environmental" (SN-094).

## What this settles

- Red is the start of triage, not its conclusion: classify the failure and name its owner (code, dispatch, guard, environment, platform, harness) before any repair (SN-031, SN-044).
- CI-trigger claims are scoped by workflow event; SN-048's absolute stands corrected by SN-074, and SN-051's local-verification gate survives as the remedy where a path is genuinely CI-blind (SN-048, SN-051, SN-074).
- Guards are judged on false positives as well as catches (SN-049); proof environments are reset and the reset recorded, or the run proves nothing (SN-087).
- No blame without the clean-main control (SN-059); harness deaths are named environment fatals, never per-case FAILs (SN-097).
- Platform deltas are investigated to the byte and fixed at the source; the residue stays UNKNOWN until traced (SN-094, SN-098).

## Human

When something shows red, the amateur move is to start fixing; the professional move is to find out what the red actually means. Sometimes the code is broken. Sometimes the check itself is broken, the test room was dirty, the alarm was crying wolf, or the failure belongs to a different computer entirely. These rules make the team name the real owner of every failure before spending a minute repairing the wrong thing — and correct their own public claims when a "never" turns out to be "not for this kind of event."

## Child

Imagine your smoke alarm goes off. It doesn't always mean fire — sometimes it's steam from the shower, sometimes the alarm itself is broken. A good detective checks which one it is before calling the fire truck. And if your friend says "my bike works fine" but it breaks at your house, you don't say your friend lied — you check what's different about your house.

## Grandma

Dear, it's the discipline of not jumping to conclusions. A red light tells you to look, not what you'll find. Check whether the thing is broken, the checker is broken, or the room was messy before the test began. And when you learn your strong claim — "that never happens" — was too strong, you correct it in the open, where everyone heard the first version.

## Naya

Triage in order: read the failed step (SN-044), classify the failure class, and treat gates as gates (SN-031). Scope trigger claims by event or don't make them (SN-074); where the path is CI-blind, your local verification carries the full gate weight (SN-051). Audit your guards for first-party false positives (SN-049). Reset proof environments and record the reset (SN-087). Run the clean-main control before blaming any change (SN-059); make your harness die loudly under its own name (SN-097). When a failure is platform-shaped, reproduce the mechanism to the byte, fix at the source, and leave the untraced residue labeled UNRESOLVED (SN-094, SN-098).

## What It All Means

Eleven notes are the team's failure epistemology: red is information with an owner, and the craft is finding the owner before touching anything. The SN-048 → SN-074 correction is preserved inside this essence deliberately — the scoped truth includes the history of the overclaim, because the next seat needs to know both the rule and how the rule was earned.

## Why It Matters

Misattributed failure is the most expensive routine waste in a build system: lanes burn mornings repairing innocent code, real defects hide behind "environment," and public claims harden into doctrine before their counterexample arrives (SN-097, SN-094, SN-048). For the reader, this essence is the guarantee that a red in this system starts an investigation with named owners — not a blame assignment — and that strong claims carry their scope on their face.

## How It Connects

This is the evidence law of essence-evidence-law.md pointed at failure: SN-059's clean-main control is that essence's own-ref comparison discipline (SN-043) in triage form, and SN-087's environment rule reappears inside essence-composition.md's qualification craft, where the environment is part of the proof. The honest-UNKNOWN residue discipline (SN-094) is the same stance essence-decide-on-evidence.md formalizes for decisions (SN-083). The SN-048 → SN-074 pair is also the block's cleanest example of essence-one-canon.md's public supersession rule (SN-042, carried in essence-count-discipline.md) working as designed.

## What Is In It For You

Your failures get cheaper. Every red is routed to its real owner before repair money is spent, platform problems get fixed at the source once instead of being re-dismissed on every machine, and when the system corrects its own claims it does so in public — so what you believe about the system stays worth believing. Apply it anywhere: before fixing, ask "what exactly failed, and whose is it?" — and treat "doesn't happen on my machine" as the start of an investigation, never its end.

## The Learning

The team's instinct flipped from *fix the red* to *attribute the red*: classification before code (SN-031), the control run before blame (SN-059), the byte-level mechanism before dismissal (SN-098). And it learned to correct itself in the open at claim strength — SN-074 did not quietly edit SN-048; it scoped it, leaving the overclaim visible as the receipt of how the scoped truth was earned.

## Coverage map — raw notes this essence covers (11)

SN-031 · SN-044 · SN-048 · SN-049 · SN-051 · SN-059 · SN-074 · SN-087 · SN-094 · SN-097 · SN-098

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 11 IDs, all in the sep-1 block list, none duplicated elsewhere in this block's accounting.
2. **The correction pair:** SN-048's original claim and SN-074's event-scoped correction must both be present and correctly related (push-event does not fire via the App-API path; pull_request-event does). Fail if the essence states the absolute as current truth, or erases the original claim's existence.
3. **Remedy survival:** SN-051's local-verification-as-gate must be presented as surviving the correction for genuinely CI-blind paths; fail if the essence treats SN-074 as voiding the remedy wholesale.
4. **Environment numbers:** SN-087's case (4 of 14 failed on pollution; 14/14 after truncation; five leftover rows) — fail on any altered number.
5. **Platform mechanism:** SN-094/SN-098's chain (fresh clone worse: 32 → 36; `PYTHONUTF8=1` → 31; cp1252/`0x9d`; fix = explicit `encoding="utf-8"` + `.gitattributes` `eol=lf`) must be reproducible from the essence's telling; fail if the essence attributes the failures to the workspace or to stale state.
6. **Harness fatal:** SN-097 requires a named environment fatal distinct from test verdicts (the case's exit-3 FATAL); fail if the essence reduces it to "log the error."
7. **Anatomy:** all ten Full Smart Note sections present (In a Nutshell · Human · Child · Grandma · Naya · What It All Means · Why It Matters · How It Connects · What Is In It For You · The Learning) and **no machine view or machine section anywhere**. Fail on any missing section or any machine-view content.
8. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.