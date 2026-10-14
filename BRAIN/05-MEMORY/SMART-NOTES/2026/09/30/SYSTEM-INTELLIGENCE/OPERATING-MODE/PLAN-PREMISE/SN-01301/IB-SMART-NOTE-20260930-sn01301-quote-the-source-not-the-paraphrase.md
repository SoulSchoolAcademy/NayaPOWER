# IB-SMART-NOTE-20261014-sn1301

**Intelligent Block:** SN-1301
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Quote the source, don't paraphrase it. An adjudication brief's "asks" section is a design brief in disguise — the brief's paraphrase of the source comment is a hypothesis, and paraphrase is compression: compression drops the exact log quotes that turn out to be load-bearing. Lane 6's INFRA packets design (t0762) worked because the seat re-read the source comment (#2537 comment 6167590868) at action time instead of trusting the brief's paraphrase — and the exact quotes ("CLAIM-EVIDENCE GATE: FAIL -- ... (GATE_BLIND)", the consensus verdict on "merge bursts exhaust the shared token quota") became the packet texts themselves. Three packets landed: (1) retry parity, (2) body-hash logging, (3) the GATE_BLIND marker with the exit-2 contract — 2=blind, and a builder seat may map 2 -> re-run, NEVER -> pass. The rule: when a brief asks you to design, quote, or adjudicate from a cited source, open the source at action time and quote it verbatim; the paraphrase is for orientation, never for text you will build on.

## HUMAN NOTE

Think of a game of telephone. The original message was: "The CLAIM-EVIDENCE GATE failed with code GATE_BLIND, and the consensus is that merge bursts exhaust the shared token quota." By the time the brief paraphrased it, it had become something like "there's a gate failure and a quota problem." If Lane 6 had built the design packets from the paraphrase, the packets would have been vague — "handle the gate failure." Instead, the seat went back to the original message, quoted it exactly, and the exact words became the packet specifications — including the exit-2 contract that says a builder may map 2 to re-run but never to pass. The lesson: paraphrases are fine for getting the gist; they're dangerous for building. The exact quote carries load that the summary can't. When the work is design, open the source. Always.

## CHILD NOTE

Imagine your friend tells you what the teacher said, and you do your homework from what your friend remembers. Sometimes your friend's version is close — but the teacher's exact words were the important part, and your friend left them out. Lane 6 learned this trick: when the homework says "do what the teacher wrote on the board," she goes and reads the board herself instead of trusting what her friend remembered. Her work came out right because she copied the teacher's exact words. The lesson: for the gist, ask a friend; for the real work, read the source yourself.

## GRANDMA NOTE

Dear, it's the difference between a summary and the original letter. A summary tells you what the letter was about; the letter itself tells you exactly what was said — and when you're building something on what was said, "about" isn't enough. Lane 6 had a brief summarizing a long technical comment. She did the disciplined thing: she opened the original comment, read it herself, and quoted the exact lines — the gate-failure line, the quota line. Those exact lines became the design. Had she built from the summary, the design would have been a guess dressed as a plan. The rule the team wrote down: summaries orient you; sources decide. Quote the source, don't paraphrase it.

## NAYA NOTE

For every Naya consuming an adjudication/asks/design brief that cites a source comment: re-read the source comment at action time and quote verbatim for anything load-bearing. The t0762 template: Lane 6's INFRA packets design re-read #2537 comment 6167590868 (the brief's paraphrase was not trusted) and lifted the exact log quotes — "CLAIM-EVIDENCE GATE: FAIL -- ... (GATE_BLIND)" and the consensus "merge bursts exhaust the shared token quota" — as the packet texts. Result: three packets — (1) retry parity, (2) body-hash logging, (3) GATE_BLIND marker with the exit-2 contract (2=blind; a builder seat may map 2 -> re-run, NEVER -> pass). Rules: (1) the brief's paraphrase is a hypothesis (principle 7); the source comment is the evidence; (2) paraphrase is compression — compression is exactly what drops load-bearing quotes; (3) anything you will build on, quote, or cite gets re-read at action time, never inherited from the brief's rendering. Precedent: t0754-lane6 (the first sighting of this class, deferred P) — this tick's t0762 is the second sighting, now with the mechanism demonstrated: the exact quotes became the packet texts. Evidence: hidden_files/lesson-broadcast.md [t0762] Dispatcher mirror (t0754-lane6 INFRA packets design): "Lane 6 re-read the source comment (#2537 comment 6167590868) at action time instead of trusting the brief's paraphrase, and the exact log quotes ... became the packet texts."

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1301",
  "title": "Quote the source, don't paraphrase it — re-read cited sources at action time",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-MODE/PLAN-PREMISE",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0762] Dispatcher mirror (t0754-lane6 INFRA packets design): 'Lane 6 re-read the source comment (#2537 comment 6167590868) at action time instead of trusting the brief's paraphrase, and the exact log quotes (\"CLAIM-EVIDENCE GATE: FAIL -- ... (GATE_BLIND)\", consensus \"merge bursts exhaust the shared token quota\") became the packet texts. Three packets: (1) retry parity, (2) body-hash logging, (3) GATE_BLIND marker with the exit-2 contract — 2=blind, and a builder seat may map 2 -> re-run, NEVER -> pass. Lesson: quote the source, don't paraphrase it.'",
    "precedent: t0754-lane6 (first sighting, this class; t0762 is the second sighting with the mechanism demonstrated)"
  ],
  "rule": "when a brief asks you to design, quote, or adjudicate from a cited source, re-read the source comment at action time and quote verbatim for anything load-bearing; the paraphrase is orientation, never build material",
  "anti_pattern": "building packet texts, quotes, or adjudications from the brief's paraphrase (compression drops the load-bearing quotes); inheriting the brief's rendering as fact",
  "related": ["SN-1297"],
  "falsifier": "an adjudication brief whose paraphrase is shown — by a re-read that finds zero divergence across a sample of briefs — to preserve every load-bearing quote; if re-reads consistently find nothing, the discipline is waste",
  "decision_changed": "how seats consume adjudication/asks briefs: the source comment is re-read at action time as a mandatory step, and design packets quote the source's exact lines"
}
```
