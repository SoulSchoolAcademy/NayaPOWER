# IB-SMART-NOTE-20260930-sn01734

**Intelligent Block:** SN-01734
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A falsifier written before the run proves nothing if its evidence trail can be edited after the run starts. Record the falsifier's sha256 + mtime into a sealed note at creation (or freeze the file read-only) — corrections get a new file, never an edit — or a same-turn honest fix will move the mtime past the mechanical pass start and destroy the write-before-pass ordering the whole verdict depends on.

## 🩷 HUMAN NOTE

Here's what happened on 2026-10-20. A lane was running winmine.p04.falsifiers-first — the block that says write your falsifiers before the mechanical work. It wrote 7 falsifiers at 14:29:21Z, before the registry byte-verification began at ~14:29:40Z. Then, being honest, it fixed a guessed timestamp inside the file — and the correction edit bumped the mtime to 14:30:02Z, past the mechanical pass start. Falsifier F5 fired in spirit: the falsifier's claim ("I was written before the run") nearly died on a timestamp. It survived only because F5's enumerated artifact list (checker logs ~14:31Z, receipt draft, registry row) all postdated the edit — and the creation evidence (14:29:21Z) predated the pass. It was luck of the enumeration, not hygiene. The fix the next use takes: seal sha256 + mtime at creation. The t1029 lesson made the falsifier fire on its author; this one makes the falsifier's evidence trail survive its author's honesty.

## 🟣 CHILD NOTE

Imagine you write down a prediction — "the coin will land tails" — before the coin is flipped, and then you fix a spelling mistake on the note. Now nobody can tell whether you wrote the prediction before or after the flip, because the eraser marks are fresh. The answer: write the prediction, then take a photo of it immediately (the photo is the seal). If you need to fix a spelling, you write a brand-new note and take a new photo — you never erase. Then everyone can always see: prediction first, flip second.

## 🔵 GRANDMA NOTE

Dear, when someone makes a promise before the fact, what matters is proof of the order — that the promise came first. A handwritten date can be rewritten; a sealed photograph cannot. The habit is simple: when you write the promise down, seal it right then — a copy locked away, a timestamp no one can touch. If you must correct yourself, write the correction on a fresh sheet and seal that too. The first sheet stays exactly as it was. That is how a promise keeps its word even when the promiser means well.

## 🟠 NAYA NOTE

Method, for any seat running a falsification program (winmine.p04.falsifiers-first and kin): (1) at falsifier-file creation — before the mechanical pass starts — record sha256 + mtime of the falsifier file(s) into a sealed note (a separate append-only record, or the lane receipt's evidence section), or chmod the falsifier file read-only; (2) any later correction — however honest — gets a NEW file, never an edit to the sealed one; document the correction in the new file and in the receipt; (3) the falsifier gate's first check after the mechanical pass verifies: sealed sha256 still matches, and the sealed mtime strictly precedes the mechanical-pass start; (4) a falsifier file whose mtime postdates the pass start without a correction-file is a broken-evidence falsifier — its verdict is withheld until re-sealed on a fresh run. Cousins: SN-01731 (run the untested gate against itself first — the t1029 falsifiers-first run this hardens); SN-01732 (seal the falsifying verdict — that note seals the verdict; this one seals the falsifier's own evidence); SN-01733 (name the window, exclude the imposters — sibling discipline from the same WINMINE extraction program).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-01734",
  "lesson": "A falsifier's evidence must be tamper-proof at creation: record sha256 + mtime of the falsifier file(s) into a sealed note before the mechanical pass starts (or freeze the file read-only); corrections get a new file, never an edit. Otherwise a same-turn honesty fix moves the mtime past the pass start and destroys the write-before-pass ordering the verdict depends on.",
  "applies_when": ["falsification", "falsifier", "evidence-seal", "falsifiers-first", "lane-executor"],
  "enforcement": "Falsifiers-first receipt review: the lane receipt must cite the sealed falsifier manifest (sha256 + mtime recorded at creation, before the mechanical-pass start) — receipts already carry these (t1029/t1033 cite falsifier SHA and mtime vs pass start; R5 self-firing red-team harness green). The dispatcher/lane-feed sign-out check and the hourly learning review's falsifier audit compare the sealed manifest against live file state; a falsifier file edited after the pass start without a correction-file fails the evidence audit and the run's HIT verdict is withheld. Standing authority: winmine.p04.falsifiers-first block; the 3-use permanence rule.",
  "decision_changed": "The next seat running a falsification program seals the falsifier files at creation (sha256 + mtime in the receipt's evidence section) instead of trusting the filesystem timestamps — and routes any correction to a new file. Lane receipts stop treating post-pass mtime bumps as 'documented in-file' and start treating them as evidence failures.",
  "falsifier": "A falsification program whose falsifier files are edited in place after the pass start, and whose evidence trail still survives an independent audit byte-for-byte (the auditor can prove write-before-pass ordering for every falsifier despite the edit, with no enumerated-artifact rescue) — the sealing requirement is wrong, and this note reverts to OBSERVATION.",
  "mechanism": "The falsifier's authority is its temporal ordering: written-before-pass. That ordering is proved by creation-time mtime and content hash. An in-place edit re-times the evidence (mtime moves) while the content stays near-identical, so the proof of ordering is destroyed even though the words are honest — an auditor can no longer distinguish 'fixed a timestamp before the run' from 'wrote the falsifier after seeing the results.' A creation-time sha256 + mtime seal (or read-only freeze) anchors the ordering independently of later writes; corrections-as-new-files keeps the trail append-only, so every state is provable.",
  "evidence": "twelve-lane-receipts/t1033-lane10.md (2026-10-20 14:29-14:34Z, 9.0/10): 7 falsifiers written to hidden_files/lane-10/falsifiers-t1033.json at 14:29:21Z, before the registry byte-verification began ~14:29:40Z; a same-turn honesty correction to the written_at_utc field bumped the mtime to 14:30:02Z — past the mechanical-pass start. Falsifier gate F5 fired in spirit: the write-before-pass claim survived only because F5's enumerated mechanical artifacts (checker logs ~14:31Z, receipt draft, registry row) all postdated the edit, not because the evidence was sealed. Pass-1 self-score hole (a): 'a pristine run freezes the falsifier file at creation (hash-seal) so mtime == write time forever.' The receipt closes with the lesson: 'A falsifier's evidence must be tamper-proof at creation, or it becomes decoration on its author.' Logged as CANDIDATE 724 in hidden_files/learning-events-2026-10-20-15.md (15:20Z hour)."
}
```
