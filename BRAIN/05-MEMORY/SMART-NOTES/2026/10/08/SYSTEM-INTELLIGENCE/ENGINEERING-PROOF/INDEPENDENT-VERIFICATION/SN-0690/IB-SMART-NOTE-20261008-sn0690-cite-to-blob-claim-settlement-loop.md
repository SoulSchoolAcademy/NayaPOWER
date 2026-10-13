# Settle Cross-Seat Claims with a Cite-to-Blob Loop

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0690-cite-to-blob-claim-settlement-loop
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6062480260 ([NAYA 4 → Naya 2] Ratification sources for the "ratified" scores, 2026-10-08T14:48:36Z); #1354 6062684554 ([NAYA 2] Score sources VERIFIED, 2026-10-08T14:59:10Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two seats disagreed about score sources and settled it in eleven minutes with a clean protocol, no escalation. Naya 2 challenged the "ratified" labels in Naya 4's nine-team baseline. Naya 4 answered (6062480260) with the exact instrument: `BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md`, the header verbatim ("RATIFIED by Shawn Vibert, Human Director, 2026-10-05" under the Scorecard Law, machine-encoded in #1444, merged as `848576425`), the canonical instance (SN-0343, weighted total 6.8/10), the full ten-score list — and explicitly marked what had NO ratified score ("Unmeasured" — Evolution, Innovation — aren't in the ten-area instrument; they are not estimates). Naya 2 then re-read the file on **live main** (blob `765af2fc`) and published the verdict (6062684554): header confirmed, all ten scores and weights match exactly, "My earlier estimates are superseded." The loop has four rungs: **challenge → cite-to-the-blob → independent re-read on live main → published verdict.** Estimates live openly until this loop closes them; afterward they die by their owner's own hand.

## 🩷 HUMAN NOTE

Shawn — a tidy little protocol the team ran today, worth keeping. Naya 2 questioned whether Naya 4's "ratified" scores were really ratified. Naya 4 answered with the exact file, the exact header text, and the full score list — and honestly labeled the two areas with no score as unmeasured, not guesses. Naya 2 then went and re-read the file on live main herself, confirmed every number, and publicly dropped her own earlier estimates. Eleven minutes, no argument, no escalation. That's now the pattern: when a claim is challenged, the answer is a precise citation, the challenger verifies it independently, and both publish the verdict.

## 🟣 CHILD NOTE

Imagine two kids arguing about the rules of a game. Instead of shouting, they do this: one says "here's the rulebook, page 5, paragraph 2 — and these two things aren't in the rulebook at all, so I guessed them." The other kid goes and reads page 5 herself, checks every word, and says "you're right — I was guessing, my guesses are gone." That's what happened here. The rule: a challenge gets answered with the exact page, the challenger reads it herself, and everyone hears the verdict out loud.

## 👵 GRANDMA NOTE

Think of a family argument over a bill: one person says "this is what we agreed," and shows the signed contract with the exact line. The other reads the line themselves, confirms it, and says "you're right, my memory was off." That's the pattern the team used today over the score numbers — show the source, read it yourself, say the result out loud. From now on, a challenged claim is settled with a citation, an independent re-read, and a published verdict — no hand-waving on either side.

## 🧠 NAYA NOTE

Cold successor: when a seat's claim is challenged, do not argue the claim — run the loop. (1) **Cite:** the defending seat answers with the exact instrument — file path, blob SHA, ratification header verbatim, per-item list, and an explicit "unmeasured" marking for anything without a ratified value (never an estimate presented as a score). (2) **Re-read:** the challenging seat independently reads the cited bytes on live main — never the challenger's memory of the file, never the defender's copy. (3) **Verdict:** the challenger publishes the result — confirmed, superseded, or still open — and withdraws their superseded estimates by their own hand. Estimates are first-class citizens until the loop runs; after it, only the loop's output stands. The contrast case is the same tick's "17 of 23" metric (SN-0688): a number that could not be cited to an audit stopped traveling — the loop's absence is the signal, not a rounding error. Evidence: #1354 6062480260 (cite), #1354 6062684554 (re-read + verdict; blob 765af2fc; all ten scores + weights confirmed; estimates superseded).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0690",
  "title": "Settle Cross-Seat Claims with a Cite-to-Blob Loop",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"],
  "cousins": ["SN-0682", "SN-0688", "SN-0668", "SN-0420"],
  "evidence": {
    "cite": "#1354 6062480260 ([NAYA 4 → Naya 2], 2026-10-08T14:48:36Z): instrument BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md; header verbatim 'RATIFIED by Shawn Vibert, Human Director, 2026-10-05' under the Scorecard Law (machine-encoded #1444, merged as 848576425); canonical instance SN-0343 (weighted total 6.8/10); full ten-score list; 'Unmeasured' (Evolution, Innovation) explicitly not in the ten-area instrument — not estimates",
    "re-read": "#1354 6062684554 ([NAYA 2] Score sources VERIFIED, 2026-10-08T14:59:10Z): re-read on live main, blob 765af2fc; header confirmed; all ten scores and weights match exactly",
    "verdict": "'My earlier estimates are superseded' — published by the challenger, eleven minutes after the challenge",
    "contrast": "same-tick '17 of 23' metric (SN-0688): uncitable, so the honest halt instead of the loop"
  },
  "rule": "challenge → cite-to-the-blob (file + blob SHA + header verbatim + per-item list, unmeasured marked as such) → independent re-read on live main → published verdict; estimates stand until the loop closes, then die by their owner's own hand"
}
```
