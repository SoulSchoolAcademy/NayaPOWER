**Intelligent Block:** IB-SMART-NOTE-20261024-sn1931-calibration-first-act
**Smart Note:** SN-1931
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1506-lane8.md (WHY-NOT audit, Mirror); learning-events-2026-10-24-06.md (LEARNING EVENT)

## ✦ IN A NUTSHELL

An adversarial re-run of a verification instrument's "honest" calibration is the seat's FIRST act, never an inherited label. t1506-lane8 re-ran the t1498 prototype's calibration adversarially before doing anything else — and found 4 real regex misses in the WHY-NOT audit (`why-not-10` phrasing in PRs 2970/2982/2987/3023), proved 0 verdict flips on the corpus, and put them on record as hardening notes, not a calibration break. The misses were honored, not rewritten. Principle: a verification instrument whose calibration you can't reproduce is prose, not machinery — and battery misses that change no verdict are hardening work, not a failure to hide.

## 🩷 HUMAN NOTE

Someone built a measuring tool and wrote a report saying "it's honestly calibrated." The next person was asked to use it. Instead of trusting the report, they rebuilt the test and ran it themselves — first thing, before anything else. They found four real gaps the report missed (the tool's patterns didn't catch four cases). But here's the honest part: they also proved the gaps changed none of the tool's actual verdicts — the misses were things to harden, not a reason to throw the tool away. And they wrote down the misses openly instead of quietly fixing them. The lesson: never inherit "this is honest." Re-prove it yourself, first thing, and treat what you find as work orders, not embarrassment.

## 🟣 CHILD NOTE

Imagine a friend builds a "who's telling the truth" machine and says "it works perfectly, trust me!" Instead of just believing them, you test the machine yourself — FIRST, before anything else. You find four times it got confused, but you also check: it never gave the WRONG answer because of those confusions. So you write down the four confusions as "things to make better" and keep using the machine. The rule: don't believe a machine works just because someone said so. Test it yourself, first thing, and be honest about what you find!

## 🔵 GRANDMA NOTE

Dear, think of a smoke detector. The box says "tested at the factory." Would you hang it up and trust it, or would you press the test button yourself? You'd press the button — first thing, before you depend on it. That's what a lane did with a computer tool: instead of believing the report that said it was honest, they pressed the test button themselves first. They found four small things it missed, checked that none of them caused a wrong alarm, and wrote them down to fix. The lesson: a tool's honesty is something you verify yourself, first — never something you inherit from someone's report.

## 🟠 NAYA NOTE

This extends t0798 (reproduce first, trust never) and CANDIDATE 894 with a worked instance and a timing bar: the adversarial re-run happens as the FIRST act, not the last — t1506-lane8 refused to inherit the report's "honest" label and ran the battery before any other work. Two distinctions that make this a new rule, not a repeat: (1) timing — re-running last means you work on top of an unverified instrument; re-running first means every later act rests on a battery you watched fire; (2) miss semantics — battery misses that flip no verdict are hardening notes recorded openly (4 regex misses, 0 verdict flips, all line-cited), not a calibration break and not something to quietly patch. The preregistered falsifier firing on the seat's own expectation (3 predicted violations, 2 real) was honored rather than rewritten — the battery's verdict beats the seat's narrative. The honest-scope line stands: the battery audits the instrument, it doesn't certify it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1931",
  "title": "Re-run the calibration battery as the first act: an adversarial re-run of 'honest' calibration is the first act, never an inherited label.",
  "applies_when": ["verify", "calibration", "claim", "lane-executor"],
  "enforcement": "Named verification step in the lane-brief preregistration: any brief claiming a verification instrument is 'honestly calibrated' must run its adversarial re-run battery as the seat's first act; the lane-receipt Mirror section records the battery result before any dependent work, and a calibration-claim receipt with no first-act battery is flagged at review. Misses that flip no verdict are recorded as hardening notes with line cites, not silently patched.",
  "decision_change": "Every future 'calibration honest' claim in a brief gets its adversarial re-run as the seat's first act — instruments are trusted only after the seat watches their battery fire on the live corpus.",
  "falsifiability": "Falsified by an adversarial re-run that reproduces the reported calibration exactly (same corpus, same battery, zero misses) — a clean re-run proves the 'honest' label was sound and the doubt was unfounded. The re-run is the falsifier of the doubt.",
  "mechanism": "Verification instruments encode their assumptions in code (regexes, thresholds, windows); reported calibration results are prose until re-executed against the live corpus — drift, stale assumptions, and untested phrasing classes hide inside summaries, and only a battery run against live bytes surfaces them.",
  "evidence": ["twelve-lane-receipts/t1506-lane8.md (WHY-NOT audit: 4 real regex misses in PRs 2970/2982/2987/3023, 0 verdict flips, misses honored not rewritten)", "learning-events-2026-10-24-06.md (LEARNING EVENT)"]
}
```
