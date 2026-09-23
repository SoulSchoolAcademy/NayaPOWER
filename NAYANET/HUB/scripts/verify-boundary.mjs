import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const mustExist=[
  'index.html',
  'package.json',
  'vite.config.ts',
  'wrangler.jsonc',
  'worker.js',
  'public/assistant-runtime.js',
  'public/hub-completeness.js',
  'public/smart-feed.js',
  'public/smart-tabs.js',
  'public/identity.html',
  'public/name-first-auth-adapter.js'
];
const legacyOutside=[
  '../../assistant-runtime.js',
  '../../hub-completeness.js',
  '../../smart-feed.js',
  '../../smart-tabs.js',
  '../../identity.html',
  '../name-first-auth-adapter.js',
  '../../scripts/build-smart-feed-projection.py',
  '../../scripts/nayanet-cognitive-engine.js'
];
const obsoleteDirs=[
  '../E02-INTELLIGENT-HUB',
  '../E02-INTELLIGENT-HUB-AAA',
  '../E02-INTELLIGENT-HUB-CLOUDFLARE',
  '../E03-INTELLIGENT-HUB'
];
for(const p of mustExist) if(!fs.existsSync(path.join(root,p))) throw new Error('MISSING_CANONICAL_HUB_FILE:'+p);
const packageText=fs.readFileSync(path.join(root,'package.json'),'utf8');
for(const ref of legacyOutside) if(packageText.includes(ref)) throw new Error('EXTERNAL_HUB_BUILD_DEPENDENCY:'+ref);
for(const p of obsoleteDirs) if(fs.existsSync(path.resolve(root,p))) throw new Error('OBSOLETE_HUB_SURFACE_PRESENT:'+p);
const index=fs.readFileSync(path.join(root,'index.html'),'utf8');
if(!index.includes('nayanet-direct-nine')) throw new Error('CANONICAL_MARKER_MISSING');
if(!index.includes('<title>NayaNET — Intelligent Hub V7 · 509 AAA</title>')) throw new Error('CANONICAL_TITLE_MISSING');
const wrangler=fs.readFileSync(path.join(root,'wrangler.jsonc'),'utf8');
if(!wrangler.includes('"assets"') || !wrangler.includes('"directory": "./dist"')) throw new Error('WRANGLER_NOT_HUB_LOCAL');
console.log('HUB_BOUNDARY_VERIFIED');
console.log('CANONICAL_SOURCE=index.html');
console.log('CANONICAL_RUNTIME=public/*');
console.log('CANONICAL_BUILD=Vite dist/');
console.log('CANONICAL_DEPLOY=Cloudflare Worker sparkling-shape-7ae5');
