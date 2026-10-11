# A Pin Is an Authority Claim — the Heal Path Follows the Artifact's Truth State

| Field | Value |
|---|---|
| Intelligent Block | SN-0761 |
| Title | A pin is an authority claim — when a manifest-coverage check fires, the heal path follows the artifact's truth state: RATIFIED gets pinned, CANDIDATE gets an exclusion with reason |
| Date | 2026-10-08 |
| Seat | Naya 4 (distillation loop) |
| Source | #1354 comment 6075260678 (PIPELINE-MONITOR, 2026-10-09T05:59:47Z / 2026-10-08 22:59 PDT) — spec-integrity RED on tip `696f4878`; repair PR #1952 (open, unmerged); drive-loop draft PR #1950 (open, same heal); failing check `tools/spec_integrity_check.py` via `tools/spec_integrity_manifest.json` |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-08 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

The spec-integrity check fired on main tip `696f4878`: PR #1949 had landed the new machine spec `BRAIN/01-GOVERNANCE/0006-naya-calculator-v1.machine.json` without registering it in `tools/spec_integrity_manifest.json`. The check's failure message offers two heal paths: **pin it in the manifest, or record an exclusion with reason.** Two lanes (drive loop #1950, pipeline-monitor #1952) independently converged on the same answer: **exclusion, not a pin** — because the spec is `status: CANDIDATE`. Pinning it in the ratified-spec manifest would have canonized an unratified spec just to buy a green check. The standing doctrine: **a pin is an authority claim.** The manifest is a law-pipeline enforcement structure; the heal path follows the artifact's truth state — RATIFIED specs get pinned, CANDIDATE specs get exclusion entries with reason (precedent: the 0003/0013/0014 exclusions). When the check fires on your new spec, read the artifact's truth state before choosing the heal path. Never pin what isn't ratified.

## HUMAN NOTE

Shawn — this one's about what a "pin" actually means. When the spec-integrity tripwire fired on the new calculator spec, the obvious fix was to pin it in the manifest and make the check green. But pinning isn't paperwork — it's a claim that says "this spec is governed, ratified law." The calculator spec is CANDIDATE; it hasn't earned that claim yet. So both lanes that looked at it independently did the same thing: recorded it as an *exclusion with reason* instead — "this exists, it's not pinned, here's why." The check goes green honestly, and the spec stays exactly as unratified as it is. The rule we're writing down: a pin is an authority claim, and you never spend authority you don't have. Green checks bought with false authority are how systems rot.

## CHILD NOTE

Imagine a club has a list on the wall: "Members." A new kid shows up and hasn't joined yet. You could write their name on the Members list to stop the argument — but then the list would be a lie. The honest thing is to write on a different note: "This kid is here, not a member yet, here's why." That's what happened: the new spec wasn't pinned (it isn't a "member" yet), it was recorded as an exclusion with the reason. The list stays honest, and the new kid can earn membership later. Never write a name on the Members list that doesn't belong there — not even to stop an argument.

## GRANDMA NOTE

Sweetheart, this is about honest lists. The team keeps a manifest — a list of the specs that are truly, officially ratified law. A new spec arrived that isn't ratified yet, and the checking machine complained it wasn't on the list. The tempting fix was to just add it to the list and make the machine quiet — but that would make the list a lie. So instead, they wrote a note next to it: "not on the list yet, and here's why." The machine is happy, the list is honest, and the spec can earn its place later. The lesson: never put a name on an official list to make a machine stop complaining. A quiet machine with a dishonest list is worse than a noisy machine with an honest one.

## NAYA NOTE

This is the SN-0420 family applied to manifest mechanics, and it is worth a note of its own because the trap is *offered by the check itself*. The failure message says "pin it in the manifest or record an exclusion with reason" — both are legitimate, both make the check green, and the wrong one (pin) is the path of least resistance. A cold Naya whose instinct is "make it green" will pin. The doctrine that stops the instinct: **a pin is an authority claim.** `tools/spec_integrity_manifest.json` is not a registry of files-that-exist; it is a registry of specs the system treats as governed. Pinning a CANDIDATE spec there is canonization-by-green-check — the exact pathology SN-0420 names (a repair that makes the check pass by absorbing the anomaly).

The selection rule is mechanical:
1. Read the artifact's truth state (the spec's own `status` field / envelope).
2. RATIFIED (DIRECTOR-RATIFIED envelope, phase structure) → pin.
3. CANDIDATE (no ratified envelope) → exclusion entry WITH REASON, citing the status. Precedent: 0003/0013/0014 exclusions already in the manifest.
4. If the status is ambiguous, exclusion is the fail-safe — an exclusion with reason can be promoted to a pin at ratification; a pin must be *unwound*, which nobody remembers to do.

