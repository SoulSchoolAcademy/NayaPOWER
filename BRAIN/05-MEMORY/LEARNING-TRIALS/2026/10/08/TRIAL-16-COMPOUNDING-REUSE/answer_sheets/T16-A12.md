PREREGISTRATION-DESIGN

Trial: behavioral isolation of L-RETRIEVE ("Retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions.")
Design date: 2026-10-08. Status: preregistered — no subjects spawned before all pre-launch audit checks pass.

1. HYPOTHESIS

Isolated behavioral effect: agents explicitly instructed to retrieve relevant Smart Notes from the corpus at decision time BEFORE answering project-specific questions will achieve a significantly higher mastery rate on questions whose correct answers exist only in the corpus than agents given a neutral brief with no corpus mention and no corpus access cue. The trial isolates the marginal behavioral effect of the retrieval step itself: treatment = corpus retrieval before each answer; control = answer from own reasoning, with the corpus path never mentioned. The expected mechanism is that treatment agents apply corpus-specific facts at decision time that control agents cannot derive from general reasoning, standing knowledge, or the task setup.

2. ARM DEFINITIONS

The EXACT brief text each arm receives, verbatim. Subjects are randomized 1:1, blinded to arm labels.

ARM A — TREATMENT (retrieval instructed):

"You are answering project-specific questions. BEFORE answering each question, retrieve relevant Smart Notes from the corpus at /corpus/notes/ and use them at decision time. Search the corpus for notes relevant to the question, read the ones that match, then compose your answer using what you retrieved. Do not answer from general reasoning alone — consult the corpus first, then answer. Answer each question as accurately and completely as you can, in your own words."

ARM B — CONTROL (lesson-free default, cold):

"You are answering project-specific questions. Answer each question as accurately and completely as you can, in your own words."

Notes on construction: the draft control brief supplied with this task ("Project reference notes are available at: /corpus/notes/ — consult them as needed before answering. Answer thoroughly using all available resources.") was REJECTED on audit. It contains two traps: (a) mentioning the corpus path contaminates availability — uninstructed agents retrieve when they see the path (L16 mode 3: observed control 9.0/9 with neutral path mention vs cold 0.0/9 without); (b) "consult them as needed before answering" states the lesson's prescription in the control brief (L16 mode 2, leaky briefing). Both phrases were removed. The final control brief contains no path, no mention of notes, no retrieval language of any kind.

3. TASK / QUESTIONS

Subjects answer 9 project-specific questions. Each question targets a concrete, project-specific fact that is recorded ONLY in the frozen corpus at /corpus/notes/ (novel project identifiers, dates, version numbers, named decision records) and is not derivable from general knowledge, standing doctrine, or the task setup. The corpus is frozen at preregistration and may not be edited during the trial.

Scoring: each question is scored 0/1 against a frozen rubric listing the required facts. A question scores 1 only if the answer contains the rubric's key fact(s) verbatim or in unmistakable paraphrase; vague or generic answers score 0. Two independent scorers apply the rubric; disagreements are resolved by majority of a third tie-breaker, all blinded to arm.

PRIMARY OUTCOME (subject level): mastery = subject answers >= 7 of 9 questions correctly. Primary statistic: proportion of subjects achieving mastery, treatment vs control.

Secondary (descriptive only): mean questions correct per subject; retrieval rate per arm (proportion of subjects referencing/accessing at least one corpus note before answering).

4. STATISTICS

- Test: Fisher's exact two-sided test on the 2x2 table (mastery yes/no x arm), alpha = 0.05.
- Effect size: Cohen's h on the two mastery proportions.
- Tier-S bar: Fisher's exact two-sided p < 0.05 AND Cohen's h >= 1.4 on the primary outcome proportions.
- Sample size: n = 20 subjects per arm (40 total), fixed in advance. No interim analysis, no peeking, no optional stopping; the bar is computed once on the full frozen dataset.
- Decision rule: Tier-S is met only if BOTH conditions hold. Either condition failing = no Tier-S claim.

5. VALIDITY GATES

Each gate has a numeric threshold. A fired gate halts the claim; no Tier-S bar may be cited from a trial with a fired gate.

GATE 1 — Derivability ceiling (L16 mode 1). Pre-check: 10 cold pilot subjects receive the control brief and the 9 questions with no corpus mention. Threshold: mean pilot score <= 1.5/9 correct AND no pilot subject scores >= 6/9. If mean > 1.5/9 or any pilot >= 6/9: task is derivable from general reasoning alone — trial INVALID, redesign the questions before any launch.

GATE 2 — Leaky control briefing (L16 mode 2). Audit: grep the final control brief for the tokens {"corpus", "notes", "retriev", "consult", "look up", "look-up", "/corpus", "reference material", "knowledge base"} and manual read for implied or exemplified retrieval instructions. Threshold: 0 hits and 0 implied prescriptions required. If >= 1 hit or any implied prescription: rewrite, re-audit, no launch until clean.

GATE 3 — Availability contamination (L16 mode 3). During the run, record whether each control subject references or accesses the corpus path. Threshold: 0 of 20 control subjects may access the corpus; if 1-2 do, their data are flagged and reported separately; if >= 3 of 20 (15%) access it: contamination — trial INVALID, abort analysis of the lesson effect, report as failed isolation.

GATE 4 — Doctrine-redundancy / unanimous ceiling (L16 mode 4). Thresholds: if control mastery rate >= 50% (10/20): the lesson is already reachable without it — INVALID (doctrine redundancy / derivability). If both arms' mastery rates are >= 80% (16/20 each): unanimous ceiling — INVALID, effect unmeasurable. If treatment mastery rate <= control mastery rate: no positive effect — fail to isolate, no Tier-S claim.

GATE 5 — Treatment compliance. Threshold: >= 16 of 20 treatment subjects (80%) must retrieve at least one corpus note before answering. If compliance < 80%: effect is unattributable — trial classified INCONCLUSIVE (compliance failure), not a lesson failure; no Tier-S claim may be made.

6. PRE-LAUNCH AUDIT CHECKLIST

All checks must pass before subject 1 is spawned. Any failure blocks launch.

1. Corpus frozen: record the corpus commit/hash at /corpus/notes/; confirm the 9 questions' answer facts are present and correct in the corpus, and absent from both briefs.
2. Cold pilot run: 10 lesson-free pilot subjects take the task with the control brief; verify GATE 1 thresholds (mean <= 1.5/9, no pilot >= 6/9).
3. Control-brief grep: run the GATE 2 token grep on the final control brief; confirm 0 hits; confirm two readers agree the brief states, implies, and exemplifies nothing of the lesson's prescription.
4. Treatment-brief check: confirm the final treatment brief names the corpus path and the retrieve-before-answering step, and adds no other novel instruction.
5. Path isolation: confirm no subject environment exposes /corpus/notes/ to the control arm (no ambient path hints in system prompts, tool defaults, or workspace files visible to subjects).
6. Rubric frozen: scoring rubric with per-question key facts is written, versioned, and stored before launch; scorers are blinded to arm.
7. Randomization: 1:1 randomization procedure defined (seed recorded); n = 20 per arm fixed; no peeking rule documented.
8. Analysis plan locked: Fisher's exact two-sided (alpha 0.05), Cohen's h, Tier-S bar (p < 0.05 AND h >= 1.4), computed once on frozen data.
9. Evidence store: results will be written to a durable workspace location at run time (never /tmp); raw subject transcripts and scores committed, not summarized from memory.
10. Gate log: an empty gate log is opened; the launcher records the outcome of every gate (pass/fire with numbers) before computing the Tier-S bar.
