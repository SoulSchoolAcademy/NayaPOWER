# NAYA POWER — REAL-TIME LIVING HUB CONTRACT V1

DATE: 2026-09-12
STATUS: CANONICAL RUNTIME CONTRACT V1
NUMBER: 49

## PURPOSE
Define how the Hub becomes living rather than a page that only changes after manual refresh.

## SOURCE OF CHANGE
Canonical events are the source of live updates. A client may receive updates through an appropriate realtime transport, polling, streaming, or server-sent mechanism depending on the actual runtime architecture.

## CLIENT RULE
The UI must never imply realtime simply because animations run. A LIVE indicator requires an observed healthy connection/subscription or equivalent verified freshness mechanism.

## UPDATE LOOP
EVENT CREATED → PERSISTED → AUTHORIZED → PROJECTED → DELIVERED → UI UPDATED → USER ACTION → NEW EVENT.

## STALE/DEGRADED
If the transport fails, retain last known data with explicit stale/degraded state and a retry path. Do not silently present old intelligence as current.

## EFFICIENCY
Use event identity and incremental updates to avoid unnecessary full-feed reloads. Deduplicate by event/version identity.

## ACCEPTANCE
A test event created after the Hub is open becomes visible without a misleading status, or the UI accurately reports that realtime is unavailable and provides a refresh/reconnect path.
