# Dispatch Premises Are Hypotheses — Carry the Dependency Check in the Brief

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1097-dispatch-premises-are-hypotheses
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 6127954114-window (2026-10-12 — lesson-broadcast t0452 Naya Librarian; `hidden_files/auto-retrieval/ask-world-needs-t0452.md`); board window `hidden_files/board-window-2026-10-12T1638Z.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Surge slice (c) was dispatched as "analyze the ask-world query log." The slice burned a full tick discovering the ask-world query log never existed — `bin/ask-world.py` is a pure read, zero logging calls; the SMARTBLOCKS spec describes the log as future work. The dispatch premise was a hypothesis dressed as a fact. The durable rule: **a slice that says "analyze X" must carry its dependency check ("prove X exists") in the brief**, or the lane burns a tick proving the premise instead of doing the work. Analysis-before-instrumentation is a chain-order violation: chains go **instrument → collect → analyze**, and the SURGE spec should name the instrumentation dependency for slice (c) at line 198, not leave it implied.

Why this is brain-grade: dispatch premises are the cheapest thing to verify and the most expensive thing to assume. One line in a brief ("dependency: the query log exists — verify before analyzing") would have converted a wasted tick into either a five-second confirmation or a redirected slice. The failure mode is systemic: any dispatcher that assigns "do Y with Z" without first establishing Z's existence manufactures phantom work at scale. Briefs are hypotheses until their premises are pinned.

## 🩷 HUMAN NOTE

Shawn — small dispatch-design lesson from the retrieval surge: one lane was sent to "analyze the ask-world query log," and spent the whole tick discovering that log doesn't exist — the tool is read-only, the log was spec'd as future work. The fix is a one-line habit: every dispatch brief that says "analyze X" must also say "first prove X exists." Chains go instrument → collect → analyze, never analyze-first. Cheap to write, saves whole ticks.

## 🟣 CHILD NOTE

Imagine your teacher tells you: "Write a report about the fish tank in the classroom." You spend all afternoon looking for a fish tank — and there isn't one. Nobody checked first! The smart rule: whenever someone gives you a job that starts with "use the thing," the very first step is to check the thing is really there. "Analyze the log" means "first prove the log exists, THEN analyze." Check first, then work — that's the rule.

## 👵 GRANDMA NOTE

A worker was told to study a record book that turned out not to exist — she spent her whole shift hunting for it. The lesson is simple and old-fashioned: before you send someone off to work with something, make sure the something is actually there. "Go analyze X" should always come with "first confirm X exists." Verify the ingredients before you start cooking.

## 💜 NAYA NOTE

Note to future me: when writing or receiving a dispatch brief, treat every premise as a hypothesis. If the brief says "analyze/collect/mine X," it must carry the dependency check — "prove X exists" — as step zero, in the brief itself, not left to the lane's initiative. Chains go instrument → collect → analyze; any brief that orders analysis before the instrumentation exists is a chain-order violation — fix the brief, don't dispatch it. When the dependency check fails, the slice redirects, it doesn't evaporate: the lane's tick becomes "prove premise absent + propose the instrumentation" rather than a burned tick.

## ⚙️ MACHINE NOTE

{"sn": "SN-1097", "title": "Dispatch Premises Are Hypotheses — Carry the Dependency Check in the Brief", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LANE-COORDINATION", "DISPATCH-DESIGN"], "cousins": ["SN-0977"], "authority": "observed lane practice 2026-10-12, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#2175 lesson-broadcast t0452 Naya Librarian (2026-10-12) — 'the ask-world query log never existed (bin/ask-world.py is a pure read, zero logging calls; the SMARTBLOCKS spec describes the log as future work); a slice that says \"analyze X\" must carry its dependency check (\"prove X exists\") in the brief, or the lane burns a tick proving the premise'"], "artifacts": ["hidden_files/auto-retrieval/ask-world-needs-t0452.md"]}, "doctrine": {"dispatch_premise_rule": "every 'analyze X' brief carries 'prove X exists' as step zero", "chain_order": "instrument → collect → analyze; analysis-before-instrumentation is a chain-order violation", "failed_dependency": "redirect the slice (prove absent + propose instrumentation), never burn the tick silently"}}
