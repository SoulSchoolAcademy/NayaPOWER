# The Falsifiability Battery — a Proof Gate Must Prove It Can Fire

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0531-falsifiability-battery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6033758045 (2026-10-07T08:08:30Z — [NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] Cycle #1702-VERIFY: independent verification of #1702, LEARNING compounding proof gate H13 cycle-2, SoulSchoolAcademy).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Cycle #1702-VERIFY independently verified the LEARNING compounding proof gate (#1702, PR-head-exact `8a542665`, EXIT=0 PASS, metrics reproducing exactly: P0=0.333, P1=0.417, P2=0.500; L2={remove→delete}; S2 cold subprocess retrieval with no_prior_context=True). But the PASS alone is not what made the gate trustworthy — the **negative-control battery** is:

1. **Neutered derivation:** with the synonym map neutered (p2=p1), F1 fires, exit 1. This does not just prove the gate can fail — it **proves causality**: the P2 gain is causally attributable to the synonym map, not to noise or a side effect.
2. **Planted canary:** a canary grant planted in the environment makes F3 fire, exit 1, naming the file — proving the gate actually reads the grant surface it claims to guard.
3. **Wrong-lesson scenario:** an incorrect lesson fails closed (exit 1, attributed via F1 precedence) — proving the gate rejects the near-miss, not only the far-miss.

The durable rule: **a proof gate whose PASS cannot be contrasted with a demanded RED proves nothing.** Every compounding/proof gate ships with its negative-control battery, and verification runs the gate *unmodified* on PR-head-exact blobs at the pinned tip — the same binary that passes must be the one that fires on the controls. A causality claim (the gain comes from X) is admissible only when neutering X flips the verdict. Pairs with SN-0440 (one exact-tip battery is enough) — the tip pin and the falsifiability battery together are what make a gate's PASS evidence-grade.

## 🩷 HUMAN NOTE

Shawn — the independent verification of the LEARNING compounding gate (#1702) came back SOURCE-VERIFIED, but here's the part worth locking in: I don't trust the PASS because it passed. I trust it because I proved the gate *can* fail — on command. We neutered the derivation (which must make it fire — and it also proves the performance gain is causally caused by the synonym map, not luck), planted a fake grant (which it caught by name), and fed it a wrong lesson (which it rejected). Rule going forward: every proof gate we build ships with a negative-control battery, run on the exact same bits as the passing run. A gate that can't go RED on demand is a green light wired to a battery — it was always going to be green.

## 🟣 CHILD NOTE

Imagine a smoke detector. Pressing its test button and hearing it beep proves it works. But if you never press the button — or the button is fake — you have a plastic circle on the ceiling and false confidence. We tested the LEARNING gate the same way: we made fake smoke (a broken setup), waved it at the detector, and confirmed it screamed. Three kinds of fake smoke, three screams. Only then did we believe the quiet.

## 👵 GRANDMA NOTE

Think of it like a home alarm system. The salesman tells you it's armed, but you don't just take his word — you open a window yourself and wait for the siren. We did exactly that with the LEARNING gate: we staged three break-ins of our own (disabled the learning map, planted a fake permission, taught it the wrong lesson) and confirmed the alarm went off each time, for the right reason. The rule we keep: no alarm is trusted until we've broken in ourselves.

## 💜 NAYA NOTE

Note to future me: whenever you build or verify a proof gate, the PASS is the *last* thing you check, not the first. First run the negative-control battery on the same unmodified binary at the pinned tip: (1) neuter the mechanism under test and demand a RED — this is the causality proof, not just a failure demo; (2) plant a canary the gate must detect by name; (3) feed the near-miss (wrong lesson, subtly invalid input) and demand fail-closed with correct attribution. If any control stays green, the gate is decorative — fix the gate before you celebrate the PASS. Record the control results next to the pass metrics; they are half the evidence. And never claim a gain is "caused by X" without the neuter-X test — correlation across runs is not causality, a single flipped verdict is.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0531",
  "rule": "falsifiability-battery",
  "statement": "A proof gate's PASS is evidence only when the same unmodified binary at the pinned tip demonstrably fires RED on its negative-control battery: neutered-mechanism, planted-canary, and wrong-input fail-closed.",
  "corollaries": [
    "Causality claims require the neuter test: neutering X must flip PASS to RED, else the gain is not attributed to X.",
    "Run the battery on PR-head-exact blobs, unmodified — a rebuilt or patched binary is a different subject.",
    "Record control verdicts alongside pass metrics; both are the evidence.",
    "A gate that cannot go RED on demand is decorative, regardless of its PASS rate."
  ],
  "source": "#1354 6033758045 (2026-10-07) — cycle #1702-VERIFY, PR #1702 head 8a542665, tip re-pinned e7de7b88"
}
```
