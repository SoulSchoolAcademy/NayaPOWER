# Fail-Silent Telemetry — The Instrument Must Not Corrupt the Instrumented

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1102-fail-silent-telemetry-instrument-cannot-corrupt
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 (2026-10-12 — lesson-broadcast t0462 Naya Librarian; bin/ask-world.py instrumentation; 22 seeded query rows; live-check OK).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Librarian's t0462 slice added append-only JSONL query logging to bin/ask-world.py — a pure read with zero logging calls, where no query log had ever existed (the t0452 absence finding). The lesson is the **order of operations**, not the logging itself:

1. **Instrument** — add the logging calls.
2. **Output-diff** — diff old-vs-new stdout, byte-identical, across all four query paths — prove the instrument did not alter the instrumented **before** any data is seeded.
3. **Seed** — 22 real query rows written to the log.
4. **Live-check** — prove the log is actually live and recording.

Plus two structural guarantees: log only **after** output (the answer is emitted before any logging call runs), and wrap the logging call in a **swallow-all try/except** — let the log die alone; a logging failure must never surface into the answer. Cheap insurance: a `format_version` field in every logged row for future schema changes.

The durable rule: **telemetry for a read-only tool must be fail-silent — if logging can ever alter the answer, the instrument has corrupted the instrumented.** This extends the SN-0979 family (gate telemetry made verdict-neutral by structure: never-raises, kill switch, negative controls on unpatched bytes) into the read-only domain, where the proof is **byte-identity of outputs**, not verdict stability. The byte-identical diff is the load-bearing proof: without it, every downstream analysis of the logged data is suspect, because you cannot tell whether a pattern came from the world or from your own instrumentation.

## 🩷 HUMAN NOTE

Shawn — instrumentation hygiene lesson: when the lane added query logging to a read-only tool, she proved the outputs were byte-identical before and after BEFORE writing a single log row — across all four query paths. Then the logging was wired so it runs only after the answer is out, wrapped so a logging failure dies silently instead of breaking the answer. The rule: telemetry on a read-only tool must be fail-silent — if the logging can ever change the answer, the instrument has corrupted the very thing it's measuring. Byte-identical output is the proof; everything after that (seed data, liveness checks) is built on it.

## 🟣 CHILD NOTE

Imagine you want to count how many birds visit a bird feeder, so you set up a camera. But the camera's flash scares the birds away — now you're counting zero birds, and you think no birds come! The smart rule: first prove your camera doesn't change what the birds do (watch with and without the camera — same birds), THEN start counting. And if the camera ever breaks, it should break quietly — never scare the birds. Your measuring tool must never change the thing you're measuring.

## 👵 GRANDMA NOTE

A team added record-keeping to a lookup tool — but first they proved, character for character, that the answers were identical before and after the change, on every kind of query. Only then did they start keeping records. And the record-keeping was built to fail quietly: if the log ever breaks, the answer still goes out fine. The lesson: your notebook must never rewrite the story. Prove the tool is untouched before you trust anything the notebook says — otherwise you're studying your own shadow.

## 💜 NAYA NOTE

Note to future me: whenever I instrument a read-only tool, the contract order is instrument → output-diff → seed → live-check, and I never skip or reorder it. The output-diff must be byte-identical across every query path before one row is seeded — that diff is the proof the instrument is a passenger. Logging runs strictly after output, inside a swallow-all try/except: the log dies alone, always. Every logged row carries a format_version from day one. And I state the sibling law explicitly in the receipt: SN-0979 made verdict-neutrality structural for gate telemetry; this note makes output-identity structural for read-only tool telemetry. If I cannot prove byte-identity, I do not ship the instrumentation — an unverified observer is a contaminant with a changelog.

## ⚙️ MACHINE NOTE

{"sn": "SN-1102", "title": "Fail-Silent Telemetry — The Instrument Must Not Corrupt the Instrumented", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INSTRUMENT-HARDENING"], "cousins": ["SN-0979", "SN-0886"], "authority": "observed lane practice 2026-10-12, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#2175 lesson-broadcast t0462 Naya Librarian (2026-10-12) — 'Telemetry for a read-only tool must be fail-SILENT — if logging can ever alter the answer, the instrument has corrupted the instrumented. Log after output, wrap the logging call in swallow-all try/except, let the log die alone. Prove it on live bytes: old-vs-new outputs diffed byte-identical BEFORE seeding any data. Contract order: instrument → output-diff → seed → live-check. A format_version field is the cheap insurance for future schema changes. (instrumented bin/ask-world.py; 22 real queries logged, live-check OK)'"], "artifacts": ["bin/ask-world.py (instrumented, append-only JSONL logging)", "hidden_files/auto-retrieval/ask-world-needs-t0452.md (t0452 absence finding: the log never existed)"]}, "doctrine": {"contract_order": "instrument → output-diff → seed → live-check; never skip or reorder", "byte_identity_proof": "old-vs-new stdout diffed byte-identical across every query path BEFORE one row is seeded", "fail_silent": "log only after output, inside swallow-all try/except; the log dies alone", "format_version": "every logged row carries format_version from day one", "sibling_law": "SN-0979 made verdict-neutrality structural for gate telemetry; this note makes output-identity structural for read-only tool telemetry"}}
