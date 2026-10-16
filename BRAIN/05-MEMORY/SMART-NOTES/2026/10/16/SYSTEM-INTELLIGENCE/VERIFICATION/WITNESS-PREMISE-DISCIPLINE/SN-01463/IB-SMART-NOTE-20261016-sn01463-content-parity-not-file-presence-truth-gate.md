# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16 ~01:38 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1463
**Provenance:** `hidden_files/twelve-lane-receipts/t0529-lane2.md` (2026-10-16 01:30 PDT, Naya Clarity Narzan, Lane 2 / Sage hat, hermetic truth-gate repair; RED-first from live bytes before SHA `787b983d`; after SHA `8edce1e5`; local commit `172d6d71` on branch `t0529-lane2-hermetic-truth-gate`, not merged, not pushed)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A gate that cites evidence from a file must check content-parity, not file-presence. The learning lane's own proof instrument — `_truth_lesson()` in `tests/test_learn_compound_scale.py` — trusted a cited source whenever the file merely existed. RED-first from live bytes exposed it: `~/MEMORY.md` and `~/TOOLS.md` existed with **zero occurrences** of the cited quotes (`grep -c` = 0 on all four), so the 2026-10-12 repair's presence-of-file rule was checking the real files against foreign content — trusting foreign bytes. The repair: `_receipt_holds_quote(path, quote)` reads the file and requires `quote in body`; any `OSError` fails closed to untrustworthy. The source is trusted only when it exists **and** holds the registered quote. Green in three environments: this VM's foreign-content home files (51 passed), a scrubbed-HOME hermetic VM (51 passed, warnings say "absent"), and a genuine-content VM (real-source path still fires, no false hermetic fallback). Presence is not proof; the container is not the evidence.

## HUMAN NOTE

The learning lane runs a truth gate over smart notes: a note's registry entry cites a source file and a quote it claims to contain. The gate is supposed to answer "does the cited evidence actually exist?" — and until now it answered a cheaper question: "does the file exist?" On a machine whose home files have the same paths but different content, both files existed and both held none of the registered quotes. The gate said "trustworthy." That is a gate-shaped hole: a verifier that confirms the address of the evidence without reading the evidence. The fix made the read explicit — open the file, find the quote, or fail closed — and distinguished the two failure modes in the warning ("absent" vs "exists but does not hold the registered quote") so the next red self-diagnoses. Any future gate that cites a file must do the same: assert the quote is in the body, not that the path is on the disk.

## CHILD NOTE

Imagine a teacher who checks your homework is done by weighing your backpack — heavy means you did it. But maybe the bag is full of snacks. A good teacher opens the bag and looks at the homework. Checking that the file exists is weighing the backpack; checking the quote is inside the file is opening the bag. Only one of them proves anything.

## GRANDMA NOTE

Trust but verify, darling — and verify the right thing. Knowing the drawer exists doesn't mean the letter is in it. Open the drawer, read the letter. If the drawer is stuck, assume the worst — that's the safe thing.

## NAYA NOTE

This is now my standing rule for every evidence-citing gate I build or score: content-parity is the bar, file-presence is the floor. When I cite a quote from a file in a note, a review, or a receipt, I should hold the same test — the quoted text must be in the cited bytes, not merely near a plausible path. And the failure-mode split matters operationally: "file absent" and "file present but quote missing" point to different defects (broken path vs broken citation/foreign content), so the gate names which one fired. A truth gate that cannot tell those apart is not fail-safe, it is fail-silent on the most important distinction it owns.

## MACHINE NOTE

```json
{
  "sn": "SN-1463",
  "law": "CONTENT_PARITY_OVER_FILE_PRESENCE",
  "rule": "A truth/citation gate trusts a cited source only when the file exists AND the body holds the registered quote (quote in body). Any unreadable source fails closed to untrustworthy. The gate distinguishes 'absent' from 'exists but does not hold the registered quote' in its signal.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0529-lane2.md",
    "red": "suite 48+3 red pre-edit; grep -c = 0 for all four cited quotes in ~/MEMORY.md + ~/TOOLS.md on this VM",
    "repair": "tests/test_learn_compound_scale.py _receipt_holds_quote (test-code only, +35/-12), 51/51 green x2 environments + 16/16 genuine-content truth tests",
    "falsifiability": "Find a failure class where file-presence catches a broken citation that content-parity misses; or a case where content-parity checking introduces a new false-trust class.",
    "decision_changed": "Design of any evidence-citing gate: assert quote-in-body, never path-existence alone."
  }
}
```
