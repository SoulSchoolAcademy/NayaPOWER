# Smart Links — redirect worker + attribution carrier

Best-of-Best application map, element **#3**: paste any URL, name it, get
`nayanet.live/<your-name>`; every click is counted on the way through
(counting never slows the visitor), and when a click leads to a join, the
join credits the link — and its owner.

## What's here

| File | Job |
|---|---|
| `worker.js` | The redirect handler. Pure logic + an injected data adapter; the production adapter talks Supabase PostgREST with the anon key. |
| `reserved-names.mjs` | The ONE reserved-name list + name validation. The migration seed mirrors it; a contract test fails on drift. |
| `attribution.mjs` | The join-attribution carrier: reader half (`readAttribution`) + cookie format. The worker is the writer half. |
| `wrangler.toml` | Worker config with the route **commented out** — deployment is human-gated. |

Data: `supabase/migrations/20261022201500_smart_links_v1.sql`
(`smart_links`, `smart_link_clicks`, `smart_link_reserved_names`, the
`resolve_smart_link` RPC, RLS). Registered in the production migration
ledger as pending; it applies only at the human gate.

## Behavior

- `GET /<name>` for an active link → **302** to the target, with
  `nl_ref=<name>` appended to the target URL (never duplicated) and an
  `nl_attr` cookie set (30 days).
- The click row (`link_id`, `referrer_class`, `referrer_host`,
  `attribution_id`) is registered with `ctx.waitUntil` — the redirect
  never waits for it. A failed count is lost, never a stalled visitor.
- Referrers are stored as a **class** (`direct` / `social` / `search` /
  `email` / `internal` / `other`) plus host — never the raw referrer.
- Reserved names and unknown names → **404, nothing recorded**, so this
  worker can never shadow `/rooms/*`, `/s/*`, `/identity.html`, or any
  other real route. Only single-segment paths are candidates at all.

## The join-attribution wiring contract

The carrier is durable two ways (cookie + param) because joins happen on
different surfaces. At the invite-join moment, the join code calls:

```js
import { readAttribution } from './attribution.mjs';
const attr = readAttribution({ cookieHeader: req.headers.get('Cookie'), url: req.url });
// attr = { link_name, attribution_id, source: 'cookie' | 'param' } | null
```

and stores `attr.link_name` / `attr.attribution_id` on the join record.
That is the whole integration: one import, one call. The flagship
invite-join surface adopts it in its own lane (Phase 1, step 8 lands the
Clicked → Joined funnel stage on this data).

## Tests

- `tests/smart_links_worker.test.mjs` — redirect, counting, referrer
  classes, reserved-name refusal, non-blocking count (negative controls
  included: reserved/unknown names record zero clicks).
- `tests/test_smart_links_contract.py` — migration ↔ reserved-list drift
  check, RLS shape (append-only clicks, no anon delete), SQL parse.
