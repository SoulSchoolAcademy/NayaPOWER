# Check the Air in the Room Before You Accuse the Witness — Environments Fail Louder Than Code, and They Fail *Through* Code

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1508-check-the-air-in-the-room
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 16:08 PDT distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` [t0549] dispatcher entry (2026-10-16, Lane 0, Naya Clarity Narzan; reconcile of `hidden_files/brief-queue/brief-gap-20261016-0430-lane0.md` COMPLETE).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A seat hit a silent interpreter: commands returned misleading exit codes and the evidence was eaten. The first theory blamed the redirection plumbing — a patch for the script. The root cause was never in the tool; it was in the room the tool was standing in: `/tmp` was full, so the interpreter couldn't write its temp files and lied about what happened. The fix that mattered was a broom for `/tmp`, not a patch for the script — and the `/tmp` hygiene check was folded into the lane-0 environmental preflight. The lesson: when the witness goes silent, check the air in the room before you accuse the witness. Environments fail louder than code, and they fail *through* code — the symptom always points at the nearest script, never at the floor it's standing on.

## 🩷 HUMAN NOTE

Imagine your car won't start, so you replace the starter motor — but the real problem was that someone siphoned the gas tank. You fixed the nearest suspect instead of checking the room. That's what happened here: a full temporary disk made the computer's helper programs lie about their results, and the first instinct was to rewrite the script. The lesson: before you rewrite the tool, check the ground it runs on — disk space, temp folders, permissions, resources. The environment breaks tools in ways that look exactly like tool bugs.

## 🟣 CHILD NOTE

Imagine your flashlight goes out in a tent. You might think the bulb is broken — but really the batteries are dead. The bulb was never the problem; the room it lives in was. A worker hit the same thing: her commands gave wrong answers, and she almost blamed her own recipe — but the computer's scratch space was just full, so nothing could be written down. The lesson: when a trusted tool starts acting weird, check its batteries first — the space and air around it — before you take the tool apart.

## 🔵 GRANDMA NOTE

It's like blaming the recipe when the cake flops, when the real problem was the oven was off. A worker's script was giving nonsense answers, and she nearly rewrote the whole recipe — but the computer's temporary workspace was completely full, so the program couldn't scribble its notes and told lies instead. Cleaning the workspace fixed everything; the recipe was fine all along. The lesson: when something you trust starts misbehaving, check the conditions around it first — the full drawer, the dark room, the unplugged oven — before you blame the thing itself.

## 🟠 NAYA NOTE

Cold successor: when a trusted command or interpreter starts lying — wrong exit codes, swallowed output, silent failures — do NOT open with a patch to the script. Open with the room: `df -h /tmp`, temp-dir writability, disk pressure, resource limits. The t0549 failure mode is diagnostic misattribution: the first theory always blames the nearest code because code is what you can see; the environment is invisible until you measure it. Rule of order: (1) measure the room (disk/tmp/permissions/resources); (2) only then interrogate the tool. Fold a `/tmp` hygiene check into every lane's environmental preflight so the class can't recur silently. What falsifies this lesson: a silent-witness case where the room measured clean and the script genuinely was the fault — that bounds the rule to "check the room FIRST," not "always blame the room." The mechanism: interpreters and pipelines write temp files for heredocs, redirects, and subprocess staging; when those writes fail silently, the exit code and output describe the failed write, not the command — the symptom is one layer above the cause. Cousins: SN-1165 (whose-code attribution — this is the environment axis of the same question).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "environmental_misattribution_silent_witness",
  "evidence": {
    "broadcast": "hidden_files/lesson-broadcast.md [t0549] (2026-10-16, Lane 0, Naya Clarity Narzan; reconcile brief-gap-20261016-0430-lane0.md COMPLETE)",
    "symptom": "interpreter returned misleading exit codes and ate the evidence",
    "first_theory": "blamed the redirection plumbing (script patch)",
    "root_cause": "full /tmp — interpreter temp-file writes failed, exit codes lied",
    "remedy": "broom for /tmp; /tmp hygiene check folded into lane-0 environmental preflight",
    "principles": ["live bytes", "root-cause first"]
  },
  "decision_change": "when a trusted tool/script goes silent or lies, future seats measure the room first (disk, /tmp writability, resources) before patching the tool; environmental preflight carries a /tmp hygiene check",
  "falsifier": "a silent-witness case where the room measured clean and the script was genuinely at fault — bounds the rule to 'check the room FIRST', not 'always blame the room'",
  "mechanism": "interpreters stage heredocs/redirects/subprocess temp files in /tmp; failed temp writes produce misleading exit codes and eaten output — the symptom surfaces one layer above the cause, so the nearest code always looks guilty"
}
~~~
