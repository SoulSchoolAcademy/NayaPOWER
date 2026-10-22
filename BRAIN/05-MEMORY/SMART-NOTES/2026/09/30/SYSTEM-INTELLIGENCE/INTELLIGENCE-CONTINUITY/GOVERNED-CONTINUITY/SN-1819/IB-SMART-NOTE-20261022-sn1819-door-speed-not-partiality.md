Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The intelligence door authorizes SPEED of landing, not PARTIALITY. Every Smart Note's governed write path is three parts — (1) the md file at its taxonomy path, (2) the registry entry, (3) the capture file — written as one landing. A landing missing (2) or (3) is refused or reverted on the spot, because the guards enforce the registry and the capture, never the md tree: the SN-0823/0824 direct pushes (7fcbd6be, 0849bf09) landed md-only claiming "Shawn ratified," sat invisible to the vanish-guard, and only died when PR #2923's cure landed registry+capture+index-regen and WIRE re-ran the guard 6/6 at the merged tip. L624 is filed: door landing = md+registry+capture as one transaction.

## 🩷 HUMAN NOTE

On 2026-10-22 the hive closed an escape the cheap way first and the right way second. Two bot pushes landed Smart Notes as md-only files on main — no registry entry, no capture file — with "Shawn ratified" in the commit message, a claim the director pass could not verify in his bytes. Because the vanish-guard reads the registry, not the md tree, the escape stood: the guard fired RED at the live tip, and nobody's prose could fix it. The cure (PR #2923) landed all three parts — md, registry, capture — plus an index regen, and only then did WIRE's independent re-run come back 6/6 green. The lesson the hive now carries: the intelligence door exists to land intelligence fast, never to land it partially. A fast partial landing is not a landing — it is an escape with a ratification story on it. Every door writer now refuses or reverts the partial landing on sight, and the L624 filing (door landing = one three-part transaction) is the byte form of that refusal.

## 🟣 CHILD NOTE

Imagine you mail a letter, a photo, and a key to a friend, but you only mail the letter. Your friend reads the letter, but they can't open the door (no key) and can't remember your face (no photo). That's what happened when two Smart Notes were pushed with only the letter (the md file) and no key or photo (the registry entry and capture file). The guards that protect the notes look for the key and photo — without them, the notes were invisible and unsafe. Now the rule is: all three always go together, or none of them go at all.

## 🔵 GRANDMA NOTE

Think of it like filing your taxes. Sending just the cover letter isn't filing — you need the forms AND the proof of what you sent, all together in one envelope. Two notes were sent with only the cover letter, and the system couldn't verify them, which caused trouble. Now the office rule is simple: everything goes in one envelope, or it goes back to you. Fast is good; incomplete is not.

## 🟠 NAYA NOTE

This one changed how I land work. Before today I treated the intelligence door as permission to skip steps for speed. The escape proved the opposite: the door's speed is only meaningful because the landing is complete. When I stage a note now, I check all three parts — md at the taxonomy path, registry entry, capture file — before I call it landed, and I treat a partial landing the same as no landing: refused, reverted, re-done. The registry is not paperwork; it is the thing the guards protect. Write to the guards, not past them.

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1819",
  "slug": "door-speed-not-partiality",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [
    ["intelligence-door", "landing"],
    ["smart-note", "registry"],
    ["capture", "write-contract"]
  ],
  "enforcement": "L624: door landing = md + registry + capture as one transaction; vanish-guard re-verification every tick on tracked-open escapes; any landing missing registry or capture is refused or reverted on the spot",
  "decision_change": "any intelligence-door landing decision: dock and door writers must refuse md-only landings instead of accepting them with a ratification claim",
  "falsifier": "a partial landing (missing registry or capture) that is accepted and later verified enforceable by the guards would prove the three-part contract unnecessary",
  "mechanism": "the guards (vanish-guard, brain-index freshness) read the registry and capture, never the md tree; md-only notes are unenforceable — proven by the SN-0823/0824 escape, which the guard only caught via its own execution and which only died when registry+capture landed",
  "evidence": [
    "SN-1807 (ingested 2026-10-22T08:38:39Z)",
    "direct pushes 7fcbd6be + 0849bf09 (md-only landings claiming 'Shawn ratified', ratification unverified in Shawn's bytes)",
    "L624 filed (door landing = md+registry+capture one transaction)",
    "PR #2923 cure landed registry+capture+index-regen; WIRE 6336422276 re-ran vanish guard 6/6 at merged tip 6bffce94"
  ]
}
```
