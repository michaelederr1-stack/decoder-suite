#!/usr/bin/env bash
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
PROJ=~/decoder_project
mkdir -p scratch src public/logistics-tracker
[ -f wrangler.jsonc ] && [ -f public/index.html ] || { echo "ERROR: wrangler.jsonc or public/index.html missing"; exit 1; }
cp wrangler.jsonc scratch/wrangler.jsonc.before-worker
cp public/index.html scratch/index.html.before-worker-nav
python3 - <<'PY'
import json, pathlib, re
p = pathlib.Path('wrangler.jsonc')
cfg = json.loads(p.read_text())
cfg['main'] = 'src/index.js'
a = cfg.get('assets', {})
a.update({'directory': './public', 'binding': 'ASSETS', 'run_worker_first': ['/api/*']})
cfg['assets'] = a
p.write_text(json.dumps(cfg, indent=2) + '\n')
h = pathlib.Path('public/index.html')
s = h.read_text(encoding='utf-8')
if 'logistics-tracker' not in s:
    m = re.search(r'<button class="nav-btn"[^>]*data-page="page-howto"[^>]*>.*?</button>', s, re.S)
    if m:
        link = '\n      <a class="nav-ext" href="/logistics-tracker/">Logistics Tracker</a>'
        s = s[:m.end()] + link + s[m.end():]
        css = ('.nav-ext{display:inline-block;text-decoration:none;background:rgba(16,22,36,.7);color:var(--muted);'
               'border:1px solid rgba(0,242,254,.15);border-radius:8px;padding:9px 16px;font-size:.9rem;font-weight:600}'
               '.nav-ext:hover{color:#fff;border-color:var(--accent)}\n  </style>')
        s = s.replace('</style>', css, 1)
        h.write_text(s, encoding='utf-8')
PY
touch .gitignore
for line in ".dev.vars" "node_modules/"; do
  grep -qxF "$line" .gitignore || echo "$line" >> .gitignore
done
echo "Setup helper complete."
