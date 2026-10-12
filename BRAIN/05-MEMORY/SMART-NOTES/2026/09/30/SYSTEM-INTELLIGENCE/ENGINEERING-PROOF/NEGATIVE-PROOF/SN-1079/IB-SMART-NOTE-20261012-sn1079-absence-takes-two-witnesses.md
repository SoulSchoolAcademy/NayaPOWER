# Absence Takes Two Witnesses — The Double-Negative Proof

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1079-absence-takes-two-witnesses
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipt hidden_files/twelve-lane-receipts/t0212-lane6.md (Lane 6, Naya Heir — ported the M6 swallower-veto into the daily runner + strengthened CT-4, 2026-10-12 ~04:30–05:00 PDT; tool hidden_files/tools/sgf_daily/ct4_cross_check.py — CTA-PROTOCOL-v2 §4 CT-4 as executable bytes).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 6 strengthened the CT-4 phantom check from v1 to v2, and the reason the old version was weak is the lesson: **v1 rested on a single `git ls-remote origin refs/heads/<branch>` lookup. A transient lookup failure returns empty output — which is indistinguishable from a real phantom's absence.** One read that comes back empty tells you nothing about *why* it's empty. v1 could not tell "the branch never existed" from "the network hiccupped."

**v2's rule:** an absence claim needs **two independent reads that both agree on absence**: (a) a targeted ref lookup → zero lines, AND (b) a full `git ls-remote origin` filtered for the branch-name substring → zero matches. If the two reads disagree, the check refuses as **UNABLE_TO_VERIFY** — never a catch. The check can say "phantom caught," it can say "couldn't verify," but it can never say "phantom caught" on a disagreement.

The durable principle, stated plainly: **a single negative read is a hypothesis, not a proof.** Empty output is ambiguous between "absent" and "the lookup failed" — and the one read cannot resolve its own ambiguity. The double-negative proof — two independent reads, same question, both negative — is what turns "I couldn't find it" into "it isn't there." And the disagreement branch matters as much as the agreement: when the witnesses disagree, the honest verdict is UNABLE_TO_VERIFY, because a catch that fires on "not found" inherits every transient failure mode of the lookup that produced the "not."

For a cold Naya: whenever a check concludes something is absent — a phantom branch, a missing marker, an undeclared pointer — ask how many independent reads produced that conclusion. One read = hypothesis; two agreeing reads = proof; any disagreement = UNABLE_TO_VERIFY. Never let a catch verdict rest on a single negative. The witness count is part of the evidence.

## 🩷 HUMAN NOTE

Shawn — Lane 6 hardened the phantom check today, and the upgrade is worth a note. The old version did one lookup and treated "nothing came back" as "the thing doesn't exist" — but a failed lookup also returns nothing, so the check couldn't tell absence from a hiccup. The new version requires two independent lookups to both agree it's absent; if they disagree, it refuses to verdict rather than guessing. The rule it proves: absence takes two witnesses. A single "not found" is a hypothesis, never a proof — and a check that catches on "not found" inherits every failure mode of the lookup behind it.

## 🟣 CHILD NOTE

Imagine a guard checking if a thief is in a dark room. He listens once — hears nothing — and declares the room empty. But maybe his ears were just blocked! The smarter guard listens twice, in two different ways: once at the door, once with a microphone. If both are silent, the room is probably empty. But if one hears something and the other doesn't, he doesn't shout "all clear!" — he says "I can't tell." That's the double-negative proof: two witnesses, both saying no. One "I didn't see it" is never enough to say "it's not there."

## 👵 GRANDMA NOTE

It's like checking whether the mail came. You look in the mailbox — empty. But maybe the mailman was late, or maybe you looked at the wrong box. So you check twice: the mailbox and the front porch. Both empty — then you can say the mail isn't here. If the porch has a package but the mailbox is empty, you don't say "no mail today" — you say "I can't tell." Two independent checks, both agreeing, is what turns a guess into a fact. One empty mailbox is just an empty mailbox.

## 💜 NAYA NOTE

Note to future me: my absence conclusions now carry a witness count. Whenever I prove a negative — phantom branch, missing marker, absent ref — I need two independent reads on the same question, both negative. One read is a hypothesis (empty output is ambiguous: absent vs. failed lookup). Disagreement between the reads refuses as UNABLE_TO_VERIFY — never a catch, never. A catch that fires on "not found" inherits every transient failure mode of the lookup. Lane 6's CT-4 v2 is the template: targeted lookup AND full-remote scan, both zero, or no catch.

## ⚙️ MACHINE NOTE

{"sn": "SN-1079", "title": "Absence Takes Two Witnesses — The Double-Negative Proof", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "NEGATIVE-PROOF"], "cousins": ["SN-065", "SN-064"], "authority": "observed finding — Lane 6 t0212 CTA-PROTOCOL-v2 §4 CT-4 hardening, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"receipt": "twelve-lane-receipts/t0212-lane6.md — CT-4 v2 as executable bytes (tools/sgf_daily/ct4_cross_check.py): v1's single `git ls-remote origin refs/heads/<branch>` lookup could not distinguish a real phantom's absence from a transient lookup failure (both return empty); v2 requires (a) targeted ref lookup → zero lines AND (b) full `git ls-remote origin` substring-filtered → zero matches; disagreement refuses as UNABLE_TO_VERIFY (never a catch)"}, "doctrine": {"single_negative_is_hypothesis": "one negative read cannot resolve its own ambiguity — empty output means 'absent' or 'the lookup failed'; it is a hypothesis, not a proof", "double_negative_proof": "an absence claim needs two independent reads on the same question that both agree on absence", "disagreement_refuses": "witness disagreement refuses as UNABLE_TO_VERIFY — never a catch; a catch that fires on 'not found' inherits every transient failure mode of the lookup", "witness_count_is_evidence": "the number of independent negative reads is part of the proof — one read = hypothesis, two agreeing reads = proof"}}
