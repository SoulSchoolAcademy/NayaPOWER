# A Current Timestamp on a Truncated Picture Is No Longer Sufficient — Previews Fail Closed

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1103-truncated-preview-fails-closed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Audit briefing #3 (2026-10-12 ~09:50 PDT — world-model truncation finding); tools/world_model.py build_mission_section (pre-fix pattern verified in repo bytes: body[:2000] cached, status reported "OK").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The morning audit caught `tools/world_model.py` `build_mission_section` caching `body[:2000]` — a 2,000-character preview of the mission issue body — while reporting `"status": "OK"`. A consumer could mistake the preview for the complete mission, and the current `as_of` timestamp made the incomplete picture look authoritative. That is the failure mode: **a current timestamp on an incomplete picture is the most convincing possible form of incompleteness.**

The audit directed a fail-closed repair: when truncated, the section reports status **PARTIAL** (never OK), with a `body_truncated` flag and `body_full_length` so every consumer can see exactly how much of the picture it holds.

The durable rule: **any pipeline that caches a preview, summary, or sample must mark its status for the truncation, never for the timestamp.** OK means "this is the whole thing"; PARTIAL means "this is a window of known size into the thing." The status field answers "how complete is this?" — the timestamp only answers "when was this taken," and a fresh timestamp on a 2,000-character window proves nothing about the other N characters. Cold-successor corollary (pairs with the t0412 Conductor finding that a 30-minute-refresh snapshot can be 2 days stale: "snapshots lie, re-verify the tip"): never derive authority, freshness, or completeness from a preview's metadata; when the decision matters, read the source. The status flag is the contract — and the contract must be incapable of saying OK about a picture it has not seen all of.

## 🩷 HUMAN NOTE

Shawn — fail-closed lesson from this morning's audit: the world-model builder was caching only the first 2,000 characters of the mission brief but stamping it "OK" with a fresh timestamp — so anyone reading it would think they had the whole current picture. The fix direction: whenever the content is truncated, the status must say PARTIAL (with how much was cut and the full length), never OK. The rule: a status field tells you how complete the data is; a timestamp only tells you when it was taken. A fresh timestamp on a partial picture is the most convincing way to be wrong. When a decision actually matters, read the source — never trust a preview's metadata.

## 🟣 CHILD NOTE

Imagine your friend reads you the first page of a long letter and says "that's the whole letter, and I just got it!" You'd believe them — it sounds complete and fresh. But there were ten more pages they never read! The smart rule: if you only read part of something, you must say "I only read part of it" — never "here's the whole thing." Fresh and complete are two different things. A brand-new first page is still just a first page.

## 👵 GRANDMA NOTE

A summary tool was reading only the first bit of an important document, then stamping it "complete" with today's date. Anyone checking would think they had the full, current story. The lesson: the stamp must say "this is only part of it" whenever part of it is missing — a fresh date on a partial summary is the most misleading kind. And when something really matters, don't rely on the summary at all: go read the original. "Complete" and "current" are two different promises, and only one of them was kept.

## 💜 NAYA NOTE

Note to future me: whenever I build or touch any pipeline that caches a preview, summary, or sample, the status field is a completeness contract, and truncation sets it to PARTIAL — never OK, never "OK because the timestamp is fresh." The payload carries the truncation explicitly (truncated flag + full length + window size) so the consumer never has to guess. I treat "as_of is current" as zero evidence of completeness — that is the audit's exact finding. When a decision crosses an authority or safety boundary, I re-read the source; previews are orientation, not evidence. If I ever catch myself (or a lane) stamping OK on a window, I file it as a fail-closed defect on the spot: the status must be incapable of claiming completeness it does not have.

## ⚙️ MACHINE NOTE

{"sn": "SN-1103", "title": "A Current Timestamp on a Truncated Picture Is No Longer Sufficient — Previews Fail Closed", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-0950", "SN-0979"], "authority": "audit finding 2026-10-12, CANDIDATE (auto-capture, not ratified); fail-closed repair directed, merge state unverified by this capture", "evidence": {"board": ["Audit briefing #3 (2026-10-12 ~09:50 PDT) — 'tools/world_model.py build_mission_section cached body[:2000] but reported status OK — a consumer could mistake the preview for the complete mission. Fixed to fail closed: status PARTIAL when truncated, with body_truncated flag and body_full_length. A current timestamp on an incomplete picture is no longer sufficient.'"], "code": ["tools/world_model.py build_mission_section — pre-fix pattern verified in repo bytes (body[:2000] cached, status 'OK'); fail-closed repair (PARTIAL + body_truncated + body_full_length) directed by audit"]}, "doctrine": {"status_is_completeness_contract": "status field answers 'how complete is this?' — truncation sets PARTIAL, never OK", "timestamp_proves_nothing_about_completeness": "a current as_of timestamp on a truncated picture is the most convincing form of incompleteness", "explicit_truncation": "payload carries truncated flag + full length + window size; the consumer never guesses", "source_when_it_matters": "across authority/safety boundaries, re-read the source; previews are orientation, not evidence"}}
