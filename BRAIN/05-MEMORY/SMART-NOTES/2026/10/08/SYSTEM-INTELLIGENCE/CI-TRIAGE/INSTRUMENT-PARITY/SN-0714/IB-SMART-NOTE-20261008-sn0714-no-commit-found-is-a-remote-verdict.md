# "No Commit Found" Is a Remote Verdict, Not an Existence Verdict

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0714-no-commit-found-is-a-remote-verdict
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6067738140 + 6067934727 (2026-10-08).
**Provenance:** #1354 comment 6067738140 (Naya 2 relay, 2026-10-08T19:44:51Z): of five sibling node_order-repair SHAs, `ec7b45df1` and `eaca9f6cb` returned "No commit found for SHA" via the commits API — asked for confirm/correct. #1354 comment 6067934727 (Naya 4, 2026-10-08T19:56:50Z): both are **local-only objects** in the shared clone, never pushed — `ec7b45df1` full `ec7b45df179eaeab613fb0aa270fa36e073b04f3` is dangling in no branch (built locally, never pushed); `eaca9f6cb` full `eaca9f6cb1967faef3245b2d7c6f07d9b0e014cb` is Naya 4's orphaned iteration of the weights-branch work. Cousins: SN-0710 (verify heal ancestry — branch-only twins); SN-0316 (local-until-pushed); SN-0236 (one repair per RED class).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The commits API answered "No commit found for SHA" on two SHAs — and both existed. They were local-only objects in the shared clone, never pushed to any remote ref. The API wasn't lying; it was answering a different question than the one being asked. **The commits API is a remote-scope instrument: its "no commit found" means "not reachable on this remote," never "never existed."** The protocol for any cold successor asked to verify a SHA: (1) try the commits API (remote view); (2) try `git cat-file` / `git branch --contains` in the shared clone (local view); (3) only after both fail may you call the SHA fictional. Declaring a SHA dead on the API verdict alone silently deletes real work from the record — here it would have erased two of five sibling repairs and corrupted the duplicate-repair count that SN-0711 stands on. Instruments have scopes; the error message names the lookup, not the world.

## 🩷 HUMAN NOTE

Shawn — a small verification trap worth a standing rule. When Naya 2 asked the commits API about two repair SHAs, it answered "no commit found" — and it turned out both commits did exist, just locally, never pushed. The API tells the truth about the remote, not about reality. So the rule: a SHA isn't declared fictional until we've checked both views — the remote (API) and the local (the shared clone's object store). If we'd stopped at the API's answer, we'd have deleted two real repairs from the record and corrupted the whole duplicate-repair count. The error message names the lookup, not the world — always ask what the instrument can actually see before trusting what it says it can't find.

## 🟣 CHILD NOTE

Imagine you ask your friend "do you have my blue pen?" and they say no. But maybe they left it at home — they checked their backpack, not their house. That doesn't mean the pen never existed! That's exactly what happened: we asked the website (which only checks its own backpack — the remote) whether two commits existed, and it said "never heard of them." But they were sitting at home — in the local copy on our computer. The new rule: "I don't have it" is not the same as "it doesn't exist." Check both places before you declare something gone.

## 👵 GRANDMA NOTE

Sweetheart, it's like calling the library to ask if a book exists, and they say they don't have it. That only means it's not on *their* shelves — it could be sitting on yours. The team learned this the hard way: the website said two of our repair records didn't exist, but they were right here on our own computer, just never sent to the website. So now the rule is simple: before we say something doesn't exist, we check the website AND our own shelves. "Not found here" is never the same as "never existed."

## 🟢 NAYA NOTE

Before ever declaring a SHA fictional, dead, or "someone else's mistake," run the two-scope check: (1) commits API — the remote view (only knows pushed refs); (2) `git cat-file -p <sha>` / `git branch -r --contains <sha>` / `git fsck --lost-found` in the shared clone — the local view (knows local-only objects, dangling commits, orphaned iterations). A "No commit found for SHA" from the API authorizes only the statement "not reachable on this remote" — never "never existed." This protects the record: sibling-repair counts, ancestry claims, and authorship audits all rest on which objects really exist. Watch the shared-clone caveat too (AGENTS.md, 2026-10-08 addendum): objects can vanish mid-run from another lane's gc, so a `cat-file` miss seconds after a hit is an instrument/environment event, not proof of fiction. Record the exact view that failed, not a global verdict.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0714",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "instrument": "GitHub commits API",
  "scope_limitation": "answers only the remote view: 'No commit found for SHA' == 'not reachable on this remote', never 'never existed'",
  "protocol": ["commits API (remote view)", "git cat-file / branch --contains / fsck in the shared clone (local view)", "only after both fail: SHA may be called fictional"],
  "witness": {"ec7b45df1": "local-only, dangling, never pushed", "eaca9f6cb": "local-only orphaned iteration of #1858 work", "17e9d620b": "on main via #1880 — the true owner"},
  "caveat": "shared-clone objects can vanish mid-run under another lane's gc — a fresh cat-file miss is an environment event, not an existence verdict",
  "moral": "instruments have scopes; the error message names the lookup, not the world"
}
```
