# IB-SMART-NOTE-20261008-sn0729-forked-nayanet-publishing-pipeline

Intelligent Block: SN-0729
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Every person gets their own forked NayaNET (`name.nayanet.live`) — their hub, their apps, their rules. They build Smart Apps with NayaPOWER inside their world, preview on instant URLs, and publish through a calculator gate: if the design scores elite and safety checks pass, it goes live. Cloudflare wildcard domains + one GitHub App publish action + the design calculator. The hard part isn't hosting — it's the standard.

## HUMAN NOTE
Shawn laid out the publishing vision on 2026-10-08: the Smart App Creator isn't complete until people can put apps live. Each person gets a forked NayaNET — their own `name.nayanet.live` with their hub. They describe what they want, NayaPOWER builds it, they iterate on preview URLs in plain language, then hit "go live." The calculator scores the design and safety gates check permissions — pass, and it's live on their fork. One more approval puts it in the public NayaNET directory, searchable by everyone. Cloudflare wildcard domains route each fork automatically; the GitHub App gets a publish action; R2 holds everything. His words: "I don't think it's that hard" — the hosting is solved problems; the standard is the real work. This goes on the running todo list as a must-do.

## CHILD NOTE
Imagine everyone gets their own little internet — like their own playground with their name on it. They tell Naya what app they want, Naya builds it beautiful, they look at it on a preview link, and when they love it they press "go live" and it appears in their playground. A smart robot checks that it's beautiful and safe first. If it's really good, it can go in the big public playground where everyone can find it.

## GRANDMA NOTE
Everyone gets their own personal space on the new internet with their name on it. You describe the app you want in plain words, the AI builds it, you look at a preview, and when you're happy you publish it — like putting a photo in your own album. A automatic checker makes sure it looks good and is safe before it goes live. The best ones can be shared publicly so others can find and use them.

## NAYA NOTE
ARCHITECTURE: per-user NayaNET forks via Cloudflare wildcard domains (`*.nayanet.live` → user namespace). Pipeline: describe → NayaPOWER builds in user's fork → preview URL (instant, shareable) → natural-language iteration → "go live" → design calculator scores output + safety gates verify permissions/data → pass → deployed to user's namespace → optional public directory submission → searchable on NayaNET. INFRA: Cloudflare Pages/Workers (hosting) + R2 (assets) + GitHub App publish action (deploy trigger) + per-app repo or monorepo (source of truth, audit trail, rollback). APPROVAL: auto-approve on elite calculator score + green safety gates; flag for human review otherwise. DEFAULTS: private by default; user controls public/private per app. DEPENDENCIES: design standard (tonight's work), design calculator, Smart App DNA contract (#1925), Cloudflare account config, GitHub App publish feature. This is the Smart App Creator's publishing half — build pipeline exists in spec, publish pipeline is now specified.

## MACHINE NOTE
```json
{
  "sn": "SN-0729",
  "type": "PRODUCT_VISION",
  "status": "CANDIDATE",
  "subject": "forked-nayanet-publishing-pipeline",
  "architecture": {
    "user_fork": "*.nayanet.live wildcard domains via Cloudflare",
    "build": "NayaPOWER builds inside user's fork",
    "preview": "instant preview URLs per app version",
    "gate": "design calculator score + safety gates",
    "publish": "GitHub App publish action triggers deploy",
    "storage": "Cloudflare R2 for assets",
    "directory": "public NayaNET directory for approved apps",
    "source_of_truth": "per-app repo or monorepo"
  },
  "pipeline": ["describe", "build", "preview", "iterate", "go-live", "calculator-gate", "publish-to-fork", "optional-public-directory"],
  "defaults": {"visibility": "private", "approval": "auto-on-elite-score"},
  "dependencies": ["design-standard", "design-calculator", "smart-app-dna-1925", "cloudflare-config", "github-app-publish"],
  "todo_list": "added as must-do item",
  "evidence": "Shawn verbal spec 2026-10-08 ~16:35 PDT, main chat"
}
```
