# SMART NOTE — The Seal Proves Consistency, Not Authorship

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-111` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn111-seal-proves-consistency-not-authorship` |
| Human title | The Seal Proves Consistency, Not Authorship |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-01 22:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (trust-semantics distinction — auditor-grade) |
| Capture type | Doctrine / Distinction |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5942032703 (Coda 1: "OWNER-PROVENANCE AUDIT CLOSED — 8c027928"; commit `bee101b47` on `coda1/owner-provenance-audit-8c027928`; 6 passed) |

---

## ✦ IN A NUTSHELL

**Coda 1 closed the owner-provenance audit with the distinction that must not collapse: the VERIFY seal proves the receipt was not altered after close — content integrity. It does NOT prove the submitter was the claimed owner — because `owner_id` is caller-asserted at receipt creation and no principal, auth, or caller identity is bound in `_refusal_precheck`/`_new_receipt`.** An unkeyed seal is evidence of consistency, not authorship — same limitation class as the correctly-rehashed counterfeit note already on record. Three sharper edges: `requesting_owner` is NOT separately allowlisted, so if a future change makes the runtime read it, the allowlist silently under-covers it (a comment at the field is the owed guard); the genuine authority check found was credited, not buried (`_refusal_precheck` refuses a cross-owner consent gap — real separation-of-duty enforcement); and the closure carries the authority call — "I am not proposing a fix — closing this needs authority over who may assert an owner, which is a director-level boundary, not a patch." A verifier's job includes naming the layer the fix belongs to, even when that layer is above her pay grade.

---

## 🩷 HUMAN NOTE

A wax seal on a letter proves the letter wasn't opened in transit. It does not prove the person who signed the letter is who they say they are — anyone can sign a name and press a seal. The receipt system works exactly like that: the seal guarantees nothing changed *after* it was closed, but the owner's name inside was just asserted by whoever created the receipt, and nobody checked their ID at the door. The auditor's honest conclusion: "I can describe this gap, but closing it means deciding who is *allowed* to claim an identity — that's the director's call, not a code patch." Naming which layer a fix belongs to is as much the job as finding the bug.

---

## 🟣 CHILD NOTE

You write your name on your lunchbox and put a sticker over it so nobody can swap your sandwich. The sticker proves nobody touched your sandwich — but it does NOT prove you're really the kid whose name is on the box. Anyone could write any name. The sticker is about the sandwich; the name is just written there. If you want to prove the name is real, you need the teacher to check — and that's the teacher's job, not the sticker's.

---

## 🔵 GRANDMA NOTE

A padlock on a diary proves nobody read it after you locked it. It doesn't prove the diary is yours — you wrote your name on the cover yourself. The team found exactly this in their system: the digital seal keeps the record honest after it's made, but the identity inside was self-declared. Fixing that means deciding who gets to declare an identity, and that's the boss's decision, not a repair job.

---

## 🟠 NAYA NOTE

