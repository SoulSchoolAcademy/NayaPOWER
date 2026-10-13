# A Vanished RED Is Not a Healed RED — a chronic external-integration check that disappears with no receipt is recorded as an unattributed external change, never as repair

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0677-vanished-red-not-healed-red
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6059327131 (overnight sweep 2026-10-08 ~11:55Z — Workers Builds noise cleared on main); SoulSchoolAcademy/NayaPOWER, main tip `53217a40`.

## ✦ IN A NUTSHELL

The chronic Cloudflare `Workers Builds` red — 17 failures on Oct-5 main, then 2, then zero — is gone from the last three main commits: no Workers Builds check-runs exist at all on `53217a40`, `871e283f`, or `65269857`. Timeline says the Cloudflare Git integrations were disconnected (Lane C's human-gated handoff), but by parties unknown to the sweep — who disconnected what, and when, is unconfirmed. SN-0386 taught us that external-integration fan-out is its own RED class: classify before repairing. This is its mirror case: when a chronic external RED vanishes with no in-repo change and no receipt, the sweep must record it as an UNATTRIBUTED EXTERNAL CHANGE (who/when unknown) — never silently accept "green" as healed, never close the underlying class, and never let the absence of a check stand in for the evidence that something was fixed. A verdict is only per-tip (SN-0668): this per-tip green covers main now, but it proves nothing about the Cloudflare surface, the original failures, or whether the noise returns the moment an integration is reconnected.

## HUMAN NOTE

Shawn: that annoying Cloudflare `Workers Builds` red that kept lighting up main is gone — not because anyone fixed anything in the repo, but because it looks like the Cloudflare integration got disconnected on Cloudflare's side (your Lane C handoff, but we don't actually know who did it or when). The important part: "green" here doesn't mean healed, it means the checker stopped running. So the sweep logged it as "unknown external change, attribution missing" instead of closing the book. If that integration ever gets reconnected, the old failures may come right back — nothing in the repo proves otherwise.

## CHILD NOTE

Imagine your smoke alarm stops beeping. You didn't put out any smoke — somebody just took the batteries out. The house might be fine, but the silence doesn't prove it. Write down "someone took the batteries out, I don't know who" instead of "the fire is fixed."

## GRANDMA NOTE

It's like the "check engine" light going dark because someone unplugged the dashboard, not because the mechanic fixed the engine. Note exactly that — "the light was unplugged, unknown by whom" — and don't throw away the repair order.

## NAYA NOTE

Sisters: this is the RED-CLASSIFICATION family's newest member — SN-0386 taught us external fan-out failures are their own class (classify before repairing), and now SN-0677 teaches the mirror: external RED *disappearances* are their own class too. The exact trap: a sweep that enumerates check-runs on the exact tip (SN-0668) finds zero check-runs and reads "GREEN" — but the green was manufactured by removing the instrument, not by passing the test. The discipline: when a chronic external check vanishes with no in-repo change and no receipt, the sweep receipt must say UNATTRIBUTED EXTERNAL CHANGE with who/when marked UNKNOWN, keep the underlying class OPEN (do not close it, do not mark it healed), and note the reversion risk (reconnect the integration → failures may return). What the 11:55Z sweep did right: it listed the timeline (17 → 2 → 0 across commits `189428155`, `8fb7831d`, `53217a40`), named the likely mechanism (Cloudflare Git integrations disconnected), and refused to attribute it — "executed by parties unknown to this sweep." A cold Naya seeing a mysteriously-cleared external check should reach for this note before claiming the pipeline is healthy.

## MACHINE NOTE

```json
{
  "sn": "SN-0677",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "taxonomy": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "extends": ["SN-0386", "SN-0668", "SN-0420"],
  "lesson": "A chronic external-integration RED that disappears with no in-repo change and no receipt must be recorded as an UNATTRIBUTED EXTERNAL CHANGE (who/when UNKNOWN). Silence is not repair: do not close the underlying RED class, do not claim the pipeline is healthy, and record the reversion risk (reconnecting the integration may restore the failures). Per-tip verdicts (SN-0668) cover the repo's current state only; they prove nothing about the external surface.",
  "evidence": {
    "board": "#1354 comment 6059327131 (overnight sweep 2026-10-08 ~11:55Z)",
    "timeline": "17 Workers Builds failures on 189428155 (Oct 5) -> 2 (maxresults, maxess-e01) on 8fb7831d -> zero check-runs on 53217a40, 871e283f, 65269857",
    "likely_mechanism": "Cloudflare Git integrations disconnected (Lane C human-gated handoff)",
    "attribution": "UNKNOWN — executed by parties unknown to the sweep"
  },
  "gate": "When a chronic external check vanishes: (1) enumerate check-runs on the exact tip to distinguish 'no failures' from 'no check-runs'; (2) if check-runs are absent with no in-repo change and no receipt, record UNATTRIBUTED EXTERNAL CHANGE with who/when UNKNOWN; (3) keep the underlying RED class OPEN — absence of the check is not evidence of a fix; (4) note reversion risk in the receipt; (5) declined: claiming pipeline healthy, closing the class, assuming a repair happened (SN-0420's mirror).",
  "proposed_repair": "None from this seat — attribution lives on the Cloudflare/connector side (human-gated). The sweep did the correct thing: name the unknown, keep the class open.",
  "ratification": "NOT_RATIFIED — only Shawn ratifies"
}
```
