# HUMAN NOTE — NAYA POWER PLAYER / CLOUDFLARE + GROOVE OPERATING MODEL

**Date:** August 30, 2026
**Purpose:** Human-readable handoff for Shawn and future NayAs.

## What we decided

Naya Power Player will not be built as one giant deployment artifact. It will be built as modular vertical experience blocks.

Each block gets its own code, QA, static ZIP, Cloudflare deployment, and URL. It is connected to the Groove page only when it is ready.

The customer experiences one seamless Naya Power application even though engineering maintains separate bounded blocks.

## The stack

**GitHub** is the canonical source of truth.

**Cloudflare Pages/static hosting** hosts each deployable static block.

**Groove** composes the blocks into the customer-facing page using embeds/iframes.

**Supabase** can later provide shared identity/authentication and data services without requiring Wrangler for ordinary browser-side Auth usage.

## Static-first rule

For direct Cloudflare upload, the ZIP must be a static deployment artifact. Do not put Wrangler configuration, build-only dependencies, server secrets, or uncompiled runtime expectations into the direct-upload ZIP.

Cloudflare's current Direct Upload limits include 1,000 files per drag-and-drop deployment and 25 MiB maximum per individual asset. The 25 MiB limit is per file, not total project size.

## Embed rule

The Cloudflare URL is the block. Groove embeds that URL. We do not need to copy the application source into Groove.

Do not connect a block to Groove until the block has passed its own QA/Oscar/proof standard.

## Iframe rule

There is no universal iframe height. Stable blocks should use a known responsive/min-height strategy. Dynamic parent resizing should use a small validated `postMessage` protocol only when testing proves it is necessary.

The iframe must be responsive internally. Groove responsiveness does not make the contents of the Cloudflare iframe responsive automatically.

## Media rule

Audio/video works inside the embedded experience, subject to normal browser autoplay and permission rules. Design media around user initiation. Where needed, the Groove iframe must grant `autoplay`, `fullscreen`, and/or `microphone` through its `allow` policy.

## Framing rule

Every Cloudflare block intended for Groove must be checked for `X-Frame-Options`, CSP `frame-ancestors`, and Permissions Policy. Never accidentally deploy a block that forbids its intended parent from framing it.

## Auth rule

Supabase Auth can be used from the static browser application. Never expose service-role or other private Supabase credentials. Production authentication must be tested in the actual Groove + Cloudflare cross-origin context before being declared complete.

The product should have one coherent identity, not nine separate login experiences.

## Evidence rule

A future Naya must distinguish:

- implemented;
- locally verified;
- Cloudflare deployed;
- production tested;
- Groove tested.

A claim is not evidence. When a Naya creates or updates a system note, the user must receive the actual GitHub path/URL and commit receipt.

## Build loop

**BUILD → QA → OSCAR → REPAIR → DEPLOY → HUMAN TEST → GROOVE EMBED → FREEZE → NEXT BLOCK.**

## Key principle

> **Solve the platform once. Build the Player many times.**

This model exists so future NayAs can immediately understand how Naya Power is delivered, what constraints they must build within, and how to extend the Player without creating one giant fragile application.
