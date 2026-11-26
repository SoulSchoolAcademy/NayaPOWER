// Portal front-page fix ROUND 6f — the fix round on the R6e build.
// Base: R6e portal (sha 01051a8f...), branch portal-frontpage-fix-20261125-r6.
// Captain's decision: REPOINT, do not amend the brief.
//
// D1. Repoint the three stage handlers (#fpChoiceLetter, #fpBridgeLetter,
//     #fpNextBtn2 — 4 relative '/agreement' navigations) to the exact
//     absolute URL https://nayanet.app/agreement. The orb (#fpCircleN)
//     already uses the exact URL — untouched. Final entry count: 4 of 4.
// D2. Zero "Read the agreement" occurrences in the build. The three
//     handlers carry that label/text — RELABELLED (not deleted): the
//     buttons keep working (they still open the agreement, now at the
//     exact URL; #fpNextBtn2 keeps its other function — opening the
//     in-place story in letter views). New label everywhere: "The
//     agreement ◆" — plain, short (fits the nowrap choice buttons), and
//     it contains neither "Read the agreement" nor "Read the full
//     agreement" (the deck-end text is relabelled too, for consistency).
//     The two dated comments that quoted the old label are reworded so
//     the string count is 0, not 6. #fpEnterDeal stays gone.
// D5d. Portal story-end deed box cut at the panel bottom on arrival at
//     desk: render() pinned the board scrollTop to 0 on every slide. On
//     the last slide it now scrolls the board just enough that the deed
//     box is whole (bottom visible + 16px margin). Other slides still
//     start at the top. Nothing else on the end slide moves.
// Node only (python writes EPERM). Base is the R6e lane portal, edited.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;

const base = readFileSync(LANE + 'portal.html');
const baseSha = sha(base);
if (baseSha !== '01051a8fb76f9b948a75505f7c6baa39a3f7d3fcd82be637448e344f23b3bc59')
  throw new Error('R6e base sha mismatch: ' + baseSha);
let html = base.toString('utf8');
const count = (sub) => html.split(sub).length - 1;
const rep = (oldS, newS, n, label) => {
  const c = html.split(oldS).length - 1;
  if (c !== n) throw new Error(label + ': expected ' + n + ' occurrence(s), found ' + c + ' :: ' + oldS.slice(0, 80));
  html = html.split(oldS).join(newS);
};

// --- D1. Repoint all four relative '/agreement' navigations. ---
rep("window.location.href='/agreement'", "window.location.href='https://nayanet.app/agreement'", 4, 'D1-repoint');

// --- D2. Relabel the three "Read the agreement" buttons. ---
rep('>Read the agreement &#9670;</button>', '>The agreement &#9670;</button>', 1, 'D2-nextBtn2-html');
rep('>Read the agreement <span class="fp-btn-jewel"', '>The agreement <span class="fp-btn-jewel"', 2, 'D2-choice-bridge-html');
rep("nextBtn2.textContent='Read the agreement \\u25C6';", "nextBtn2.textContent='The agreement \\u25C6';", 1, 'D2-updateChrome-intro');
rep("nextBtn2.textContent='Read the full agreement \\u25C6';", "nextBtn2.textContent='The agreement \\u25C6';", 1, 'D2-updateChrome-deckend');
// D2. Reword the two dated comments that quoted the old label.
rep("login's 'Read the agreement' button", "login's agreement button", 1, 'D2-comment-4706');
rep('"Read the agreement" button is gone (B2).', 'the bottom agreement button is gone (B2).', 1, 'D2-comment-4882');

// --- D5d. Story-end deed box whole on arrival (desk). ---
rep(`    var board = story.querySelector('.fp-story-board');
    if (board) board.scrollTop = 0;`,
`    var board = story.querySelector('.fp-story-board');
    /* ROUND 6f (D5d) — on the last slide the deed box was cut at the panel
       bottom on arrival: scroll the board just enough that the deed box is
       whole (its bottom visible, 16px margin) instead of pinning the top.
       Other slides still start at the top. */
    if (board) { if (last) { var deed = endBox.querySelector('.fp-story-deed'); if (deed) board.scrollTop = Math.max(0, board.scrollTop + deed.getBoundingClientRect().bottom - board.getBoundingClientRect().bottom + 16); else board.scrollTop = 0; } else board.scrollTop = 0; }`,
  1, 'D5d-board-scroll');

