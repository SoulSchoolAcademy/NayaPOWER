# Factory Pipeline — Contract → Live App

NayaPOWER's build pipeline. Takes a contract JSON, outputs a live deployed app.

## Components

- `customize.py` — Takes proven 9/10 template + contract → customized HTML
- `deploy.py` — Takes HTML → deploys to Cloudflare worker → live URL  
- `build-api.py` — Full pipeline: contract in → {build_id, url, receipt} out
- `contracts.json` — Contract definitions for all 12 templates

## Usage

```bash
# Customize a template
python3 customize.py <template.html> <contract.json> <output.html>

# Deploy to live URL
python3 deploy.py <html_file> <worker_name>

# Full pipeline (contract → live app)
python3 build-api.py <contract.json>
# or: cat contract.json | python3 build-api.py
```

## Templates

All 12 templates live at:
- Personal: https://naya-showpiece.nayapower.workers.dev/
- Business: https://naya-template-business.nayapower.workers.dev/
- Booking: https://naya-template-booking.nayapower.workers.dev/
- Product: https://naya-template-product.nayapower.workers.dev/
- Portfolio: https://naya-template-portfolio.nayapower.workers.dev/
- Event: https://naya-template-event.nayapower.workers.dev/
- Menu: https://naya-template-menu.nayapower.workers.dev/
- Community: https://naya-template-community.nayapower.workers.dev/
- Signup: https://naya-template-signup.nayapower.workers.dev/
- Dashboard: https://naya-template-dashboard.nayapower.workers.dev/
- Personal Hub: https://naya-template-personal-hub.nayapower.workers.dev/
- Business Hub: https://naya-template-business-hub.nayapower.workers.dev/

## Design Language

All templates follow the Nayanet Design Language (locked 2026-10-19):
1. Spectrum walk (never repeat colors)
2. White at rest, color ignites
3. Elevation everywhere
4. Rectangles, not squares
5. Full width
6. Real pieces only
7. Color = identity
