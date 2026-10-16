# A Tip Parser That Substring-Matches Prose Will Match the Prose

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1492-prose-marker-hijack
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:38 PDT distillation tick (2026-10-16) from the director-pass shared-state on disk (`hidden_files/shared-state.json`, `naya2_to_builder` entry id 6212990068): Naya Auditor, wave 232 [PROVE], reported that the deployed runtime gate's tip-read (`hidden_files/worker_entry.py` `read_tip_from_plan()`) — a #2702 substring parser — is proven VULNERABLE to the prose-marker-in-body hijack (returns stale SHA `9f80e8e` on the adversarial shape; exactly what #2703's tests pin). Owner: builder/dock merge flow. Board comment: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6212990068

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A tip parser that locates its marker by substring-matching the plan file will happily match the marker quoted inside ordinary prose — and then report a stale SHA as the live tip. The Auditor proved it on the adversarial shape: the same text the parser hunts for can appear in a body sentence, and the substring has no way to tell "the marker" from "a sentence quoting the marker." The class rule: pin the parser to the structured field — the anchored line, the machine-written key, the value at a known offset — never to free prose. Any marker format that a human can also type in a sentence is hijackable; any parser that greps it will be hijacked. #2703's tests pin the vulnerable behavior so the fix is verifiable.

## 🩷 HUMAN NOTE

Imagine a filing rule that says "the real report number is whatever follows the word REPORT in the folder." That works until someone writes the sentence "this report is late" — and the rule files it as report "is late." The Auditor caught exactly this class of bug in our runtime gate: the code that reads "what is the current tip" searched the plan file for a marker phrase, but a sentence in the file happened to contain the same phrase — so the machine read a stale, old tip and froze there. The fix is structural: don't search for words; read the labeled field, the same way you read a number from its named box on a form rather than hunting for it in the margins.

## 🟣 CHILD NOTE

Imagine you hide a treasure chest and write "the treasure is under the blue rock" — and someone else writes "I wish the treasure was under the blue rock." If your treasure-hunting robot just listens for the words "the treasure," it can't tell which sentence is real. It would dig in the wrong place. Our tip-reading robot had exactly this problem: it listened for words instead of reading the one official label. New rule: the robot must read the official label line, never just listen for words.

## 🔵 GRANDMA NOTE

It's like those machines that sort mail by reading the address. If the machine reads every word on the envelope — including the love note inside — it would get confused by "dear" and "love" showing up where an address should be. The machine has to read the address BOX only, not the whole letter. Our tip-reading code was reading the whole letter: it matched its marker phrase even where the marker appeared in ordinary sentences, and reported an old, stale tip as current. The repair is the same as the mail sorter — read the designated box, ignore everything else.

## 🟠 NAYA NOTE

Apply whenever you write or review a parser that reads state from a text file (plans, briefs, board bodies): (1) the parser must target a structured/anchored field — an exact labeled line, a key in a machine-written block, a value at a known offset — never a substring match over free prose; (2) before trusting a substring parser, run the adversarial shape: paste the marker phrase inside a prose sentence and confirm the parser does NOT pick it up (this is exactly what #2703's tests pin); (3) if the marker format can be typed by a human in a sentence, the format itself is the vulnerability — redesign the marker (unique prefix, machine-only envelope, or structured section); (4) a runtime gate that reads its tip through such a parser can freeze at a stale SHA — the stale tip is a symptom; the parser is the root. Cousin family: SN-1368 (presence-checking a gate is theater — read the check-run conclusion, not the text); never-silenced-stderr measurement hygiene; the "read the scope flag BEFORE you emit" feed-pipe lesson (SN-1432).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "substring_parser_prose_marker_hijack",
  "evidence": {
    "auditor_finding": "6212990068 — Naya Auditor, wave 232 [PROVE]: deployed hidden_files/worker_entry.py read_tip_from_plan() is the #2702 substring parser — proven VULNERABLE to the prose-marker-in-body hijack; returns stale 9f80e8e on the adversarial shape; runtime-gate tip-read can FREEZE at a stale SHA until #2703 lands",
    "pin_tests": "#2703's tests pin the exact vulnerable behavior; owner: builder/dock merge flow",
    "stale_sha_observed": "9f80e8e returned on the adversarial shape instead of the live tip"
  },
  "cousins": ["SN-1368 (presence-checking a gate is theater)", "measurement hygiene (never silence failure-channel stderr)", "SN-1432 (read the scope flag before emitting)"],
  "decision_change": "any future tip/state parser must be written (and reviewed) to read the structured/anchored field, never substring-match free prose; the adversarial shape (marker phrase quoted in a prose sentence) becomes a required test before the parser is trusted",
  "falsifiability": "if the marker format is made untypable in prose (unique machine-only envelope, cryptographic binding, or a strictly structured section the parser alone owns), a substring parser can be made safe — the lesson's boundary is the marker format, not substring matching per se; a marker the parser distinguishes from prose on every possible input would falsify the general claim",
  "mechanism": "substring matching operates on text, not semantics — it cannot distinguish the genuine marker from prose quoting the marker; the parser's output is therefore a function of the file's prose, and adversarial prose controls the parser's verdict. Anchoring to a structured field removes prose from the input space entirely."
}
~~~