// --- Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R6e base sha verified', baseSha.startsWith('01051a8f'));
assert('D1: zero relative /agreement navigations left', count("window.location.href='/agreement'") === 0);
assert('D1: 4 of 4 agreement entries on the exact URL (orb + 3 stage handlers)', count("window.location.href='https://nayanet.app/agreement'") === 4 && count("window.location.href = 'https://nayanet.app/agreement'") === 1);
assert('D2: zero "Read the agreement" occurrences in the whole file', count('Read the agreement') === 0);
assert('D2: zero "Read the full agreement" occurrences', count('Read the full agreement') === 0);
assert('D2: the three buttons relabelled "The agreement" (HTML 3 + JS 2)', count('>The agreement') === 3 && count("textContent='The agreement") === 2);
assert('D2: #fpNextBtn2 keeps its story function in letter views', html.includes("else if(S.view==='letter'||S.view==='letterPage'){if(window.__fpOpenStory)window.__fpOpenStory(0);}"));
assert('D2: #fpEnterDeal still gone (0 element, 1 dated comment)', (html.match(/fpEnterDeal/g) || []).length === 1 && (html.match(/id="fpEnterDeal"/g) || []).length === 0);
assert('D5d: board scrolls deed whole on last slide', html.includes("deed.getBoundingClientRect().bottom - board.getBoundingClientRect().bottom + 16"));
assert('R6e kept: orb navigates DIRECTLY to the exact URL', html.includes("if (circleN) circleN.addEventListener('click', function () { window.location.href = 'https://nayanet.app/agreement'; });"));
assert('R6e kept: corner Ns are home links, not entries', html.includes('class="ncorner ncorner-right" href="https://nayanet.app/" aria-label="NayaNET — home"'));
assert('R6e kept: orb energy ring + halo, N upright', html.includes('animation:eco-spin 12s linear infinite') && html.includes('@keyframes fpOrbHalo') && !html.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;   display:block;animation:eco-spin'));
assert('R6e kept: completion flag on BOTH Agree paths', (html.match(/localStorage\.setItem\('nayanet_agreement_done'/g) || []).length === 2);
assert('R6e kept: certificate links at the LIVE address', (html.match(/https:\/\/nayanet\.app\/identity\.html/g) || []).length === 2);
assert('R6e kept: /agreement boot present (fallback)', html.includes("if(window.location.pathname!=='/agreement')return;"));
assert('R6e kept: three boards at a time', html.includes('show(cur); show(cur + 1); show(cur + 2);'));
assert('R6e kept: story end slide deed + agree wording', html.includes('I agree &mdash; show me my world &#9670;') && html.includes('<p class="fp-story-deed">By entering your name, you make it official'));
assert('R6e kept: 27-slide story + FP_SLIDES', html.includes('FP_SLIDES'));
assert('R6e kept: (i) exactly as R5 (3 comment occurrences)', (html.match(/ⓘ/g) || []).length === 3);
assert('R6e kept: menu hover-only (eco-tip, no eco-label)', !html.includes('eco-label') && html.includes('.eco-item .eco-tip{'));
assert('R6e kept: nine destinations', (html.match(/class="eco-item"/g) || []).length === 9);
assert('structure: 7 style elements, 10 scripts', (html.match(/<style>/g) || []).length === 7 && (html.match(/<script>/g) || []).length === 10);
{
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  let bad = [];
  blocks.forEach((code, i) => { try { new vm.Script(code); } catch (e) { bad.push(i + ': ' + e.message); } });
  assert('all ' + blocks.length + ' inline scripts compile (vm.Script)', bad.length === 0);
  if (bad.length) console.log('  COMPILE FAILURES: ' + bad.join(' | '));
}

const out = Buffer.from(html, 'utf8');
writeFileSync(LANE + 'portal-r6f.html', out);
console.log('portal-r6f.html', out.length, 'B sha256', sha(out));
console.log('R6e portal was', base.length, 'B; delta', out.length - base.length, 'B');
