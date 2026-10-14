# SMART NOTE — Blind Is a Property of the Artifact Chain (2026-10-14)

> **"Blind" is a property of the artifact chain, not of intentions. Pin and fetch in one logged step; blindness is provable by mtime ordering and checkable by a cold successor. Before reading any file that may carry the key, grep for key-shaped fields first — extract-then-read, never read-then-regret.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1270` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1270-blind-is-an-artifact-chain-property` |
| Human title | Blind Is a Property of the Artifact Chain |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | VERIFICATION DOCTRINE |
| Captured | 2026-10-14 07:50 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

Sentinel's first blind level-drill run (t0720-lane8, PR #2568) passed 8/8 — but the real product was the protocol, not the score. The pre-mortem's novel blindness hazard was met with structure: "blind" treated as a property of the extract→commit→key chain, the attestation naming exactly what eyes touched, pin-and-fetch in one logged step, blindness provable by mtime ordering (answers-blind at 07:01:44 UTC, key contact in the verdict log at 07:02:04 UTC) and checkable by a cold successor. The same night proved the cost of the alternative: Lane 10 (t0723-lane10) read tools/level_drill.py linearly, hit the inline key mid-read, and voided instantly — zero ratings, zero laundering, fail-closed worked, but the data point was paid for. The structural embedding named from that lesson: blind-task protocol = grep the authorized file for key-shaped fields FIRST ("rung"/"key"/"label"); subjects get a text-only scenario extraction, never the source file.

---

## 🩷 HUMAN NOTE

Two seats ran the same blind drill in the same night. One treated "blind" as a property of the artifacts: extract the scenarios, commit the answers to disk, and only then touch the key — with timestamps proving the order. Anyone, months later, can check the mtimes and confirm: the answers existed before the key was seen. Blindness you can check beats blindness you have to believe.

The other seat read the tool file straight through, like reading a manual — and the answer key was sitting inline in the file. The seat saw it, voided immediately, wrote nothing. Fail-closed worked exactly as designed. But the data point was lost, and the instrument turned out to have a real defect: the authorized read path routes subjects straight through the key.

The durable principle: intentions are not observable. A cold successor cannot check what you meant — only what the artifacts prove. So make blindness an artifact: one logged step, timestamped, in an order that a stranger can verify. And before your eyes touch any file that might carry the key, grep it for key-shaped fields first. Extract-then-read, never read-then-regret.

---

## 🟣 CHILD NOTE

Imagine a taste test where you're not supposed to know which cookie is which. One taster puts on a blindfold, tastes, and writes down the answer — then takes the blindfold off to check. You can verify she was blindfolded because she wrote her answer BEFORE looking. The other taster read the recipe book first and accidentally saw "cookie #3 is chocolate." She told everyone immediately and threw her answers away — honest! — but now there's no taste-test result.

The lesson: don't promise you didn't peek. Set things up so nobody has to take your word for it — write the answer down before the secret is anywhere near you.

---

## 🔵 GRANDMA NOTE

Two people took a test where they weren't supposed to see the answers. The first one wrote her answers down, and only then looked at the answer sheet — the timestamps on the files prove the order, so nobody has to trust her word. The second one opened the test file and the answers were written right inside it; she saw them by accident and honestly threw her work away.

The lesson that lasts: set up the test so the honesty is checkable, not promised. Answers committed before the key is touched, with the order stamped by the files themselves. And when a file might contain the secret, check for it with a search before you read a single line.

---

## 🟠 NAYA NOTE

When I run or design a blind task:

1. **Extract before reading.** If the authorized file may carry the forbidden thing, grep it for key-shaped fields FIRST (`"rung"`/`"key"`/`"label"`). Subjects get a text-only scenario extraction — never the source file.
2. **Pin and fetch in one logged step.** Pin the head and fetch the instrument in one command; log both SHAs. A tiny pin/fetch window is a measured risk, not an assumed one.
3. **Commit answers before key contact.** Answers file on disk with its mtime; key contact in a separate, later artifact. Blindness = answers' mtime precedes key contact — provable, cold-successor-checkable.
4. **Run the instrument's own suite before the blind run** (7/7 green), and **probe unknown API shapes on live bytes before writing the harness** (the brief is a hypothesis; the bytes adjudicate).
5. **Attest exactly what eyes touched.** Name the breach verbatim if one happens (one extra `key()` contact owned in t0720), void instantly on key sight, and convert the paid-for lesson into structure: the t0723-lane10 +5 Foresight — a `run_blind` wrapper that refuses to load the key until an answers file exists — is the template update that prevents the next paid-for lesson.

The t0720 chain: `scenarios-blind-t0720.md` → `answers-blind-t0720.md` (mtime 07:01:44 UTC) → `drill-verdict-t0720.log` (key contact 07:02:04 UTC). Verdict PASS 1.0, worst miss 0, quoted verbatim. Worktree retained as the evidence anchor.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1270-blind-is-an-artifact-chain-property",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "blindness_as_checkable_artifact_chain_property",
  "rule": "blind is a property of the artifact chain, not of intentions: pin and fetch in one logged step; blindness provable by mtime ordering and checkable by a cold successor; grep for key-shaped fields before reading any file that may carry the key; extract-then-read, never read-then-regret",
  "decision_it_changes": "a future seat running a blind task builds the extract→commit-answers→key-contact chain with timestamped artifacts and greps key-shaped fields before any read, instead of relying on read discipline and promising blindness",
  "falsifier": "a blind run attested by intentions alone that an independent second seat confirms was genuinely uncompromised — the chain ceremony would then be belt-and-suspenders, not load-bearing",
  "mechanism": "blindness = 'no eyes touched the key' is not observable from intentions, but IS checkable from artifacts: an answers file whose mtime precedes the key-contact artifact proves the answers predated exposure. Linear reading defeats this because the authorized read path may route eyes through an inline key — hence grep-first and text-only extraction as structural prevention",
  "evidence": {
    "blind_run": "hidden_files/twelve-lane-receipts/t0720-lane8.md — first blind level-drill run PASS 8/8, score 1.0, worst miss 0",
    "chain": "scenarios-blind-t0720.md → answers-blind-t0720.md (mtime 07:01:44 UTC) → drill-verdict-t0720.log (key contact 07:02:04 UTC); worktree hidden_files/lane-8/drill-worktree-t0720 at 21f089d56f15",
    "counter_case": "hidden_files/twelve-lane-receipts/t0723-lane10.md — linear read hit the inline key mid-read; voided instantly, zero ratings, zero laundering; +5 Foresight: grep key-shaped fields FIRST; text-only scenario extraction",
    "board": "#2537 sign-in 6162805248, result 6162832054",
    "events": "hidden_files/learning-events-2026-10-14-00.md (candidate 248)"
  }
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** one blind run where the mtime-ordered chain made blindness checkable (PASS 8/8), and one counter-case where linear reading defeated intentions and the seat voided correctly.

**Not automatically implied:** that mtime ordering alone constitutes a complete blind protocol — single-seat attestation still needs a second seat's re-derivation (owed to Naya Verity), and a `run_blind` wrapper mechanizing the refusal is the honest upgrade path. CANDIDATE until two independent blind data points exist.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
