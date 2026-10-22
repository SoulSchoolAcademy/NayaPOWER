Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Check where the artifact lives before naming the pin shape. A commit SHA cannot pin an artifact that lives outside every git repo on the machine — for workspace-local instruments the honest pin is hash + manifest + archived re-runnable experiment + receipt chain. And a hash without a fresh experiment is a rumor with good formatting.

## 🩷 HUMAN NOTE

A pin is like the tag on your luggage — it only works if it points at the right bag. On 2026-10-22 the lane-9 scorer was asked to prove a tie-experiment's result, but the experiment lived in a workspace directory, not inside any git repo — so there was no commit SHA to name. The honest pin turned out to be four things: the hash of the artifact, a manifest saying what the hash covers, the archived experiment you can re-run, and the receipt chain. The seat re-ran the experiment fresh and got byte-identical output to the October 18 archive — and along the way retired a +-0.03 tolerance as VOID at five places it had been byte-carried. A tolerance that was never proven is not precision — it's decoration.

## 🟣 CHILD NOTE

If you want to prove you built the same LEGO tower twice, you can't point at a photo of somebody else's tower. You point at YOUR tower, show the instructions, and build it again the same way.

## 🔵 GRANDMA NOTE

Darling, a label on a jar is only honest if it's the right jar. And a recipe you can't cook again isn't a recipe — it's a memory. Write down what's in the jar AND keep the recipe working.

## 🟠 NAYA NOTE

Pins have an address space. A git commit SHA addresses the object store of one specific repo; workspace-local artifacts (experiments, generated manifests, local instruments) live in no repo's address space, so naming a SHA is a dangling reference dressed as rigor. The pin for an out-of-repo artifact is a bundle: content hash + manifest (what the hash covers) + archived re-runnable experiment + receipt chain. The fresh re-run is what converts the bundle from claim to evidence — a hash without a fresh experiment is a rumor with good formatting. Tolerances byte-carried through receipts act as facts on read; an unproven tolerance must be struck, not inherited (the +-0.03 retired VOID at five byte-carried sites).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1814",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T10:48:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "VERIFICATION",
  "sub": "INSTRUMENT-DISCIPLINE",
  "lesson": "A pin is only as good as its address. Commit SHAs cannot pin artifacts that live outside every git repo on the machine; for workspace-local instruments the honest pin is hash + manifest + archived re-runnable experiment + receipt chain. A hash without a fresh experiment is a rumor with good formatting — the fresh re-run byte-compared against the archive is what converts the bundle from claim to evidence. Tolerances byte-carried through receipts act as facts on read; an unproven tolerance must be struck, not inherited.",
  "decision_change": "The 'how do I pin this artifact?' decision: first check where the artifact lives. In-repo => commit SHA (plus tree/hash as needed). Out-of-repo => hash + manifest + archived re-runnable experiment + receipt chain, and the evidence package must include a fresh re-run byte-compared to the archive. Never cite a tolerance that was carried but never proven — retire it or prove it.",
  "falsifiability": "This lesson breaks if a case shows a commit SHA resolving to an out-of-repo workspace artifact, or a hash-only pin (no re-run) surviving an independent replication. The lane-9 re-run is the control: byte-identical output on re-run — had the re-run diverged, the pin would have been wrong, proving the bundle insufficient.",
  "mechanism": "A SHA addresses bytes inside one object store; it cannot address what the store never contained, so naming it for an out-of-repo artifact is a dangling reference. Evidence for out-of-repo artifacts must be self-contained: hash (content identity) + manifest (coverage of the hash) + archived experiment (replayability) + receipts (provenance) + fresh re-run (present-tense truth). Tolerances carried byte-for-byte through receipts are read as facts downstream — unproven tolerances compound into false precision.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-scorer-20261014-2200-lane9.md (2026-10-22): fresh tie-experiment re-run byte-identical to the 2026-10-18 archive; +-0.03 tolerance retired as VOID at five byte-carried sites",
    "hidden_files/learning-events-2026-10-22-10.md, CANDIDATE 801 (window ending 2026-10-22T10:20:19Z): 'a pin is only as good as its address' — new principle"
  ],
  "cousins": [
    "SN-1812 (detection is not remediation — the guard re-run requirement; same demand for present-tense proof, different leg: guards vs pins)",
    "SN-1806 (detection-not-remediation — the prior generation of the same demand; this note extends it to artifact pins)"
  ],
  "applies_when": [["verification", "pin"], ["artifact", "pinning"], ["experiment", "reproducibility"], ["scorecard", "evidence-pin"]],
  "enforcement": "A verification receipt that pins an artifact must include a fresh re-run of the archived experiment with a byte comparison against the archive (lane-9's fresh tie-experiment re-run is the worked example). Scorecard/verify gates reject pins that name a commit SHA for artifacts outside every repo, and reject hash-only pins with no re-run — a hash without a fresh experiment is a rumor with good formatting.",
  "dedupe_guard": "Not a duplicate: SN-1812 covers the guard-output contract (remediation_state + hand_prep_owner, guard re-run green at the landed tip); SN-1806 is the earlier detection-vs-remediation note. Neither names the address-space question — what a SHA can and cannot address — or the hash+manifest+experiment+receipt bundle for out-of-repo artifacts. This note closes that leg."
}
```
