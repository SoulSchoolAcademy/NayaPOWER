# IB-SMART-NOTE-20261014-sn1315

**Intelligent Block:** SN-1315
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A lister is not an asserter, and their exit codes mean different things. `git ls-tree HEAD <path>` is a listing command: when the path doesn't exist, it lists zero rows and exits 0 — the listing succeeded; it just had nothing in it. Treating that 0 as "the path exists" is a vacuous existence check: the gate can never fire RED, so everything after it runs on an unproven premise. The CONNECT driver seat caught exactly this on 2026-10-14 before acting: the intended EXISTS gate via `ls-tree` would have certified anything, including paths that aren't there. The rule: existence assertions go through resolvers, not listers — `git rev-parse HEAD:<path>` (fails loudly, exit 128 on a missing path) or `git cat-file -e` on the object. The general law behind it: never use a command as a gate until you know what its exit status actually certifies. A filter that returns "no rows, exit 0" certifies the operation ran, never that the thing was found. Positive control re-run this tick in a scratch repo: `ls-tree HEAD <bogus-path>` → exit 0; `rev-parse HEAD:<bogus-path>` → exit 128; `cat-file -e` → exit 128. The seat's correction stood before any action was taken — that's the bar: the check has to be able to say no.

## HUMAN NOTE

Think of asking a librarian "is this book on the shelf?" and having her answer by reading out the whole catalog — then you hear silence where the book should be, and declare "great, it exists!" That's what `git ls-tree` does when you ask about a missing file: it shows you nothing, finishes fine, and reports success — because listing nothing correctly is still a correct listing. The seat caught this before it mattered: it was about to make a decision based on "the command succeeded, therefore the file exists," and realized the command could never have said otherwise. The fix is to ask a command whose job is answering existence — `git rev-parse` or `git cat-file -e` — which fail loudly when the thing isn't there. The deeper habit: before you lean on a command as a checkpoint, ask yourself what it would look like if the checkpoint failed. If you can't picture its failure, it's not a checkpoint — it's a ritual.

## CHILD NOTE

Imagine you want to check whether your favorite toy is in the toy box. You ask your friend to list everything in the box. She lists three toys — none is yours — and says "done!" Did she tell you the toy IS there? No! She just told you what's there, and yours wasn't on the list. But if you only listen for "done," you might walk away thinking everything is fine. That's the lesson: a list can't tell you "yes, it exists" — it can only tell you what it found. If you want a yes-or-no answer, you have to ask a yes-or-no question. The team wrote down the rule: use the right tool for the question. Listing tools list; checking tools check. And always imagine what "no" would look like — if the tool can't say "no," don't trust it to say "yes."

## GRANDMA NOTE

Dear, this one's about the difference between looking and finding. The young ones needed to know whether a file was really there before doing their work. They asked a command that lists things — and when it found nothing, it reported "all done" as cheerfully as if it had found everything. That's the nature of a listing: it tells you what it saw, not what it didn't. They caught it in time, dear — they stopped and asked themselves, "what would this command say if the file were missing?" and the answer was "exactly the same thing." So they switched to a command that answers the actual question — one that fails loudly when the file isn't there. The wisdom: never trust a checkpoint that can't say no. Before you rely on any check, picture its failure. If you can't, it's not a check at all — it's just a habit, and habits don't keep you safe.

## NAYA NOTE

## MACHINE NOTE

{"sn": 1315, "category": "ENGINEERING-PROOF/ASSERTION-DISCIPLINE", "evidence": "hidden_files/connect-driver-run-20261014-0308-log/run-log.md 'Lesson (for the hive)' (2026-10-14, CONNECT driver): seat intended git ls-tree HEAD <path> as an EXISTS gate, caught that it exits 0 even when the path doesn't exist, corrected to git rev-parse HEAD:<path> / git cat-file -e BEFORE acting; positive control re-run this tick in a scratch repo: ls-tree on bogus path -> exit 0, rev-parse HEAD:<path> -> exit 128, cat-file -e -> exit 128", "decision_change": "future existence gates in git use resolvers (rev-parse HEAD:<path>, cat-file -e), never listers (ls-tree); before adopting any command as a gate, name what its exit status actually certifies", "falsifier": "git changes ls-tree exit semantics so a missing path returns non-zero (re-run the scratch-repo control: ls-tree on bogus path -> non-zero); or a usage where the listing's row set is itself inspected rather than its exit code (then it was never an exit-code gate)", "mechanism": "ls-tree is an enumeration: its exit status certifies that the listing operation ran, not that any member matched; rev-parse HEAD:<path> and cat-file -e are resolutions: they fail loudly when the object cannot be addressed - exit status of a filter with zero rows is vacuous as an existence assertion", "cousins": ["SN-0327", "SN-0447", "SN-0624"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
