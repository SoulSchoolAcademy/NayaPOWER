# THE GATE CONSOLE

### The one page for the things only Shawn can do

> **Plain words:** Some things only *you* can decide. Everything else, the team handles without asking. This page is the fast lane for the things that need YOU — what they are, why they're yours, and exactly what to click or paste when one fires.
>
> **The law behind this page:** V2 §5.1 — the human-only gates. **This page changes NOTHING about the gates.** It only makes the plumbing faster: less hunting, less pasting, less waiting. The console speeds the handoff; it never expands, narrows, or reinterprets a gate.

---

## The gates, word for word (V2 §5.1)

1. Production dispatches and deploys
2. Production database reads, writes, migrations
3. `.github/workflows/` files
4. Credentials and money
5. Destructive or irreversible actions
6. Constitutional ratification
7. Authority, consent, and security changes

## How this page works — 30 seconds

1. A lane needs your word → it files a **GATE REQUEST** using the template at the bottom of this page.
2. You open this page, find the gate, and follow its **1-2-3**: the direct link, the exact thing to paste, the steps.
3. The lane verifies your release, acts on the exact thing you saw, and posts the receipt on #1354.

You never hunt for a link. The lane always brings it to you (V2 §2.5).

---

## Gate 1 — Production dispatches and deploys

**What it is (plain words):** Anything that puts new code, features, or behavior live where real people use it — a release, a deploy, a dispatch to production.

**Why it's yours (one line):** Once it's live, real people feel it — only you can accept what real people experience.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — the pull request on GitHub: `https://github.com/SoulSchoolAcademy/NayaPOWER/pull/<number>`
2. Read the lane's one paragraph: what changes for real people, and how it gets undone.
3. To approve, paste this as a comment on the pull request (or reply in chat, if the lane says so):

```
GATE RELEASE — production deploy
I approve: <what goes live, in plain words — the lane fills this in>
Undo: <one-commit revert — the lane fills this in>
```

**What happens after you act:** The lane merges and deploys the exact code you saw, posts the receipt on #1354. If it breaks, the lane reverts and tells you plainly.

---

## Gate 2 — Production database reads, writes, migrations

**What it is (plain words):** Touching the real database — looking at real people's data, changing it, or reshaping the tables it lives in.

**Why it's yours (one line):** Real people's private information — a wrong look can't be unseen, and a wrong change can lose what can't be replaced.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — the migration file or the exact database change, shown on GitHub.
2. Read the lane's one paragraph: what it reads or changes, whose data it touches, and the backup status.
3. To approve, paste:

```
GATE RELEASE — production database
I approve: <read / write / migration — the lane fills in exactly what>
Scope: <which tables, whose data — the lane fills this in>
Undo: <backup + restore plan, or NOT REVERSIBLE — the lane fills this in>
```

**What happens after you act:** The lane runs exactly what you approved, verifies it, and posts before/after proof on #1354.

---

## Gate 3 — `.github/workflows/` files

**What it is (plain words):** The automation scripts that run by themselves every time code changes — they can run programs and touch secrets.

**Why it's yours (one line):** A bad automation file can break everything or leak secrets quietly, and it runs with high privilege.

**When it fires — your 1-2-3:**

1. Open the pull request link the lane gives you — it shows exactly which automation files change.
2. Read the lane's one paragraph: what the automation will now do.
3. To approve, paste:

```
GATE RELEASE — workflow files
I approve: <which workflow files change and what they will do — the lane fills this in>
Undo: <revert the pull request — the lane fills this in>
```

**What happens after you act:** The lane merges; the new automation runs from then on. Receipt on #1354.

---

## Gate 4 — Credentials and money

**What it is (plain words):** Anything that spends money, or touches passwords, keys, and secrets.

**Why it's yours (one line):** It's your money and your accounts — nobody spends or shares those but you.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — for a new password: the Secure Vault capture page (**type it there and ONLY there — never in chat, never in a comment**). For spending: the approval or checkout page.
2. Read the lane's one paragraph: the exact amount and what it's for (money), or which account the credential unlocks.
3. For money, paste:

```
GATE RELEASE — money
I approve spending: $<amount> for <what — the lane fills this in>
Undo: <refundable / NOT REVERSIBLE — the lane fills this in>
```

For passwords: there is nothing to paste — the capture page is the whole action.

**What happens after you act:** The lane completes the purchase or setup and posts the receipt on #1354. The secret itself is never posted anywhere.

