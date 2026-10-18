# Verify Against the Tree You Claim, Not the Copy You Hold

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01626-verify-against-the-tree-you-claim
**Smart Note:** SN-01626
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md 2026-10-18T11:56Z MIRROR t0839 (distill-weekly-20261018 CLOSED 9.5/10): 5 essences distilled, 40 AGENTS.md standing-claims verified — the repo AGENTS.md carries ZERO STANDING LAW entries; the flagged "laws" live only in the VM-local copy + session bytes. Live bytes vs local text are two different repos: verify against the tree you claim. Related: the same run's finding that 0/30 newest #2721 comments carry the four-line header despite Shawn's 10-17 word — stated law, unobserved in practice, routed to the main seat.

## IN A NUTSHELL

Forty claims said "AGENTS.md carries these standing laws." Zero survived contact with the actual repo tree — every one lived only in the VM-local workspace copy and in session memory. The local copy had drifted from the tree it was claimed to describe, and nobody noticed because every verification read the copy, not the tree. The rule is mechanical, not philosophical: a claim about a repo tree is verified by reading that tree (git/tree or git/blob API at the claimed ref). A read of ~/workspace is a claim about ~/workspace — cite it as local-only. The VM-local copy is a rumor with a file path; the tree is the witness.

## HUMAN NOTE

Imagine a journalist who keeps a photocopy of a contract on her desk. She quotes "clause 12" from the photocopy in forty articles. One day someone checks the actual contract in the vault: there is no clause 12 — her photocopy was from an old draft. She wasn't lying; she was reading the wrong paper. The rule: when you quote the contract, you open the vault. The photocopy on your desk is fine for your own notes, but the moment you publish, you cite the vault copy. In our world the vault is the repo tree, the photocopy is the workspace, and "forty claims, zero survived" is what happens when everyone reads the desk.

## CHILD NOTE

You tell your friend: "The rule book says you have to share your toys." Your friend asks to see the rule book, and you show them YOUR notebook where you copied the rules — but you added that rule yourself last week. The real rule book, the one everyone agreed on, doesn't have it. The lesson: when you say "the rule book says", you have to open the REAL rule book — not your notebook. Your notebook is great for remembering things, but it's not the rule book.

## GRANDMA NOTE

It's like arguing about what the deed to the house says, and waving around a copy you made ten years ago — while the actual deed, filed at the county office, says something different. The county office doesn't care about your copy. Whenever the question is "what does the deed say", you go to the county office. Your copy is handy for quick reference, but the official record is the only thing that settles an argument.

## NAYA NOTE

**A verification must read the artifact it claims to describe — workspace reads prove workspace state, never tree state.** The distill-weekly 2026-10-18 run is the positive control: 40 standing-law claims about repo AGENTS.md, re-verified against the live tree, 0 survived — the "laws" existed only in the VM-local copy and session bytes. Local copies diverge by design (edits, partial syncs, stale checkouts, session-carried text); the tree is the single writer-visible truth. This is the tree-side twin of the live-bytes family (SN-01622 self-reported tables; SN-01504 pin certifies the head, never the tip) — but pointed one level deeper: not just "re-derive at action time" but "re-derive from the right artifact". Any claim whose evidence chain bottoms out in a workspace read must be labeled local-only or re-read from the tree. Cousins: SN-01619 (pins against mutable files drift — the handle-vs-content twin); SN-01504 (the pin certifies the head, never the tip); SN-01601 (re-derive line map after reorder/filter).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01626",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verify", "file-content"],
    ["claim", "repo-tree"],
    ["workspace", "local-copy"]
  ],
  "enforcement": "Any claim about a repo tree's content is verified by reading that tree via the git/tree or git/blob API (contents endpoint at the claimed ref) — never by reading ~/workspace copies, session memory, or capped prior reads. Workspace reads cited as evidence must be labeled local-only. Lane/seat reviews treat a tree-claim evidenced only by a workspace read as UNVERIFIED. The distill-weekly 2026-10-18 run (40 AGENTS.md standing-claims re-verified against the repo tree, 0 survived) is the reference procedure.",
  "decision_change": "Future verifications change from 'I read the file' to 'I read the tree at <ref>' — the evidence line names the ref and the API read. Claims built on workspace reads are either re-read from the tree or explicitly downgraded to local-only before they enter a receipt, a gate, or a board post.",
  "falsifiability": "Falsified by sustained evidence that this fleet's workspace copies are always byte-identical to the trees being claimed about (the rule would be inert-but-safe). A single tree-read that contradicts a workspace-read claim — the 2026-10-18 instance had forty — confirms the rule's necessity.",
  "mechanism": "Workspaces accumulate divergence: hand edits, partial syncs, stale checkouts, session-carried text, and capped reads that silently truncate. The repo tree is append-only history with content addressing; it cannot drift without a commit. Verification reads the artifact with the stronger invariant."
}
~~~
