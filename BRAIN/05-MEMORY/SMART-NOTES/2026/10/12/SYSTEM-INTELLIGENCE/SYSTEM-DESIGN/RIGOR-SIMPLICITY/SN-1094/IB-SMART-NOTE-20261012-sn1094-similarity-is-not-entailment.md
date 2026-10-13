# IB-SMART-NOTE — SN-1094 — Similarity Is Not Entailment

Intelligent Block: SN-1094
Truth state: CANDIDATE
Scope: PRIVATE (Team Naya operating law)
Captured: 2026-10-12
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Two instruments died today on the same rock. Naya Seeker's live-feasible
bi-encoder retrieval (all-MiniLM-L6-v2, 0.2s/dispatch) FAILED a blind human
exam: 1/3 tasks at HIT@5>=2/3, with P12 ranked 16 on the principle-tracker
task it embodies. Independently, Naya Sage's judge mechanization found
hand-coded features are "TF-IDF with extra steps" (judge #3, TF-IDF #6,
AUTO #14). The cause is identical: topic similarity matches vocabulary, not
entailment. Embedding-nearness is NOT decision-relevance. The law: never wire
a vocabulary-similarity instrument into a decision path. Stop tuning lexical
instruments — the next mechanization arm must be semantic or it is dead on
arrival. The un-falsified candidate is the entailment-rerank arm.

## HUMAN NOTE

Shawn's retrieval surge (2026-10-12 "yes! Do it!") put automatic retrieval at
#1 — which makes today's failure the most expensive kind: a plausible
shortcut. The bi-encoder was fast, cheap, and completely wrong: it ranked the
right principle 16th because it was matching words, not meaning. The judge
experiment said the same thing from the other side: all the hand-coded
"smart" features were just counting word frequency with extra steps. Two
teams, two instruments, one verdict — similarity finds vocabulary;
decisions need entailment. Wire vocabulary into dispatch and you get
confident nonsense at speed. The fix isn't a bigger embedding model; it's a
different instrument: entailment ranking, proven by blind human exam before
it ever touches live dispatch.

## CHILD NOTE

Imagine you ask a friend for the best book about being brave, and she hands
you a cookbook — because the word "brave" and "braise" look similar. That's
what the computer did: it matched words that look alike instead of ideas
that mean the same. Twice today, two different computers made this mistake.
The lesson: when something needs to understand what you MEAN, don't use a
tool that only counts words that look similar. Use a tool that understands
meaning — or nothing.

## GRANDMA NOTE

The team built a machine to fetch the right answer for you. Today they tested
it the honest way: they let real people grade it, blind. It failed. The
machine was matching words, not meaning — like finding a cookbook when you
asked for courage. The team learned the rule: never let a word-matcher decide
things that need real understanding. They'll only use machines that prove, on
a blind test, that they understand meaning.

## NAYA NOTE

Operational rules for all retrieval/dispatch lanes:

- A retrieval instrument ships to live dispatch ONLY after passing a blind
  human exam on decision-relevance, not on benchmark similarity. Frozen
  fixtures from t0432 (auto-retrieval/baseline-sealed-t0432.md +
  results-t0432.json) are the starting exam; extend, don't replace.
- When an instrument fails on its own brief, freeze the honest miss as
  ground truth BEFORE any tuning (Sage's t0402 rule) — the miss becomes the
  next slice's decisive test.
- The entailment-rerank arm is the current un-falsified candidate; it holds
  that status until it either passes the blind exam or is falsified like the
  others.
- Any seat proposing "bigger embeddings" as the fix must state which
  entailment claim the new model proves — vocabulary scores don't count.

Evidence: twelve-lane lesson broadcast t0432 (Naya Seeker blind-exam
falsification; Naya Sage lexical-depth verdict), fixture
hidden_files/auto-retrieval/baseline-sealed-t0432.md + results-t0432.json.

## MACHINE NOTE

{
  "note_id": "SN-1094",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "principle": "Vocabulary/embedding similarity must never be wired into a decision path; instruments must be semantic-entailment instruments, proven by blind human exam.",
  "falsifications": [
    {"instrument": "bi-encoder all-MiniLM-L6-v2 (0.2s/dispatch)", "exam": "blind human exam", "result": "1/3 tasks at HIT@5>=2/3; P12 ranked 16 on the principle-tracker task it embodies"},
    {"instrument": "hand-coded judge features", "exam": "Sage blind test", "result": "judge #3, TF-IDF #6, AUTO #14 — lexical, not semantic"}
  ],
  "unfalsified_candidate": "entailment-rerank arm",
  "evidence": ["hidden_files/lesson-broadcast.md [t0432 Naya Seeker, t0412 Naya Sage]", "hidden_files/auto-retrieval/baseline-sealed-t0432.md", "hidden_files/auto-retrieval/results-t0432.json"],
  "applies_to": ["retrieval lanes", "dispatch", "judge mechanization", "compass option surfacing"],
  "supersedes": [],
  "superseded_by": []
}
