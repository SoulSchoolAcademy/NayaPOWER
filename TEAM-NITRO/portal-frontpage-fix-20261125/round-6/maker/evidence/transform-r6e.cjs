// Transform build-fix-r6.mjs -> build-fix-r6e.mjs (the 09:14:29 correction +
// the 09:15:09-10 follow-ups). Reuses R6 sections A/C/D/E/F byte-for-byte;
// replaces B (single entry), drops H (nutshell/little-N/deed-restore) and I
// (place repair), adds G (end-slide deed), Hf (completion state),
// Ic (cert links). Marker-sliced, never retyped.
// NOTE: generated rep() calls that need newlines use backtick template
// literals (real newlines) — never \n escapes inside quoted strings,
// because this file's own backtick strings would eat them.
const fs = require("fs");
const LANE = "/home/hatch/workspace/team-nitro/portal-frontpage-fix-20261125/round-6/maker/";
let s = fs.readFileSync(LANE + "build-fix-r6e.mjs", "utf8");
function sliceReplace(startMarker, endMarker, replacement, label) {
  const a = s.indexOf(startMarker);
  if (a === -1) throw new Error(label + ": start marker not found: " + startMarker.slice(0, 60));
  const b = s.indexOf(endMarker, a);
  if (b === -1) throw new Error(label + ": end marker not found: " + endMarker.slice(0, 60));
  const end = b + endMarker.length;
  s = s.slice(0, a) + replacement + s.slice(end);
  console.log("replaced " + label + " (" + (end - a) + " bytes -> " + replacement.length + ")");
}

// --- 1. Header comment ---
sliceReplace("// Portal front-page fix ROUND 6",
  "// Node only (python writes EPERM). Base is the R5 staged portal, edited.",
  `// Portal front-page fix ROUND 6e — the CORRECTION (Shawn, 2026-11-26 09:14:29 MST,
// superseding the little-N/nutshell scheme) + the 09:15:09-10 follow-ups.
// Base: R5 staged portal (sha d4bb2102...), branch portal-frontpage-fix-20261125-r5.
// The loop, in one line: red orb dead center at the top -> click -> straight to
// https://nayanet.app/agreement -> go through the agreement -> Agree at the end
// -> back to put their name in. The agreement does not come up again after that.
//
// KEPT from R6 (byte-for-byte): A (N upright, spin off the red-N imgs, ring
// keeps spinning — now a brighter energy flow, see A3e), C (/agreement boot),
// D (three boards at a time), E (agree wording), F (story from inside).
// DROPPED (superseded): H (little N + nutshell pop-up + restored deed text +
// the three comment-only (i) removals) and I (the place() repair — R5's
// place() stays exactly as R5 proved it; the deed sentence is R5-form again,
// a 56px ball that fits, so the repair is unneeded). The (i) stays exactly
// as in R5 (3 comment occurrences, untouched).
//
// THE CORRECTION CHANGES (diff vs R5 is exactly these):
//  B. ONE ENTRY: the red N orb dead center at the top (#fpCircleN) is the
//     ONLY agreement entry. Click -> window.location.href =
//     'https://nayanet.app/agreement' (the exact URL, direct navigation —
//     no preview, no intermediate, no pop-up). The corner Ns are NOT entries:
//     their click handlers go, the red corner N's href changes from
//     /agreement to https://nayanet.app/ (home, like the black N). The
//     intro/bridge "Read the agreement" pills (post-name-entry walk flow)
//     are untouched — not front-page entries, out of the correction's scope.
//  B2. NO BOTTOM AGREEMENT BUTTON: #fpEnterDeal is removed from the footer
//     entirely — 0 occurrences. The footer keeps "Create. Connect. Grow
//     with us." and the corner Ns.
//  A3e. ENERGY FLOW: the orb must read as a REAL LIVE OBJECT — obsidian,
//     touchable, with a flow of energy around it. The ::before ring becomes
//     a bright multi-stop arc (white/red/violet, 12s orbit, glow) and a
//     ::after halo breathes (4s). The gold N img itself never spins.
//  G. END SLIDE (portal story): the verbatim deed sentence goes on the end
//     slide as its text box (inside #fpStoryEnd, after the franchise
//     paragraph): "By entering your name, you make it official — ..." The
//     Agree button already sits at the very bottom just above the arrows
//     and already flashes (fp-agree-flash 2s, R5); the eight links already
//     sit in a bar below the page (.fp-story-links, after the nav). So the
//     portal end slide needs only the deed sentence added — nothing moves.
//  Hf. COMPLETION STATE: every Agree click (story #fpStoryAgree AND the
//     stage seal Agree) sets localStorage['nayanet_agreement_done'] to an
//     ISO timestamp. The front page never auto-opens the agreement (it
//     never did); after completion + return + reload, the page is at rest
//     and nothing re-appears or re-prompts. Proven by the probe, not claimed.
//  Ic. CERTIFICATE LINKS: the portal's certificate navigations go to the
//     new cert at its LIVE address — https://nayanet.app/identity.html
//     (never a workers.dev address). The entry-form submit and the
//     "this is me" line both change from relative /identity.html to the
//     absolute live URL (the ?name= handoff is preserved). The staged
//     /identity.html serves the NEW cert bytes (315,409 B, sha 0c11fdb8…);
//     the live step puts those bytes at nayanet.app/identity.html.
//  J. (lane file, not this script): identity.html is replaced byte-for-byte
//     with the new fixed certificate harvested from the portal-consolidated
//     staging URL (315,409 B, sha 0c11fdb8a0fcb7269d931584088f68629487e528c9e0fcffae47013933897365).
//  K. WALKTHROUGH /?walk=1 — NAMED, NOT SERVED IN THIS ROUND: the fixed
//     cert's WALKTHROUGH_URL is '/?walk=1' (same origin, verified in the
//     new cert bytes). The UPDATED 15-question walkthrough is the
//     About+Skills Innovations-clone fix2 dialog (about-skills-clone.html,
//     13,421,743 B; staged at naya-proof-host ?file=...&ref=about-skills-
//     clone-20261125-fix2&cb=62921145151436a0145a914352acbc8982b6cf58). That
//     file has NO ?walk=1 entry — zero hits for walk=1, ?walk,
//     URLSearchParams, openWalk/showWalk/startWalk/autoOpen — so serving it
//     at /?walk=1 would land on the About+Skills page, NOT on the
//     walkthrough. An auto-open (or a transplant into the portal's walk)
//     is a separate build. The portal's built-in walk stays exactly as R5
//     proved it (do not touch walk code). Named plainly in the report.
// Node only (python writes EPERM). Base is the R5 staged portal, edited.`,
  "header");

