# Read the Canonical Contract Before Proposing a Competing Format — Withdraw the Competing Format, Answer Under the Contract

**Intelligent Block:** IB-SMART-NOTE-20260930-sn068-canonical-contract-before-competing-format
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5934656876 (Naya 2 sign-in, Second Master Execution Directive, 2026-10-01T15:28:51Z); Naya 4's seam question 5934391765; Naya 4 → Naya 2 AGREE note 5934741237; Naya 2's seam answer 5934779683 (PR #1243).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 proposed `naya-receipt-contract/1` as a new receipt/lineage payload contract (5934427074) — then, on sign-in for the second directive (5934656876), withdrew it: she had **not yet read the canonical `NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md`**. Her correction was explicit: the proposal was premature, she was withdrawing it *as a competing format*, the canonical 12-field contract stands, and her job was to specify the seam **under** it, not beside it. She named Naya 4's seam question (5934391765 — kernel projects receipts onto the 12 fields; kernel supplies content+hashes+lineage, never decides owner scope) as the right frame and committed to a sourced answer. Naya 4's AGREE note (5934741237) reinforced the discipline: "this is implementation agreement **under the existing contract — not new governance**." Naya 2's sourced answer (5934779683, PR #1243) then operated strictly inside the 12-field contract. The lesson: proposing a new contract before reading the canonical one manufactures a governance problem — a competing format — out of what was an engineering question. The first move is always to read the canonical artifact; if it exists and stands, withdraw the competing proposal and do the seam work under it. This is the process-side twin of SN-018 (one canonical spec per node): SN-018 fixes the artifact structure, this fixes the proposal discipline that protects it.

## 🩷 HUMAN NOTE

It's like drafting a new house rulebook for the family without checking the drawer where the actual house rules already live — and then proudly announcing your new rules. Naya 2 caught herself: the canonical contract already existed, so her new proposal wasn't a solution, it was a *second rulebook* — a governance problem she had just created. The honest fix: publicly withdraw it, say "I hadn't read the canonical contract," and do the real work inside the existing rules instead. She did, and the seam work (PR #1243) moved fast once it sat under the contract instead of beside it. New formats multiply; canonical contracts anchor. Always check the drawer first.

## 🟣 CHILD NOTE

Imagine you invent a whole new game with new rules because you didn't know the family already had rules written on the fridge. When someone shows you the fridge, you don't argue that your new game is better — you say, "Oops, I didn't see the rules," put your game away, and play by the fridge rules. That's what Naya 2 did: she had proposed a brand-new receipt contract, then read the real one and withdrew hers. The rule for everyone: **look at the fridge before inventing a game.** If the real rules already exist, work inside them — don't make a competing set.

## 🔵 GRANDMA NOTE

It's like one granddaughter writing up a brand-new recipe for the family casserole before checking grandmother's recipe box — and announcing her version as the new standard. When she opens the box and finds the canonical recipe already there, the gracious move is not to defend her rewrite; it's to say "I hadn't looked in the box," set her version aside, and spend her energy getting the actual casserole right. Naya 2 did exactly that: she withdrew her competing contract proposal, honored the canonical twelve-field contract, and did the seam work *under* it. Two recipe boxes for one casserole only create arguments. Check the box first.

## 🟠 NAYA NOTE

Apply this before any lane proposes a contract, schema, format, or convention: (1) search for the canonical artifact first — if a canonical contract/spec governs the boundary, read it before drafting anything; (2) if the canonical artifact stands, **withdraw the competing proposal explicitly on the board** — name what you had not read, say the canonical artifact stands, and re-scope your work as a seam *under* it (not beside it); (3) frame lane agreement as "implementation agreement under the existing contract — not new governance" (5934741237); (4) never let two formats coexist pending review — a competing format is itself a governance defect, resolve it by withdrawal before building; (5) credit the lane whose question held the right frame (here: Naya 4's seam question 5934391765). Format proliferation is a defect class; canonical-first proposal discipline is the control. Note the relation: SN-018 makes one canonical spec per node the artifact rule; this note makes *check the drawer before drafting* the proposal rule that keeps SN-018 from being undermined.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "premature_competing_format_proposal",
  "evidence": {
    "proposal": "#554 comment 5934427074 (Naya 2: naya-receipt-contract/1)",
    "withdrawal": "#554 comment 5934656876 (2026-10-01T15:28:51Z) — 'premature — I had not yet read the canonical NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md'; withdrawn as a competing format; canonical 12-field contract stands",
    "right_frame": "#554 comment 5934391765 (Naya 4 seam question: kernel projects receipts onto the 12 fields; kernel never decides owner scope)",
    "agreement_discipline": "#554 comment 5934741237 — 'implementation agreement under the existing contract — not new governance'",
    "sourced_answer": "#554 comment 5934779683 + PR #1243 (naya2/persistence-integration-package) — seam specified under the canonical contract"
  },
  "rule": [
    "read the canonical artifact before proposing any contract/format/convention",
    "withdraw competing formats explicitly on the board; never let two formats coexist pending review",
    "scope lane agreement as implementation under the existing contract, not new governance",
    "competing-format proposal without reading the canonical artifact is a governance defect, not an engineering contribution"
  ],
  "relation": "SN-018 (one canonical spec per node) fixes the artifact structure; this note fixes the proposal discipline that protects it.",
  "lesson_line": "Check the drawer before drafting — a new format proposed without reading the canonical contract is a competing format, not a solution."
}
~~~
