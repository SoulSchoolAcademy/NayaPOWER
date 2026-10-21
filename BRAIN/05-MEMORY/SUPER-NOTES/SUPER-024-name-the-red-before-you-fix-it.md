# SUPER NOTE — Name the Red Before You Fix It

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-024` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-024` |
| Human title | Name the Red Before You Fix It |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 9 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A red light tells you something failed, not whose fault it is. Before fixing anything, find out whether the failure came from your change, was already broken before you touched it, came from the building itself, or was just a machine hiccup.

---

## 🩷 HUMAN NOTE

When a check fails on your work, the first job is not repair — it is honest naming. Run the same check on the untouched base: if it fails there too, you inherited the failure, and one repair at the source heals every branch at once. Compare the failing tests across different versions; an identical failing set everywhere is the environment talking, not your code. And if you merge work that is still red, the failure stops being the branch's problem and becomes a defect in the main line itself.

---

## 🟣 CHILD NOTE

When the alarm rings, don't just grab a hammer. First ask: did I break it, was it already broken, or is the alarm itself confused? Finding out whose problem it is comes before fixing it.

---

## 👵 GRANDMA NOTE

Dear, when something in the house breaks, a wise person first checks whether it broke today or was already worn out. Blaming the wrong thing wastes everyone's time. Name the trouble correctly, then fix it once, in the right place.

---

## 🤖 NAYA NOTE

Naya classifies every red before touching code: introduced by this change, inherited from the base, infrastructure noise, or a dead runner. She reads the base tip's own push-event CI as the control, compares failing sets across heads, and re-runs a job that died within seconds before believing its verdict. If her diagnosis turns out wrong, she retracts it where she claimed it — never quietly, and never by painting over the main line's red inside her own branch.

---

## WHAT IT MEANS

Most wasted repair work is misattributed work: lanes fixing failures they did not cause, or duplicating the same inherited repair across three branches. Classification turns a confusing wall of red into one owned problem with one repair. It also protects trust — a team that names failures honestly can believe its own green.

---

## WHAT'S IN IT FOR YOU

You stop paying for the same failure three times. Problems get fixed once, at the root, by the right owner — and when someone says 'this is broken,' you know exactly what kind of broken it is and what happens next.

---

## HOW IT APPLIES

For every red: reproduce it on the bare base commit; compare the failing set with a sibling branch or earlier head — identical sets mean environment; if the job died almost instantly, re-run that exact job before classifying; label it introduced, inherited, infrastructure, or runner, in writing; then make one repair per failure class, at the source.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0535-base-tip-push-runs-are-the-base-control`
- `IB-SMART-NOTE-20261004-sn0237-failing-set-identity-across-heads`
- `IB-SMART-NOTE-20261004-sn0236-one-repair-per-red-class`
- `IB-SMART-NOTE-20261004-sn0240-pr-introduced-drift-is-correct-red`
- `IB-SMART-NOTE-20261004-sn0320-infra-red-is-not-code-regression`
- `IB-SMART-NOTE-20261004-sn0323-infra-noise-repetition-test`
- `IB-SMART-NOTE-20260930-sn0578-merge-red-ci-converts-red-to-base-defect`
- `IB-SMART-NOTE-20261007-sn0549-a-dead-runner-is-not-a-verdict`
- `IB-SMART-NOTE-20261005-sn0374-diagnosis-integrity-retract-and-no-greenwash`