Note the convergence: two independent lanes (drive loop #1950, pipeline-monitor #1952) reached exclusion-not-pin without coordinating. When two lanes derive the same heal from the same evidence, the doctrine is re-derivable — it belongs in the brain, not in lane memory. (Both repair PRs are still open and unmerged at capture; the merge protocol governs them. Two open PRs for one manifest line is itself a live SN-0236/SN-0711 situation for the wave owners to reconcile — recorded, not absorbed.)

## MACHINE NOTE

```json
{
  "intelligent_block": "SN-0761",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "rule": {
    "id": "PIN-IS-AN-AUTHORITY-CLAIM",
    "trigger": "spec_integrity_check.py fails with 'unpinned machine spec <path> -- pin it in the manifest or record an exclusion with reason'",
    "action": "read the artifact's truth state FIRST, then choose the heal path",
    "paths": {
      "RATIFIED": "pin in tools/spec_integrity_manifest.json",
      "CANDIDATE": "exclusion entry with reason (status=CANDIDATE, no ratified envelope)",
      "ambiguous": "exclusion (fail-safe; promotion to pin happens at ratification)"
    },
    "prohibition": "never pin a CANDIDATE artifact to silence the check — a pin claims governance; spending unheld authority is canonization",
    "precedent": "0003/0013/0014 exclusions already recorded in the manifest"
  },
  "relations": [
    {"type": "SPECIALIZES", "target": "SN-0420", "note": "SN-0420 forbids absorbing the anomaly; this note is the manifest-mechanics instance: pinning a CANDIDATE spec is the absorption"},
    {"type": "COMPOSES_WITH", "target": "SN-0438", "note": "the tripwire firing was correct — this note governs the heal, not the trip"},
    {"type": "MECHANISM_OF", "target": "LAW-IS-CODE", "note": "the manifest is an enforcement structure; pins are authority claims written into it"}
  ],
  "canonical_example": {
    "date": "2026-10-08",
    "check": "spec-integrity on tip 696f4878",
    "artifact": "BRAIN/01-GOVERNANCE/0006-naya-calculator-v1.machine.json (status=CANDIDATE, landed via PR #1949)",
    "heal": "exclusion with reason (two independent lanes: #1950 drive loop, #1952 pipeline-monitor)",
    "not_heal": "pinning the CANDIDATE spec in the ratified manifest"
  }
}
```

## LEARNING LESSON

The check offers both heal paths, which means the check cannot protect you from choosing wrong — both paths turn it green. The protection has to live one layer up, in the seat: know what a pin *claims* before you write one. This is the general form of a whole class of tripwires — any check whose heal is "register X in the governed list" tempts the seat to register first and earn later. The durable habit: when a check offers registration as the heal, ask "does this artifact currently hold the authority this registration claims?" If not, record the exclusion with the reason, honestly.

## HOW IT CONNECTS

- **SN-0420** (never absorb the anomaly): this note is its manifest-mechanics specialization — pinning the CANDIDATE spec would have been absorption.
- **SN-0438** (fail-closed is the design working): the tripwire firing was correct behavior; this note is only about choosing the heal.
- **LAW-IS-CODE (Prime 2)**: the manifest is law encoded as an enforcement point — which is exactly why writing a false pin into it is disobedience, not housekeeping.
- **SN-0236 / SN-0711**: the two open repair PRs (#1950, #1952) for one manifest line are a live duplicate-repair situation; the wave owners reconcile, the lanes do not self-merge.

## EPISTEMIC STATE

- **CONFIRMED** (board, live API): the RED (comment 6075260678: exact failure reproduced locally, classification PR-introduced by #1949, tripwire fired correctly); both repair PRs exist, open, unmerged, each touching only `tools/spec_integrity_manifest.json` (#1950 drive loop, #1952 pipeline-monitor).
- **CONFIRMED** (comment text): both lanes chose exclusion-not-pin with the same stated reason (status=CANDIDATE, precedent 0003/0013/0014); the convergence is documented, not inferred.
- **UNCONFIRMED**: which of #1950/#1952 survives the wave-owner reconciliation, and whether the exclusion text in the surviving PR matches the canonical reason.
- **JUDGMENT**: the pin-is-an-authority-claim rule is CANDIDATE — one incident, two independent derivations; it has not yet governed a second incident.

## UNCERTAINTY

- Whether exclusion entries need a machine-readable expiry or a ratification-promotion trigger, or whether the manifest's current free-text reason field suffices.
- Whether a third truth state exists (e.g., DEPRECATED specs) that needs its own heal path.
- The exact reconciliation outcome between #1950 and #1952 — wave-owner decision pending.

## APPLICABILITY

Any seat, any lane, any time `tools/spec_integrity_check.py` (or any manifest-coverage tripwire) fires on a newly added artifact. Applies to machine specs, and by extension to any governed registry where registration is offered as the heal (migration ledgers, pin manifests, grant registries).

## SUCCESSOR EFFECT

A future seat facing an unpinned-artifact RED reads the artifact's truth state first and picks exclusion-with-reason for CANDIDATEs without hesitation — no green-bought pins, no unwound canonizations. The measure: count of pins in the manifest whose artifact lacks a ratified envelope, trending to and staying at zero.
