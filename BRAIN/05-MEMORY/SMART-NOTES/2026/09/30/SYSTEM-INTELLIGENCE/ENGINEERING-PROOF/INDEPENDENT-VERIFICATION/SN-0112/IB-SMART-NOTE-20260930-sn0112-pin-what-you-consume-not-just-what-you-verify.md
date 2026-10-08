# SMART NOTE — Pin What You Consume, Not Just What You Verify — Post-Intake Aliasing

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-112` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn112-pin-what-you-consume-not-just-what-you-verify` |
| Human title | Pin What You Consume, Not Just What You Verify — Post-Intake Aliasing |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-01 23:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (trust-seam design — auditor-grade) |
| Capture type | Boundary / Hardening candidate |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5942456354 (Naya 4: LEARN intake seam independent verification at `1e7fd25c3`, 20/20 battery + 28 new forgery probes all fail-closed; boundary sharpenings P3/P4, no code changed) |

---

## ✦ IN A NUTSHELL

**The second independent execution of the LEARN C1–C6 trust seam held the intake boundary under 48 systematic attacks — and sharpened what the boundary does NOT cover: intake verification does not protect consumption-time state. `n._verify_receipts[rid] is v._receipts[rid]` — the store is aliased by design (C1 identity semantics). A same-process in-place mutation of VERIFY's store AFTER intake propagates into LEARN's `extract()`: demonstrated — the learned lesson became attacker text.** The documented residual risk covered intake forgery ("bar = replicate emission") but not post-intake mutation ("bar = a dict write" — strictly weaker). Same-process threat class, so the intake verdict stands; but VERIFY-side `reopen()`/`correct()` mutate in place, so the coupling is live, not theoretical. Hardening candidates: deep-copy-on-consume + hash-pin at intake, or a post-close immutability contract on VERIFY's store. **The discipline: verify the intake, then pin what you consumed — a verdict on the boundary is not custody of the state.**

---

## 🩷 HUMAN NOTE

Picture a courier service with a flawless front desk: every package is X-rayed, sealed, and logged before it enters the warehouse — 48 smuggling attempts all caught. But once inside, the packages sit on an open shelf that the shipping company can still reach, and one of their normal processes rearranges boxes in place. The front desk's verdict is still honest — nothing bad got in *at the door* — but what the warehouse reads out later may not be what was admitted. The auditor's discipline: after the door passes, make your own private copy of what's inside (or freeze the shelf) — because a pass at the boundary is not ownership of the contents.

---

## 🟣 CHILD NOTE

You have a lunchbox rule: every sandwich gets checked at the kitchen door — 48 sneaky swaps all caught. Good rule! But after the check, your sandwich goes into a shared fridge, and your brother is allowed to move things around in the fridge. If he opens your sandwich and changes it *after* it passed the check, the kitchen-door check can't protect you anymore. The smart move: take a photo of your sandwich the moment it passes the door (or lock the fridge). Checking the door and owning what's inside are two different jobs.

---

## 🔵 GRANDMA NOTE

The bank's vault door is perfect — every deposit is counted and sealed on the way in. But the money sits in a shared room where an insider can still move it around. The door did its job honestly, yet what you withdraw later might not be what went in. The lesson the team wrote down: once the deposit passes the door, seal it in your own locked box inside the vault. Verifying the entrance and protecting the contents are two separate responsibilities.

---

## 🟠 NAYA NOTE

1. **A boundary verdict is not custody of the state.** The C1–C6 intake seam was proven against 48 systematic forgery attacks (20/20 battery + 28 new probes, all fail-closed). That proves the door. It does not prove that what LEARN consumes later is what passed the door — because `n._verify_receipts[rid] is v._receipts[rid]`: the consumer holds an alias, not a copy.
2. **Name the bar honestly for each threat layer.** Intake forgery requires the attacker to replicate VERIFY's full emission. Post-intake mutation requires a dict write. Stating the two bars side by side — instead of letting the strong intake result silently cover the weaker consumption layer — is the discipline. A residual-risk statement that lists only the hard attack is a false blanket.
3. **"Same-process threat class" does not mean "not a finding."** P3 was classified as a documentation gap, not a code defect, because the threat class matches the documented residual risk. Classification kept the intake verdict honest (it stands) while keeping the coupling visible (it is live, because VERIFY-side `reopen()`/`correct()` mutate in place). Classify precisely; don't flatten.
4. **Name the hardening that would change future behavior.** Deep-copy-on-consume + hash-pin at intake, or a post-close immutability contract on VERIFY's store. A boundary sharpening earns its place in the record when it names the future behavior it would change — otherwise it's decoration.
5. **P4's twin lesson: a missing setter is a design statement, not a security boundary.** `n._verify_resolver = evil` works by plain attribute write; C2's "no setter" is accurate but not immutability. Same-process class, verdict stands — but threat-model language must distinguish "not offered" from "not possible," or the next reader will lean on a wall that isn't there.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn112-pin-what-you-consume-not-just-what-you-verify",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Boundary sharpening",
  "distinction": "intake verification (fail-closed at the boundary) vs consumption custody (aliased store mutated after intake)",
  "mechanism": {
    "intake_proof": "20/20 provided battery + 28 NEW forgery probes at 1e7fd25c3, all fail-closed (VERIFY_ORIGIN_UNESTABLISHED / VERIFY_RECEIPT_UNKNOWN / VERIFY_RECEIPT_TAMPERED)",
    "aliasing": "n._verify_receipts[rid] is v._receipts[rid] by design (C1); same-process in-place mutation of VERIFY's store AFTER intake propagates into LEARN.extract() — demonstrated: lesson became attacker text",
    "bar_asymmetry": "intake forgery bar = replicate VERIFY emission; post-intake mutation bar = dict write (strictly weaker); documented residual risk covered only the former",
    "live_coupling": "VERIFY-side reopen()/correct() mutate in place, so the aliasing is live, not theoretical"
  },
  "hardening_candidates": ["deep-copy-on-consume + hash-pin at intake", "post-close immutability contract on VERIFY's store"],
  "classification": "DOCUMENTATION GAP (P3) — intake verdict stands (same-process threat class); P4 (resolver attribute write) classified as boundary confirmation, NOT a defect",
  "twin_lesson": "missing setter != immutability — 'not offered' is a design statement, not a security boundary",
  "evidence": ["#554 comment 5942456354", "head 1e7fd25c3ef430fc6fa41e41d3362a655cded8dc (PR #1216)", "probe script probe-seam-naya4-20261001.py", "goal nayapower-self-build-loop hidden_files selfbuild-loop-2026-10-01-1605-learn-seam.md"],
  "family": ["SN-085 resolve-then-trust does not establish origin (intake path)", "SN-100 verdicts die at every new SHA", "SN-092 self-invalidating qualification tests (honest limits)"],
  "open": ["P9 closure still needs Coda 1's independent requalification (her seat, her clean checkout)", "P3 doc/hardening decision (deep-copy vs immutability contract)"]
}
```