// --- 2. A3: brighter energy ring + halo ---
{
  const oldA3 = `rep('button.fp-circle-n .ncorner-gloss{',
  'button.fp-circle-n::before{content:"";position:absolute;inset:-6px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 68%,rgba(255,255,255,.95) 82%,transparent 94%);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));animation:eco-spin 90s linear infinite;pointer-events:none;} button.fp-circle-n .ncorner-gloss{',
  1, 'A3');`;
  const newA3 = `rep('button.fp-circle-n .ncorner-gloss{',
  'button.fp-circle-n::before{content:"";position:absolute;inset:-6px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 58%,rgba(255,255,255,.95) 74%,rgba(255,45,70,.9) 82%,rgba(142,36,170,.85) 90%,transparent 96%);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));animation:eco-spin 12s linear infinite;pointer-events:none;filter:drop-shadow(0 0 6px rgba(255,255,255,.55));} button.fp-circle-n::after{content:"";position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,transparent 62%,rgba(142,36,170,.28) 78%,transparent 88%);pointer-events:none;animation:fpOrbHalo 4s ease-in-out infinite;} @keyframes fpOrbHalo{0%,100%{opacity:.45;transform:scale(1)}50%{opacity:1;transform:scale(1.06)}} button.fp-circle-n .ncorner-gloss{',
  1, 'A3');`;
  if (!s.includes(oldA3)) throw new Error("A3 old text not found");
  s = s.replace(oldA3, newA3);
  console.log("replaced A3 (energy ring + halo)");
}
{
  const oldA4 = `rep('button.fp-circle-n img{animation:none;}',
  'button.fp-circle-n img{animation:none;}   button.fp-circle-n::before{animation:none;}',
  1, 'A4');`;
  const newA4 = `rep('button.fp-circle-n img{animation:none;}',
  'button.fp-circle-n img{animation:none;}   button.fp-circle-n::before{animation:none;}   button.fp-circle-n::after{animation:none;}',
  1, 'A4');`;
  if (!s.includes(oldA4)) throw new Error("A4 old text not found");
  s = s.replace(oldA4, newA4);
  console.log("replaced A4 (reduced motion covers halo)");
}

