# 🔱 NAYANET — ENGINEERING BLUEPRINT

## 1. Engineering objective

Deliver a premium static-first application that can be deployed immediately, remains modular, and has clean seams for future authenticated intelligence services.

## 2. Default block stack

Each static block should be self-contained:

```text
BLOCK/
 ├── index.html
 ├── block.css
 ├── block.js
 ├── assets/
 ├── data/
 ├── README.md
 └── tests/
```

Avoid unnecessary frameworks for blocks whose primary requirement is direct static deployment.

## 3. Isolation rules

Each block must:

- namespace CSS;
- namespace JavaScript globals;
- avoid modifying parent DOM;
- avoid assumptions about parent framework;
- expose documented entry points only;
- degrade gracefully if optional dependencies fail.

## 4. Static-first rules

The block must function when served as ordinary static files.

Do not require:

- Node runtime;
- build step;
- Wrangler;
- server-side rendering;
- API availability;
- database availability;

for baseline presentation and interactions.

## 5. Data/config

Prefer versioned local JSON/config for static content.

Never hard-code content that future operators need to edit frequently when a small config structure is more appropriate.

## 6. State

Use the smallest state model that can produce the experience.

Local persistence is appropriate for non-sensitive temporary state such as challenge progress when the product specification permits it.

Never place secrets or security credentials in client code.

## 7. API seams

Future API calls should use a single provider-neutral client abstraction.

Conceptual interface:

```text
naya.ask(input, context)
notes.create(event)
notes.list(query)
report.daily(date)
superbrain.status()
collective.discover(query)
collective.contribute(candidate)
network.discover(intent)
```

Static fallback implementations may return deterministic demonstration content but must be explicitly identified as demo/local behavior.

## 8. Cloudflare deployment

The static artifact must be compatible with direct static upload when the chosen Cloudflare product supports it.

Do not include Wrangler configuration in a ZIP intended for the no-build static uploader unless the deployment path explicitly supports it.

For Worker applications, use the Worker deployment path instead of pretending the static uploader is equivalent.

This distinction is a canonical deployment lesson.

## 9. Groove embedding

Each finished block receives a stable Cloudflare URL.

Groove embeds that URL using an iframe.

The block should:

- be fully responsive inside an iframe;
- not assume viewport width equals browser width;
- avoid fixed heights where content can grow;
- expose a clear internal navigation model;
- provide a safe fallback for deep links.

## 10. postMessage

Do not add cross-frame messaging until a concrete requirement exists.

When required, define:

```text
message version
message type
payload schema
sender origin
receiver origin
request/response semantics
error semantics
```

Accept messages only from an explicit allowlist of trusted origins.

Never trust arbitrary `event.data` or `event.origin`.

## 11. Media

Audio/video belongs to the block and must use browser-native media capabilities where practical.

Autoplay must not be assumed.

User-initiated play is the default reliable interaction.

Provide:

- play/pause;
- progress;
- volume/mute;
- captions/transcript where applicable;
- accessible labels;
- graceful unavailable-media state.

## 12. Performance

Target:

- minimal blocking JavaScript;
- compressed assets;
- lazy loading for noncritical media;
- efficient animations;
- no unnecessary dependencies;
- no giant framework for a simple block;
- stable layout during load.

The first screen must become useful before secondary media finishes loading.

## 13. Security

Never expose:

- API keys;
- service-role credentials;
- GitHub installation secrets;
- database admin credentials;

in static assets.

Any privileged operation belongs behind a trusted server boundary.

## 14. Testing

Each block requires:

### Static
HTML validity, CSS sanity, JavaScript syntax, asset existence, no accidental secrets.

### Behavioral
Primary CTA, all meaningful states, persistence, media, keyboard navigation.

### Responsive
320–1280px matrix.

### Accessibility
Keyboard, focus, labels, contrast, reduced motion, media alternatives.

### Embed
Test at realistic Groove iframe widths and heights.

### Deployment
Verify the actual Cloudflare URL, not merely local output.

## 15. Completion gate

A block is complete only when:

**SPECIFIED → IMPLEMENTED → TESTED → DEPLOYED → HUMAN-VERIFIED → FROZEN**

with evidence for every claimed state.

## 16. Engineering law

> **The simplest deployable artifact is the default. Complexity must earn its place.**