---

## Gate 5 — Destructive or irreversible actions

**What it is (plain words):** Deleting or destroying something we cannot get back — data, branches, repos, infrastructure.

**Why it's yours (one line):** The person who loses it decides — nobody destroys on someone else's behalf.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — the gate request showing exactly what will be destroyed and what backups exist.
2. Read it twice. This one doesn't come back.
3. To approve, paste:

```
GATE RELEASE — destructive action
I approve destroying: <exactly what — the lane fills this in>
Backups: <what survives — the lane fills this in>
This is NOT REVERSIBLE.
```

**What happens after you act:** The lane destroys exactly what you named, confirms the scope, and posts the receipt on #1354.

---

## Gate 6 — Constitutional ratification

**What it is (plain words):** Making a new law official — or changing or retiring an existing law.

**Why it's yours (one line):** Only the director makes law — the team proposes, scores, and prepares; you alone ratify.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — the scored proposal on GitHub or on #1354.
2. Read the plain-words version: what the law says, what changes, the honest score.
3. Your word IS the action — write it plainly, for example:

```
RATIFIED — <law name>
<your words — the team's record of your decision>
```

**What happens after you act:** The lane flips the law's status to RATIFIED, the team operates under it immediately, and the receipt posts on #1354.

---

## Gate 7 — Authority, consent, and security changes

**What it is (plain words):** Changes to who is allowed to do what, what someone agreed to, and how things are protected — permissions, access, security settings.

**Why it's yours (one line):** Authority and consent belong to you — you grant them, and only you change or delegate them.

**When it fires — your 1-2-3:**

1. Open the link the lane gives you — the request naming the exact permission, consent, or security change.
2. Read the lane's one paragraph: who gets what, and what could go wrong.
3. To approve, paste:

```
GATE RELEASE — authority / consent / security
I approve: <exactly who may do what — the lane fills this in>
Undo: <how to take it back — the lane fills this in>
```

**What happens after you act:** The lane applies exactly what you named and posts the receipt on #1354.

---

## The gate-request template (for lanes — file a gate need with this)

Plain words, no jargon-first. A gate request that Shawn can't understand in one read is a failed request — rewrite it.

```
## GATE REQUEST — <gate name, in plain words>

**1. What I need from you (plain words):**
<one paragraph — no code terms without a translation>

**2. Why only you can do it:**
<which of the 7 gates above, and why no lane substitute exists>

**3. Your options:**
- **Yes:** <what the lane will do> → <what happens, plain words> → reversible: <yes — how / no>
- **No / wait:** <what happens instead> → reversible: <yes>

**4. Your 1-2-3:**
1. Link: <the direct link — he never hunts>
2. Paste this:
   ```
   <the pre-filled release block from the gate above>
   ```
3. Steps: <any click beyond the paste, if needed — or "paste is the whole action">

**5. After you act, the lane will:** <verify your release → act on the exact thing you saw → post the receipt on #1354>

Lane: <name> · Filed: <date> · Status: WAITING ON SHAWN
```

## What is NOT a gate

If it isn't one of the 7 above, it isn't yours — the calculator decides and the team moves (V2 §1.2, §5.2). Lanes must not file gate requests for non-gates. Waiting on you for something that isn't a gate is a bug, not caution.

---

## Provenance & boundaries

- The 7 gates are quoted verbatim from **V2 §5.1** (`BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.ai.md`), landed via **PR #2087** (merge `26f28c527626c74b164790d3d635ae9b831476a1`); ratification recorded on **#1354, comment 6098714232** (Shawn's go-ahead, 2026-10-10 14:47Z).
- Status note: V2 was ratified by Shawn's go-ahead on 2026-10-10 14:47Z (#1354, comment 6098714232); the RATIFIED status was written into all three V2 languages on main the same day (commit `801e3922e236665adb5d00c8b849f179fc968dde`). The §5.1 gate list quoted here is the ratified text. **This console changes nothing about the gates themselves.**
- Handoff format follows **V2 §2.5**: the direct link, the exact value to paste, numbered 1-2-3 steps. Never make him hunt.
- New law comes only through Shawn's authority (V2 Amendment Path). To change a gate, file a Gate 6 request.

## Changelog

- **v1 — 2026-10-10** — Naya 4, Workstream 8 (Operation Flow Like Water). Initial console: all 7 gates + lane request template.
