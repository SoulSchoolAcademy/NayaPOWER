# IB-SMART-NOTE-20261009-sn0767-stand-down-expires-on-fresh-evidence.md

| Field | Value |
|---|---|
| Smart Note ID | SN-0767 |
| Intelligent Block ID | IB-SMART-NOTE-20261009-sn0767-stand-down-expires-on-fresh-evidence |
| Truth state | CANDIDATE (proposed intelligence — ratification is Shawn's word) |
| Scope | SYSTEM |
| Captured | 2026-10-09 |
| Source | Naya 2 brain-build loop, battery run 2026-10-09 ~11:26–11:36Z; PR #1959; scorecard receipt #1354 comment 6080067135 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

A stand-down classification — "this defect belongs to another seat's repair, hold" — is an **assumption about coverage, not coverage**. It expires the moment fresher evidence arrives. Before honoring a prior stand-down (even one your own lane posted hours earlier), verify the covering repair's **head bytes** actually cover your defect instances. Not the claim. Not the PR title. The bytes.

## HUMAN NOTE

This morning, my own lane's 04:19Z battery report classified the SN-0742/0743/0744 registry defects as "wave-owned (#1838/#1844/#1854)" and stood down. Eight hours later my battery found the same REDs still live. Instead of re-honoring the stand-down, I checked the three covering PRs on exact bytes: #1838's head registers only SN-0632..0639 (8 ids in its index.json patch); #1844 and #1854's patches mention SN-0742/0743/0744 zero times. The wave never covered these instances — the stand-down's premise was an unverified assumption, and it was falsified by a two-minute check. The repair (#1959) was built, tested, byte-verified, and merged the same run.

## CHILD NOTE

Imagine your friend says "don't worry, I already packed your lunch." You check the lunchbox — your sandwich isn't there. Their lunch is packed; yours isn't. Checking the box took ten seconds. Now you both eat.

## GRANDMA NOTE

"Trust, but verify" — the old saying. Someone said the problem was already fixed by someone else. It wasn't, quite. A quick look at the actual work (not the promise of the work) told the truth, and then the real fix got done in the same morning.

## NAYA NOTE

I am the loop that almost honored a stale disposition. The mechanism that saved the run: **the no-duplicate rule already requires re-verifying the open repair on exact bytes** — I applied that rule to the stand-down itself, not just to repair PRs. The rule generalizes: any disposition ("stand down", "owned by lane X", "will be fixed by wave Y") is a claim about future bytes. Claims expire; bytes don't lie.

## MACHINE NOTE

```
ON prior_stand_down(defect_instances D, covering_claim C):
  DO NOT honor C by reference.
  FETCH head(C).index_bytes (or the covering artifact at its claimed ref).
  IF D ⊆ covered(head(C)): stand down remains valid; log the byte-proof.
  ELSE: stand-down is STALE. Treat D as uncovered; proceed with own repair
        per the no-duplicate rule (scope-disjoint, claim-scan CLEAR).
ASSERT: "wave-sequenced" (L168) protects the wave's OWN scope only;
        it never extends coverage to instances the wave's bytes don't touch.
```

## LEARNING LESSON

**Coverage is a property of bytes, not of claims.** The board comment is the registry of *claims*; the tree at the claimed ref is the registry of *truth*. A lane that stands down on a claim without checking the bytes risks converting a live RED into an invisible one — the worst kind, because everyone believes it's owned.

Corollary: when you post a stand-down, post the byte-proof with it (the covering PR's head SHA + the exact ids/paths it covers). That turns your disposition from an assumption into checkable evidence — and lets the next run re-verify it in seconds instead of re-diagnosing from zero.

## HOW IT CONNECTS

- **No-duplicate repair rule (2026-10-02):** this note extends its "re-verify the open repair on exact bytes" step from repair-PR decisions to stand-down dispositions generally.
- **L168/L170 (2026-10-09):** wave-sequenced repairs are protected from consolidation *within their scope*; this note prevents that protection from being stretched over instances the wave never touched.
- **Evidence law:** a stand-down honored on an unchecked claim is UNKNOWN dressed as VERIFIED.
- **Team mutual-oversight:** "say it plainly and fix it" — the 04:19Z disposition was corrected openly on #1354 (comment 6080067135), own lane's miss included, no blame attached.

## EPISTEMIC STATE

- **Status:** CANDIDATE. One run of behavioral evidence (this run's decision chain); not yet a repeated pattern.
- **Falsifier:** a future case where the covering repair's head bytes DO contain the defect instances at claim time — then the stand-down was valid and this note's caution was unnecessary for that case. Two such consecutive cases would downgrade this from a lesson to a footnote.
- **What would strengthen it:** a second independent run where a wave-claim failed the byte check and the correction changed the outcome.

## UNCERTAINTY

- Medium: this is a single-incident lesson. It may be that most wave classifications are accurate and byte-checks usually confirm them — the lesson then costs a two-minute check per run, which is cheap insurance either way.
- The cost model favors the check: a false stand-down leaves a RED invisible indefinitely; a redundant check costs minutes.

## APPLICABILITY

- Every battery/verification run that classifies a RED as "owned by another lane's repair."
- Any relay or coordinator run that inherits a prior run's "no action" disposition.
- Merge-wave coordination: wave owners should publish the exact instance list their wave covers at entry (L169 re-anchor already requires byte-verification at exit).

## SUCCESSOR EFFECT

A successor run reading this note will: (1) never honor a stand-down by claim-reference alone; (2) include the byte-proof in its own stand-down receipts, making the next run's check a one-line re-fetch; (3) treat "wave-owned" as scoped protection, never as blanket coverage. The loop gets faster and the invisible-RED failure mode disappears.
