# SMART NOTE — The Verifier Names Its Boundary

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-121` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn121-verifier-names-its-boundary` |
| Human title | The Verifier Names Its Boundary |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-02 01:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (verification method — pending taxonomy adoption) |
| Capture type | Method / Process fix |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5943580968 (Naya 2 relay: "v3 correction received, evidence verified" — `naya4/hub-rooms-v1 @ 3fc7a23c`): the sha256 of the staged base blob matched Naya 4's claimed prefix "exactly", followed by the named bound: "(Epistemic bound: I verify what the branch holds; I don't hold the original upload, so the byte-equality half of that claim is yours, not independently confirmed.)" |

---

## ✦ IN A NUTSHELL

**A verification report is only as honest as its stated boundary.** Naya 2 independently verified Naya 4's v3 repair and confirmed the uploaded base file's sha256 matched the claimed prefix — then wrote down exactly what she did *not* verify: she could confirm what the branch holds, but she did not hold the original user-supplied upload, so the byte-equality half of "identical to the original" remained Naya 4's claim, not her independent confirmation. Without that one parenthetical, a reader would have inferred full end-to-end coverage from a partial check. The rule: every verification ends with the named epistemic bound — what I checked, and what remains somebody else's claim.

---

## 🩷 HUMAN NOTE

Imagine a home inspector who checks every room of the house you're buying — and then tells you, in writing, "I inspected everything inside the house; I did not inspect the foundation because I couldn't access it." That's the inspector you trust. The one who just says "all good" and leaves the foundation unmentioned is the one who costs you money later. Naya 2 did the first thing: she confirmed everything she could check, and named the one thing she couldn't. A verification without a stated boundary is an implied promise you never made.

---

## 🟣 CHILD NOTE

Your friend says "I checked your LEGO castle and it's perfect!" — but she never looked at the bottom pieces because they were stuck to the table. The good friend says "I checked everything I could see, but I couldn't check the bottom pieces." That's honest. Always say what you checked AND what you couldn't check.

---

## 🔵 GRANDMA NOTE

When someone checks your work for you, the most trustworthy ones tell you the limits of their checking. "I looked at this and this — but not that." An unchecked claim that everyone assumes was checked is how mistakes hide. Name the boundary, every time.

---

## 🟠 NAYA NOTE

1. **State the bound in the verification itself, not in a footnote later.** The epistemic bound ("I verify what the branch holds; I don't hold the original upload") was delivered inside the verification report — that's what makes it load-bearing. A bound stated only when asked is a confession; a bound stated upfront is a method.
2. **A partial check without a bound reads as a full check.** The reader's default inference is "verified = fully verified." The verifier's job is to defeat that inference explicitly: name the unchecked half, name whose claim it remains, and say what would be needed to check it (here: access to the original upload).
3. **Owning the bound is verifier-side correction culture.** The sibling event — Naya 4's public correction of her own false staging claim (5943536247) — is the builder side. The verifier side is this: never let a favorable verdict outrun your coverage. The bound protects the verdict's credibility more than the verdict protects itself.
4. **Make the bound checkable.** "I verify what the branch holds" is operational: anyone can re-run the same check on the same commit (`3fc7a23c`) and get the same answer. The bound is not vagueness — it's a precise contour of what the evidence supports.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn121-verifier-names-its-boundary",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "method": "named epistemic boundary in verification reports",
  "instance": {
    "verification": {"verifier": "Naya 2", "subject": "naya4/hub-rooms-v1 @ 3fc7a23c", "evidence": "#554 comment 5943580968"},
    "confirmed": "base blob sha256 c08a7fee…d436 matches claimed prefix; base files present in branch tree (864,094 B + 501 B); v3-harness reproduced 50/50 twice",
    "bound": "branch-holdings verified; original-upload byte-equality NOT independently confirmed — remains builder's claim",
    "sibling": "#554 comment 5943536247 (builder's public correction of the false staging claim that made this verification necessary)"
  },
  "rule": "every independent verification report states its coverage boundary explicitly — what was checked and what remains unverified or someone else's claim; a partial check without a named bound is silently overclaimed as a full check",
  "family": ["SN-058 (adversarial implementation-fidelity audit)", "SN-043 (compare at ONE commit)", "SN-061 (post-merge verification at the pin)", "SN-083 (retain the UNKNOWN with its missing evidence named)"],
  "open": ["nothing open — the bound was honored; the note records the method"],
  "evidence": ["#554 comment 5943580968"]
}
```

---

## 🔗 HOW IT CONNECTS

- **SN-058** (adversarial implementation-fidelity audit): the verifier checks field-level fidelity; SN-121 adds the mandatory scope statement to that check.
- **SN-043** (compare at ONE commit): the commit pin defines the verified subject; SN-121 defines the verified *extent* at that pin.
- **SN-061** (post-merge verification at the pin): verdicts die at every new SHA; SN-121 adds that verdicts also die at the coverage boundary.
- **SN-083** (retain the UNKNOWN with its missing evidence named): the same honesty applied to open findings; SN-121 applies it to closed verdicts.

---

*Truth state: CANDIDATE — auto-captured, not ratified. Only Shawn ratifies.*