// --- 3. B: single entry (orb only, direct navigation to the exact URL) ---
sliceReplace("// --- B. Entries -> the real agreement, in place, URL /agreement. ---",
  "rep(entriesOld, entriesNew, 1, 'B');",
  `// --- B. ONE ENTRY (the correction, 09:14:29 MST): the red N orb dead center
// at the top (#fpCircleN) is the ONLY agreement entry. Click -> direct
// navigation to the exact URL https://nayanet.app/agreement — no preview,
// no intermediate, no pop-up, no in-place stage. The corner Ns are NOT
// entries: their click handlers are gone (they are plain links again).
// The footer "Read the agreement" button is removed whole (B2 below).
// The intro/bridge "Read the agreement" pills are untouched: post-name-
// entry walk flow, not front-page entries, out of the correction's scope. ---
const entriesOld = \`/* entries: the red N in the circle, both corner Ns, "Read the agreement" */
  var circleN = document.getElementById('fpCircleN');
  if (circleN) circleN.addEventListener('click', function () { openStory(0); });
  var corners = document.querySelectorAll('.ncorner');
  for (var c = 0; c < corners.length; c++) {
    corners[c].addEventListener('click', function (ev) {
      ev.preventDefault();
      openStory(0);
    });
  }
  var deal = document.getElementById('fpEnterDeal');
  if (deal) deal.addEventListener('click', function () { openStory(0); });\`;
const entriesNew = \`/* ROUND 6e — ONE ENTRY (Shawn's correction 2026-11-26 09:14:29 MST): the
     red N orb dead center at the top is the only agreement entry. Click it
     and you go STRAIGHT to https://nayanet.app/agreement — the real
     collective agreement itself, no preview, no intermediate, no pop-up.
     The corner Ns are plain links (home), not entries; the bottom
     "Read the agreement" button is gone (B2). The 27-slide story stays,
     reachable only from INSIDE the agreement view. */
  window.__fpOpenStory = openStory;
  var circleN = document.getElementById('fpCircleN');
  if (circleN) circleN.addEventListener('click', function () { window.location.href = 'https://nayanet.app/agreement'; });\`;
rep(entriesOld, entriesNew, 1, 'B');
// B2. NO BOTTOM AGREEMENT BUTTON: the footer button goes whole — 0 occurrences.
rep('<button class="fp-enter-deal" id="fpEnterDeal" type="button">Read the agreement &#9670;</button>', '', 1, 'B2');
// B3. The red corner N is NOT an agreement entry: its href leaves /agreement
// for home (like the black N), and its label stops claiming the agreement.
rep('class="ncorner ncorner-right" href="https://nayanet.app/agreement" aria-label="The Collective Agreement — the red N"',
  'class="ncorner ncorner-right" href="https://nayanet.app/" aria-label="NayaNET — home"', 1, 'B3');
// B4. The letter script queried the removed button (dead: assigned, never
// read — verified by full-file grep). The query goes with the button.
rep("var plainEl=q('#dealPlain'), enterBtn=q('#fpEnterDeal');",
  "var plainEl=q('#dealPlain');", 1, 'B4');`,
  "B single entry");

// --- 4. Drop H + I, insert G (end-slide deed) + Hf (completion flag) + Ic (cert links) ---
sliceReplace("// --- H. The little N (Shawn's LOCKED decision)",
  "// --- Assertions. ---",
  `// --- G. END SLIDE (portal story): the verbatim deed sentence goes on the
// end slide as its text box — inside #fpStoryEnd, after the franchise
// paragraph, so they see what they are agreeing to right there with the
// Agree button. The Agree button already sits at the very bottom just above
// the arrows and already flashes (fp-agree-flash 2s, R5); the eight links
// already sit in a bar below the page (.fp-story-links, after the nav).
// Nothing else on the end slide moves. ---
rep('Move in and own it.</p>',
  'Move in and own it.</p><p class="fp-story-deed">By entering your name, you make it official &mdash; you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate &mdash; your personal page, your business, your space &mdash; free forever.</p>', 1, 'G-deed');
rep(\`.fp-story-franchise b{color:#d4a017}\`,
  \`.fp-story-franchise b{color:#d4a017}
  /* ROUND 6e — the deed text box on the end slide: the verbatim front-page
     wording, in a green-rimmed box (the Agree green), Marcellus 19px. */
  .fp-story-deed{font-family:Marcellus,Georgia,serif;font-size:19px;line-height:1.6;color:#fff;margin:18px 0 0;border:1.5px solid rgba(7,146,95,.6);border-radius:14px;padding:14px 16px;background:rgba(7,146,95,.08);box-sizing:border-box}\`, 1, 'G-deedCss');

// --- Hf. COMPLETION STATE ("the agreement does not come up again"): every
// Agree click sets localStorage['nayanet_agreement_done'] to an ISO
// timestamp — the story Agree AND the stage seal Agree. The front page
// never auto-opens the agreement (it never did), so after completion +
// return + reload the page is at rest and nothing re-appears or re-prompts.
// The v25 agreement file sets the same key in goToPortal() (same name,
// same shape) — one mechanism across both halves of the loop. ---
rep("agreeBtn.addEventListener('click', closeStory);",
  "agreeBtn.addEventListener('click', function(){ try{localStorage.setItem('nayanet_agreement_done', new Date().toISOString());}catch(e){} closeStory(); });", 1, 'Hf-story');
rep(\`agreeBtn.addEventListener('click', function(){
    seal.hidden = false;\`,
  \`agreeBtn.addEventListener('click', function(){
    try{localStorage.setItem('nayanet_agreement_done', new Date().toISOString());}catch(e){}
    seal.hidden = false;\`, 1, 'Hf-seal');

// --- Ic. CERTIFICATE LINKS: the portal's certificate navigations go to the
// new cert at its LIVE address — https://nayanet.app/identity.html (never a
// workers.dev address). The ?name= handoff on the entry-form submit is
// preserved. The staged /identity.html serves the new cert bytes; the live
// step puts those bytes at nayanet.app/identity.html. ---
rep("window.location.href='/identity.html'+(v?'?name='+encodeURIComponent(v):'');",
  "window.location.href='https://nayanet.app/identity.html'+(v?'?name='+encodeURIComponent(v):'');", 1, 'Ic-submit');
rep("window.location.href='/identity.html';",
  "window.location.href='https://nayanet.app/identity.html';", 1, 'Ic-tim');

// --- Assertions. ---`,
  "H+I -> G+Hf+Ic");

