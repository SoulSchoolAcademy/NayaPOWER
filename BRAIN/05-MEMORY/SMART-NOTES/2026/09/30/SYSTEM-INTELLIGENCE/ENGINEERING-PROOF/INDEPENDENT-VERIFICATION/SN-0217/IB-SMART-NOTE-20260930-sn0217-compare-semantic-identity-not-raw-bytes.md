# Compare Semantic Identity, Not Raw Bytes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0217-compare-semantic-identity-not-raw-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5966378212 (brain-build watchtower, 2026-10-03T06:30:45Z, SoulSchoolAcademy) — verification note for future runs, battery `hidden_files/batt-2216` on exact tip `5b68f8dcac78873741ed78d740f546b6f4083a22`

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two independently regenerated artifacts are compared to decide whether they are the same repair class (no-duplicate-repair triage), **do not compare raw bytes** — generated artifacts carry volatile stamps that roll across UTC midnight. The brain-build watchtower independently regenerated PR #1343's index from exact tip `5b68f8dc` and found it **semantically identical** to #1343's head `02eec14a` (same basis SHA, 177 files, same domain counts, identical file set) — but the raw blobs differed by one thing only: the `generated_at` date stamp, which rolled at UTC midnight between the two runs.

A naive blob-byte comparison would have false-positived this as "not the same repair" and could have caused a duplicate repair lane to stand up its own PR. The fix is mechanical: verify equivalence through the tool's own normalizers (the brain-index `--check` normalizes the stamp before comparing) — basis SHA + inventory + file set + domain counts — and only then declare same-class and stand down (which is what happened: zero push, #1343 stays the canonical lane).

This is the complementary cousin of SN-0100 ("a mechanical change is still a change — verdicts die at every new SHA"): SN-100 says a mechanical change breaks identity; SN-217 says a mechanical *stamp roll* does not break identity — **compare what identity means for this artifact class, not its bytes**. Both flow through SN-0052's "diff the diffs" discipline and SN-0177's byte-identical-stand-down practice.

## 🩷 HUMAN NOTE

Shawn — a small but real verification discipline that just saved the lane a duplicate PR: when two runs regenerate the brain index, their files will differ by one harmless thing if the runs straddle midnight UTC — a `generated_at` date stamp inside the files. A naive byte comparison would say "different" and invite a duplicate repair. The watchtower instead compared *semantic* identity through the tool's own normalizers (same basis commit, 177 files, same counts) and stood down correctly: #1343 stays the single canonical repair. Rule of thumb: compare what identity means for the artifact, not its raw bytes.

## 🟣 CHILD NOTE

Imagine two children draw the exact same picture of a house, but one writes "Monday" and the other writes "Tuesday" in the corner. If you only compare whether the two drawings are pixel-for-pixel identical, you'd say "different drawings!" — but that's silly. The right check is: is it the same house? Same windows, same door, same chimney? The written day doesn't matter. The same goes for computer-generated files: some carry a little date stamp that changes overnight. Compare the *meaningful* parts, and know which parts are allowed to be "just the date."

## 👵 GRANDMA NOTE

Think of two editions of the same cookbook — same recipes, same pages, same chapter order — but the printer's slip inside says one was printed on Monday and one on Tuesday. Nobody would call those different books. Computer programs that regenerate files sometimes stamp the current date inside them, so a file made at 11pm and one made at 1am look different to a careless comparison even when everything that matters is identical. The lesson: when checking "are these the same?", compare the recipe, not the printer's slip.

## 🤖 NAYA NOTE

Watchtower battery 2026-10-02 23:26 PDT (`hidden_files/batt-2216` @ exact SHA `5b68f8dcac78873741ed78d740f546b6f4083a22`): full pytest 550 passed / 3 skipped / 0 failures; brain index `--check` RED exit=1 (drift: 5 daily intelligence reports 2026/09/27–10/02 landed without regen; ledger 29→34, inventory 172→177 — the class the canonical #1312 repair fixed at 16:57Z, reopened by later landings). No-duplicate-repair triage: PR #1343 open for this exact drift (head `02eec14a`, base = exact tip, non-draft); independent regen from `5b68f8dc` semantically identical (same basis SHA, 177 files, same domain counts, identical file set); sole byte delta = `generated_at` stamp across UTC midnight rollover. `--check` normalizes the stamp; raw blob comparison false-positives. Stood down, zero push. Blocker re-scan (live GETs): #1224 open draft @ `a71fbfe1` (8 qualify items merge-gated), #1136 open, no PRs merged to main during battery. Cousin family: SN-0100 (verdict dies at every new SHA — mechanical change breaks identity), SN-0052 (diff the diffs), SN-0059 (attribute before blaming), SN-0177 (byte-identical-stand-down), SN-0061 (non-vacuous negative proofs). Graph state: 8.5/10 unchanged, zero production mutation.

## ⚙️ MACHINE NOTE

{"sn": "SN-0217", "title": "Compare Semantic Identity, Not Raw Bytes", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0100", "SN-0052", "SN-0059", "SN-0177", "SN-0061"], "evidence": {"board": ["#554 5966378212 (brain-build watchtower, 2026-10-03T06:30:45Z)"], "pin": "main 5b68f8dcac78873741ed78d740f546b6f4083a22 (ls-remote HEAD, tip unchanged through scan)", "battery": "hidden_files/batt-2216 @ exact SHA: pytest 550 passed / 3 skipped / 0 failures; brain index --check RED exit=1 (drift: 5 daily reports 2026/09/27-10/02, ledger 29->34, inventory 172->177)", "same_class_repair": "#1343 brain-build/index-regen-5b68f8dc head 02eec14a base=exact tip non-draft; independent regen semantically identical (same basis SHA, 177 files, same domain counts, identical file set); only byte delta = generated_at UTC-midnight rollover; stood down, zero push"}, "rule": "when comparing two independently regenerated artifacts to decide same-repair-class, verify semantic identity (basis SHA + inventory + file set + counts) via the tool's own normalizers — never raw blob-byte comparison, because volatile stamps (generated_at) roll at UTC midnight and false-positive as difference"}
