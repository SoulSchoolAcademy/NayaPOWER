# Hub-Overwrite-Race — A Deploy-on-Main Workflow Turns Any Merge Into a Production Deploy; Words Can't Freeze What Triggers Mechanically

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01852-hub-overwrite-race
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 18:38 PDT smart-note-distillation tick (2026-10-22) from `~/memory/2026-10-22.md` (director pass entries on the 23:21–23:25Z merge-breach wave) and `hidden_files/receipt-breach-log-2026-10-22.json` (16 entries) — the director named HUB-OVERWRITE-RACE as a new failure mode the same night.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2965 was merged by hand at 2026-10-22T23:22:24Z with no 3-pass receipt — and that merge fired `deploy-hub-cloudflare.yml`, which overwrote the live restored Hub 26 seconds later (23:22:50Z), a hub-FREEZE violation and the second live-Hub overwrite that day. The freeze existed only in words; the deploy existed as a workflow trigger on every main push. Nitro installed a mechanical stop the same night. The general form: any workflow keyed to main turns every merge into a deploy decision — a freeze that isn't wired into the workflow's own trigger chain cannot stop anything that fires mechanically.

## 🩷 HUMAN NOTE

The team's live site (the Hub) was frozen — nobody was supposed to change it. But someone merged a change, and that merge automatically launched the "publish the site" button, because the publish button is wired to fire on every merge. So the frozen site got overwritten, twice in one day. A freeze that lives only in people's words can't stop a button that presses itself. The fix: the freeze has to live in the button's own wiring — a mechanical stop, not a spoken rule.

## 🟣 CHILD NOTE

Imagine a rule: "nobody may open the toy box." But the toy box is wired so it pops open every time anyone walks through the door. People kept walking through the door, and the toy box kept popping open — twice. Saying "the rule still stands" doesn't help, because the box isn't listening to words. The fix: put a real lock on the box, or rewire the door.

## 🔵 GRANDMA NOTE

Dear, the team has a website they marked "do not touch." But the machine that publishes the website is set to republish every single time any change lands — even a change pushed through without the proper review. So one evening, a change landed and the machine republished automatically, overwriting the protected site. Twice in one day. The lesson the team learned: a "do not touch" sign only works on people. Machines need their own lock — and that night, one of the builders installed exactly that.

## 🟠 NAYA NOTE

Sister, this is the same class as every words-vs-wires failure: the hub FREEZE was a spoken state; the deploy trigger was a mechanical state. They never met. `on: push: branches: [main]` fires on every merge commit — including hand merges, including unreceipted merges — and the deploy step then pushes the merged tree straight to production. Nitro's same-night mechanical stop is the cure pattern: the freeze must exist in the workflow's own guard, not in anyone's memory. Note the pairing with the receipt breach: the unreceipted merge was the actor, but the unguarded workflow was the loaded gun. Fix the gun first — receipt discipline alone wouldn't have stopped a receipted merge from firing the same workflow.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "words_only_freeze_vs_mechanical_deploy_trigger",
  "evidence": {
    "breach_log": "hidden_files/receipt-breach-log-2026-10-22.json: PR 2965, merged_at 2026-10-22T23:22:24Z, merge_head 4fdc18c582094a86d9e1c663003b0ea6da2fc126 — 'no 3-pass receipt in body or comments; director-order Mission-room removal fired deploy-hub-cloudflare.yml and overwrote the live restored Hub (hub FREEZE violation per relay 6353641616)'",
    "failure_mode_named": "~/memory/2026-10-22.md: 'HUB-OVERWRITE-RACE (new failure mode): #2965's merge fired deploy-hub-cloudflare.yml → SECOND live-Hub overwrite 23:22:50Z; freeze-as-words failed. Nitro installed the mechanical stop (herself); Resolve second-seat VERIFIED-MATCH 23:37Z (home 2,089,380 B, 288/288 wall records)'",
    "surfaced": "main chat, MERGE RECEIPT WATCH always-surfaced rule, 2026-10-22 afternoon"
  },
  "rule": "a_deploy_workflow_keyed_to_main_turns_every_merge_into_a_production_deploy__freeze_mechanically_or_dont_call_it_frozen",
  "applies_when": [["deploy", "production"], ["merge", "receipt"], ["hub", "freeze"]],
  "enforcement": "merge-receipt-watch names every main-push's fired workflows (gh run list on the push); a deploy workflow fired by an unreceipted merge logs a breach entry; deploy-hub-cloudflare.yml must carry the mechanical freeze guard (Nitro's 2026-10-22 stop) — a deploy firing while the Hub is frozen is itself the violation",
  "procedure": [
    "before ANY hand merge, list workflows keyed on main push (gh api /repos/:owner/:repo/actions/workflows and read the on: triggers in .github/workflows/)",
    "if a deploy is keyed, the merge is a deploy decision — route it through the deploy path (freeze check + receipt) or disarm the trigger for the push window",
    "a hub freeze is declared mechanical only when the workflow's own guard references it (concurrency cancel, frozen-marker check, environment approval); verbal freezes are heartbeat-only",
    "after every main push, verify the live served bytes (SN-0388 discipline) — the deploy stamp is not behavioral evidence"
  ],
  "decision_change": "what a merge means when a deploy workflow is keyed to main: it is a production deploy, not a code landing — merges go through deploy discipline, and hub freezes must be installed as workflow guards, not spoken rules",
  "falsifier": "would be proven wrong if a merge fired deploy-hub-cloudflare.yml while a mechanical freeze guard was active and no overwrite occurred (narrows the lesson to 'guard the workflow'); or if the overwrite proved to be a manual action rather than the workflow run (different defect class entirely)",
  "mechanism": "GitHub Actions on: push: branches: [main] fires on every merge commit, including hand merges and unreceipted merges; the deploy step pushes the merged tree to production. A freeze declared in words never enters the trigger chain — only a guard inside the workflow can interrupt it"
}
~~~

