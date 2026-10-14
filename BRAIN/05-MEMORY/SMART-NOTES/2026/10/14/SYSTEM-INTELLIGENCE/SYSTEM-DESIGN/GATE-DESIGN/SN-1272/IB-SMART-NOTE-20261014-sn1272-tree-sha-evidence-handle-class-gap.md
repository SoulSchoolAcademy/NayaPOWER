# SMART NOTE — A 40-hex string is not necessarily a commit SHA (receipt-gate handle-class gap)

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1272` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1272-tree-sha-evidence-handle-class-gap` |
| Human title | A 40-hex string is not necessarily a commit SHA (receipt-gate handle-class gap) |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | GATE DESIGN |
| Captured | 2026-10-14 08:38:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Automatic truth ceiling | CANDIDATE |

---

## ✦ IN A NUTSHELL

**The receipt gate refused true evidence because its handle taxonomy has no tree-SHA class.** PR #2525's `## Evidence` cited one handle — a tree SHA (`bad8a301…`) that is byte-identity proof (`git rev-parse 99c5deb7^{tree}` equals the cited value exactly). The gate read the 40-hex string as a *commit* SHA, ran `merge-base`, and rejected it as "not a commit in this PR." Binding logic correct, handle-class gap: a 40-hex string must be object-class-resolved before it is type-assumed.

---

## 🩷 HUMAN NOTE

A lane's evidence was genuinely true — the cited tree hash matched the real tree byte-for-byte — and the checker threw it out anyway. Not because the evidence was wrong, but because the checker only understands three kinds of evidence handles (URL, commit SHA, repo path) and had no box labeled "tree SHA." It saw 40 hex characters, assumed "commit," asked git to treat a tree like a commit, and git said no. The lesson for the next gate: when evidence arrives as a 40-hex string, ask git what kind of object it is *first*, then decide which check applies. True evidence rejected by a type assumption is a false reject — and false rejects erode trust in the gate just as surely as false passes do.

---

## 🟣 CHILD NOTE

Imagine a bouncer who only knows three kinds of ID: a passport, a driver's license, and a library card. You show up with a perfectly valid student ID. The bouncer looks at it, says "that's not a passport," and turns you away — even though the school confirmed it's real. The student ID was fine; the bouncer just didn't have a box for it. Next time, the bouncer should check what *kind* of ID it is before deciding.

---

## 🔵 GRANDMA NOTE

When a checker rejects good evidence, the problem may not be the evidence — it may be the checker's list of what counts as evidence. A 40-character code can be several different git objects; assuming it's always a commit is the trap. Resolve what it actually is before judging it.

---

## 🟠 NAYA NOTE

1. **Object-class before type-assumption.** Any evidence handle that arrives as a 40-hex string gets `git cat-file -t` (or equivalent) before any commit-specific operation (`merge-base`, rev-list) runs on it.
2. **Handle taxonomy is a design surface, not a constant.** When a battery's false-reject probe finds a genuine handle class the gate doesn't model, the finding is a gate defect — route to the authoring lane as measurement, not as a repair prescription.
3. **Probe past the author's boundary.** The finding came from a 9-body false-reject sample run *outside* the author's own battery — 8/9 PASS, 1/9 a genuine false reject. Batteries that only replay the author's RED cases confirm the fix; the hole lives past the calibrated edge.
4. **A false reject is a gate defect, full stop.** It does not become acceptable because the gate is "strict." Strictness without precision is noise.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1272-tree-sha-evidence-handle-class-gap",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "finding": {
    "class": "handle-taxonomy gap",
    "gate": "receipt gate (check_pr_receipt.py)",
    "trigger": "PR #2525 ## Evidence cited tree SHA bad8a301…",
    "ground_truth": "git rev-parse 99c5deb7^{tree} == bad8a301… (TRUE byte-identity proof)",
    "gate_behavior": "read 40-hex as commit SHA; merge-base failed on tree object → 'not a commit in this PR' → REFUSED",
    "binding_logic": "correct",
    "defect": "handle taxonomy has no tree-SHA (content-identity) class"
  },
  "rule": "resolve object class (git cat-file -t) before type-assuming any 40-hex evidence handle",
  "falsifier": "the gate gains a tree-SHA handle class and #2525's cited handle passes",
  "routed_to": "Lane 9 (authoring lane), measurement-only",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6163175990",
    "receipt": "hidden_files/auditor-wave120-2574battery-20261014.md",
    "trace_dir": "hidden_files/auditor-wave120-2574battery/",
    "probe": "Probe B false-reject sample: 8/9 PASS, 1/9 FAIL (#2525)"
  },
  "human_projection_root": "BRAIN/05-MEMORY/SMART-NOTES",
  "decision_change": "future evidence-handle taxonomies must include a tree-SHA (content-identity) class; 40-hex handles are object-class-resolved, never type-assumed",
  "connects_to": ["SN-1267 (touch-map before battery)", "SN-251-candidate (probe past the author's boundary)"]
}
```

---

## 🧾 PROOF / PROVENANCE

| Object | Value |
|---|---|
| Board comment | `6163175990` (#2537, 2026-10-14T07:25:31Z, Naya Auditor sign-out wave 120) |
| Receipt | `hidden_files/auditor-wave120-2574battery-20261014.md` + trace dir |
| True-bytes check | `git rev-parse 99c5deb7^{tree}` == cited `bad8a301…` |
| Probe design | Probe A sabotage 12/12 CORROBORATED; Probe B 9-body false-reject sample 8/9 PASS, 1/9 REFUTED |
| Tip anchor | `92329c5795ef8a50d02adf94ee6c91c313c26daf` (unchanged in-step) |

---

## ⚠️ TRUTH BOUNDARY

**Proven:** #2525's cited handle is true byte-identity proof; the gate refused it on a type assumption, not on content.

**Not implied:** the gate's other refusals are wrong; tree-SHA handles are always appropriate evidence; the routed repair shape (authoring lane's call).

This note stays **CANDIDATE** until the authoring lane repairs the taxonomy and a re-run battery shows the handle passing.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
