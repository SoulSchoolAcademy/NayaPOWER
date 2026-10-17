# Verify the Seam, Not the Cited Instances

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01559-verify-the-seam-not-the-cited-instances
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-17 08:46–09:25 PDT (15:46–16:25 UTC) Lane 11 receipt `twelve-lane-receipts/t0672-lane11.md` (Naya Clarity Narzan, retrieval-auth-gate migration packet review — wordable-form packet headed to Shawn's word with the caller's §3 verdict incomplete).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A migration packet headed to Shawn's word claimed a "complete caller list" for the wiring-day test surface — and missed 9 unlisted call sites, including the whole drill bank. The packet's error was mechanical: it grepped the test file it already knew instead of sweeping the seam across the tree. A repo-wide seam sweep (`git grep` on the seam name across the entire tree, every hit classified as call / string / different-seam) found the drill-bank four that no cited-instance check could ever find. The root cause is structural, not personal: authors cite what they touched — their diff, their packet's listed lines. Completeness is not a property of the cited instances; it is a property of the tree. Any review that accepts a "complete list" on the strength of the packet's cited instances is verifying the author's memory, not the artifact. The discipline: for any completeness claim, sweep the seam name across the tree first, classify every hit, and put the classification table in the verdict table. The drill-bank four went to his word as unknown; catching them before his attention was spent was the highest-value move the brief allowed. It worked because the sweep came first, not because the packet was mistrusted.

## 🩷 HUMAN NOTE

Imagine an electrician hands you a map of every outlet on a circuit, and you approve the renovation based on his map. Then the walls come down and there are four outlets he never drew — because he mapped the outlets he remembered touching, not the wires in the walls. This morning a seat caught exactly that: a migration packet claimed its caller list was complete, but the reviewer ran the electrical trace across the whole building (every use of the seam's name, everywhere in the code) and found nine connections the packet's map never showed — including four in a test bank that would have broken on wiring day. The packet wasn't lying; it grepped the test file it already knew. The lesson is that "complete" is a property of the building, not of the map. The check isn't to mistrust the electrician — it's to walk the wires yourself, every time, before you approve.

## 🟣 CHILD NOTE

Your friend makes a list of everyone she invited to her party and says "that's everybody." If you only check her list, you'll always agree with her — because her list only has the people she remembered. The smart way: search the whole school for anyone who might think they're invited, and check each name one by one. This morning a checker did the code version of that: instead of trusting the packet's list of "everywhere this thing is used," she searched the entire codebase for the thing's name and looked at every single hit. She found nine the packet had missed — four of them in a test bank that would have broken on the big day. Trust the list, but search the school.

## 🔵 GRANDMA NOTE

Dear, this one is about the difference between a map and the territory, and it will keep you honest for years. When someone hands you a claim that a list is complete — every caller, every call site, every place a thing is wired — the natural instinct is to check their list. Resist it. Their list contains what they touched, what they remember, what they already knew. What they forgot lives outside their list, and no amount of re-reading their list will find it. The discipline is: take the seam's name — the function, the gate, the thing — and search the whole tree for it. Every hit gets classified: is it a real call, a string that only mentions it, a different seam with a similar name? That classification table goes in your verdict, in writing. This morning that table found nine callers a packet's author had never seen, four of them in a test bank that would have failed silently on wiring day. The packet was headed to Shawn's desk. It did not go there incomplete, because the checker swept the tree instead of trusting the map.

## 🟠 NAYA NOTE

Apply on every "complete list" claim, forever: (1) the claim is completeness of the TREE, so the check runs on the tree — `git grep` (or the repo's equivalent) on the seam name across the entire codebase, not the files the packet cites; (2) every hit is classified into three buckets — real call site, string/reference only, different seam with a similar name — and the classification table is written into the verdict table, verbatim, before any verdict is issued; (3) the cited-instances check may follow, but it never substitutes: a verdict that rests on cited instances alone is filed as unverified; (4) when the sweep finds hits the packet missed, the packet goes back to the author with the named gaps and owners — it does not proceed to Shawn's word with the gaps attached as footnotes; (5) the receipt names the sweep command, the hit count, and the classification counts — "sweep: 47 hits, 31 calls, 12 strings, 4 different-seam" — so a cold successor can re-run it byte-for-byte. Cousin map: per-leaf-verification (verify the leaf bytes, not the directory — this is the CALLER-LIST twin); SN-1558 (pre-register the spot-check spread — different: that is about selection bias inside a known set, this is about discovering the set itself); the live-bytes principle (parent — prose never outranks bytes).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1559,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "verify_the_seam_not_the_cited_instances",
  "applies_when": [["review","completeness"],["wiring","migration"],["call-sites","callers"]],
  "enforcement": "Any review verdict on a 'complete list' claim is bounced unless its verdict table carries the tree-wide seam sweep: git grep on the seam name across the whole tree, every hit classified as call / string / different-seam, with the classification table in the receipt. A cited-instances-only check is filed as UNVERIFIED, never as verification — the gap claimability gate and the distillation filing gate both bounce it (BOUNCED <slug>: missing seam-sweep classification table).",
  "evidence": {
    "the_receipt": "twelve-lane-receipts/t0672-lane11.md, 2026-10-17 08:46-09:25 PDT (Naya Clarity Narzan, Lane 11; retrieval-auth-gate migration packet wordable-form review)",
    "the_packet": "headed to Shawn's word with §3 (wordable form) judged INCOMPLETE: §1 undercount named, 9 unlisted call sites found, G1 vocabulary call on 14 `..._BY_HUMAN_DIRECTOR_REQUEST` entries unnamed (Shawn's disclosure-policy decision per spec §7)",
    "the_sweep": "repo-wide seam sweep on the seam name found the 9 unlisted call sites including the drill-bank four; the packet had grepped only the test file it already knew",
    "the_root_cause": "authors cite what they touched (their diff, the packet's listed lines); completeness is a property of the tree, not of the cited instances",
    "the_routing": "packet routed back to the wordable surface with G1 + G2 as pre-word corrections; §1 amendment to the author seat, G1 to Shawn's §7 decision — never sent to him with the gaps unamed"
  },
  "procedure": [
    "name the seam: the function, gate, or hook the completeness claim is about",
    "sweep the tree: git grep on the seam name across the entire codebase — not the packet's cited files",
    "classify every hit: real call site / string-or-reference-only / different seam with a similar name",
    "write the classification table into the verdict table before issuing any verdict",
    "misses route the packet back to the author with named gaps and owners — never forward incomplete to Shawn's word",
    "the receipt records the sweep command, hit count, and classification counts for cold re-runs"
  ],
  "falsifier": "if tree-wide sweeps repeatedly return exactly the cited set across N reviews AND the missed-call-site rate falls to zero on cited-only checks, the extra sweep adds no value and this note is withdrawn",
  "decision_changed": "whether a packet claiming a complete caller/call-site list is accepted for forwarding to Shawn's word — and specifically whether the retrieval-auth-gate migration packet went to him complete or missing 9 call sites"
}
~~~
