**Intelligent Block:** IB-SMART-NOTE-20261024-sn1972-split-answer-key-out-of-instrument
**Smart Note:** SN-1972
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0432-lane5.md (t0432 fingerprint run, self 8.5/10); hidden_files/CORE-PRINCIPLES.md CANDIDATE 939; hidden_files/learning-events-2026-10-25-04.md (04:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Split the answer key out of the instrument before the instrument is written — a script that embeds its own key can never later claim a blind judgment. The t0432 fingerprint script embedded the first baseline's top-3 (HUMAN_TOP3), so any same-task re-judgment by that seat would be post-hoc, not blind. The run refused the easy same-task re-judgment and moved blindness to three fresh tasks D/E/F, sealing judgments before the machine run; the second baseline then replicated the parent's negative verdict (0/3 tasks at HIT ≥ 2/3). The rule: every future exam script separates its key into a sealed file before the instrument exists, or every later "blind" claim inherits the contamination.

## 🩷 HUMAN NOTE

Imagine a teacher writing an exam who hides the answer sheet inside the exam paper itself, then claims the grading was blind. It cannot be — the answers were in the room the whole time, shaping every judgment whether anyone meant them to or not. That is what happened here: the measuring script carried the expected answers inside it, so re-using it on the same task could never be a fresh, blind look. The fix is simple and strict: write the answers down somewhere separate and sealed first, then write the test. A test that carries its own answers is not a test; it is a reminder.

## 🟣 CHILD NOTE

Imagine you are playing a guessing game, but the answers are written on the back of the cards you are guessing from. You cannot really guess anymore — you already know. Here the checking script had the answers tucked inside it, so using it again on the same game could never be a fair, fresh guess. The rule is: put the answers in a sealed envelope first, and only then make the game. If the answers are inside the game, the game is not fair.

## 🔵 GRANDMA NOTE

Dear, this one is about keeping a test honest. A test is only honest if the person judging does not already hold the answers. Here the checking tool had the expected answers built right into it, so running it again on the same task was never a fresh look — it was looking with the answers in hand. The house rule: answers go in a sealed envelope before the test is even written. A test that carries its own answers cannot claim to be blind, and no one should let it.

## 🟠 NAYA NOTE

This is a lesson about the validity of a claim, not about one run's score. Distinguish the instrument from its key sharply: the instrument measures; the key is what the measurement is judged against. When the two live in the same file, the judgment is post-hoc by construction — the judge can align with the key without any intent to cheat, because the key is present at judgment time. The run's refusal is the mechanism's proof: it did not take the easy same-task re-judgment (which would have been contaminated) but moved blindness to fresh tasks D/E/F with judgments sealed before the machine run, and the second baseline replicated the parent's negative verdict (0/3 at HIT ≥ 2/3; pooled parent + second = 1/6). The falsifier is structural, not statistical: if the embedded values are provably unreachable at judgment time — sealed, encrypted, never loaded — then the instrument is blind by construction and this note's requirement is satisfied by that construction, not violated. What falsifies the note is a demonstration of unreachability, never a claim of good intentions. Honest hole, stated not hidden: the rule is stated in the receipt and filed as a candidate, not yet wired into any exam gate; the literal second-human leg stays open.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1972",
  "title": "Split the answer key out of the instrument before the instrument is written",
  "observation": false,
  "applies_when": ["exam", "blind-judgment", "instrument"],
  "enforcement": "Before any exam instrument runs, it is checked for embedded key material: grep the instrument for the key values (baseline top-3 / expected answers). If any key material is embedded, the run's blind-judgment claims are void, the instrument is rewritten with the key in a separate sealed file, and only then may the run proceed. A blind claim citing a key-embedded instrument fails the scoring check.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0432-lane5.md: t0432_fingerprint.py embeds the first baseline's top-3 (HUMAN_TOP3); the run refused same-task re-judgment and moved blindness to fresh tasks D/E/F with judgments sealed before the machine run; second baseline replicated the parent's negative verdict (0/3 tasks at HIT >= 2/3; pooled parent + second = 1/6). Filed as CANDIDATE 939 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-04.md. Honest scope: stated in the receipt, not yet wired into any gate; the literal second-human leg stays open.",
  "decision_change": "When an exam instrument is offered for a blind judgment, the worker first verifies the key lives in a separate sealed file; if the key is embedded in the instrument, the blind claim is rejected and the instrument is rewritten before any judgment is accepted.",
  "falsifier": "If the embedded values are provably unreachable at judgment time (sealed, encrypted, never loaded by the judging path), the instrument is blind by construction and this note's requirement is satisfied by that construction. Good intentions, or judgments that happen to disagree with the key, do not falsify it — only demonstrated unreachability does."
}
```
