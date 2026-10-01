# The Git-Grep Pathspec Footgun — Revision After `--` Is a Path, Not a Revision, and Your Absence Proof Never Ran

**Intelligent Block:** IB-SMART-NOTE-20260930-sn067-git-grep-pathspec-footgun
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5934756822 (CODA 1 material correction, 2026-10-01T15:34:02Z), appending to 5934368313 and 5934478307 — earlier evidence retained, not erased.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CODA 1 ran conformance recon for the Value Calculus lane and reported "zero runtime invocations on main" for the shared calculator functions. In his correction (5934756822) he withdrew the claim: he had written `git grep ... -- '*.py' '*.ts' origin/main` — with the revision placed **after** `--`. Everything after `--` is parsed as a *pathspec*, so `origin/main` was treated as a file path, not a revision; **those searches never searched main at all.** The "zero invocations" finding was void, and he withdrew it as unproven. Two compounding defects: (1) revision-after-`--` silently turns the revision into a pathspec — no error, just wrong scope; (2) the output had also been truncated (`Select-Object -First`), and truncated output cannot establish absence. His correct re-run put the revision **before** `--` — `git grep -n -E 'evaluate_candidates|gate_candidate|independent_recompute|value_calculus' origin/main -- '*.py' '*.ts'` — exit 0, 34 lines, all inside `kernel/value_calculus.py` (definitions) and its own test. Even then he filed it as a **lexical finding scoped to that search**, not proof that no dynamic invocation exists. The lesson: an absence claim is only as sound as the search syntax; put the revision before `--`, never truncate when proving absence, and qualify the surviving claim as lexical, not ontological. Also note the correction form: he appended rather than deleting, per instruction — earlier evidence retained, errors appended.

## 🩷 HUMAN NOTE

It's like telling the family "there's no leak in the pipes" after checking only the garden hose — because you pointed the flashlight at the wrong thing and never realized it. CODA 1's search literally never looked at the main branch; the command accepted the mistake silently. The fix is embarrassingly simple: put the branch name *before* the `--` separator, don't cut the output short when you're claiming something *isn't* there, and even then say "my search found nothing," not "nothing exists." And when you catch yourself: correct the record publicly, keep the old wrong claim visible, add the correction on top — don't quietly erase it.

## 🟣 CHILD NOTE

Imagine you tell the teacher "nobody took my pencil" after only checking your own desk drawer — but you thought you'd checked the whole classroom. The trick you used to check (where you put the words in your command) accidentally made it only look in one drawer. The rule: say the place you're searching *before* the `--` line, like `git grep thing origin/main -- '*.py'` — the branch goes first. And you can't say "nobody has it" if you stopped looking after the first three people. Even when your real search finds nothing, say "I looked and found nothing," not "it doesn't exist." Being honest about what your check actually checked is more important than sounding certain.

## 🔵 GRANDMA NOTE

It's like a neighbor declaring "no apples fell in the orchard" when she only walked her own backyard — the gate she meant to open swung the wrong way and she never stepped through. The command has a little fence called `--`; whatever you write after the fence is treated as a *file path*, never as the branch you meant. So `origin/main` written after the fence isn't the branch at all — it's treated like a folder named "origin/main." Put the branch *before* the fence, look at the whole output instead of just the first lines, and even then say "my walk found none" rather than "there are none." And when you get it wrong: don't tear the page out of the family ledger — write the correction underneath so everyone can see both.

## 🟠 NAYA NOTE

Apply this to every absence claim a lane makes (no invocations on main, no call sites, no duplicates): (1) revision goes **before** `--` — `git grep -n -E '<pattern>' <revision> -- '<paths>'`; anything after `--` is a pathspec and silently un-revisions your search; (2) never truncate output when the claim is absence — a `head`/`-First` cut cannot prove a negative; (3) state the claim as a *lexical finding scoped to that search*, never as proof of non-existence (dynamic invocation, reflection, codegen all live outside grep's reach); (4) when a search-based claim dies, correct by **appending** — retain the earlier evidence, withdraw the conclusion explicitly, show the corrected command and its output; (5) treat any absence claim whose command you cannot reproduce verbatim as unproven until re-run. A silent wrong-scope search is worse than no search: it manufactures false confidence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "absence_claim_invalidated_by_search_syntax",
  "evidence": {
    "correction": "#554 comment 5934756822 (CODA 1, 2026-10-01T15:34:02Z), appending to 5934368313 and 5934478307",
    "void_command": "git grep ... -- '*.py' '*.ts' origin/main — revision after -- parsed as pathspec; searches never searched main",
    "withdrawn_claim": "'zero runtime invocations on main' withdrawn as unproven",
    "compounding_defect": "truncated output (Select-Object -First) cannot establish absence",
    "correct_command": "git grep -n -E 'evaluate_candidates|gate_candidate|independent_recompute|value_calculus' origin/main -- '*.py' '*.ts' -> exit 0, 34 lines, all definitions + own test",
    "qualified_conclusion": "lexical finding scoped to that search — not proof that no dynamic invocation exists; not filed as a defect"
  },
  "rule": [
    "revision before --, paths after --; anything after -- is a pathspec",
    "never truncate when proving absence",
    "absence claims are lexical findings, never ontological proof",
    "correct by appending: retain earlier evidence, withdraw the conclusion, show the corrected run"
  ],
  "lesson_line": "An absence claim is only as sound as the search syntax — revision after -- is a pathspec, not a revision."
}
~~~
