# A Seat Token Is a Registry Key, Not a Label — Placeholders Fail Closed, Provenance Fills Them

**Intelligent Block:** IB-SMART-NOTE-20261021-sn01774-seat-token-is-a-registry-key-not-a-label
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/shared-state.json `naya2_to_builder` entry (added_utc 2026-10-21T16:08:00Z; comment 6319976042, Naya Resolve Narzan, integration / corrective pass — "blocker root-caused: consensus-gate `Seat: Naya N` placeholder reds on builder PRs"; https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6319976042). Corrected receipts verified on gate run 39627447054 (receipt + no-silent-deletions PASS).

## ✦ IN A NUTSHELL

The consensus gate kept failing builder PRs red, and the root cause was not the code and not the parser — it was `Seat: Naya N`, a placeholder, where the gate expected a registry key. tools/check_merge_consensus.py accepts numeric seats 1–5 or registered names (Alpha-Mu, Nitro, Chi, Relay, Clarity, Verity, Resolve) and fail-closes on anything else. The fix was not to make the placeholder parse — it was to replace each token with the real author seat resolved from provenance (#2835 → Naya Resolve, #2832 → Naya Resolve, #2834 → Naya 5 / Verity, #2829 → Naya 5 / Verity; #2830/#2831/#2833 still owed — determine from provenance, do not guess). A seat token that resolves nowhere is an unattributed claim, and an unattributed claim can never pass as verified — fail-closed is the correct behavior, not the bug.

## 🩷 HUMAN NOTE

Shawn — four builder PRs were red on the consensus gate for a silly-but-serious reason: the seat line on each PR body said "Seat: Naya N", which is a placeholder, not a real seat. The gate checks seat names against a registered list and rejects anything it doesn't know. Naya Resolve root-caused it and filled in the real author seats from provenance (#2835 and #2832 are hers, #2834 and #2829 are Naya 5 / Verity's); three more PRs still need their seats determined from the actual record, not guessed. The standing rule now: a seat token must name a registered seat resolved from provenance — placeholders fail closed by design, and guessing a seat is worse than leaving it owed.

## 🟣 CHILD NOTE

Think of the seat line like a name tag at a checkpoint. The guard has a list of real names. If your tag says "Naya N" — which is just "some Naya, probably" — the guard can't look you up, so you don't get through. That's not the guard being mean; that's the guard doing its job. The fix isn't to make the guard accept fake tags — it's to write the real name, the one that matches the record of who did the work. And if you don't know whose name it is, you look it up — you never write down a guess, because a guessed name tag is just another fake tag.

## 🔵 GRANDMA NOTE

It's like the sign-in sheet at a volunteer kitchen: everyone writes their real name so the coordinator knows who cooked what. One week four dishes arrived with the cook's name written as "Naya N" — nobody's actual name. The coordinator couldn't credit anyone, so she set the dishes aside until the real cooks were identified from the schedule. She didn't throw the dishes out, and she didn't make up names either. New kitchen rule: write your real name, or check the schedule to find it — a made-up name is no better than a blank.

## 🟠 NAYA NOTE

Seat-attribution is a trust boundary, not a label field. The consensus gate's `Seat:` token is a foreign key into the seat registry: numeric 1–5 or a registered name (Alpha-Mu, Nitro, Chi, Relay, Clarity, Verity, Resolve). Any other string — including a plausible-looking placeholder like `Seat: Naya N` — fail-closes, and that fail-closed is the enforcement working, not a defect to patch around. Two failure modes live here: (1) the placeholder author — writing something seat-shaped instead of seat-resolved; (2) the guesser — filling an owed seat from intuition instead of provenance (commit authorship, claim record, lane receipts). Both produce unattributable claims, and the gate is correct to reject them. The ordered procedure: determine the author seat from provenance → write the registered token → re-fire the gate; if provenance cannot resolve it, leave it owed and name the owner. Related: SN-0351 (sign-in/out law — claims need a named actor); the TOOLS.md gh-api quirk "never add a bare Seat: Naya N line" family.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1774",
  "title": "A Seat Token Is a Registry Key, Not a Label — Placeholders Fail Closed, Provenance Fills Them",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-VERDICTS"],
  "applies_when": ["merge", "consensus-gate", "seat-attribution", "receipt", "claim"],
  "enforcement": "tools/check_merge_consensus.py rejects any Seat: token outside the closed registry (numeric seats 1-5 or registered names Alpha-Mu, Nitro, Chi, Relay, Clarity, Verity, Resolve) with a red verdict naming the unrecognized token — fail-closed by construction; an unattributable claim can never pass as verified. Filer-side: any PR-body seat token must cite the provenance (commit authorship / claim record / lane receipt) that resolves it; seats that cannot be resolved are left owed and named, never guessed. The scorer bounces seat-token fixes that do not quote the resolving provenance.",
  "cousins": ["SN-0351 (sign-in/out law — every work claim opens with a named actor; this is the gate-enforced byte form of that law)", "SN-1660 (name the gate's read surface — the consensus gate's read surface includes the Seat: token registry lookup)"],
  "evidence": {
    "root_cause_comment": "board #2793 comment 6319976042 (2026-10-21T16:08Z, Naya Resolve Narzan, integration / corrective pass): 'Seat: Naya N' is a placeholder, not a registered seat; gate accepts numeric 1-5 or registered names (Alpha-Mu, Nitro, Chi, Relay, Clarity, Verity, Resolve)",
    "corrections": "seat declarations corrected on #2835 (Naya Resolve), #2832 (Naya Resolve), #2834 (Naya 5 / Verity), #2829 (Naya 5 / Verity); #2835 '## Deletions' heading corrected to exact parser contract; receipt + no-silent-deletions PASS on gate run 39627447054",
    "owed_not_guessed": "#2830/#2831/#2833 author seats still owed — determine from provenance, do not guess (same comment)",
    "meta": "Metadata fixes change no code heads; nothing merge-ready"
  },
  "falsifiability": "tools/check_merge_consensus.py's accepted-seat list is the falsifier: if a placeholder or unregistered token ever passes the gate, this note's fail-closed claim is wrong and the note must be amended.",
  "mechanism": "Fail-closed registry lookup. An attribution token must resolve to a registered seat for the claim to be checkable; an unresolvable token is unattributable by construction, and an unattributable claim cannot be trusted — rejection is the enforcement working, not a defect.",
  "decision_change": "When writing a Seat: token on a PR body or receipt, resolve the author seat from provenance (commit authorship, claim record, lane receipts) and write the registered token; never write a placeholder, and never guess an owed seat."
}
```
