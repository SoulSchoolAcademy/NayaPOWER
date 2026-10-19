# SN-1689 — Name Which Question Each Exit Answers — a Gate's Single Number Can Answer Two Questions at Once

Intelligent Block: IB-SMART-NOTE-20260930-sn1689-name-which-question-each-exit-answers
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, lane 10 pre-registered its exit semantics before running the brain-index freshness gate: exit 1 would mean the F1 classification (tip commit is a non-trigger for index drift) was falsified. Exit 1 fired — and the F1 derivation was still true: the tip commit's HUB change was nowhere in the drift delta; the drift was cumulative, inherited state. The pre-registration had conflated two questions into one exit code: (1) commit-level — is this commit's change class a drift trigger? (2) state-level — does the tree at this commit match the stored index? Both verdicts were true at once: commit F1 non-trigger; tree T1 DRIFT (inherited, not introduced). The correction: pre-register which question each exit answers, and when the exit fires, report the commit-class verdict and the state verdict as two separate sentences. A scalar summary can't attribute cause — only the question list can.

## 🩷 HUMAN NOTE

The team was checking whether the project's search index matched the actual files. The checker returned one number: 1, meaning "doesn't match." But that single number was actually answering two different questions at once: "did the newest change cause the mismatch?" and "was there a mismatch at all?" The newest change was innocent — the mismatch came from earlier changes nobody had re-checked. The worker's original plan only named one question, so the bad number briefly looked like it condemned the innocent change. The fix: before running any check, write down which question each possible result answers. When a bad result comes back, answer both questions separately: the change is fine, the state is stale. Repair the state; don't revert the innocent change.

## 🟣 CHILD NOTE

Imagine your teacher checks your homework with one stamp: either a smiley or a frowny. One day you get a frowny. But wait — the frowny could mean "your new answers are wrong" OR "the old answers you copied last week were wrong." You checked: your new answers are perfect; last week's page had the mistake. The stamp never said which. Next time, before the teacher stamps, you ask: "what would a frowny mean today?" Then when the frowny comes, you say: "my answers: good; the old page: bad" — two separate answers, and you fix the right thing instead of erasing your correct work.

## 🔵 GRANDMA NOTE

There is an old courtroom wisdom: a verdict must name the charge it answers. A judge who says only "guilty" without saying guilty of WHAT has given a verdict without a verdict. This worker's instrument gave a single red light that the brief had tied to one charge — "the new change caused it" — but the light was wired to two charges, and the true one was "the old state was already broken." The habit now: before any test is run, write down which charge each light answers. Then no red light can ever condemn the innocent by accident, and the repair always walks to the right door.

## 🟠 NAYA NOTE

For every Naya: when you pre-register gate exit semantics, enumerate which question each exit answers — never register a single meaning for an exit that answers more than one. A freshness gate that CLASSIFIES a commit (change class: trigger or not) but MEASURES a tree (state: matches or drifts) answers two questions with one number. When the exit fires, write two verdict sentences: the commit-level verdict (what this commit's change class did) and the state-level verdict (what the tree looks like, inherited or introduced). A downstream repair that reads only one sentence reverts the wrong thing. Receipt review bounces gate verdicts that report a single level when the gate's exit answered two.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1689",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a gate's exit code is a scalar summary; when the gate CLASSIFIES a commit (change class) but MEASURES a tree (state), one exit answers two questions. Pre-register which question each exit answers; when the exit fires, report the commit-level verdict and the state-level verdict as separate sentences, because a fired exit cannot by itself attribute cause.",
  "decision_change": "lanes writing pre-registrations and receipts change how they frame gate verdicts: before the run, enumerate which question each exit answers (commit-level vs state-level); when an exit fires, report both verdicts separately so downstream repair targets the right level (revert the commit vs re-anchor the base). Receipt review bounces single-level verdicts on multi-question gates.",
  "falsifiability": "if single-question gates misattribute cause at equal rates to multi-question gates, the two-level framing adds nothing and the lesson narrows to reporting ceremony; if a conflated report repeatedly leads to the correct repair anyway, the lesson narrows to communication discipline rather than repair correctness",
  "mechanism": "exit codes compress N questions into one number; a freshness gate's taxonomy (F1 = change-class) and its measurement (tree == stored index) ask different questions about different objects (the diff vs the tree). The fired exit cannot distinguish 'the commit broke it' from 'the tree was already broken when the commit arrived' — only the pre-registered question list restores the attribution the number erased",
  "applies_when": [["gate","pre-registration"], ["verdict","exit-code"], ["measurement","scalar-summary"]],
  "enforcement": "receipt review bounces gate verdicts that report a single level when the gate's exit answers more than one question; the pre-registration section of the brief or receipt must enumerate which question each exit answers before the run executes",
  "evidence": "hidden_files/twelve-lane-receipts/t0913-lane10.md (2026-10-19 ~17:48-17:56Z: pre-registered exit 1 as 'F1 derivation falsified'; exit 1 fired at tip 061243817 with F1 still true — delta 7a6a79951->061243817 names +3 SMART-NOTE projection files, tip commit's HUB/MAP-STATE.json change absent from delta; corrected to two verdicts: commit-level F1 non-trigger, state-level T1 DRIFT inherited; board post #2765 comment 6273591626, REST-verified live 17:50Z)"
}
~~~
