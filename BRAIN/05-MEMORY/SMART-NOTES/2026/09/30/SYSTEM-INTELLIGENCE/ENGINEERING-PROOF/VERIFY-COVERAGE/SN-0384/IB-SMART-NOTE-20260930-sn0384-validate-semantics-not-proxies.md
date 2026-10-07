# Gate the Retry Break on Validity, Not a Proxy

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0384-validate-semantics-not-proxies
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6001421665 ([NAYA 4][SCORECARD RECEIPT] PR #1501 merged, 2026-10-05T19:19:47Z / 12:19 PDT): "Gate the retry break on JSON validity, not file size." Evidence: run 37361232498 log line 353 — `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`: HTTP 200 with a non-JSON body passed the `-s` size check, the retry loop broke early on the false success, and the JSON decode crashed downstream.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The cold-runtime retry loop declared success by checking the response file's size (`-s`): bytes present = we got it. Run 37361232498 returned HTTP 200 with a non-JSON body — the size check passed, the loop broke out of retry on a false success, and the consumer crashed at `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. PR #1501 repaired the exact seam: the retry-break gate now parses the body and requires valid JSON before accepting it. The change-detector test was updated to encode the JSON gate, and invalid bodies still fail closed after 5 attempts.

The durable lesson is wider than one loop: **the check that declares success must assert the semantic requirement the consumer actually needs — never a proxy metric.** Size ≠ validity, HTTP 200 ≠ parseable. A proxy check fails exactly in the case that matters: when the upstream lies politely. This is the success-side twin of the failure-classification doctrine — SN-0320 teaches classify the red before chasing code; this one teaches the break-condition IS the verification. If the consumer needs X, the success check asserts X. Anything cheaper is a false-success factory.

Why this is brain-grade: a cold Naya writing a retry, wait, or acceptance gate months from now will reach for the cheap signal — file size, non-empty output, exit code 0, HTTP 200 — because the cheap signal is convenient and usually correlates. This note names the exact shape of the trap and the one-line rule: parse it before you break. It scored itself into a merge receipt (9 vs 2 vs 4 on the real options), so the evidence trail is complete.

## 🩷 HUMAN NOTE

Shawn — small sharp one from the cold-runtime lane: the retry loop was declaring "success" because the response file was non-empty. Then a 200 came back with garbage in it, passed the size check, and crashed the JSON decode. PR #1501 changed the gate to actually parse the body before accepting it. Banked rule: the thing that declares success has to test the thing the code actually needs — not a stand-in metric like file size.

## 🟣 CHILD NOTE

Imagine you decide your sandwich is ready by weighing your lunchbox — a heavy lunchbox can still hold a terrible sandwich. The real test is taking a bite. The retry loop was weighing the lunchbox; now it takes a bite (parses the JSON) before saying "done."

## 👵 GRANDMA NOTE

If you're waiting for an important letter and decide it must have arrived because the mailbox feels heavy — it could be full of junk mail. Open the envelope and read it before you tell everyone the letter came. The code now reads the letter before it stops waiting.

## 💜 NAYA NOTE

Note to future me: whenever I write a retry break, wait-loop exit, or acceptance gate, the condition must assert the semantic requirement of the downstream consumer — here: `json.loads(body)` succeeds — not a proxy like file size (`-s`), non-empty output, or HTTP 200 alone. Proxies lie exactly in the cases that matter (200 + non-JSON body), and the lie converts to a downstream crash with full retry budget unspent. Gate on validity; fail closed on invalid input (here: 5 attempts, then fail).

## ⚙️ MACHINE NOTE

{"sn": "SN-0384", "title": "Gate the Retry Break on Validity, Not a Proxy", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"], "cousins": ["SN-0320"], "authority": "observed repair — Naya 4 scorecard receipt, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6001421665 (2026-10-05T19:19:47Z / 2026-10-05 12:19 PDT): SCORECARD RECEIPT — PR #1501 merged (validate JSON body before accepting cold-runtime response)", "crash": "run 37361232498 log line 353: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0) — HTTP 200 with non-JSON body passed the -s size check", "scorecard": "option 1 (gate on JSON validity) scored 9 — fixes the exact crash, reversible, no prod impact; option 2 (leave -s check) scored 2 — crash recurs on every empty-200; option 3 (defensive Python) scored 4 — wrong layer, retry contract should guarantee valid input", "repair": "PR #1501: gate retry break on JSON validity; change-detector test updated to encode the JSON gate; invalid bodies fail closed after 5 attempts; YAML parses; 675/0 locally; PR CI test + chain-readiness-gate green"}, "doctrine": {"rule": "the check that declares success must assert the semantic requirement the consumer needs, never a proxy metric", "proxies": "file size (-s), non-empty output, HTTP 200 alone are proxies, not validity", "break_condition_is_verification": "in a retry loop, the break condition IS the verification — it defines what the loop can tolerate", "fail_closed": "invalid bodies still fail closed after N attempts; validity-gating never silently accepts garbage"}}
