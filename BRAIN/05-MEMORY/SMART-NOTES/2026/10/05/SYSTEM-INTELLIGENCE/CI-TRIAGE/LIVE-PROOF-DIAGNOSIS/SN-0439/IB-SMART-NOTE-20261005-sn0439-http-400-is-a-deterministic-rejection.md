# A 400 from the Prove Runtime Is a Deterministic Rejection — Archive the Log, Read the Body, Never Re-Dispatch Blind

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0439-http-400-is-a-deterministic-rejection
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip `613133b6`, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The sweep found a NEW failure since the previous sweep: `live-prove-proof` — run 37384065800 (2026-10-05T22:41:33Z, main `cc2465f6`, manual dispatch) — failed at `independent-prove-verification` / "Independently recompute positive PROVE assessment" with curl exit 22: **HTTP 400 from `nayanet-prove-runtime` on the inspect POST**. The sweep's response is the whole lesson: log archived in sweep scratch, no re-dispatch, no fix attempted.

Why this is brain-grade: HTTP 400 is a deterministic rejection — the runtime refused the request's shape, and it will refuse the identical request every time. Re-dispatching the same inspect POST does not gather evidence; it replays the rejection. Worse, `live-prove-proof` dispatches are human-only, so a blind re-dispatch burns a human action for zero information. The classification order is fixed: (1) archive the log, (2) read the response body — note that `curl -f` discards it, so re-capture with the body intact or read the archived run log — (3) understand what shape was rejected, (4) only then decide: fix the request, escalate the runtime, or leave it. The discipline is the re-dispatch twin of SN-0329 (reproduce in the target environment before patching): classify the failure class — deterministic rejection vs flaky infrastructure — before spending the most expensive token in the system (a human dispatch). A cold Naya inheriting this failure must learn: a 400 is the runtime talking to you. Listen before you resend.

## 🩷 HUMAN NOTE

Shawn — one clean discipline from the overnight sweep: the new `live-prove-proof` failure is an HTTP 400 from the prove runtime on the inspect POST — a deterministic rejection of the request's shape, not a flake. The sweep archived the log and deliberately did NOT re-dispatch, because re-dispatching would just replay the same rejection and burn a human-only dispatch. Banked rule: on a 400, archive the log and read the response body first — never re-dispatch blind. The first move is understanding what shape got rejected, not sending it again.

## 🟣 CHILD NOTE

Imagine you try to mail a letter but the post office hands it back with a big stamp that says "WRONG ADDRESS FORMAT." Mailing the exact same letter again doesn't help — it comes back again. The smart move is to read the stamp, figure out what part of the address is wrong, and fix it before mailing again. An HTTP 400 is that stamp: the runtime is telling you what's wrong with your request. Read the message first. Sending it again without reading is just doing the same wrong thing twice.

## 👵 GRANDMA NOTE

If you knock on someone's door and they say "you're at the wrong house," you don't knock again hoping for a different answer — you check the address. A 400 error is the runtime saying "wrong address." The sweep did the wise thing: it wrote down what happened (archived the log) and didn't knock again. Grandma's rule: when someone tells you plainly why they said no, listen the first time. Knocking twice without listening wastes everyone's evening — and in our house, some knocks can only be made by Shawn.

## 💜 NAYA NOTE

Note to future me: when a live-prove run fails with HTTP 400 on the inspect POST (curl exit 22 from nayanet-prove-runtime), classify before you spend. A 400 is a deterministic rejection of the request shape — re-dispatching the identical request replays the rejection and burns a human-only dispatch for zero information. The order is fixed: (1) archive the log in sweep scratch, (2) read the response body — curl -f discards it, so capture the body explicitly or read the archived run log, (3) name what shape was rejected, (4) then decide: fix the request, escalate the runtime, or park it. No re-dispatch, no fix attempted until step 3 is done. This is the re-dispatch twin of SN-0329: that one says don't patch before reproducing in the target environment; this one says don't re-dispatch a deterministic failure before reading what it rejected.

## ⚙️ MACHINE NOTE

{"sn": "SN-0439", "title": "A 400 from the Prove Runtime Is a Deterministic Rejection — Archive the Log, Read the Body, Never Re-Dispatch Blind", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "LIVE-PROOF-DIAGNOSIS"], "cousins": ["SN-0329", "SN-0386", "SN-0240"], "authority": "observed episode — Naya 2 overnight sweep gate report, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6010347808 ([Naya 2][overnight-sweep] 22:52 PDT gate report — tip 613133b6, 2026-10-06T05:59:57Z / 2026-10-05 22:52 PDT)", "failure": "live-prove-proof RED — NEW since last sweep: run 37384065800 (2026-10-05T22:41:33Z, main cc2465f6, manual dispatch), step 'Independently recompute positive PROVE assessment': curl exit 22, HTTP 400 from nayanet-prove-runtime on the inspect POST", "response": "log archived in sweep scratch; no re-dispatch, no fix attempted", "context": "live-prove-proof dispatches are human-only — a blind re-dispatch burns a human action"}, "doctrine": {"classify_before_spending": "classify failure class — deterministic rejection vs flaky infrastructure — before spending the most expensive token in the system (a human dispatch)", "400_is_deterministic": "HTTP 400 means the runtime rejected the request shape; the identical request will be rejected every time — re-dispatching replays the rejection, it does not gather evidence", "read_the_body_first": "fixed order: (1) archive the log, (2) read the response body (curl -f discards it — re-capture with body intact or read the archived run log), (3) name what shape was rejected, (4) then decide: fix the request, escalate the runtime, or park", "family": "re-dispatch twin of SN-0329 (reproduce in the target environment before patching the demo) — that one governs repairs, this one governs re-dispatches"}}
