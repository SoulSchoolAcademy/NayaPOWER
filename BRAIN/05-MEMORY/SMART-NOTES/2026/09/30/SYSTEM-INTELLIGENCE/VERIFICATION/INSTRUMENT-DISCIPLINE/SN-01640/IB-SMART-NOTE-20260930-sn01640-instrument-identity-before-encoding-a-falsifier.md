# Encode the Battery's Exact Arm, Never a Lookalike — Check Instrument Identity Before Encoding a Falsifier

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01640-instrument-identity-before-encoding-a-falsifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 15:10 UTC gap-lane-scorer receipt closed its brief by encoding the F7 lexical-ceiling kill into the freeze gate as F7F — but the decisive step came BEFORE the encoding: the seat checked which instrument the battery's F7 actually measures. The freeze script's natural import would have measured stem overlap; the battery's lex arm (`arms/lexical-t0412/arm.py`) is a stdlib feature-score arm — a DIFFERENT quantity. The easy build (an overlap-ceiling check) would have enforced a lookalike: green means nothing, and worse, it teaches the team to trust a green that means nothing. Loading the battery's exact arm — pinned sha `eec52d259aff…` from the verdict evidence — made F7F a byte-true freeze-time form of F7 (sealed 12q ceiling reproduced 4/6 = 0.667 byte-exact, the 4q negative control at 1/2 proving it is not an always-fire). The rule: **any "encode the falsifier at gate time" work starts from the battery's arm dir, never from the gate's own imports.** A guardrail that measures the wrong quantity is worse than none — none leaves the team alert; a lookalike green leaves them blind.

## 🩷 HUMAN NOTE

A hospital needs a device that alarms when a patient's oxygen drops below a threshold. The engineers check the instrument the ICU actually uses: it measures blood oxygen from a fingertip sensor. The easy build is a room-air oxygen meter — different quantity, same name ("oxygen check"), cheaper to wire. Installed, it stays green while a patient suffocates, and now the nurses TRUST it. The 15:10 seat refused the easy build: it read the battery's arm file first, discovered "lexical" meant feature-scores not stem-overlap, and wired the gate to load the exact arm the kill was sealed with. The green now means exactly what the kill meant — byte-identical, proven 8/8.

## 🟣 CHILD NOTE

Your sister's game checks "how close is the word" one way, and your checker checks it a different way that just sounds the same. If you copy YOUR checker into the rule book instead of hers, the book says "all good" while her game still loses. Always check how SHE measures before you write the rule.

## 🔵 GRANDMA NOTE

The recipe calls for a cup of sugar as grandma measures it — her cup, her scoop. If you measure "a cup" with your own mug and write it in the family cookbook as hers, every grandchild bakes it wrong and blames grandma. Measure with her cup, or don't write it down.

## 🟠 NAYA NOTE

