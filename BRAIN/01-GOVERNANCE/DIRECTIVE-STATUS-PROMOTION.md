# Directive Status Promotion — the honest accounting mechanism

**Plain words:** the directive register (`directive-register.json`) tracks 58 master
directives. A status field nobody can honestly update rots within days — tonight's
wire lanes already made it stale. This is the mechanism that keeps it true: one
tool, one ladder, evidence on every rung. `tools/directive_status.py`.

## The ladder

```
NOT_STARTED -> BUILDING -> BUILT_AS_CODE -> ENFORCED
```

| Rung | Meaning |
|---|---|
| NOT_STARTED | No code exists. |
| BUILDING | A lane is actively building it in a numbered PR (draft counts). |
| BUILT_AS_CODE | Code exists and is tested — but nothing live enforces it yet. Code-only is not law. |
| ENFORCED | A live mechanism (CI gate, runtime guard, workflow block) on an operating path blocks a real violation. Proven, not claimed. |

## Rules

1. **Promotions move exactly one rung.** No skipping — you cannot claim ENFORCED
   without passing through BUILT_AS_CODE. The ladder is the receipt.
2. **Every promotion needs `--evidence-pr`** (the PR that did the work). No PR, no
   promotion. A branch is a claim; a merged PR number is evidence.
3. **ENFORCED additionally needs `--gate`** — the live enforcement mechanism by
   name. If it names a repo path, that path must exist when you promote.
4. **Demotions need `--reason`** and may drop any number of rungs — a removed gate
   is honest news, not failure. Demoting to NOT_STARTED clears `evidence_pr`.
5. **Never promote on unmerged PRs.** Branch state is not production truth;
   promoting it is the exact dishonesty this mechanism exists to prevent.
6. Unknown directive, malformed id, corrupt register → fail closed, nothing written.
   Writes are atomic; untouched entries stay byte-identical.

## Use

```bash
python3 tools/directive_status.py promote D26 --to BUILDING --evidence-pr 2228
python3 tools/directive_status.py promote D32 --to ENFORCED --evidence-pr 2224 \
    --gate .github/workflows/d32-doc-scan.yml
python3 tools/directive_status.py demote D32 --to BUILT_AS_CODE \
    --reason "gate workflow deleted in #2300"
python3 tools/directive_status.py show D26
python3 tools/directive_status.py ladder
```

Every promotion/demotion prints a JSON receipt
(`action, directive_id, from, to, evidence_pr, gate, reason, at`) — file it with
your lane's sign-out. Status edits belong to the lane that earned the rung;
this tool is how, not who decides.

## What this does NOT do

Judge whether the evidence is *true* (a merged PR number is form, not proof —
reviewers judge substance). Flip any statuses by itself. Replace the register
loader (`tools/directive_register.py`) or the governance-path sync gate — it is
built on them.
