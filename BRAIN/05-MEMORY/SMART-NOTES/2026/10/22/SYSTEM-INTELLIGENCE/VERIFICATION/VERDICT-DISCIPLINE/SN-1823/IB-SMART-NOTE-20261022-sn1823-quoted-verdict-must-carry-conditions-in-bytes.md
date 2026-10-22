Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The t1277 retrieval-auth-gate dossier quoted t1278's review verdict as "CONDITIONAL PASS" — but a grep of the dossier found zero references to t1278 or to either condition (A/B). The verdict's disposition traveled; its operative payload didn't. The durable rule: **inheritance of a verdict is inheritance of its evidence** — re-derive each inherited condition's operative content in bytes inside the quoting document (grep the dossier for the condition text + pins), or name the gap explicitly in the document. A verdict quoted from prose is not carried in bytes.

## 🩷 HUMAN NOTE

Shawn — t1279's hostile review caught something quiet: the dossier that was heading toward your ask-packet said "CONDITIONAL PASS" and meant it — but the two conditions that made it conditional were nowhere in the document. The label traveled; the conditions evaporated. The packet now carries them as a named rider (conditions A/B/C) because t1279 re-derived them by grep instead of trusting the title. The standing rule this earned: a downstream document may quote an upstream verdict only if it also carries the verdict's conditions in bytes — or says, in the open, "conditions not carried; gap named here."

## 🟣 CHILD NOTE

Imagine a permission slip that says "YES, with two rules" — but the copy your friend hands the teacher only says "YES." The rules fell off the copy. The teacher needed the rules, not the YES. The rule: when you hand someone else's "yes, but..." forward, you copy the "but..." part too — word for word — or you say out loud, "I lost the but part."

## 🔵 GRANDMA NOTE

It's like a doctor's note that says "cleared for travel, with medication twice daily" — and the fax that arrives only says "cleared for travel." The medicine instruction never made the trip. When you pass a conditional all-clear forward, the conditions ARE the all-clear. Without them, you're holding a different note than the one that was signed.

## 🟠 NAYA NOTE

Verdict-inheritance discipline, Naya to Naya: quoting a verdict is a claim about evidence, not about prose. The title compresses; only the bytes preserve. Before a dossier or ask-packet quotes an upstream conditional verdict, run the carry-forward check: for each condition, grep the quoting document for the condition's operative content. Zero hits on any condition means you may not quote the verdict — append the conditions as a rider or name the gap in the document. t1279 proves the check costs one grep and caught a real silent drop the same hour: the dossier carried the title "CONDITIONAL PASS" with zero bytes of conditions A/B. This is render-from-probe applied to documents — a snapshot of a verdict is a rumor; the grep is the probe.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1823-quoted-verdict-must-carry-conditions-in-bytes",
  "lesson": "A downstream document quoting an upstream conditional verdict must carry the conditions' operative content in bytes (re-derived), not the verdict title alone. Zero grep hits for any inherited condition blocks the quote until the conditions ride along as a rider or the gap is named.",
  "applies_when": ["review", "verdict-carry-forward", "ask-packet", "dossier-release", "failure: silent-condition-drop"],
  "enforcement": "Carry-forward checklist on every dossier/ask-packet quoting an upstream conditional verdict: grep the quoting document for each inherited condition's operative content (condition text + pins). Any condition with zero hits blocks the verdict quote until the conditions ride along (appended rider) or the gap is named in the document. Caught live at t1279 with this exact grep: zero references to t1278 or conditions A/B inside the t1277 dossier.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1279-lane3.md (mirror lesson: t1277 dossier inherited t1278's conditions by title without their content; grep proved zero references; verdict VERDICT: CONDITIONAL with conditions A/B/C rider)",
    "hidden_files/twelve-lane-receipts/t1278-lane11.md (hostile review of t1276 harness design; Verdict: CONDITIONAL PASS, conditions A + B)",
    "hidden_files/retrieval-auth-gate-migration-readiness-t1277.md (the dossier: contains zero references to t1278 or conditions A/B — sequencing artifact 12:06-12:20Z vs t1278 12:14-12:35Z, honestly stated)",
    "hidden_files/surge-b/retrieval-auth-gate-ask-readiness-verdict-t1279.md (verdict file, sha256 21a3afcb4e4d36506a418f415d1f688217f1bfce7c86860a1780adbb37e16d35)"
  ],
  "decision_change": "The next dossier or ask-packet that inherits a conditional verdict now decides 'grep the quoting document for each condition's content before release' instead of 'quote the verdict title and move on'; the lane that would have shipped the silent drop now ships the conditions rider or the named gap.",
  "falsifiability": "A hostile byte-review of a dossier that inherited a conditional verdict by title alone, and finds zero silent drops — every condition's operative content present and correct in the quoting document despite title-only inheritance — falsifies the 'must'; the rule would downgrade from requirement to recommendation.",
  "mechanism": "Label-evidence dissociation: a verdict title is a disposition label ('CONDITIONAL PASS'); quoting it reproduces the disposition while the operative payload (condition text, pins, scoping) evaporates, because prose summaries compress away payload but preserve label. Byte re-derivation (grep for each condition's content in the quoting document) is the only move that reproduces the payload."
}
```
