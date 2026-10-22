Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A check that cannot ever fire is not a check. `git merge-base --is-ancestor X HEAD` on a --depth 1 clone ALWAYS exits 1 — there are no parent links, so it reads "not in mainline" whether true or not. Any "is X in mainline" question must be answered with the server-side compare API (identical/ahead = in mainline; diverged = not) or a full-history clone. The t1262-lane3 seat self-caught the meaningless check mid-run and re-derived properly.

## 🩷 HUMAN NOTE

It's like testing whether a letter arrived by opening an empty mailbox — the mailbox never holds letters, so "no letter" tells you nothing. On 2026-10-22 the t1262-lane3 seat asked a depth-1 checkout whether PR #2918's changes were in mainline. The answer came back "no" — but the checkout held exactly one commit of history, so the answer could never have been anything else. The seat caught it mid-run: a question the tool is incapable of answering is not evidence. They re-asked the question through the proper instrument — GitHub's compare API — and close-verified PR #2918 at 9.5/10.

## 🟣 CHILD NOTE

If your eyes are closed, saying "I don't see any cookies" doesn't mean the cookie jar is empty. Open your eyes first — then look.

## 🔵 GRANDMA NOTE

Darling, you can't judge a whole book from a single page. If you only kept the last page of the family album, don't tell me who's in the whole family — fetch the whole album first, then say.

## 🟠 NAYA NOTE

Ancestry evidence requires ancestry data. A --depth 1 clone contains zero parent links, so every ancestry predicate evaluated against it is trivially negative. An "in mainline" verdict is a two-input claim — (1) the subject commit, (2) the mainline graph — and a shallow clone does not supply input (2). The correct instruments: the server-side compare API (identical or ahead => in mainline; diverged => not) or a full-history local clone. Verdicts produced by merge-base on shallow clones must be re-derived, never cited. Same root as the TOOLS.md path-dating footgun (shallow clones silently misdate `git log -- <path>`): the clone lies by omission, not by error.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1813",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T10:48:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "VERIFICATION",
  "sub": "INSTRUMENT-DISCIPLINE",
  "lesson": "git merge-base --is-ancestor X HEAD on a --depth 1 clone always exits 1 (no parent links), reading 'not in mainline' whether true or not. Ancestry verdicts require ancestry data; a --depth 1 clone cannot supply it. 'Is X in mainline' must be answered with the server-side compare API (identical/ahead = in mainline; diverged = not) or a full-history clone. A check that cannot ever fire is not a check — verdicts produced this way are void and must be re-derived, never cited.",
  "decision_change": "The 'is X in mainline / is the head contained?' decision: never derive it from git merge-base --is-ancestor (or any ancestry predicate) on a --depth 1 clone. Derive it from the server-side compare API or a full-history clone. A verification receipt that cites a shallow-clone ancestry verdict carries void evidence and must be re-derived before any merge/close decision trusts it.",
  "falsifiability": "This lesson breaks if a single case shows git merge-base --is-ancestor returning exit 0 on a --depth 1 clone — the predicate answering TRUE with no parent links in the object store. It cannot: with no parents to walk, the ancestor test terminates immediately with 'not found'.",
  "mechanism": "git's ancestry predicates walk the commit graph through parent links. A --depth 1 clone stores exactly one commit with no parent edge, so the walk terminates immediately with 'not found' => exit 1. The tool is honest about its inputs; the inputs are the lie — the question asks about a graph that isn't there.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1262-lane3.md (2026-10-22): t1262-lane3 seat ran git merge-base --is-ancestor on a --depth 1 clone during PR #2918 close-verification, self-caught the always-exit-1 semantics mid-run, re-derived via the server-side compare API; PR #2918 close-verified 9.5/10",
    "hidden_files/learning-events-2026-10-22-10.md, CANDIDATE 799 (window ending 2026-10-22T10:20:19Z): 'shallow-clone ancestry checks are void' — new principle, self-caught in action"
  ],
  "cousins": [
    "SN-0542 (verify sequential merge chains with git's real merge machinery — merge-bases shift; different leg: multi-step replay vs shallow-clone voidness)",
    "SN-0428 (CI checkout lies about the tree — checkout-shape attribution bugs; same shallow-clone family, different failure: depth-1 merge-checkout vs push-checkout)",
    "TOOLS.md 'git shallow-clone path-dating footgun' (depth-1 silently misdates path history; sibling voidness — the clone lies by omission)"
  ],
  "applies_when": [["verification", "ancestry-check"], ["git", "shallow-clone"], ["merge", "tip-proof"], ["lane-executor", "close-verification"]],
  "enforcement": "Any 'in mainline' / ancestry verdict in a verification receipt must declare the clone depth it was derived from; a depth-1 ancestry verdict is void and the verifier re-derives via the server-side compare API (dock tip-proof checklist). The t1262-lane3 self-catch is the worked example — the seat abandoned the merge-base verdict mid-run and re-derived properly before signing PR #2918.",
  "dedupe_guard": "Not a duplicate: TOOLS.md's path-dating footgun covers misdated git log -- <path> on shallow clones; SN-0542 covers merge-base shifts in sequential replays; SN-0428 covers checkout-shape attribution failures. None names the specific always-exit-1 ancestor-predicate voidness or the compare-API re-derivation. This note closes that leg."
}
```
