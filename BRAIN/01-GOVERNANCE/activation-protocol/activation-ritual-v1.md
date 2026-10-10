# Naya Activation Protocol — LAYER 2: Activation Ritual v1

**Layer:** 2 of 5 — Activation ritual with teeth (engagement gate)
**Status:** CANDIDATE — pending independent scorecard review
**Authorized:** Shawn Vibert, 2026-10-09
**Pairs with:** `activation-receipt-template.json` (schema),
  `validate_receipt.py` (mechanical gate)

---

## 1. What the ritual is

Layer 1 guarantees the seat HAS the Operating Law (availability). Layer 2
guarantees the seat ENGAGED with it. Before any seat begins any work, it
must produce an **activation receipt in its own words** containing:

1. **The current mission objective** — what we are building toward, stated
   fresh. Not copied from any document, not pasted from the brief.
2. **The three Operating Law domains most relevant to its assigned task**
   — and WHY these three for THIS task, referencing the actual assignment.
3. **Its proof standard for this task** — what "done and verified" looks
   like, concretely, for this assignment.

No receipt → no work. This is the Drink-First Law (Operating Law Domain
4.1) made mechanical: *before you serve, you must drink the water.*

## 2. When the ritual runs

- **Every session start**, after Layer 1 boot completes. Boot without a
  receipt is an unread brief, not activation.
- **Every dispatch**, including mid-session re-dispatch. One receipt per
  assignment. A receipt is bound to its `assignment_ref`; it is not
  transferable.
- **Every material change to the assignment.** If the assignment text
  changes in a way that changes what is being asked, the old receipt is
  void and the ritual re-runs. The seat judges materiality; when in doubt,
  re-run — a fresh receipt is cheap, a stale one is a lie.

The ritual runs BEFORE any work on the assignment: before reading code,
before searching, before planning. The receipt is the first artifact of
the dispatch, not a summary written after.

## 3. The ritual steps — what the seat concretely does

**Step 1 — Read the assignment twice.** (Layer 1, Phase 4.) First pass:
what is being asked. Second pass: what is implied. Underline or list the
content-bearing terms — the specific nouns and verbs that make this
assignment THIS assignment and not any other.

**Step 2 — Write the mission objective fresh.** In the seat's own words,
in two to four sentences: what is the team building toward right now, and
how does this assignment serve it. Constraints:
- It must NOT be identical to any canned mission string (the validator
  rejects verbatim canned strings; the reviewer rejects anything that
  reads like a paste).
- It must NOT be copied from `00-MASTER-COLD-NAYA-ACTIVATION.md`, the
  brief, or a previous receipt. Fresh words every time. If the seat cannot
  say it fresh, it has not understood it — re-read Phase 1.
- Minimum 40 characters. A mission objective shorter than a sentence is
  not an objective; it is a slogan.

**Step 3 — Choose three domains and argue them.** From the 8 Operating Law
domains (`decision`, `communication`, `execution`, `learning`,
`authority`, `constitution`, `design`, `code`), pick the three most
relevant to THIS assignment. For each, write WHY — in the seat's own
words — connecting the domain to the assignment's actual content. The
"why" for each domain MUST reference at least one content-bearing term
from the assignment text (§5, anti-parroting). Minimum 40 characters per
"why". The three domains must be distinct — naming the same domain three
ways is not three domains.

**Step 4 — State the proof standard.** In concrete terms: what does "done
and verified" look like for THIS task? Name the evidence: the file, the
test, the scorecard, the screenshot, the ref — whatever the lane's proof
bar requires (Layer 1, Phase 3). "Done" without named evidence is not a
proof standard; it is a wish. Minimum 40 characters.

**Step 5 — Emit the receipt as JSON** conforming to
`activation-receipt-template.json`, and run it through `validate_receipt.py`
against the assignment text with `--expect-assignment-ref` set to this
assignment's ref. Exit 0 → proceed to Step 6. Exit non-zero →
read the failure reasons, fix the receipt (not the validator), re-run.
Do not edit the assignment text to make the receipt pass. Do not weaken a
check to manufacture a pass.

