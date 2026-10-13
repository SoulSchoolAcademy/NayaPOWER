# A Sealed Verdict Expires When the World Moves — FAILs Expire Too

**Intelligent Block:** IB-SMART-NOTE-20261013-sn01220-sealed-verdict-expires-when-world-moves-fails-too
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE HEART] Naya Heart (Lane 11) tick t0660 — sign-in #2175 comment 6153820810 (2026-10-13 ~20:13Z), sign-out #2175 comment 6153897694 (2026-10-13 ~20:13Z); receipt `hidden_files/twelve-lane-receipts/t0660-lane11.md`; verdict `retrieval/cold-retrieve-isolated-t0660.md`; live tip `582e5e5f`. Related: SN-0493 (decisions expire when the tip moves), SN-1069 / SN-1206 (dispatch-time premise re-verification), SN-080 (frozen evidence retirement).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0660 brief arrived claiming the cold-retrieve hole was "HOLDS-OPEN since t1052." The dispatch-time pin check (Heir t0659's lesson, SN-1206) showed the premise was stale: t0601 (FAIL, sealed) and t0614 (FAIL, sealed) had already closed the hole — the cold band was known-failing, not open. That made the tempting move obvious: inherit the sealed FAIL and skip the measurement.

The seat refused. Two expiry triggers were live: the main tip had moved since t0614 (`e47a650e` → `582e5e5f`), AND the subject code itself had changed (`smart_note_v2.py` pin `fe6f2b4c…` ≠ `92d8b2b…`). A sealed verdict — PASS or FAIL — is a statement about the universe it was sealed in. When the tip moves or the subject's bytes change, the verdict expires; inheriting it would be a claim about a world that no longer exists. The seat re-measured on live bytes — "live bytes, not memory," the oath, stated explicitly — and got a fresh FAIL: cold median 0.9682s vs the 0.5s CR-ACCEPT bar (n_cold=2, n_warm=3), mincore 0-pre proven on 605 tree files both trials.

The re-measurement paid for itself in a way inheritance never could: the new code runs cold at 0.95–0.99s — 25–35% faster than t0601/t0614's 1.28–1.59s. The old sealed FAIL wasn't wrong; the world moved under it, and the code improved in the meantime. A stale FAIL inherited would have frozen the story at the old number and buried the progress; a stale FAIL re-measured honestly found it.

The durable doctrine, completing SN-0493's symmetric half:

1. **Inherit nothing across a changed universe** — not PASS verdicts (the classic trap SN-0493 names) and not FAIL verdicts (the symmetric trap this incident names). A stale PASS inherited lets a broken thing look fixed; a stale FAIL inherited lets an improving thing look stuck — and hides the slope of progress.
2. **A sealed verdict binds to its pins: the tip and the subject bytes.** Two expiry triggers — tip moved, or the subject code's pin mismatches. Either one retires the verdict. "Sealed" makes the verdict trustworthy *about its own universe*; it does not make it portable.
3. **When expiry triggers, re-measure on live bytes.** The expired verdict is retired, not dishonored: cite it, retire it with the reason (tip + pin mismatch), and replace it with a fresh measurement. The retired FAIL remains evidence that the old code failed — it just isn't evidence about the new code.

## 🩷 HUMAN NOTE

Shawn — a small but real piece of measurement doctrine from Lane 11's cold-retrieve drill tonight. The old sealed runs said the cold band FAILS the half-second bar. The honest move wasn't to trust those runs or distrust them — it was to notice the world had changed (new tip, changed code) and re-measure on today's bytes. The fresh run still failed the bar, but it also found the code 25–35% faster than the sealed runs said. The lesson we're banking: a sealed verdict — pass OR fail — expires when the world moves. Inheriting a stale pass hides breakage; inheriting a stale fail hides progress. When the tip or the code changes, the old verdict retires and you measure again.

## 🟣 CHILD NOTE

Imagine a thermometer was sealed in a box that said "the soup is too cold." But since the box was sealed, someone put the soup back on the stove and stirred in new spices. If you open the box now, the note is about the OLD soup — the soup that's in the pot today is different. The smart cook doesn't trust the old note or throw it away in anger — she tastes the soup again. When she tastes it, she might find it's still too cold, BUT she might also find it's getting warmer — progress she would never have seen if she'd just believed the old note. Sealed notes are promises about the moment they were written, not the moment you're living in.

## 👵 GRANDMA NOTE

It's like an old inspection sticker on a car. The sticker said the brakes failed in June — and the inspection was honest and the seal was real. But since June the car got new brakes and a new engine. If you read the old sticker today, you're judging a car that doesn't exist anymore. The right move isn't to ignore the sticker (the old failure was real) or to obey it blindly (the car changed) — it's to get a fresh inspection and read the new sticker, which might say the brakes still need work but the car is getting better. Verdicts are dated to the world they measured. When the world changes, the verdict's date passes — not because it lied, but because it was telling the truth about a world that's gone.

## 💜 NAYA NOTE

Note to future me: SEALED VERDICTS EXPIRE — BOTH DIRECTIONS. The failure mode everyone guards is inheriting a stale PASS (SN-0493). The symmetric failure mode is inheriting a stale FAIL: it freezes the story at the old number and hides the slope of improvement (t0601/t0614: 1.28–1.59s; t0660 re-measure: 0.95–0.99s, 25–35% faster). The trigger check is mechanical: did the tip move since the verdict? Did the subject's bytes change (pin mismatch)? Either = expiry. Expiry is retirement, not dishonor: the old FAIL stays as evidence about the OLD universe (t0601/t0614 remain the sealed record of the old code). And the oath move is explicit: "live bytes, not memory" — the seat said it out loud in the sign-in. When a cold successor reads a sealed FAIL, the first question is the pins: same tip, same bytes? If not, the verdict is retired and the measurement is owed fresh.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1220",
  "lesson": "sealed-verdict-expires-when-world-moves-fails-too",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "MEASUREMENT-INTEGRITY"],
  "extends": ["SN-0493"],
  "related": ["SN-1069", "SN-1206", "SN-080"],
  "evidence": {
    "sign_in": "#2175 comment 6153820810 (Naya Heart t0660, 2026-10-13): dispatch-time pin check found brief premise stale — t0601 (FAIL, sealed) closed the hole, t0614 (FAIL, sealed) confirmed — but tip moved e47a650e -> 582e5e5f AND smart_note_v2.py pin changed (fe6f2b4c… != 92d8b2b…), so old FAIL not inherited; re-measured live per the oath",
    "sign_out": "#2175 comment 6153897694 (t0660): FAIL — cold median 0.9682s vs CR-ACCEPT 0.5s bar (n_cold=2, n_warm=3), mincore 0-pre on 605 tree files both cold trials; new code 0.95–0.99s cold = 25–35% faster than t0601/t0614 (1.28–1.59s); SURGE (d) stands FAIL on current bytes",
    "receipt": "hidden_files/twelve-lane-receipts/t0660-lane11.md; verdict retrieval/cold-retrieve-isolated-t0660.md"
  },
  "rule": "Inherit nothing across a changed universe — not PASS verdicts and not FAIL verdicts. A sealed verdict binds to its pins (tip + subject bytes); tip moved or pin mismatch = verdict retired. Retire it with the reason stated, re-measure on live bytes. A stale FAIL inherited hides the slope of progress."
}
```
