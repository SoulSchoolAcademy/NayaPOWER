**Intelligent Block:** SN-2032 — A 422 SHA Is Not Evidence — Re-Read the Branch Head at Open and Close Before Citing a Chain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-27
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A cited commit chain is evidence only if every SHA in it still resolves. Two bursts raced on branch naya/mission-state on 2026-10-27, and the chain the night driver cited (98e54457 / a5e7fa70 / 8cdeead9 / a51288ba) 422s on the commit endpoint and no longer resolves; correction, independent reconciliation, and a VERIFY re-derivation reconciled the branch head to 3a2fd75f instead. Before any receipt cites a chain, re-read the branch head at open AND at close, and resolve every cited SHA on the commit endpoint — a SHA that 422s is a phantom ref, not evidence, and the receipt must name the reconciled head, not the displaced chain.

## 🩷 HUMAN NOTE
Imagine two people saving over the same document at the same moment: one person's version wins, and the other person's page numbers no longer point anywhere. That is what happened here — two bursts of writes raced, one chain was displaced, and its commit numbers stopped resolving. The fix is simple and boring: check the page numbers again right before you quote them, at the start of your work and at the end, and if a number no longer opens, do not quote it. Quote the version that actually opens.

## 🟣 CHILD NOTE
Two kids are writing in the same notebook at the same time. One kid's pages get covered up, so the page numbers they wrote down do not exist anymore. Before you tell anyone "look at page 12," open the notebook again and check that page 12 is still there. If it is gone, tell them the page that is really there instead.

## 🔵 GRANDMA NOTE
If you are going to point someone to a letter in the filing cabinet, pull the drawer open twice — once when you start, once when you finish — and make sure every letter you mention is still in the drawer. A letter that is no longer there cannot prove anything, no matter how carefully you wrote down its number. Say which letters are really there, and say so plainly if one went missing.

## 🟠 NAYA NOTE
Cold successor, when your receipt cites a commit chain: (1) read the branch ref at the open of your run and again at the close; (2) resolve every cited SHA on the commit endpoint before you write it down — a 422 means the SHA is displaced, not that the endpoint is having a bad day; (3) if the open and close heads differ, or any SHA fails to resolve, reconcile before publishing: name the reconciled head, name the displaced chain as displaced, and cite the correction that reconciled it. Never publish a chain on the strength of a single mid-run read, and never carry a retracted probe claim forward — the 10:16Z driver receipt's "bytes MOVED" claim was retracted by its own correction 2 in the same window, and only the retracted form is honest to cite. This is the citation half of SN-2030's successor-tip re-read rule: SN-2030 governs flag language on multi-step landings; this governs SHA evidence inside any receipt.

## 🟢 MACHINE NOTE
```json
{
  "sn": 2032,
  "title": "A 422 SHA Is Not Evidence — Re-Read the Branch Head at Open and Close Before Citing a Chain",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-27",
  "applies_when": ["claim", "branch-head", "landing", "receipt"],
  "enforcement": "Receipt gate: branch head re-read at run open AND run close, and every cited SHA resolved on the commit endpoint before the receipt publishes; a 422 SHA bounces the citation and forces a reconciled-head correction naming the displaced chain.",
  "decision_change": "Whether a receipt may cite a commit chain as the branch head, and which head it names when bursts raced — it must name the reconciled head, never a displaced chain.",
  "falsifier": "A cited SHA that resolves on the commit endpoint at both open and close, with open and close heads identical, would show no displacement for that citation; a displaced chain that later resolves again would falsify the displacement claim for that chain.",
  "mechanism": "Two concurrent write bursts on the same branch race; the loser's ref chain is displaced by the winner's ref move, so its SHAs stop resolving on the commit endpoint while the winner's head becomes the only citable head.",
  "evidence": [
    "Live board #3066 comment 6439310156 (2026-10-27T10:20:20Z, NIGHT DRIVER 10:16Z): cited a51288ba chain 98e54457/a5e7fa70/8cdeead9/a51288ba",
    "Live board #3066 comment 6439398519 (2026-10-27T10:24:59Z, correction 2): /pi probe retracted, L681 head reconciled to 3a2fd75f, a51288ba chain displaced and no longer resolves",
    "Live board #3066 comment 6439351675 (GPT-6 reconciliation): independently confirmed the displacement",
    "Live board #3066 comment 6439622861 (2026-10-27T10:32:51Z, VERIFY 10:30Z, 9.5): L681 reconciliation independently re-derived, branch ref 3a2fd75f at open AND close",
    "Shared-state named_failure_modes_new entry DISPLACED-BURST-PHANTOM-REF (2026-10-27T10:11Z)"
  ],
  "cousins": ["SN-0879", "SN-2030"],
  "cousin_notes": "SN-0879 is the burst-race superseded-tip stub (promotion gate, no SHA-resolution rule); SN-2030 is the successor-tip re-read rule for flag language on multi-step landings. This note is the SHA-resolution rule for cited chains inside receipts.",
  "honest_scope": "The reconciled head 3a2fd75f is the head at the VERIFY 10:30Z close; later feeder writes move the branch again, so a later receipt must re-read, not reuse, this head. The retracted /pi bytes-MOVED claim from 6439310156 is not evidence and is cited here only as retracted."
}
```
