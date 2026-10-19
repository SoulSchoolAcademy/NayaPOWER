# INTELLIGENT BLOCK — SN-1671

**Intelligent Block:** IB-SMART-NOTE
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A keyword-matching authorship guard (claim-brief.py exit 7) fired on two phrases during a lane-executor stall receipt: "the non-author review gate is a different seat's job" and "the 10 exit-7 second-seat bar mappings are not byte-visible." The first was constraint-language about a FUTURE review step, not a demand of the repair in progress. The second was the visibility-fix brief's own SUBJECT — the guard read the task's own subject matter as a violation and recursively stalled the repair of its own documentation. A keyword guard reads three different speech acts the same: a demand of this execution, a constraint on a future step, and the subject of the task. Ship every guard rule with a dry-fire control set from the live population, and make it distinguish the three scopes before it may fire.

## 🩷 HUMAN NOTE

An automated safety checker refused a work order because it found certain words in it. The problem: the words appeared in two completely different ways — once describing what someone else must do later, once describing what the work itself was about. The checker couldn't tell the difference between "do this now," "someone must do this later," and "this is what we're fixing." So it blocked the repair of its own instruction manual, twice. Before any word-matching checker goes live, run it over real work orders first, count the mistakes, and teach it the difference between an order, a future rule, and the topic itself.

## 🟣 CHILD NOTE

Imagine a hall monitor with a list of banned words. A kid writing a report about why the banned words are banned gets sent to detention — because the monitor matched the words, not the meaning. And a kid saying "tomorrow the rule about banned words changes" also gets detention — the monitor heard the words and stopped listening. The monitor needs to learn three questions before blowing the whistle: "Is this an order right now?", "Is this about a future rule?", or "Is this just what we're talking about?" Test the whistle on real homework first.

## 🔵 GRANDMA NOTE

The smoke alarm went off twice: once because the neighbors were talking about buying a fire extinguisher next week, and once because someone was reading the alarm's own instruction manual out loud. A good alarm must know the difference between a fire now, a fire rule for later, and a conversation about the alarm itself. Otherwise it evacuates the house every time you read its manual. Test every alarm on a normal week of kitchen sounds before you screw it to the ceiling.

## 🟠 NAYA NOTE

For lanes building or repairing keyword/regex guards on claim machinery: the authorship regex in claim-brief.py now fires on three semantic scopes it cannot distinguish. The F3/F4 repair in the 07:16Z stall receipt hit two of them: future-step constraint language ("the non-author review gate is a different seat's job" — a constraint on a review step that doesn't exist yet) and subject matter ("the 10 exit-7 second-seat bar mappings are not byte-visible" — the visibility-fix brief's own topic). The seat correctly refused to patch mid-run — loosening shared machinery could unbar genuine second-seat work — and flagged it for the script owner. The owed repair is specific: task-demand vs constraint-language vs subject-matter parsing (hyphen-stemmed tokens and prose-union parsing, per the t0846 authorship lesson) plus a dry-fire control set drawn from the live brief population before any rule ships. Same-scope family: CANDIDATE 157 (violations defined from mechanism convenience ship false positives) and CANDIDATE 581 (compound-token bar matching). Filing-side twin still open: file-gap-brief.py has no authorship awareness (dispatcher-owned, per t0846 mirror) — re-check any scope-aware repair against both entry points.

## 🟢 MACHINE NOTE

```json
{
  "slug": "keyword-guard-scope-awareness",
  "sn": "SN-1671",
  "title": "Keyword Guards Need Scope-Awareness: Distinguish the Demand of This Execution from a Constraint on a Future Step from the Subject of the Task",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["guard", "keyword-guard", "regex-guard", "claim-brief.py", "authorship-guard", "false-positive", "scope-awareness", "claim-machinery", "lane-executor"],
  "enforcement": "Every guard rule ships with a dry-fire control set drawn from the live population before activation, with demand-vs-constraint-vs-subject hits classified and counted; a rule that fires on constraint-language or subject-matter alone is bounced as a scope false positive. The claim-brief.py script owner owes the task-demand vs constraint-language vs subject-matter distinction (flagged in gate-stall-20261019-0715.md, captured as CANDIDATE 660). The filing-side twin (file-gap-brief.py authorship unawareness, dispatcher-owned) must be re-checked when the repair lands.",
  "evidence": {
    "gate_stall_receipt": "twelve-lane-receipts/gate-stall-20261019-0715.md (2026-10-19 07:16Z) — correct stall, 0/29 claimable; authorship regex fired on constraint-language of a future review step and on the visibility-fix brief's own subject, recursively stalling its own repair; seat flagged for script owner, no mid-run patch",
    "learning_hour": "hidden_files/learning-events-2026-10-19-07.md (06:20-07:20Z window) — NEW PRINCIPLE CANDIDATE 660: keyword guards need scope-awareness; cousins CANDIDATE 157 and CANDIDATE 581; appended to CORE-PRINCIPLES.md (Shawn ratifies)"
  },
  "decision_changed": "How a keyword/regex guard is allowed to ship: it must parse task-demand vs constraint-language vs subject-matter, and every future guard rule ships with a dry-fire control set from the live population. A guard that reads its own subject matter as a demand stalls the repair of its own documentation.",
  "falsifier": "A keyword guard with no scope parsing runs 20+ real executions with zero false positives on the live population (the distinction buys nothing), or the repaired authorship regex's dry-fire control set shows demand-vs-constraint-vs-subject classification does not change the fire set.",
  "mechanism": "Keyword matching conflates three speech acts: imperative demand of this execution, constraint language about a future step, and descriptive subject matter of the task. Without scope parsing, the guard self-references — it reads its own documentation as a violation and recursively stalls its own repair. Hyphen-stemmed tokens and prose-union parsing (per the t0846 authorship lesson) give the parser the vocabulary to separate the scopes; the dry-fire control set from the live population calibrates it."
}
```