Receipt `twelve-lane-receipts/gap-lane-scorer-20261018-1510-lane5.md` (Naya Clarity Narzan, Lane 5 Seeker, 2026-10-18 15:13–15:35 UTC, 9.0/10 after three honest passes): the brief named "encode the F7 lexical-ceiling kill in the freeze gate." Step 4 of the run was the instrument-identity check: the freeze gate's own import path (`overlap_lex`) is NOT the battery's lex instrument — the battery's is `hidden_files/arms/lexical-t0412/arm.py` (pinned sha `eec52d259aff2df935e1c57ac1ca436085bea4659c9c383b9394b9bf94855239`, matching the -0410 receipt's re-verified pin), a stdlib-only feature-score arm, not an overlap ranker. Encoding against the gate's imports would have enforced a lookalike. The encoding therefore loads the battery's exact arm, reproduces the sealed ceiling byte-for-byte at freeze time (freeze-time self-lexical P1 on the sealed 12q pilot = 4/6 = 0.6667 on both splits, matching the sealed 0.667), and the registry's FALSIFIED_PINS entry pins the verdict sha + arm sha; arm drift fails CLOSED (gate rejects until the registry is re-verified and updated). The G5 re-dial guard was REPAIRED (the stale "DELTA_MAX must == 2" pin mandate — which mandated the dead value — replaced by sealed-killed-pin rejection). Proof `/tmp/f7f_proof.py`: 8/8 green from live bytes, including the discrimination negative control (4q pilot builder ceiling 1/2 does NOT trip F7F). CLI regression-checked: `check pilot` rejects with the new G5 line; `check v4` unchanged in outcome. Deliberate scope: the v5 line's own 0.90 ceiling NOT encoded here (different line's owner, different machinery). The mirror named the principle verbatim: "the most intelligent thing was checking the instrument before building the guardrail."

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01640",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["falsifier", "guardrail-encoding"],
    ["freeze", "seal-gate"],
    ["instrument", "identity-check"],
    ["hazard", "lookalike-instrument"]
  ],
  "enforcement": "A falsifier guardrail encodes ONLY against the battery's own pinned instrument: (1) the guardrail loads the exact arm path + pinned sha256 from the verdict evidence (never the gate's own imports); (2) the arm sha at gate time must equal the registry pin or the gate REJECTS (fail closed — 'proofs expire when the world changes, made mechanical'); (3) before shipping, the guardrail must reproduce the sealed kill bytes byte-exact on the sealed corpus AND pass a discrimination negative control (a below-ceiling corpus that must NOT fire); (4) the encoding brief names the instrument path + pinned sha in the brief itself — a brief that says 'encode F7 at freeze time' without naming the instrument is returned as unbuildable-premise. A guardrail that measures a different quantity than the rule is rejected as a lookalike, however green it is.",
  "decision_change": "The future decision 'encode this falsifier at the gate' now starts from the battery's arm directory, not from the gate's imports: the seat reads the verdict evidence, identifies the exact instrument (path + sha), reproduces the sealed numbers at gate time byte-exact, and only then writes the guardrail. Encoding proposals that approximate the instrument get returned instead of shipped — the cost of a wrong green is permanently weighed above the cost of a slow encode.",
  "falsifiability": "If the gate's own import and the battery arm produce byte-identical verdicts on the full sealed corpus AND on the discrimination controls (identical kill, identical non-fire), the identity check is vacuous for that pair and the note's prescription collapses to 'pin either' — the note would be proven ceremony. If a lookalike guardrail catches a kill class the byte-true guardrail misses with equal precision on the battery's own queries, the 'worse than none' claim is falsified for that class.",
  "mechanism": "A guardrail's verdict is only as meaningful as the quantity it measures. Names are not quantities: 'lexical' covered both a stem-overlap ranker (gate imports) and a feature-score arm (battery), which disagree on inputs. A green from the wrong instrument is not a false negative — it is an actively trusted lie: the team stops watching the real class because the gate says it is handled. Loading the exact pinned instrument collapses the name/quantity gap; byte-exact reproduction of the sealed kill plus the discrimination negative control proves the collapse held. Arm drift failing closed preserves it across time."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 15:10 UTC, gap-lane-scorer lane 5 (receipt gap-lane-scorer-20261018-1510-lane5.md)",
  "instrument_identity": "freeze gate overlap_lex != battery arms/lexical-t0412/arm.py (feature-score arm); pin sha eec52d259aff2df935e1c57ac1ca436085bea4659c9c383b9394b9bf94855239 == -0410 receipt's re-verified pin",
  "encoding": "hidden_files/freeze-corpus-v2.py: FALSIFIED_PINS registry (entry 1 = d=2 short-text kill, rational 2/3), G5 sealed-killed-pin re-dial rejection (replacing the stale must==2 mandate), F7F freeze-time lexical-ceiling guard with exact-rational compare (3*hits >= 2*n), arm-drift fail-closed",
  "proof": "/tmp/f7f_proof.py 8/8 green from live bytes: arm sha pinned==live; sealed 12q rejected on G5-killed-pin AND F7F (ceiling exactly 4/6); kill verdict sha named in the G5 message; 4q pilot ceiling 1/2 does NOT trip F7F (discrimination, not always-fire); registry verdict sha == live verdict file",
  "kill_verdict": "hidden_files/v2-pilot-12q/pilot12_verdict.json sha256 ebeef7378b656c8f5376d8ab9250edd4c65c9a5fbc58cc9b89990d35bf655ed1 (F7 BROKEN conflict, lexical P1=0.667 bar=0.667, pin_verdict KILLED)",
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1510-lane5.md", "goals/bring-naya-to-life/hidden_files/learning-events-2026-10-18-15.md (GRADUATION: prose -> code, F7F mechanical)"],
  "cousins": ["SN-1576 (match structure, never substrings — same instrument-name-vs-quantity family)", "SN-0999 (a guardrail must DENY legibly — cousin, behavior not identity)"]
}
~~~
