import { chromium } from 'playwright';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const runtime = (process.env.NAYA_RUNTIME_URL || 'https://sparkling-shape-7ae5.smartnetpodcast.workers.dev').replace(/\/$/, '');
const boards = ['What Is Naya Power?','What Is Naya?','What Are Smart Notes?','Your Intelligence Today','Intelligence Reports','What Is the Intelligent Library?','Smart Lists','Smart Spaces','Smart Mail'];
const sidebar = ['Your Intelligence Today','Your Report','Intelligent Library','Smart Share','Smart Ledger','Your Connections','Smart Lists','Smart Spaces','Smart Mail','Settings'];
const layers = ['In a Nutshell','Human Note','Child Note','Grandma Note','Naya Note','Machine Note','Learning Lesson','What It Means','How to Use / How to Apply',"What's In It For You"];
const forbidden = ['Collective','Evidence','Smart Mail New','Providence','Truth','Protection','Source Separated','What/Human/Simple/Simplified/Why/Notice/Naya/Learning/So What/For You'];
const viewports = [['desktop',{width:1440,height:900}],['tablet',{width:1024,height:900}],['mobile',{width:390,height:844}]];

function assert(ok, message) { if (!ok) throw new Error(message); }
function sha256(buffer) { return createHash('sha256').update(buffer).digest('hex'); }
async function visibleButtonText(page, selector) { return page.locator(selector).evaluateAll((nodes) => nodes.filter((n) => { const s=getComputedStyle(n); const r=n.getBoundingClientRect(); return s.visibility!=='hidden' && s.display!=='none' && r.width>0 && r.height>0; }).map((n) => n.textContent.replace(/\s+/g,' ').trim())); }

try {
  const localIndex = await readFile('dist/index.html');
  const indexText = localIndex.toString('utf8');
  const assetMatch = indexText.match(/src="(\/assets\/[^\"]+\.js)"/);
  assert(assetMatch, 'source binding: built index.html does not reference a hashed JS asset');
  const assetPath = assetMatch[1];
  const runtimeIndexResponse = await fetch(`${runtime}/index.html?source-bind=${Date.now()}`, { cache: 'no-store' });
  assert(runtimeIndexResponse.ok, `source binding: runtime index HTTP ${runtimeIndexResponse.status}`);
  const runtimeIndex = Buffer.from(await runtimeIndexResponse.arrayBuffer());
  assert(sha256(runtimeIndex) === sha256(localIndex), 'source binding: deployed index.html hash differs from current build');
  const localAsset = await readFile(`dist${assetPath}`);
  const runtimeAssetResponse = await fetch(`${runtime}${assetPath}?source-bind=${Date.now()}`, { cache: 'no-store' });
  assert(runtimeAssetResponse.ok, `source binding: runtime JS HTTP ${runtimeAssetResponse.status}`);
  const runtimeAsset = Buffer.from(await runtimeAssetResponse.arrayBuffer());
  assert(sha256(runtimeAsset) === sha256(localAsset), 'source binding: deployed hashed JS asset differs from current build');
  console.log(`SOURCE_BINDING_PASS: index.html sha256=${sha256(localIndex)}`);
  console.log(`SOURCE_BINDING_PASS: ${assetPath} sha256=${sha256(localAsset)}`);

  const browser = await chromium.launch({ headless: true });
  try {
    for (const [name, viewport] of viewports) {
      const page = await browser.newPage({ viewport });
      const response = await page.goto(runtime, { waitUntil: 'networkidle', timeout: 30000 });
      assert(response?.ok(), `${name}: root HTTP response failed`);
      await page.waitForTimeout(250);

      const boardNodes = page.locator('.smart-board');
      assert(await boardNodes.count() === 9, `${name}: expected 9 Smart Boards`);
      const titles = await page.locator('.smart-board h2').allTextContents();
      for (const title of boards) assert(titles.includes(title), `${name}: missing board "${title}"`);

      const navTexts = await visibleButtonText(page, 'nav button');
      for (const label of sidebar) assert(navTexts.some((text) => text.includes(label)), `${name}: missing sidebar "${label}"`);

      const layerCounts = await boardNodes.evaluateAll((nodes) => nodes.map((board) => board.querySelectorAll('.layer-tab').length));
      assert(layerCounts.every((count) => count === 10), `${name}: every board must have 10 layer controls; got ${layerCounts.join(',')}`);
      const firstLayerTexts = await visibleButtonText(page, '.smart-board:first-of-type .layer-tab');
      for (const label of layers) assert(firstLayerTexts.some((text) => text.includes(label)), `${name}: missing layer "${label}"`);

      const actionTexts = await visibleButtonText(page, '.smart-board:first-of-type .board-actions button');
      for (const label of ['CREATE SPACE','FAVORITE','SAVE']) assert(actionTexts.some((text) => text.includes(label)), `${name}: missing action "${label}"`);

      for (const legacy of forbidden) {
        const exact = page.getByText(legacy, { exact: true });
        assert(await exact.count() === 0, `${name}: forbidden legacy label visible: "${legacy}"`);
      }

      const overflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 2);
      assert(overflow, `${name}: horizontal overflow detected`);

      if (name === 'desktop') {
        const navReport = page.locator('nav button').filter({ hasText: 'Your Report' });
        await navReport.click();
        assert(await navReport.evaluate((el) => el.classList.contains('active')), 'desktop: Your Report did not become active');
        assert(await page.locator('#smart-board-4').count() === 1, 'desktop: report board target missing');
        const favorite = page.locator('.smart-board:first-of-type .favorite');
        await favorite.click();
        assert((await favorite.innerText()).includes('★'), 'desktop: Favorite interaction did not change state');
        const save = page.locator('.smart-board:first-of-type .save');
        await save.click();
        assert((await save.innerText()).includes('SAVED'), 'desktop: Save interaction did not change state');
      }

      console.log(`RUNTIME_ACCEPTANCE_PASS: ${name} ${viewport.width}x${viewport.height}`);
      await page.close();
    }
    console.log(`RUNTIME_ACCEPTANCE_PASS: ${runtime}`);
  } finally {
    await browser.close();
  }
} catch (error) {
  console.error(`RUNTIME_ACCEPTANCE_FAIL: ${error.message}`);
  process.exitCode = 1;
}
