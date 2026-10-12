# VERIFIED ≠ QUALIFIED: Never Conflate Receipt-Recorded with Content-Qualified

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1045-verified-not-qualified-receipt-vs-content
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6105342847 (Naya 4 · LEARN-DRIVER CHECKPOINT 2 disposition, 2026-10-11T04:15:34Z) — read from the director's board-window snapshot on the 21:38 PDT distillation tick.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The CHECKPOINT 2 disposition did two things a cold successor should study. First, it measured the real population: the qualification trial rows live in Supabase `nayanet_execution_outcomes` + 3 mirror tables, batch `QUAL-20261010-CIQ-001` — **130 rows** (40 control + 50 correct-lesson + 40 wrong-lesson), NOT the "163 rows" the mission issue still says. The source document was wrong; the disposition named the one-line correction instead of letting the stale number keep circulating. Second, and durably: it flagged a **labeling hazard hiding in plain sight** — the ledger's `status='VERIFIED'` means *receipt recorded*; the outcome row's `verified=false` means *not yet qualified* (PENDING_INDEPENDENT_RUNTIME_VERIFICATION, scored only by sealed_answer_key_v1 on answer-key match). Two fields, same word, opposite evidentiary weight. Conflate them and "we logged it" silently becomes "it passed."

The durable rule: **a field named "verified" records only what the writer verified.** A receipt ledger's VERIFIED means the receipt was recorded — never read it as the outcome being qualified. When a cold successor triages a qualification state, the distinction receipt-recorded vs content-qualified is load-bearing: one is bookkeeping, the other is evidence. And when the measured population disagrees with the canonical document (163 claimed, 130 measured), correct the document — stale counts compound into stale authority.

## 🩷 HUMAN NOTE

Shawn — a labeling lesson from the CHECKPOINT 2 disposition tonight. Two corrections. First, the qualification trial population is 130 rows, not the 163 the mission issue says — the disposition measured the real rows and asked for the one-line fix on the mission issue. Second, a trap hiding in our own data: the ledger says VERIFIED where that means "receipt recorded," while the outcome row says verified=false where that means "not yet qualified." Same word, completely different weight. If anyone ever reads the ledger's VERIFIED as proof the trials passed, we get a false green on something unqualified. The disposition named the hazard explicitly so it can't happen silently. Nothing for you to decide — just a cleaner truth on the record.

## 🟣 CHILD NOTE

Imagine two teachers both write "done" on your homework — but one means "I saw you turned it in" and the other means "I checked every answer and it's all right." If you read them both the same way, "I saw it" turns into "I checked it." That's what happened tonight: one database field said VERIFIED and meant "we recorded it," while another field said NOT VERIFIED and meant "nobody has checked the answers yet." The team caught it before anyone mixed them up. Also, the official paper said there were 163 test questions, but counting showed 130 — so they fixed the paper. The lesson: always check what "done" actually means before trusting it.

## 👵 GRANDMA NOTE

It's like the difference between a package arriving and a package being inspected. The mailroom stamps every box "RECEIVED" when it lands — that's just proof the truck came. The inspector stamps "PASSED" only after opening it and checking the contents. If you treat the mailroom stamp like the inspector's stamp, you ship boxes nobody opened. The team found exactly this confusion waiting to happen in their own records — one system stamps VERIFIED when it files the paperwork, another leaves verified=false until the work is actually proven. They labeled both stamps clearly tonight so nobody confuses arrival with approval. And they corrected the count on the official form — 130 items, not 163 — because a wrong count on the form becomes a wrong decision later.

## 💜 NAYA NOTE

Note to future me: FIELD-SEMANTICS HYGIENE. (1) Never trust a flag named "verified" at face value — ask WHO verified, WHAT they verified, and AGAINST WHAT. The ledger's VERIFIED = receipt recorded (bookkeeping). The outcome's verified=false = not qualified (evidence). Same word, opposite weight. (2) When I triage any qualification state, I read both flags and their definitions, not one label. (3) Conflating receipt-recorded with content-qualified is how "we logged it" becomes "it passed" — a false green that compounds. (4) When the measured population (130 rows, 40/50/40) disagrees with the canonical document (163), correct the document — the count becomes authority downstream, and stale authority corrupts every decision built on it. Evidence: #2175 comment 6105342847 (CHECKPOINT 2 disposition, sealed_answer_key_v1, mirror lineage receipts → ledger → index 1:1).

## ⚙️ MACHINE NOTE

{"sn": "SN-1045", "title": "VERIFIED ≠ QUALIFIED: Never Conflate Receipt-Recorded with Content-Qualified", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "QUALIFICATION-SEMANTICS"], "extends": [], "related": ["SN-1041/SN-1043/SN-1044 (same transfer-test/CHECKPOINT family — this is the qualification-labeling sibling)"], "evidence": {"disposition": "#2175 comment 6105342847 (2026-10-11T04:15:34Z): Naya 4 LEARN-DRIVER CHECKPOINT 2 disposition — answers Naya 2's ask 6103434993", "population": "trial rows in Supabase nayanet_execution_outcomes + 3 mirror tables, batch QUAL-20261010-CIQ-001: 130 rows (40 control + 50 correct-lesson + 40 wrong-lesson), NOT the mission issue's '163 rows'; all verified=false / PENDING_INDEPENDENT_RUNTIME_VERIFICATION; scored by sealed_answer_key_v1 on answer-key match only; mirror lineage receipts -> ledger -> index 1:1", "hazard": "labeling hazard: ledger status='VERIFIED' (= receipt recorded) vs outcome verified=false (= not qualified) — never conflate", "correction": "mission-issue body still says '163 rows' — disposition requested the one-line correction"}, "rule": "a field named 'verified' records only what the writer verified: receipt-recorded (bookkeeping) is never content-qualified (evidence); read both flags and their definitions when triaging a qualification state, never one label; when the measured population disagrees with the canonical document, correct the document — stale counts compound into stale authority"}
