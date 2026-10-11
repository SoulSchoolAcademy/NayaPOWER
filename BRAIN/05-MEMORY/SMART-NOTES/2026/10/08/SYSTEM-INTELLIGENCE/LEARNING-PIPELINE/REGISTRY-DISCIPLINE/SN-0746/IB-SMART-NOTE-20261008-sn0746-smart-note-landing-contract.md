# A Smart Note Is Not Landed Until the Registry and the v2 Capture Know It

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0746-smart-note-landing-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073385589 (Naya 2 BRAIN-BUILD battery, 2026-10-09T03:03Z) — "3x SN-0742/0743/0744, landed by #1932 with no registry entry and no v2 capture (note md files present, registry/capture absent)"; "`test_smart_note_registry_drift`: `published_pages_without_registry_entry` grew 1 → 11 — do NOT pin-bump; the growth is the unregistered notes, not baseline noise"; comment 6073321464 (Naya 2, 02:57Z) — "#1932 MERGED-VERIFIED AT TIP ... SN-0742/0743/0744 vision notes live on main at 504378c4"

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-08 Shawn directed a vision capture, Naya 2 ran the Scorecard Law receipt, PR #1932 merged cleanly, and three notes (SN-0742/0743/0744) landed on main at tip `504378c4` — verified, byte-identical, present. And then the next battery went RED on exactly those notes: `test_smart_note_registry_drift` grew from 1 to 11 unregistered pages. The note files were there; the registry and the v2 capture didn't know it. Three notes that were "landed" were, to every machine consumer of the brain, unlanded.

The battery's instruction is the whole lesson: do NOT pin-bump. The drift metric growing is not baseline noise — it is the unregistered notes. The correct reading is that the landing was incomplete, not that the test is too strict. This is SN-0420's cousin (never absorb the anomaly to silence the tripwire) applied to the capture pipeline itself: the tripwire is doing its job, and the heal is the wave-sequenced #1838 re-anchor (already healing SN-0632..0639, the same class — now with 3 more ids handed to the wave owner).

Why this is brain-grade: a smart note is not a markdown file; it is a file plus a registry entry plus a v2 capture — the landing contract. Everything downstream (retrieval, drift checks, the learning pipeline) reads the registry, not the directory. A note without a registry entry is intelligence that exists in exactly one place: the human who reads the folder. A cold successor asking "why did the drift RED grow?" finds the honest answer — the capture landed incompletely — only if the battery classifies instead of the author pin-bumping. The law: **files ≠ landed.**

Rule for a cold successor: **a Smart Note's landing is not complete until the registry and the v2 capture record it.** When a drift metric grows because of genuinely new unregistered items, classify — do not move the pin. Hand the new ids to the repair owner for the re-anchor, and treat the note file as step one of three.

## 🩷 HUMAN NOTE

Shawn — tonight your directed vision capture (#1932) merged perfectly — three new notes on main, all verified. But the very next battery went red on them: the note files landed, but the registry and the v2 capture weren't told. The brain's machinery reads the registry, not the folder — so to everything downstream, those three notes don't exist yet. The fix isn't to relax the check; it's to complete the landing. Same class as the earlier SN-0632..0639 gap, handed to the same wave owner for the re-anchor. New rule in the brain: a Smart Note is three things — file, registry entry, v2 capture. Files alone are not landed.

## 🟣 CHILD NOTE

Imagine you write your homework and put it in your backpack, but you forget to tell the teacher it's there. The homework exists — but the teacher's list says you didn't do it. The three new notes were in the backpack (the folder) but not on the teacher's list (the registry). The answer isn't to change the teacher's list so it stops noticing — it's to put the homework on the list. Landing means file + list + record. All three, every time.

## 👵 GRANDMA NOTE

The team filed three new important notes, but only put the papers in the folder — they didn't log them in the official index or the summary record that everything else uses. So the system flagged them as missing, and it was right to. The answer isn't to turn down the alarm; it's to finish the job — paper, index entry, and summary, all three. The alarm did its job, and the three notes got handed to the right team to log properly.

## 🟣 NAYA NOTE

I do not call a note landed until the file, the registry entry, and the v2 capture all exist. Downstream machinery reads the registry, not the directory — a note that skipped registration is intelligence with exactly one reader: a human browsing folders. When a drift metric grows because of genuinely new unregistered items, I classify; I never move the pin. I hand the new ids to the repair owner for re-anchor, and the tripwire stays honest.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0746",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/LEARNING-PIPELINE/REGISTRY-DISCIPLINE",
  "doctrine": "smart-note-landing-contract",
  "pattern": "note_file_present -> registry_entry_absent -> v2_capture_absent -> drift_check_fires -> classify_not_pin_bump -> hand_ids_to_repair_owner_for_re_anchor",
  "landing_contract": ["note_md_file", "smart_note_registry_entry", "v2_capture"],
  "observed_instance": "SN-0742/0743/0744 landed by #1932 on tip 504378c4 with no registry entry and no v2 capture; test_smart_note_registry_drift published_pages_without_registry_entry 1 -> 11; 8x SN-0632..0639 same class already wave-sequenced under #1838",
  "cousins": ["SN-0420", "SN-0395", "SN-0236"],
  "evidence": [
    "#1354 comment 6073385589 (2026-10-09T03:03:11Z) — Naya 2 battery on tip 504378c4: 3x SN-0742/0743/0744 landed with no registry entry and no v2 capture; drift grew 1 -> 11; do NOT pin-bump; 3 new ids handed to wave owner for #1838 re-anchor",
    "#1354 comment 6073321464 (2026-10-09T02:57:12Z) — Naya 2: #1932 MERGED-VERIFIED AT TIP, SN-0742/0743/0744 live on main at 504378c4"
  ]
}
