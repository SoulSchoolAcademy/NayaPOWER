# SMART NOTE — GITHUB-FIRST FREEZE-POINT DELIVERY

**DATE:** 2026-09-17
**TYPE:** OPERATING PREFERENCE / DELIVERY LEARNING
**STATUS:** RECORDED

## WHAT HAPPENED

Shawn clarified how he wants Naya work delivered and preserved.

## CORE LEARNING

The delivery platform is secondary. The durable GitHub source of truth is primary.

Preferred order:

**GitHub edit → freeze point → direct GitHub save/download → optional live deployment → runtime proof.**

Cloudflare and Vercel are both acceptable when a live deployment adds value. Neither should replace the GitHub source of truth.

## WHY THIS MATTERS

This reduces the risk of lost work, makes progress independently inspectable, and gives Shawn a simple way to save a known-good state to his computer.

A live URL is useful, but it is a projection of the system. A GitHub commit/file is the durable handoff another Naya can restore.

## MACHINE CONSEQUENCE

When implementing future work, Naya should:

1. edit the canonical GitHub repository first when practical;
2. leave a clear commit/freeze point after meaningful work;
3. provide a direct GitHub source/file link;
4. provide a live URL only when deployed and verified;
5. never claim a live deployment is the saved source of truth;
6. preserve the exact state needed for the next Naya to continue.

## LEARNING STATE

**L0 RECORDED:** This Smart Note exists.

**L1 RETAINED:** Pending governed CIS transaction verification for this specific preference.

**L2 RETRIEVABLE:** The preference is now in the Team Naya delivery standard and Smart Note path.

**L3-L6:** Not claimed. Future work must demonstrate retrieval, application, observed benefit, verification, and durable adaptation where appropriate.

## EVIDENCE

Canonical delivery standard:
`.naya/TEAM-NAYA/09-GITHUB-FIRST-FREEZE-POINT-DELIVERY-STANDARD.md`

## NEXT ACTION

Apply this standard to every subsequent Hub/Naya artifact and preserve a GitHub freeze point before treating a deployment as complete.

**END — SMART NOTE**
