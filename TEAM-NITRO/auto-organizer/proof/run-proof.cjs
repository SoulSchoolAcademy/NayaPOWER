/* Node proof runner for the Auto Organizer.
   Pulls REAL rows from Supabase hub_smart_notes (read-only), runs the
   module over every one, then runs the three live-path items (new smart
   note, post, contact) plus the user-move override and the learning test.
   Writes placements to proof-placements.json for hand verification.
   Usage: node proof/run-proof.mjs
*/
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const AO = require('../auto-organizer.js');

function now() {
  const d = new Date();
  const mst = new Date(d.getTime() - 7 * 60 * 60 * 1000);
  return { utc: d.toISOString(), mst: mst.toISOString().replace('T', ' ').slice(0, 19) + ' MST' };
}
function stamp(label) {
  const t = now();
  console.log(`[${t.utc} | ${t.mst}] ${label}`);
  return t;
}
function sb(query) {
  const out = execSync(
    `python3 ~/workspace/custom-connectors/custom.supabase/bin/sb-api GET "/rest/v1/hub_smart_notes?${query}"`,
    { maxBuffer: 64 * 1024 * 1024 }
  ).toString();
  return JSON.parse(out);
}

stamp('PROOF START — Auto Organizer, Node, real Supabase data (read-only)');

// ---- 1. Every real note through the engine -------------------------------
const rows = sb('select=id,ib_id,title,nutshell,github_path&limit=200');
console.log(`rows pulled: ${rows.length}`);
const items = rows.map((r) => ({
  id: r.ib_id, type: 'note', title: r.title, nutshell: r.nutshell || '',
}));
const t1 = stamp('organizeAll() over all real notes');
const res = AO.organizeAll(items, {});
const t2 = stamp(`organizeAll() done — ${res.total} placed`);
console.log('distribution (subcategoryId: count):');
console.log(JSON.stringify(res.distribution, null, 2));
const bySource = {};
res.placements.forEach((p) => { bySource[p.source] = (bySource[p.source] || 0) + 1; });
console.log('by source:', JSON.stringify(bySource));
const byConf = {};
res.placements.forEach((p) => { byConf[p.confidence] = (byConf[p.confidence] || 0) + 1; });
console.log('by confidence:', JSON.stringify(byConf));
fs.writeFileSync(
  path.join(__dirname, 'proof-placements.json'),
  JSON.stringify({ generated_at_utc: t2.utc, total: res.total, distribution: res.distribution, placements: res.placements }, null, 2)
);
console.log('placements written to proof/proof-placements.json (hand-check sample in PROOF-RESULTS.md)');

// ---- 2. Live-path item 1: a NEW smart note -------------------------------
const note = {
  id: 'live-note-1', type: 'note',
  title: 'Sourdough on Sunday — what the slow rise taught me',
  nutshell: 'Home cooking, baking bread from a starter I keep on the counter. The kitchen smells like a bakery by noon.',
  body: 'The recipe is simple: flour, water, salt, time. Baking teaches patience the way nothing else does — you cannot rush a rise, you can only keep the starter alive and wait. Home cooking at its best.',
};
const pNote = AO.organize(note, {});
stamp('LIVE ITEM 1 — new smart note placed');
console.log(JSON.stringify(pNote, null, 2));

// ---- 3. Live-path item 2: a post ------------------------------------------
const post = {
  id: 'live-post-1', type: 'post',
  title: 'Sunrise on the Elk Trail — five quiet miles before the town woke up',
  body: 'Trail walking at dawn, birding along the ridge, the park empty except for us. Hiking the long way home.',
};
const pPost = AO.organize(post, {});
stamp('LIVE ITEM 2 — post placed');
console.log(JSON.stringify(pPost, null, 2));

// ---- 4. Live-path item 3: a contact ---------------------------------------
const contact = {
  id: 'live-contact-1', type: 'contact',
  name: 'Mara Ellison',
  about: 'Plays violin in a community orchestra, never misses a concert, teaches piano on Saturdays.',
  interests: ['concerts', 'playing instruments'],
};
const pContact = AO.organize(contact, {});
stamp('LIVE ITEM 3 — contact placed');
console.log(JSON.stringify(pContact, null, 2));

// ---- 5. User move overrides it -------------------------------------------
const moved = AO.moveItem(post, 'outdoors-travel', 'travel-exploration');
stamp('USER MOVE — citizen moves the trail post to Travel & Exploration');
console.log(JSON.stringify(moved, null, 2));
console.log('learned rules now:', JSON.stringify(AO.learnedRules(), null, 2));
const pPostAfterMove = AO.organize(post, {});
console.log('re-organize after move (override must win):', pPostAfterMove.subcategory, '| source:', pPostAfterMove.source);

// ---- 6. Learning: a second similar item follows the lesson ---------------
const post2 = {
  id: 'live-post-2', type: 'post',
  title: 'Morning trail walking on the ridge, then a road trip home',
  body: 'Trail walking before breakfast, then a road trip back down the valley.',
};
const pPost2 = AO.organize(post2, {});
stamp('LEARNING TEST — second similar post (without the rule, Hiking would win 4–3)');
console.log(JSON.stringify(pPost2, null, 2));

// ---- 7. Match handoff for each live item ----------------------------------
stamp('MATCH HANDOFF — what Smart Match receives for each placed item');
console.log('note matchInput:', JSON.stringify(pNote.matchInput, null, 2));
console.log('post matchInput (after move):', JSON.stringify(moved.matchInput, null, 2));
console.log('contact matchInput:', JSON.stringify(pContact.matchInput, null, 2));

stamp('PROOF END');
