# Demote Falsified at the Retrieve Seam — Downstream Veracity Cannot Recover a Poisoned Ranking

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1082-demote-falsified-at-the-retrieve-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0292-lane8.md (Lane 8 t0292 FALSIFIED governance verdict, 2026-10-12 ~12:33–12:42Z); decisions/20261012T052831Z-next-t1302-veracity-hole-mechanism-choice.json (seam demotion 7.2 vs downstream-veracity 4.2, margin 3.0); t1302 RED-first battery 14/14 on faithful tip bytes; Lane 5 t1282 hole (FALSIFIED SN-D4 outranked genuine SN-D5, 82.30 vs 73.93, silently); spec hidden_files/specs/veracity-seam-demotion-candidate.md; #2175 comment 6124373922.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 8 delivered the governance verdict on Lane 5's t1282 hole: a **FALSIFIED** record (SN-D4) silently outranked a genuine one (SN-D5), 82.30 vs 73.93 — served to downstream consumers unflagged. The calculator ruled: **demote FALSIFIED at the retrieve seam, not downstream** — seam demotion 7.2 vs downstream-veracity 4.2, margin 3.0 (`decisions/20261012T052831Z-next-t1302-veracity-hole-mechanism-choice.json`), with a RED-first battery at 14/14 on faithful tip bytes (t1302).

The reasoning, plainly: once a falsified record enters the scored pool, it corrupts every downstream conclusion under the Evidence-Bounded Uncertainty law (D32) — uncertainty cannot shrink downstream, so downstream veracity machinery **cannot recover a poisoned ranking it never sees**. The repair must live at the single choke point every candidate passes through: `retrieve()`. The mechanism: a **VERACITY_GUARD inside `retrieve()`** (the one public path; `_ranked_candidates` stays byte-stable), FALSIFIED demoted with best-genuine substitution + a flag, refusal when no genuine clears the floor. Wiring stays Shawn's gate (SN-1015 family); zero production bytes changed.

For a cold Naya: veracity is a **seam property**, not a downstream repair. If your falsification fix lives in consumers, you must audit every consumer — and every future one — for the same poisoning. Put the guard where the data enters the math. One choke point, one fix, every downstream conclusion protected.

## 🩷 HUMAN NOTE

Shawn — Lane 8 closed a real governance hole today: a falsified record was silently outranking genuine ones at the retrieval seam (82.30 vs 73.93). The verdict is mechanical, not philosophical: the guard goes inside the single retrieval path — every falsified record gets demoted and replaced by the best genuine one before anything downstream scores it. The alternative (fixing it in every downstream consumer) scored 4.2 vs 7.2 and lost: you can never recover a ranking you never see. Wiring it into production is your gate, as always; nothing production changed.

## 🟣 CHILD NOTE

Imagine a contest where the judges score the dancers — but one dancer is wearing an invisible costume that makes her look taller. If nobody catches the costume at the door, every judge's score is wrong, and no judge can fix it later because they never saw the costume. The lesson: catch the cheating **at the door**, not at the judges' table. One guard at the entrance protects every judge.

## 👵 GRANDMA NOTE

It's like a recipe contest where one entry has a secret artificial flavor enhancer. If the judges don't know about it, their scores are wrong — and you can't fix their scores afterwards, because they were scoring something fake. The fix isn't re-training every judge; it's one inspection at the door: the bad entry gets swapped for a real one before any judging starts. One checkpoint, everything downstream stays honest.

## 💜 NAYA NOTE

Note to future me: the FALSIFIED verdict is the pattern — when a corruption class poisons rankings, the fix goes in the **single public path** (`retrieve()`), never in the consumers. The calculator is how the verdict was made (7.2 vs 4.2, margin 3.0), the RED-first battery (14/14 on faithful tip bytes) is how it was trusted, and the spec file is where the mechanism lives. And the wiring rule holds: spec written, production untouched, human gate respected. When I find a "downstream can't see it" class, I demote at the seam.

## ⚙️ MACHINE NOTE

{"sn": "SN-1082", "title": "Demote Falsified at the Retrieve Seam — Downstream Veracity Cannot Recover a Poisoned Ranking", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-1081", "SN-1073", "SN-1015"], "authority": "observed finding + verdict — Lane 8 t0292 governance verdict on live bytes, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"hole": "Lane 5 t1282: FALSIFIED SN-D4 outranked genuine SN-D5 82.30 vs 73.93 silently at the retrieval seam", "verdict": "seam demotion 7.2 vs downstream-veracity 4.2, margin 3.0 — decisions/20261012T052831Z-next-t1302-veracity-hole-mechanism-choice.json", "battery": "t1302 RED-first 14/14 on faithful tip bytes", "mechanism": "VERACITY_GUARD inside retrieve() — single public path, _ranked_candidates byte-stable; FALSIFIED demoted with best-genuine substitution + flag; refusal when no genuine clears the floor", "spec": "hidden_files/specs/veracity-seam-demotion-candidate.md", "board": "#2175 comment 6124373922", "gates": "wiring is Shawn's gate (SN-1015 family); zero production bytes changed"}, "doctrine": {"seam_property": "veracity is a seam property, not a downstream repair — a falsified record entering the scored pool corrupts every downstream conclusion under D32 (Evidence-Bounded Uncertainty)", "poisoned_ranking": "downstream veracity cannot recover a poisoned ranking it never sees", "one_choke_point": "fix at the single public path every candidate passes through — one guard, every consumer protected; a fix living in consumers must be re-audited per consumer, per future consumer"}}
