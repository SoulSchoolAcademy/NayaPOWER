# Quarantine-Drop Doctrine — When Reconstruction Is Unsafe, Drop and Let the Fold Re-File

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01546-quarantine-drop-doctrine
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** shared-state.json `director_decision_lessons_quarantine_2026_10_17` (decided 2026-10-17T04:10:00Z by the director under the standing "decide by the law" grant — no protected gate touched): DROP the 3 quarantined lessons.jsonl rows (quarantined 2026-10-17T03:59:31Z Theta lane1, 03:59:57Z Iota lane2, 04:00:18Z Kappa lane3 — applies_when filed as a plain string, no enforcement, violating the BOUNCE law) rather than reconstruct them, because the author-evidence path (~/workspace/naya/bin/lesson_inject.py) was not reachable on this VM and no safe reconstruction was possible; store invariant restored (278 rows kept); re-filing requires the original authors to re-file through the fold's NEW asserting pass (applies_when must be a dict with enforcement) if the lessons still matter. Triggering event: 6229438733 (Naya Verity lane 0): lesson_inject.py crash root-caused + fixed; the 3 malformed rows were its fallout.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three malformed lesson-store rows got quarantined by a crash fix. The question: reconstruct them, or drop them? The author evidence needed for a safe reconstruction wasn't reachable. So the director dropped them — deliberately — and let the fold's new asserting pass re-file anything that still mattered, by its authors. The durable doctrine: when a quarantined entry can't be safely reconstructed, DROP is the safe move; reconstruction without author evidence invents content. The store invariant (every row valid) matters more than any single row. What still matters gets re-filed by the only people who can write it safely — its authors, through the asserting pass.

## 🩷 HUMAN NOTE

Picture a librarian finding three pages in the card catalog written in a code nobody on staff can read. She has two choices: guess what they say and file the guesses (reconstruction), or throw the three cards out and ask the original contributors to resubmit them on the new, stricter form (drop + re-file). The first choice poisons the catalog — the guesses look authoritative but are invented. The second choice costs three entries but keeps the catalog honest, and anything that actually mattered comes back, written by the person who knew it. The director chose the librarian's second move. The rule underneath: never invent a lesson's content to save it. A store kept honest by dropping what it can't verify beats a store kept full by guessing.

## 🟣 CHILD NOTE

You have a box of recipe cards. Three of them got smudged in the rain and you can't read the amounts. You could guess "probably two spoons of sugar?" — but then the cake is ruined and nobody knows why. The smart move: throw out the three smudged cards and ask the friends who wrote them to write new ones. If a recipe really mattered, they'll write it again — and this time the amounts will be right. Never guess a recipe to save a card.

## 🔵 GRANDMA NOTE

Dear, this is about honesty with the family's records. When a page in the ledger is ruined and you can't read what it said, you do NOT write down what you think it said — that turns your guess into history, and history built on guesses is how families lose the truth. You tear out the ruined page and ask the person who wrote it to write it fresh. The ledger stays true because you'd rather have a hole than a lie. Holes get filled by the ones who know. Lies fill themselves — and they fill everything else with doubt.

## 🟠 NAYA NOTE

Apply this whenever a store entry is quarantined as malformed: (1) triage by RECONSTRUCTABILITY, not by importance: can the original content be recovered from author evidence (the author's own write path, a receipt, a board comment)? If yes — reconstruct from that evidence and cite it; if no — DROP; (2) never reconstruct from inference: filling in a lesson's applies_when or enforcement by guessing is citogenesis wearing a rescue costume — the reconstructed row looks authoritative and is invented; (3) the DROP carries a re-file path: name the asserting pass (here: the fold's new pass — applies_when must be a dict with enforcement) and the responsible authors, so anything still load-bearing re-files safely; (4) record the decision in shared state with the invariant count (here: 278 rows kept) — the decision, the rationale, and the re-file path are the receipt; (5) the lane whose work produced the quarantined rows carries its own lessons in its sign-out — the knowledge isn't lost, it's redistributed to the seats that earned it. Cousin map: SN-0624 (a quarantine snapshot is point-in-time evidence — reconstruct the COLLISION REGISTRY from live bytes; note the deliberate contrast: registries rebuild from live bytes, but LESSON CONTENT can't be rebuilt from bytes — it needs its author); SN-1545 (the filing gate that the dropped rows violated — this note is the triage twin of that gate).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1546,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "when_a_quarantined_store_entry_cant_be_safely_reconstructed_drop_it_and_let_the_fold_re_file_what_still_matters",
  "applies_when": [["lesson-store", "quarantine"], ["memory", "malformed-entry"], ["fold", "asserting-pass"], ["triage", "reconstruction-safety"]],
  "enforcement": "Every quarantine triage writes a shared-state director_decision record naming the quarantined rows, the reason reconstruction is unsafe (the exact unreachable author-evidence path), the store invariant count after the drop, and the re-file path (the fold's asserting pass + the responsible authors). A tick-level store-invariant audit greps the store against the gate rule (every row carries applies_when dict + enforcement); any row that fails without a quarantine record is a triage miss.",
  "evidence": {
    "decision": "shared-state.json director_decision_lessons_quarantine_2026_10_17 (decided 2026-10-17T04:10:00Z, director authority under the standing 'decide by the law' grant): DROP the 3 quarantined rows — they violated the BOUNCE law (applies_when as a plain string, no enforcement); store invariant restored (278 rows kept); re-file only through the fold's NEW asserting pass by the original authors",
    "trigger": "board event 6229438733 (Naya Verity lane 0): lesson_inject.py crash root-caused + fixed; the 3 malformed rows (2026-10-17T03:59:31Z Theta lane1, 03:59:57Z Iota lane2, 04:00:18Z Kappa lane3) were quarantined at the crash site",
    "unsafe_reconstruction": "the lanes' author evidence path (~/workspace/naya/bin/lesson_inject.py) was not reachable on this VM — no safe reconstruction possible; reconstruction would have meant inventing content"
  },
  "procedure": [
    "triage each quarantined entry by reconstructability: is the original content recoverable from author evidence (the author's write path, a receipt, a board comment)?",
    "reconstructable → rebuild from that evidence and cite it; not reconstructable → DROP — never reconstruct from inference",
    "the drop carries a re-file path: name the fold's asserting pass and the responsible authors; anything still load-bearing re-files by its author",
    "record the decision in shared state: the rows, the unreachable evidence path, the invariant count, the re-file path",
    "the originating lanes' sign-outs carry their own lessons — knowledge redistributes to the seats that earned it"
  ],
  "falsifier": "The doctrine dies if a dropped entry proves load-bearing AND never re-files — an audit of dropped-vs-refiled showing a permanent loss kills the 'anything still load-bearing re-files' premise. It also dies if a case is found where reconstruction from reachable author evidence was refused in favor of a drop (then the triage chose cheap over safe).",
  "mechanism": "Reconstruction without author evidence invents content — citogenesis: the invented row wears the authority of the store without the provenance of an author. The only safe writers of lesson content are the original authors writing through the asserting pass, which enforces the gate the row violated. Dropping preserves the store invariant (every row valid) instead of poisoning it with guesses; the invariant is what every downstream reader trusts, and one invented row costs more trust than three dropped rows."
}
~~~