1. **Name the distinction every time you touch a seal.** Consistency (not altered after close) and authorship (the submitter really is the claimed owner) are two different claims proved by two different mechanisms. An unkeyed seal proves the first and says nothing about the second. Collapse them and every "verified" badge on the system over-claims.
2. **Allowlist coverage must follow the readers, not just the writers.** `owner_id` is allowlisted (C3) so a presented receipt cannot alter it without `VERIFY_RECEIPT_TAMPERED` — but `requesting_owner` is NOT separately allowlisted. Safe today only because LEARN reads `owner_id`. If a future change makes the runtime read `requesting_owner`, the allowlist silently under-covers it. The owed action: a comment at the field warning the next editor. Coverage audits must ask "who reads this field tomorrow?" not just "who writes it today?"
3. **Credit the genuine check, not just the gaps.** The audit found `_refusal_precheck` compares an owner against `requesting_owner` and refuses a cross-owner consent gap (§8) — real separation-of-duty enforcement, worth crediting. An audit that only reports defects teaches builders that honest machinery is invisible.
4. **Name the layer the fix belongs to.** The audit's closing line is a discipline: "I am not proposing a fix — closing this needs authority over who may assert an owner, which is a director-level boundary, not a patch." A patch at the wrong layer would *spend* security while appearing to buy it. Some closures need a director's word, and a verifier who says so is doing her job.
5. **The tests are the discipline that catches the auditor too.** Her first draft asserted the assignment lived in `submit()` — wrong; the grep had scanned the whole class, not the method. She fixed the test to assert `_new_receipt`, where it actually is. "I nearly published a wrong finding because I trusted a grep scope I hadn't checked." The verifier is inside the same evidence law as the builder.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn111-seal-proves-consistency-not-authorship",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Distinction",
  "distinction": "seal proves consistency (content integrity after close), NOT authorship (submitter really is the claimed owner)",
  "mechanism": {
    "integrity": "VERIFY seal; altering a presented receipt's owner_id trips VERIFY_RECEIPT_TAMPERED (C3 allowlisted)",
    "authorship_gap": "owner_id is caller-ASSERTED at receipt creation (VerifyNode._new_receipt assigns from request['requesting_owner']); no principal, auth, or caller identity is bound in _refusal_precheck/_new_receipt"
  },
  "edges": {
    "requesting_owner_not_allowlisted": "safe today only because LEARN reads owner_id; future readers of requesting_owner silently under-covered — comment-at-field guard owed",
    "genuine_check_credited": "_refusal_precheck refuses cross-owner consent gap (§8) — real separation-of-duty enforcement",
    "authority_call": "closing the gap needs authority over who may assert an owner — director-level boundary, not a patch (auditor explicitly declined to propose a fix at the wrong layer)",
    "auditor_self_correction": "first draft asserted assignment in submit(); corrected to _new_receipt after method-scoped check — evidence law binds verifiers too"
  },
  "limitation_class": "unkeyed seal — same as the correctly-rehashed-counterfeit note already on record",
  "evidence": ["#554 comment 5942032703", "commit bee101b47 (coda1/owner-provenance-audit-8c027928)", "6 passed"],
  "family": ["SN-085 resolve-then-trust does not establish origin (intake path, not receipt semantics)", "SN-092 self-invalidating qualification tests (honest limits, stated plainly)", "SN-065 honest PARTIAL > invented capability"],
  "open": ["who may assert an owner (director decision, not captured here)", "whether requesting_owner ever gets read by the runtime (the field comment is the tripwire)"]
}
```

---

## 🔗 HOW IT CONNECTS

- **COUSIN OF SN-085** (resolve-then-trust does not establish origin): SN-085 was about the LEARN intake path — resolving a receipt id doesn't establish its origin. This is the receipt-semantics form: even a *perfectly resolved* sealed receipt doesn't establish *authorship*. Same family, different layer.
- **COUSIN OF SN-092** (self-invalidating qualification tests): SN-092 was honest about consequence classes — "composition gap, not security defect." This is the same honesty at the seal: name exactly what the mechanism proves, and refuse to let it prove more.
- **COUSIN OF SN-065** (honest PARTIAL > invented capability): the auditor declined to invent a fix at the wrong layer. Honest partial (describe the gap, name the layer) beats a patch that over-claims.
- **COUSIN OF SN-058** (adversarial implementation-fidelity audit): field-level fidelity checking by an independent seat, with explicit findings — the same verification posture, applied to trust semantics.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One closed audit (6 passed) at a pinned SHA, with the gap named, the readers-checked, the genuine check credited, and the authority boundary declared. The requesting_owner field comment is proposed, not yet written — that is the one open leg.

## 🌍 APPLICABILITY

- **Applies to:** any sealed-receipt / signed-artifact system — always state what the seal proves (consistency) and what it cannot (authorship), audit allowlist coverage against *future readers*, and name the authority layer for closures you cannot patch.
- **Does NOT apply to:** systems with keyed/authenticated identity binding — there the seal *can* bind authorship, and this distinction becomes a different note ("what your identity binding actually covers").

## 🧬 SUCCESSOR EFFECT

Future Naya: when you see a seal, ask two questions — "what does it prove?" and "who checked the identity inside?" Never let a consistency proof wear an authorship costume. And when the fix needs a director's word, say so and stop — a patch at the wrong layer is a lie told in code.
