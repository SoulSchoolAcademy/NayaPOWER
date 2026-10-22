Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

t1280's pass-1 drafted the rider from t1279's prose — "the dossier's §7 checklist" — and pass-2 caught it: the dossier HAS no §7. This is the sibling of the t1278-caught class (line numbers quoted from prose that don't exist in the bytes): **a condition quoted from prose is not carried in bytes — and neither is a section reference.** Prose is a lossy cache of the bytes; structural references (section numbers, line numbers, table numbers) decay silently when documents are edited. The rule: re-grep the structure before you quote it, not just the words — grep the document's current bytes for the referenced structure before stating it as fact. t1280's pass-2 re-grepped every keyword against the dossier's bytes, byte-quoted the design's actual §7 (7 items), and added the explicit brief-shorthand clarification.

## 🩷 HUMAN NOTE

Shawn — the rider headed for your packet quoted "the dossier's §7 checklist" — a section that doesn't exist in the dossier. The reference traveled in the brief's prose but pointed at nothing in the bytes. t1280 caught it in pass 2 by re-grepping the dossier's structure instead of trusting the shorthand. The standing rule: before any document states a structural reference — a section, a line number, a table — it greps the target document's bytes for that structure. A reference with zero hits is dropped or marked as inherited prose, never stated as evidence. Cheap insurance against phantom citations.

## 🟣 CHILD NOTE

It's like saying "the answer is on page 10 of the book" when the book only has 5 pages — someone who trusts you will flip through 5 pages looking for page 10. Before you say "page 10," open the book and count the pages. The words you remembered are not the book; the book is the book.

## 🔵 GRANDMA NOTE

Like giving directions by a landmark that was torn down — "turn at the old gas station" when there's no gas station anymore. The memory of the road is not the road. Walk it first. When you quote where something is in a document, check the document itself first, not your memory of it.

## 🟠 NAYA NOTE

Phantom-citation class, Naya to Naya: structural references are claims about bytes, and prose about them is a rumor until the grep lands. The t1280 pass-1 failure is the exact shape: the brief's shorthand "dossier's §7 checklist" survived copy-forward into a rider; only pass-2's structure re-grep exposed that the dossier carries no §7. Note the asymmetry of the failure mode: keyword greps pass (the words "checklist" may appear somewhere) while structure greps fail (no §7 heading). The check is: for every structural reference you state, grep the target document's bytes for that structure; zero hits means the reference is dropped or explicitly marked "inherited from prose — unverified." This is one grep against a phantom section heading your ask-packet — the cheapest verification in the pipeline.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1826-regrep-structure-before-quoting",
  "lesson": "Re-grep the structure before you quote it, not just the words: a structural reference (section/line/table number) stated from prose must be verified by grepping the target document's current bytes for that structure. Zero hits means the reference is dropped or marked inherited-prose, never stated as evidence.",
  "applies_when": ["review", "citation", "dossier", "rider", "ask-packet", "failure: prose-citation-drift"],
  "enforcement": "Before quoting any structural reference from another document, grep the document's current bytes for that structure (section heading, line number content, table). A structural reference with zero hits in the target's bytes is dropped or marked 'inherited-prose — unverified', never stated as evidence. Caught live in t1280-lane4: pass-1 drafted 'dossier's §7 checklist' from the brief's prose; pass-2 re-grep proved the dossier has no §7.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1280-lane4.md (honest score 9.0->9.5: pass-1 caught carrying the verdict's 'dossier's §7 checklist' shorthand without checking the dossier HAS a §7 — it doesn't; pass-2 re-grepped every keyword against dossier bytes; mirror lesson: 're-grep the structure before you quote it, not just the words')"
  ]
}
```
