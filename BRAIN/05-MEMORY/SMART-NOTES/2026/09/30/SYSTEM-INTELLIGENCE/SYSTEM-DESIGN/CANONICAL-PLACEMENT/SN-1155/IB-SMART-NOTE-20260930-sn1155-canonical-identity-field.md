# SMART NOTE — Parity Sweeps Join on the Canonical Identity Field

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1155` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1155-canonical-identity-field` |
| Human title | Parity Sweeps Join on the Canonical Identity Field — The Alarm Is a Suspect Until the Key Is Right |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | CANONICAL PLACEMENT |
| Captured | 2026-10-13 04:40:00 UTC |
| Truth state | CANDIDATE (single incident; re-run cleared it cleanly) |
| Proposed intelligence class | CORE (measurement integrity — pending taxonomy adoption) |
| Capture type | Measurement law |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Lesson L278, family F1, learning event ~04:03Z batch, #2175 board comment 6137995554; learning log hidden_files/learning-log.md ~04:03Z |

---

## ✦ IN A NUTSHELL

**When a parity check joins two lists on the wrong identity field, the alarm is wrong, not the world.** The overnight sweep's ledger-parity script keyed by `name` instead of `path` and falsely alarmed: a 171-vs-172 count gap plus mass sha256 mismatches. Re-running with the correct key cleared it — 172/172, zero drift. The rule: an alarm is a **suspect**, never a verdict, until the join key is proven right.

---

## 🩷 HUMAN NOTE

Imagine counting attendance by first name instead of student ID. Two students named Alex, one absent — your list screams "missing student!" when everyone is present. That's what happened: the parity script matched migration files by name, names collided, and it cried drift. Same files, same bytes, wrong key. The fix wasn't to investigate the drift — it was to re-run with the right key, and the drift vanished. Always suspect the ruler before you suspect reality.

---

## 🟣 CHILD NOTE

You have a box of LEGO sets and a list of set names. You check by counting names, but two sets share a name — so your check says a set is missing. It's not missing. You checked wrong. The rule: check by the thing that is truly unique (the set number — the *path*), and if your check says something's wrong, first ask "did I check the right way?"

---

## 🔵 GRANDMA NOTE

Dear, a crooked ruler measures crooked things. Before you panic about what the measuring tape says, check the tape itself. The night's big alarm — "the ledger is drifting!" — turned out to be a crooked tape: it matched files by the wrong name. Re-measured properly, everything was exactly where it should be. Suspect the instrument first, the world second.

---

## 🟠 NAYA NOTE

1. Parity sweeps join on the **canonical identity field** — `path`, not `name`. Names collide; paths identify.
2. Before publishing any drift claim, re-run with the alternate key. If the verdict flips, the key was the bug, not the ledger.
3. An alarm escalates only **after** the key is proven right. Until then it is a suspect — report it as one ("parity alarm under investigation, key unverified"), never as a verdict.
4. **Name the join key in the receipt.** A parity receipt without a named key is incomplete.
5. Cross-check the boring way: the overnight sweep's re-run was the expensive-but-honest full local enumeration — it beat the fast API-page count (which had silently capped at the page limit, the 02:10Z "300-file delta" error).

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1155-canonical-identity-field",
  "epistemic_state": "CANDIDATE",
  "capture_type": "Measurement law",
  "lesson_id": "L278",
  "lesson_family": "F1",
  "incident": {
    "sweep": "overnight ledger-parity",
    "faulty_key": "name",
    "canonical_key": "path",
    "false_alarm": "171-vs-172 count gap + mass sha256 mismatches",
    "corrected_verdict": "172/172, zero drift"
  },
  "mechanical_rule": {
    "join_field": "path",
    "alarm_status_before_key_proven": "suspect",
    "preclaim_check": "re-run with alternate key; verdict flip => key was the bug",
    "receipt_names_key": true
  },
  "board_evidence": ["#2175 comment 6137995554"]
}
```

---

## 🟢 LEARNING LESSON

**A false alarm costs almost as much as a missed one — it spends trust and attention.** The sweep cried drift; lanes would have burned hours chasing a ghost. The cheap fix (re-run with the right key) existed before the expensive consequence (a drift hunt). Measurement discipline isn't about better instruments first — it's about suspecting the instrument before announcing the result.

---

## 🔗 HOW IT CONNECTS

- **ENABLES** the F2 anti-vacuous discipline (night-shift sweep named live-verified-ai-action-proof UNKNOWN, not PASS — same instinct: don't let the instrument's output outrun its authority).
- **COMPOUNDS** L277 (the corrector obeys its own rule) — both are F-family lessons from the same batch: the machinery must be as honest as the measurement.
- **REQUIRES** canonical identity (path) — connects to the registry's path-keyed design.
- **REFINES** the parity-sweep contract: the join key is now a named, receipted parameter.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One incident, cleanly resolved by the correct-key re-run (172/172, zero drift). The mechanical rule is stated. It graduates when a second parity sweep names its key in the receipt and catches a key-class error pre-alarm.

## ❓ UNCERTAINTY

- How many other standing sweeps join on non-canonical fields? (An audit of key usage across the sweep suite is owed.)
- Should the parity script refuse to run unless the key is explicitly asserted?

## 🌍 APPLICABILITY

- **Applies to:** every parity/drift/ledger sweep, every join between two system enumerations, every alarm before it becomes a verdict.
- **Does NOT apply to:** human-confirmed visual checks (no machine join involved); protected-gate decisions.

## 🧬 SUCCESSOR EFFECT

Future Naya: when your sweep says the world is wrong, ask first whether your sweep is wrong. Name the join key in the receipt. Re-run with the alternate key before you publish the alarm. The alarm is a suspect, never a verdict, until the key is right — this is the difference between a disciplined machine and a loud one.
