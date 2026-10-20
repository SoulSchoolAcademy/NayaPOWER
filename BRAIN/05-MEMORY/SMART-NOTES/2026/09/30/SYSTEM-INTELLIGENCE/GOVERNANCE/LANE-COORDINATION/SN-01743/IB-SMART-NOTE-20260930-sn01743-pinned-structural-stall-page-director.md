# A Pinned Structural Stall Is Not Four Stalls: When the Barred-Share Pins at 100% for 3+ Ticks, Page the Director — Don't Burn Another Receipt

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01743-pinned-structural-stall-page-director
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Four consecutive lane-executor ticks (17:42 → 18:44 → 19:47 → 20:58 UTC, 2026-10-20) each burned a stall receipt on the byte-identical verdict: the same 30 queued briefs, the same A:10/B:20 exit-code classification, zero claims, barred-share pinned at 100% (10 explicit non-Clarity CLAIMABILITY GATEs + 20 script-refused exit-7 second-seat demands on Clarity-authored parents). Each receipt's own mirror lesson named the same missing machinery: a queue-composition monitor that, when the next executor seat's barred-share pins at 100% for 3+ consecutive ticks, pages the director with the backlog composition instead of emitting another stall receipt. A stall this structural is not operational — its signal is the composition itself, and the only actor who can change the composition is the dispatcher/director, not the ticking executor. The rule: hash the verdict-relevant bytes (sorted queued filename list + per-file claim exit-code classification) before writing a stall receipt; if the hash matches the last three stall-receipt verdict hashes and the barred-share is 100%, write one director page, not a receipt; receipts resume only when the verdict hash changes.

## 🩷 HUMAN NOTE

Shawn — imagine a security guard who clocks in, finds the same locked door, and writes the same incident report every hour for four hours. After the first report, the next three add nothing — the fix isn't a fifth report, it's telling the building manager the door is still locked and asking who can unlock it. Same here: the seat-stall receipts keep saying "nothing claimable" over the same 30 files. The fix: after three identical reports, stop writing reports and send one note to the person who can actually unlock the queue.

## 🟣 CHILD NOTE

A kid's lemonade stand: nobody can buy because every cup costs a coin the kid doesn't have. The kid writes "no sales today" in the notebook — four days in a row, the same sentence. The notebook isn't the business plan; the missing coin is. The smart move: on day three, hand the notebook to a grown-up and ask which coin problem to fix first. Writing day four's sentence first is just a habit.

## 🔵 GRANDMA NOTE

Like checking the mailbox every day for a letter that was never sent, and writing "no letter" in the diary each time. The diary entry doesn't change anything. After three "no letter" entries, the sensible thing is to call the sender and ask whether they mailed it — then only write again when something actually arrives or changes.

## 🟠 NAYA NOTE

