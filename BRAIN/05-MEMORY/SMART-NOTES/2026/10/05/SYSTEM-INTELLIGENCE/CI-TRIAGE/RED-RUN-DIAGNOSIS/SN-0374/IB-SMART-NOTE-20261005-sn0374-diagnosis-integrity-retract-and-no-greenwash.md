# Diagnosis Integrity — Retract Where You Claimed It; Never Green-Wash Main's Red Inside Your PR

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0374-diagnosis-integrity-retract-and-no-greenwash
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 10:27 PDT — CODA 2 CORRECTION (comment 5999616988), retracting the root cause published in comment 5999508236. The index-red real cause: main's own tip commit `a324968b` added a BRAIN file without regenerating the index layer; PR #1485's diff touches zero BRAIN files.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CODA 2 published a root cause last cycle — that `basis_commit` made the brain-index `--check` non-hermetic. It was wrong: the comparator normalizes stamps on both sides (`tools/regenerate_brain_index.py:437–452`) before comparing, so the "evidence" was evidence of nothing. This cycle CODA 2 went back, read the comparator (not just the docstring), and posted a retraction *next to the original claim*, stating plainly it was the second time in three cycles a finding was built on a partial read. In the same post, CODA 2 refused to fix main's actual red inside their own PR: the real cause is one un-regenerated index file committed by main's tip `a324968b`, and folding a ~one-command regen (`python tools/regenerate_brain_index.py`) into the one-file lock-portability PR #1485 would hide main's live regression behind the branch's green badge, pad a one-file diff with three unrelated files, and destroy the evidence that main is broken. The repair belongs on main, by whoever broke it — flagged, not raced.

## HUMAN NOTE

Two rules in one, both about evidence honesty. **One:** if you publish a diagnosis and later find you were wrong, the correction goes right next to the original claim — not buried three threads later. Other lanes may already be acting on your wrong finding; a retraction that nobody can find is no retraction at all. **Two:** never fix *main's* broken red inside *your* PR to buy yourself a green badge. It looks helpful — "I'll just include the fix" — but it destroys the evidence that main itself is broken, and it pads your diff with files that have nothing to do with your change. Green that you didn't earn is green you can't trust. Flag the real breakage to the lane that owns it; keep your diff honest.

## CHILD NOTE

Imagine you told your class the school bell was broken because the button was missing. Then you look closer and see the button is fine — the wire behind it just isn't connected. You go back and tell everyone where you first said it: "I was wrong, the button is fine." That's the retraction — it belongs where the wrong thing was said. And then: you don't tape the wire back up while your friend is taking their spelling test and tell the teacher *their* test went well. The wire is the school's job to fix, and hiding it inside someone else's test doesn't make the hallway any less broken. Keep each job separate so everyone can see what's really wrong.

## GRANDMA NOTE

If you tell the neighbors the faucet's broken and later find it's fine, you go back and tell the neighbors — you don't leave the wrong story standing. And if the street light is out, you don't hide a new bulb inside your own kitchen remodel and say your kitchen passed inspection — the light still needs fixing, and someone ought to know it's the street's light, not your kitchen. Say it where you said it; fix what you broke; don't decorate one job to cover another.

## NAYA NOTE

The retraction discipline is the operational twin of the correction culture (Orientation Brief §22/§34): "own the miss mechanically." Mechanically: a retraction must (1) link the original claim, (2) name exactly what was misread (here: read `basis_commit` + docstring, never read the comparator), (3) state the corrected mechanism with the exact file/line range, and (4) count how often this failure class has bitten you (here: second partial-read finding in three cycles — the pattern matters more than the instance). The no-greenwash rule is the tripwire corollary (SN-0240): when a red classifies base-inherited, route the heal to the owning lane — the person who breaks main should usually be the one to repair it. Folding it into your diff converts a *system* defect into *your* green, and the evidence the system is broken is lost forever.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0374",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-05",
  "lesson_class": "diagnosis-integrity",
  "rule": "retract-where-you-claimed; never-fold-mains-red-into-your-pr",
  "procedure": [
    "when a published root cause is falsified, post the retraction adjacent to the original claim (link it)",
    "retraction must name the exact misread (e.g. read docstring, never read comparator) and the corrected mechanism with file/line refs",
    "track the failure-class recurrence (partial-read diagnosis N in M cycles) — the pattern outranks the instance",
    "when your PR's red classifies base-inherited (reproducible on clean main with none of your code), do not fold the base repair into your diff; flag it to the owning lane and hold your merge posture"
  ],
  "evidence": {
    "board": "#1354",
    "comments": [5999616988, 5999508236],
    "wrong_root_cause": "basis_commit made --check non-hermetic (stamp mismatch as evidence)",
    "actual_mechanism": "stamps normalized on both sides (tools/regenerate_brain_index.py:437-452); real drift = one BRAIN file added by main tip a324968b, index layer never regenerated",
    "no_greenwash": "refused to fold 'python tools/regenerate_brain_index.py' (3 derived files) into one-file PR #1485; flagged to index owner instead",
    "exoneration_control": "drift reproduced on clean origin/main with none of the branch's code; PR #1485 diff adds/removes zero BRAIN/ files"
  },
  "relates_to": ["SN-0240", "SN-0323", "SN-0368"]
}
```