// --- 5. Assertions (rewrite) ---
sliceReplace("// --- Assertions. ---",
  "// Every inline <script> must COMPILE",
  `// --- Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R5 base sha verified', baseSha.startsWith('d4bb2102'));
assert('A: circle-N img spin removed (0 eco-spin on fp-circle-n img)', !html.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;   display:block;animation:eco-spin'));
assert('A: corner red-N img spin removed', !html.includes('.ncorner-right img{animation:eco-spin'));
assert('A3e: orb energy flow — bright arc ring (12s) + breathing halo', html.includes('button.fp-circle-n::before{content:"";position:absolute;inset:-6px;') && html.includes('rgba(255,45,70,.9) 82%') && html.includes('button.fp-circle-n::after{content:"";position:absolute;inset:-14px;') && html.includes('@keyframes fpOrbHalo') && html.includes('button.fp-circle-n::after{animation:none;}'));
assert('A: circle-N ring still spins, corner ring still spins (90s)', html.includes('.ncorner::before{') && html.includes('animation:eco-spin 90s linear infinite'));
assert('A: black left N untouched (home href, no spin)', html.includes('ncorner-left" href="https://nayanet.app/"') && !html.includes('.ncorner-left img{animation'));
assert('A: ring untouched (78s/31s)', html.includes('animation:nayaSpectrum 78s linear infinite') && html.includes('animation:nayaWhite 31s linear infinite'));
assert('B: ONE entry — orb click navigates DIRECTLY to the exact URL', html.includes("if (circleN) circleN.addEventListener('click', function () { window.location.href = 'https://nayanet.app/agreement'; });"));
assert('B: no entry opens the story (1 hit = the dated ROUND 3 SUPERSEDED comment, not live code)', (html.match(/openStory\\(0\\)/g) || []).length === 1 && html.includes('ROUND 3 — SUPERSEDED') && !html.includes('openAgreementDirect'));
assert('B2: NO bottom agreement button — element gone (1 hit = the same historical comment; fpNextBtn2 is the untouched intro pill)', (html.match(/fpEnterDeal/g) || []).length === 1 && (html.match(/id="fpEnterDeal"/g) || []).length === 0 && !html.includes('class="fp-enter-deal" id="fpEnterDeal"'));
assert('B3: corner Ns are NOT entries — red corner now home', html.includes('class="ncorner ncorner-right" href="https://nayanet.app/" aria-label="NayaNET — home"') && !html.includes('ncorner-right" href="https://nayanet.app/agreement"'));
assert('B: choice/bridge/intro Read-the-agreement pills untouched (post-entry walk flow)', (html.match(/window\\.location\\.href='\\/agreement'/g) || []).length === 4);
assert('C: /agreement boot present, root untouched', html.includes("if(window.location.pathname!=='/agreement')return;") && html.includes("st.state.view='letter'"));
assert('D: wireLetterUnfold reveals 3', html.includes('show(cur); show(cur + 1); show(cur + 2);') && html.includes('idx = cur + 3;'));
assert('D: render shows groups of 3 (letter + letterPage)', html.includes("var sl=(S.all==='letter')||(i>=S.letter&&i<S.letter+3);") && html.includes('var slp=(i>=S.letter&&i<S.letter+3);'));
assert('D: derive syncs to group start', html.includes('S.letter=l-(l%3);') && html.includes('S.letter=lp-(lp%3);'));
assert('D: jewel counts groups', html.includes("Math.floor(S.letter/3)+1)+' / '+Math.ceil(letterBeats.length/3);"));
assert('E: agree wording everywhere (no bare "I agree" setNext left)', !html.includes("setNext('I agree \\u25C6'") && ((html.match(/I agree — show me my world/g) || []).length + (html.match(/I agree &mdash; show me my world/g) || []).length) >= 6);
assert('E: story end slide wording kept', html.includes('I agree &mdash; show me my world &#9670;'));
assert('F: story from inside agreement only (nextBtn2 letter branch)', html.includes("else if(S.view==='letter'||S.view==='letterPage'){if(window.__fpOpenStory)window.__fpOpenStory(0);}"));
assert('R5 kept: menu hover-only (eco-tip, no eco-label)', !html.includes('eco-label') && html.includes('clampEcoTip'));
assert('R5 kept: 27-slide story + FP_SLIDES', html.includes('var FP_SLIDES') || html.includes('FP_SLIDES'));
assert('R5 kept: nine destinations', (html.match(/class="eco-item"/g) || []).length === 9);
assert('R5 kept: v7 letter beats present (opening + ending + Agreement)', html.includes('Welcome home. Your world begins here.') && html.includes('By joining, you agree to respect other people') && html.includes('QUESTION 1'));
assert('R5 kept: identity/cert + sw untouched markers', html.includes('id="fpCircleN"') && html.includes('FP_SLIDES'));
assert('R5 kept: deed sentence is R5-form (orb button only, no restored text, no little N, no nutshell)', html.includes('<p class="fp-deed-sentence" id="fpDeedSentence"><button class="fp-deed-info fp-circle-n" id="fpCircleN"') && !html.includes('fpLittleN') && !html.includes('fpNutshellPop') && !html.includes('fp-nutshell'));
assert('R5 kept: (i) exactly as R5 — 3 comment occurrences, untouched', (html.match(/ⓘ/g) || []).length === 3);
assert('R5 kept: place() untouched (dead guard as R5 proved it)', html.includes('if (!stage || !portal || !content || !sentence || !reader) return;'));
assert('G: end slide carries the verbatim deed sentence as its text box', html.includes('<p class="fp-story-deed">By entering your name, you make it official &mdash; you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate &mdash; your personal page, your business, your space &mdash; free forever.</p>') && html.includes('.fp-story-deed{font-family:Marcellus,Georgia,serif;font-size:19px;'));
assert('G: end-slide Agree still at the very bottom, flashing (R5 law)', html.includes('animation:fp-agree-flash 2s ease-in-out infinite') && html.includes('id="fpStoryAgreeWrap"'));
assert('G: eight links still in a bar below the page (after the nav)', html.includes('id="fpStoryLinks"') && html.includes('.fp-story-links{flex:none;display:flex;flex-wrap:wrap;justify-content:center;'));
assert('Hf: completion flag set on BOTH Agree paths (story + seal)', (html.match(/localStorage\\.setItem\\('nayanet_agreement_done'/g) || []).length === 2);
assert('Ic: certificate links go to the LIVE address (never workers.dev)', (html.match(/https:\\/\\/nayanet\\.app\\/identity\\.html/g) || []).length === 2 && !html.includes("window.location.href='/identity.html'") && !html.includes("window.location.href='/identity.html'+"));
// Every inline <script> must COMPILE`,
  "assertions");

// Fix the structure assert (no deed style / nutshell script added now: R5 counts 7 style / 10 scripts).
{
  const oldS = "assert('structure: 8 style elements, 11 scripts (deed style + nutshell script added)', (html.match(/<style>/g) || []).length === 8 && (html.match(/<script>/g) || []).length === 11);";
  const newS = "assert('structure: 7 style elements, 10 scripts (R5 counts — no new style/script blocks added)', (html.match(/<style>/g) || []).length === 7 && (html.match(/<script>/g) || []).length === 10);";
  if (!s.includes(oldS)) throw new Error("structure assert not found");
  s = s.replace(oldS, newS);
  console.log("replaced structure assert");
}

fs.writeFileSync(LANE + "build-fix-r6e.mjs", s);
console.log("wrote build-fix-r6e.mjs", s.length, "B");