Apply to the lane-executor and the dispatcher: (1) a stall is STRUCTURAL when 100% of queued briefs demand a seat the executing seat cannot supply (stamped CLAIMABILITY GATEs, second-seat demands, authorship bars) — its signal is the queue composition, not the tick; (2) before writing any seat-stall receipt, hash the verdict-relevant bytes (sorted `queued` filename list + per-file claim exit-code classification); (3) if the verdict hash equals the last three stall-receipt verdict hashes AND the barred-share is 100%, do not write another receipt — append one director page (`seat-stall-PINNED-<ts>.md`: composition, pinned-tick count, the two demand classes) to the learning-events log instead; (4) receipts resume the moment the verdict hash changes (arrival, claim, eligibility lift); (5) this is the dispatcher-side sibling of SN-1672 (third consecutive stall on an ownerless finding → escalate, do not file) — where SN-1672 escalates a FINDING to an OWNER, this escalates a COMPOSITION to the DIRECTOR; SN-1673's failure mode (escalation named an absent owner) is why the escalation target is the director, whose presence the loop guarantees.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "pinned-structural-stall-page-director",
  "sn": "SN-1743",
  "title": "A Pinned Structural Stall Is Not Four Stalls: When the Barred-Share Pins at 100% for 3+ Ticks, Page the Director — Don't Burn Another Receipt",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-20",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["lane-executor", "stall-receipt", "dispatcher", "queue-composition", "eligibility", "seat-barred"],
  "enforcement": "Before writing any seat-stall receipt, the executor hashes the verdict-relevant bytes (sorted queued filename list + per-file claim exit-code classification). If the verdict hash matches the last three stall-receipt verdict hashes AND the barred-share is 100%, no receipt is written; instead one seat-stall-PINNED-<ts>.md director page (backlog composition + pinned-tick count + the two demand classes) is appended to the learning-events log. Receipt-writing resumes only when the verdict hash changes. A stall-receipt series with more than three identical verdicts is a tripwire violation: the monitor never fired.",
  "evidence": {
    "seat-stall-2058": "hidden_files/twelve-lane-receipts/seat-stall-20261020-2058.md (2026-10-20 20:58 UTC): fourth consecutive tick on the byte-identical verdict (same 30 filenames, A:10/B:20 classification, zero claims, barred-share 100%); closing paragraph names the missing loop verbatim — 'the missing loop is a queue-composition monitor — if the barred-share for the next executor seat pins at 100% for 3+ consecutive ticks, the dispatcher should page the director with the backlog composition instead of emitting another receipt'",
    "seat-stall-1844": "hidden_files/twelve-lane-receipts/seat-stall-20261020-1844.md (18:44 UTC): the same verdict; closing paragraph — 'When 100% of a queue's briefs demand a seat the executor cannot supply, the executor's stall is structural, not operational — the signal to route upward is the queue composition itself, not repeated stall receipts'",
    "learning-events": "hidden_files/learning-events-2026-10-20-19.md and learning-events-2026-10-20-20.md: four consecutive pinned verdicts (17:42 → 18:44 → 19:47 → 20:58 UTC) recorded with the recommendation explicitly marked 'unadopted recommendation, not a principle — joins the unadopted queue'"
  },
  "decision_changed": "How an executor tick and the dispatcher respond to a 100%-barred stall: instead of burning one receipt per tick on an unchanged verdict, the seat stops emitting after three identical verdicts and the dispatcher pages the director once with the backlog composition. Deploys/operates against: lane-executor stall-receipt writing, dispatcher queue-composition monitoring, the learning-events log (PINNED pages), ingestion-loop noise.",
  "falsifier": "A seat-stall-PINNED page that fires while the verdict bytes differ across ticks (queue composition changed, barred-share dropped below 100%, or a claim succeeded) — a false positive proving the pin detector is wrong. Or: 3+ pinned 100%-barred ticks pass with zero pages and N more identical receipts burned — the tripwire never fired, proving the machinery was never adopted.",
  "mechanism": "A stall receipt whose verdict is identical to the prior receipt's (same queued filenames, same exit-code classification, same zero claims) carries zero information — receipts are the lane's scarce signal channel (ledger bytes, ingestion-loop attention), and zero-entropy messages are noise. The stall is structural: the fixable variable is queue composition (which briefs are barred to which seats), and the only actor that can change it is the dispatcher/director, never the ticking executor. So the correct tick output at pin+3 is not a fourth identical message into the channel — it is one escalation to the actor holding the fixable variable, with the channel re-armed (receipts resume) exactly when the verdict hash changes. That is also why SN-1673's failure mode (escalation named an absent owner) does not apply here: the director's presence is guaranteed by the loop itself.",
  "cousins": ["SN-1672 (third consecutive stall on an ownerless finding → escalate, do not file — the finding-side sibling)", "SN-1673 (SN-1672's escalation named an absent owner — why this escalates to the director instead)", "SN-1737 / CANDIDATE 728 (3+ identical unprocessed alerts → one adjudication, not N more alerts — the watcher-side sibling)"]
}
~~~
