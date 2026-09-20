#!/usr/bin/env bash
set -euo pipefail

# Canonical build adapter: run the existing repository-owned feed projection,
# copy the existing cognition runtime, then build the existing React/Vite Hub.
python3 ../../scripts/build-smart-feed-projection.py
mkdir -p public
cp ../../scripts/nayanet-cognitive-engine.js public/nayanet-cognitive-engine.js
npx vite build

python3 - <<'PY'
from pathlib import Path
p = Path('dist/index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- NAYANET-HUB-REACT-CANONICAL -->'
if marker not in s:
    s = s.replace('<head>', '<head>\n  ' + marker, 1)
p.write_text(s, encoding='utf-8')
PY

echo "CANONICAL_REACT_HUB_BUILD=PASS"