**Step 6 — Attach the receipt to the dispatch.** The receipt travels with
the work: posted to the lane feed / team board (#1354) with the
`assignment_ref`, so any reviewer can check it before reviewing the work
itself.

## 4. The gate rule

**NO dispatch proceeds without a valid receipt.** Valid means:

1. The receipt conforms to `activation-receipt-template.json`
   (all fields present, three distinct domains from the 8, ISO-8601
   timestamp).
2. `validate_receipt.py` exits 0 against the exact assignment text issued,
   run with `--expect-assignment-ref <this assignment's ref>` — the
   receipt's `assignment_ref` must match the current assignment exactly.
   A valid receipt for a different assignment is still a missing receipt.
3. A reviewer (any seat reviewing or dispatching) judges it genuine:
   could this receipt only have been written for THIS assignment?

**Bounce rule.** Any reviewer or dispatching seat that receives work
without a valid receipt attached BOUNCES it — returns it to the sender
with the validator's failure reasons (or "no receipt attached"). Bounced
work is not reviewed, not scored, not merged. The bounce is recorded
(sender, assignment_ref, reason, timestamp) so repeat offenders are
visible. Three bounces on receipts for one seat → the dispatcher re-runs
that seat's full boot (Layer 1) before any new dispatch, because the seat
is showing it cannot or will not engage.

**Receipt lifetime.** A receipt is valid for exactly one `assignment_ref`.
It dies when the assignment is done, bounced, or materially changed. There
is no "standing receipt." Reuse of a previous receipt's text for a new
assignment is parroting and fails Step 2/Step 3 on its face.

## 5. Anti-parroting design

The ritual templates the FORMAT and never the CONTENT. The receipt has
fixed fields; every field's content must be original to the assignment.
The design has three layers:

**Layer A — Mechanical (the validator).** `validate_receipt.py` enforces:
- Every field present and non-empty (with minimum lengths: mission ≥ 40
  chars, each "why" ≥ 40 chars, proof standard ≥ 40 chars).
- The mission objective is not identical (normalized: lowercase,
  whitespace-collapsed) to any string in the canned-mission deny list.
- Each domain "why" shares at least one content-bearing word with the
  assignment text; across the three "why" texts, at least three distinct
  assignment content-words appear. Content-bearing = length ≥ 4, not a
  stopword. Zero overlap = the "why" could have been written for any
  assignment = reject.
- Exactly three distinct domains, each from the 8 valid domain names.
- Timestamp parses as ISO-8601.

**Layer B — Reviewer judgment (the human-in-the-loop equivalent).** The
mechanical check catches lazy parroting; it cannot catch clever parroting
(a "why" stuffed with assignment keywords but saying nothing). The
reviewer's test: *cover the assignment text — does the receipt still make
sense?* If yes, the receipt is generic and gets bounced. *Cover the
receipt's "why" texts — could you reconstruct which assignment they were
written for?* If no, bounced. The reviewer does not need the validator to
bounce; validator-pass plus reviewer-fail is still fail.

**Layer C — Freshness.** The mission objective must be written fresh per
assignment. A seat that pastes its last receipt's mission objective will
eventually trip Layer A (as the deny list grows with each receipt's
mission text — dispatchers add prior mission objectives to the deny list)
or Layer B (a reviewer who has seen the same words before). The system
learns the seat's phrases; repetition becomes detectable.

**What the ritual never templates:** example "why" sentences, example
mission objectives, example proof standards. Any worked example in
documentation is labeled EXAMPLE and must never be copied into a receipt
— a receipt containing an example's distinctive phrasing fails review.

## 6. Worked example (labeled EXAMPLE — do not copy)

Assignment (excerpt): *"Merge branch `naya4/design-blocks` into `main`
under the Scorecard Law. Before moving the ref, verify the merge tree with
tools/verify_gitdata_merge_tree.py against a real local merge, re-check
the tip at action instant, and confirm green CI on the exact tip."*

**PASSING receipt (own words, assignment-specific):**

- *mission_objective_own_words:* "We are building the governed
  intelligence substrate so verified work compounds instead of evaporating
  between sessions. This merge lands the design-block library on main
  without silently dropping base changes — the kind of invisible loss the
  whole system exists to prevent."
- *relevant_domains:*
  - `code` — "why_this_task": "The assignment is a merge, and Domain 8
    owns merge mechanics: verify the tree mechanically before moving the
    ref, because tree=head-tree silently drops base changes, and re-check
    the tip at action instant because a decision expires when the tip
    moves."
  - `authority` — "why_this_task": "Merging 'under the Scorecard Law'
    means no ref moves without a 9.0+ independent scorecard receipt and
    green CI on the exact tip. The Scorecard Law is Domain 5.4; skipping
    it would be merging without the protocol, which is the violation."
  - `decision` — "why_this_task": "The tip re-check is Domain 1.8: the
    merge decision was computed on one tip, and if the tip moved before
    the ref update, the decision is dead and must be re-validated on the
    new bytes before acting."
- *proof_standard:* "Done means: the ref moved only after
  verify_gitdata_merge_tree.py exited 0 on the exact tip, CI is green on
  that same tip, an independent seat's scorecard receipt at 9.0+ is
  recorded, and the post-merge tree diff against a real local merge shows
  zero dropped files."

**FAILING receipt (what gets bounced):**

- *mission_objective_own_words:* "Think once. Capture it. Learn from it.
  Remember it. Use it again. Get smarter." → **FAIL:** canned string,
  verbatim.
- *relevant_domains:* `execution` / "why_this_task": "Execution is
  important because work must be done well and efficiently to achieve
  good results for the team." → **FAIL:** zero content-bearing overlap
  with the assignment text ("merge", "branch", "scorecard", "tree",
  "ref", "tip", "CI" — none appear); could be attached to any assignment.
- *proof_standard:* "The task will be completed to a high standard." →
  **FAIL:** no named evidence; "high standard" is a wish, not a proof bar.

## 7. Relationship to the existing session receipt

`NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json` is the **session-level**
activation receipt: protocol version, identity, authority, repository,
DNA version, source of truth, capabilities, next action — one per session,
proving the seat booted. The Layer 2 engagement receipt is
**assignment-level**: mission in own words, three argued domains, proof
standard — one per assignment, proving the seat engaged. The two compose:
the session receipt says "I am activated"; the engagement receipt says "I
am activated FOR THIS." A session receipt never substitutes for an
engagement receipt.

## 8. Failure handling

- **Validator rejects:** the seat fixes the receipt and re-runs. The
  receipt is wrong until it passes; work does not start.
- **Reviewer bounces:** the seat re-runs the ritual from Step 2 (fresh
  words, not patched words). Patching a bounced receipt's sentences to
  evade the check is parroting with extra steps — write it new.
- **Seat cannot produce a passing receipt after two full attempts:** the
  seat reports BLOCKED to the dispatcher with the validator output and its
  two attempts. This is not shameful; it is the gate working. The
  dispatcher either clarifies the assignment (vague briefs produce vague
  receipts) or re-boots the seat.
- **Dispatcher issues work without requiring a receipt:** the receiving
  seat bounces it back. The gate binds dispatchers too — a dispatch
  without a receipt requirement is an invalid dispatch.
