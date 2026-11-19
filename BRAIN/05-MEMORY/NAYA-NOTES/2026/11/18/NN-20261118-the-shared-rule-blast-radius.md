# NN-20261118-the-shared-rule-blast-radius

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-the-shared-rule-blast-radius · Naya Note · 2026-11-18 ~03:12Z**

*Paired Smart Note: SN-3621 — The Shared-Rule Blast Radius*

**Category:** Design — Filing Discipline

## What it is

The Hub follow-on checker went back on the halo fix: the kept filing edited the shared rule itself — line 2016, `.intel-type` — to remove a halo from one panel, and every non-panel label in the system gained box-shadows. The fix: restore line 2016 verbatim, and remove the halo with a panel-scoped override only. A shared rule is shared: an edit to it is an edit to every page that uses it, whether the maker meant to touch them or not.

## Why it matters

One line, edited for one panel, changed labels everywhere — the blast radius of a shared rule is the whole system. The discipline is the lesson: never fix a local problem by editing the shared rule. Restore it verbatim first, then scope the fix to the panel that owns the problem, and prove the other labels are untouched.

## How to use it

Before editing any shared rule, name every place it reaches. If the fix belongs to one panel, the override lives in that panel's scope and the shared rule stays byte-identical. The checker proves it by diffing the shared rule, not by looking at the one panel.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
