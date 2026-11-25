# The Vault Organizes Itself

SN-4841 · VAULT / AUTO-ORGANIZATION

**Created:** 2026-11-24T19:40:00Z

**Kinds:** Multiplication · Craft

## Hook

No hand-filing: a note dropped in the Inbox finds its own folder and its own kind, by logic and math — and the moment it is filed, it is in the vault.

## Nutshell

The vault organizes itself. Every note routes to its folder and its skill category by its own content — the five-part shape sends a daily log to Daily, a settled ruling sends a decision to Memories, a stated category sends a skill to Resources under its kind — and whatever matches nothing waits in the Inbox, sorted later, never lost. The router is the existing organizer with one small addition, not a new machine: it reads what the note already says and files by that, deterministically, the same input always giving the same answer. And a note is not in the vault until it is seen there: filed to the maker's Box and to the shared live store in the same pass, and read back live to prove it.

## Human

Think of a library where every book knows its own shelf. You hand a book to the front desk, the librarian reads its title page, and the book walks itself to the right room — the day's log to the diary shelf, the judge's ruling to the decisions shelf, the craft manual to the craft shelf. No one carries it there by hand, and no book ever lands on the wrong shelf because someone guessed. And the library keeps two copies of the record: one on its own shelves, one in the town's shared archive, so any librarian in any branch can find the same book.

## Child

Imagine a toy box that sorts itself. You drop in a red car and it drives to the cars; you drop in a puzzle and it hops to the puzzles; you drop in something strange and it waits in the tray until someone knows where it goes. Nobody has to remember where everything lives — the box remembers, because every toy says what it is.

## Grandma

It is the oldest housekeeping, dear: a place for everything, and everything finding its place without being carried. The pantry labels itself, the diary keeps its own days, the rulings sit together where they can be found again. And the house keeps its books twice — one copy at home, one with the family — so nothing is ever truly lost, and anyone who needs a page can read it back the same day.

## Naya

Run the existing organizer and add only the vault cut: content to folder and category by fixed, written rules — five-part shape to Daily, decision record to Memories, stated category to Resources under its kind, keyword kind with two or more distinct signals, canon to Resources, author line to that agent's folder, superseded to Archive, area line to Areas, and everything else to the Inbox, never a guessed folder. Keep the router pure and deterministic: same input, same answer, every time. File every note twice in one pass — the maker's Box and the shared live store — and read both back live before claiming it landed. Never hand-file what the rule can place, and never let a note sit unrouted.

## What it means

1. Auto-organization is logic and math, not a new app: the hook that already organizes the Box gains one deterministic rule, content to folder and category.
2. The two cuts stay together: folders say where a thing lives, the six categories say what kind of intelligence it is — a decision about a skill is a Memory of system-and-business kind.
3. The Inbox is a rule, not a failure: unsure goes there first, sorted later, never left — and a note that matches nothing is safer waiting than wrongly filed.
4. A note is not in the vault until it is seen there: the maker's Box and the shared live store, both read back live, in the same pass.
5. Distill, don't dump: the router places distilled notes; raw chats never enter, because a vault full of raw notes gets slow and confused.

## Why it matters

1. Without self-organization, the vault becomes a junk drawer within weeks: every agent hand-files differently, nothing is findable, and the hive re-explains what it already knows.
2. One deterministic rule means every Naya files the same way — a fresh agent finds a decision in Memories, a skill in Resources, today's log in Daily, without being told twice.
3. Filing twice in one pass is the sync proof: the note is in the maker's vault and the collective vault at the same time, and either side can prove it by reading back.
4. The Inbox default protects the vault from confident mistakes: a wrong folder is worse than a waiting note, because a wrong folder is a lost note.
5. The vault only stays fast if it stays distilled: a hundred raw notes go in as ten distilled ones, and the raw is deleted after distilling — or the vault gets slow and confused.

## What changes now

1. Route every new note through the rule (`vault_route.py`): Inbox first, router places it, the routing log records it.
2. File every note twice in one pass — the maker's Box via the organizer hook, the shared live store in Supabase — and read both back live before reporting it landed.
3. Write the nightly log the same way: the shared day-note in Daily, your own nightly log in your Agents folder, same five parts.
4. Distill, don't dump: 100 notes down to about 10, raw deleted after distilling — the existing raw backlog is counted, not mass-deleted, until its deletion run is proven with a restore path.
5. Keep the vault in sync with NayaNET as its interface: name any gap between the store and the interface plainly instead of claiming sync that was not proven.

## Real-world example

On 2026-11-24, the star-ladder ruling — level 9 is Ultimate Star, level 10 is Ten Star, settled by Shawn at ~12:06 MST — sat unfiled in the day's record. Dropped raw into the vault Inbox, the router read it and placed it in Memories with category system-and-business (signals: ladder, star), no hand-filing step: the routing log recorded the move, the Memories index gained the line, the Inbox stood empty again. That is the rule working on a real note.
