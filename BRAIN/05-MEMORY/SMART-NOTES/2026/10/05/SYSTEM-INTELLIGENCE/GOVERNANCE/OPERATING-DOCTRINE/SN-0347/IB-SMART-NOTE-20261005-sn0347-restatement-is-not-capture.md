# Restatement Is Not Capture — Encode Against the Existing Note

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0347-restatement-is-not-capture
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A standing law must be ENCODED against the note that already carries it, never restaged as a new note. When a lane restates doctrine that already lives in the brain (the collision that produced SN-0340 and SN-0343 on 2026-10-05 is the live example: SN-0341 was first-claimed, the 10-area scorecard was renumbered to SN-0343, the Scorecard Law to SN-0340 — all verified free, none duplicated), the distillation loop must not stage a fresh capture of the same method. Instead: bind the new work to the existing Smart Note — add the binding (e.g., bind SN-0340's machine note to the canonical V2.1 calculus object, closing the drill's G1 gap), reference it, and let the standing law's encoding (here: auto_merge_gate.py) point at the existing SN.

Every duplicate capture of existing doctrine dilutes the brain: two notes claiming one truth splits provenance, confuses the retrieve path, and forces every future consumer to reconcile a question the brain should answer once. The admission gate's "new — not duplicating an existing Smart Note" clause is the front door; this rule is the back door: it covers restatement of captured METHOD, not just captured content. When in doubt, the default action is a binding, not a note.

## 🩷 HUMAN NOTE

Don't re-write a law the brain already has. If a new piece of work proves, uses, or restates a rule that's already captured as a Smart Note, connect the new work TO that note — link it, reference it, bind to it. Writing the same law again in a second note doesn't make it stronger; it splits it in two and leaves every future Naya guessing which copy is real.

## 🟣 CHILD NOTE

If the rule already exists in the brain, do not write it again — point to the existing one instead.

## 🔵 GRANDMA NOTE

One truth, one record. Restating what is already recorded does not preserve it twice — it divides it.

## 🟠 NAYA NOTE

Make "encode, don't restage" a standing step of the capture loop: before staging, scan the tree for an existing SN carrying the doctrine; if one exists, produce the binding (machine-note reference, canonical-object pointer, or code constraint) and stop — no new SN number is taken. This protects the admission gate against the quietest form of noise: restatement that is true, evidence-backed, and durable, but already captured. The 2026-10-05 renumbering sequence (SN-0341 → SN-0343, SN-0340 first-claim standing, branch commits deleting the duplicated file) is the canonical example of this repair applied in flight.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "restatement of captured method is not a new note; bind new work to the existing SN instead of staging a duplicate",
  "procedure": ["scan tree for existing SN carrying the doctrine", "if present, produce binding (machine-note reference / canonical-object pointer / code constraint)", "take no new SN number"],
  "canonical_example": {
    "event": "SN-0341 first-claimed per collision rule; 10-area scorecard renumbered to SN-0343; Scorecard Law staged as SN-0340",
    "binding": "G1 gap closed by binding SN-0340 machine note to canonical V2.1 calculus object (commit a9890527)",
    "flag": "lock-in lane must encode the standing law against SN-0340, not restage the method"
  },
  "guards": "admission gate clause 'new — not duplicating an existing Smart Note' (front door); this rule covers restatement of captured METHOD (back door)",
  "evidence": {
    "board_comments": [5995525760, 5995616251, 5995578997],
    "branch": "naya4/smart-notes-2026-09-30",
    "related": ["SN-0340", "SN-0343", "SN-0341"]
  }
}
~~~
