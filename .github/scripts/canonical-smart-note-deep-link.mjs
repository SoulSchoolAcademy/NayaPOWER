import { chromium } from 'playwright';
import crypto from 'node:crypto';
import fs from 'node:fs';

const hub = process.env.HUB_URL;
if (!hub) throw new Error('HUB_URL_REQUIRED');

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ serviceWorkers: 'block', viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();

const alias = ('golden' + Date.now() + crypto.randomBytes(3).toString('hex')).slice(0, 48).toLowerCase();
const title = 'Canonical Smart Note Deep-Link Golden Path ' + new Date().toISOString();
const content = 'Real human Smart Note regression proof: capture, canonical Intelligent Block identity, source-event provenance, deep-link retrieval, Feed, Activity, and reload continuity.';
const trace = [];
const mark = (step, extra = {}) => {
  trace.push({ step, at: new Date().toISOString(), ...extra });
  console.log('CANONICAL_SN_DEEPLINK_TRACE', JSON.stringify(trace.at(-1)));
};

try {
  await page.goto(hub + '/?name=' + encodeURIComponent('Naya Golden') + '&alias=' + encodeURIComponent(alias), {
    waitUntil: 'networkidle',
    timeout: 60000
  });
  await page.waitForFunction(() => !!window.NayaNETNameFirstAuth?.establish, { timeout: 30000 });
  const auth = await page.evaluate(({ alias }) =>
    window.NayaNETNameFirstAuth.establish({ name: 'Naya Golden', alias }), { alias });
  if (!auth?.authenticated || !auth?.userId) throw new Error('AUTHENTICATION_FAILED');
  mark('AUTHENTICATED', { userId: auth.userId });

  await page.waitForFunction(() => !!window.NayaAssistantRuntime?.captureSmartNote, { timeout: 30000 });
  await page.evaluate(() => {
    window.__cap = null;
    const rt = window.NayaAssistantRuntime;
    const old = rt.captureSmartNote.bind(rt);
    rt.captureSmartNote = async (...args) => {
      const result = await old(...args);
      window.__cap = result;
      return result;
    };
  });

  await page.locator('[data-ws-action="open-notes"]').first().click();
  await page.getByTestId('smart-note-title').fill(title);
  await page.getByTestId('smart-note-content').fill(content);
  await page.getByTestId('smart-note-capture-submit').click();
  await page.waitForFunction(() => !!window.__cap, { timeout: 30000 });

  const capture = await page.evaluate(() => window.__cap);
  const ibId = capture?.intelligent_block_id;
  const eventId = capture?.event?.event_id || capture?.event_id;
  const transactionId = capture?.transaction?.id;
  if (!/^IB-\d{6}$/.test(String(ibId || ''))) throw new Error('CANONICAL_IB_ID_MISSING');
  if (!eventId || !transactionId) throw new Error('CAPTURE_LINEAGE_INCOMPLETE');
  mark('CAPTURE_VERIFIED', { ibId, eventId, transactionId });

  const db = await page.evaluate(async ({ ibId, userId, eventId }) => {
    const { data, error } = await window.__NayaNETSupabaseClient
      .from('nayanet_intelligent_blocks')
      .select('intelligent_block_id,owner_id,source_event_ids,provenance,status,schema_version')
      .eq('intelligent_block_id', ibId)
      .eq('owner_id', userId)
      .maybeSingle();
    return { data, error: error?.message || null };
  }, { ibId, userId: auth.userId, eventId });
  if (db.error || !db.data || !db.data.source_event_ids.includes(eventId)) {
    throw new Error('DB_PROVENANCE_FAILED:' + JSON.stringify(db));
  }
  mark('DATABASE_PROVENANCE_VERIFIED', { ibId, eventId, source_event_ids: db.data.source_event_ids });

  const deepUrl = hub + '/hub?ib=' + encodeURIComponent(ibId);
  await page.goto(deepUrl, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForFunction(
    () => document.documentElement.dataset.nayaDeepLinkStatus === 'resolved' &&
      !!document.querySelector('[data-naya-deep-link-target="true"]'),
    { timeout: 30000 }
  );
  const deep = await page.evaluate(() => ({
    status: document.documentElement.dataset.nayaDeepLinkStatus,
    ib: document.documentElement.dataset.nayaDeepLinkIb,
    event: document.documentElement.dataset.nayaDeepLinkEvent,
    target: [...document.querySelectorAll('[data-naya-deep-link-target="true"]')].map(x => ({
      ib: x.dataset.intelligenceId,
      event: x.dataset.eventId,
      source: x.dataset.sourceEventId
    })),
    url: location.href
  }));
  if (deep.ib !== ibId || deep.event !== eventId || deep.target[0]?.ib !== ibId || deep.target[0]?.event !== eventId) {
    throw new Error('DEEP_LINK_IDENTITY_FAILED:' + JSON.stringify(deep));
  }
  mark('DEEP_LINK_VERIFIED', deep);

  await page.reload({ waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForFunction(
    () => document.documentElement.dataset.nayaDeepLinkStatus === 'resolved' &&
      !!document.querySelector('[data-naya-deep-link-target="true"]'),
    { timeout: 30000 }
  );
  const reload = await page.evaluate(() => ({
    status: document.documentElement.dataset.nayaDeepLinkStatus,
    ib: document.documentElement.dataset.nayaDeepLinkIb,
    event: document.documentElement.dataset.nayaDeepLinkEvent,
    target: [...document.querySelectorAll('[data-naya-deep-link-target="true"]')].map(x => ({
      ib: x.dataset.intelligenceId,
      event: x.dataset.eventId,
      source: x.dataset.sourceEventId
    })),
    url: location.href
  }));
  if (reload.ib !== ibId || reload.event !== eventId || reload.target[0]?.ib !== ibId || reload.target[0]?.event !== eventId) {
    throw new Error('RELOAD_IDENTITY_FAILED:' + JSON.stringify(reload));
  }
  mark('RELOAD_IDENTITY_VERIFIED', reload);

  await page.goto(hub + '/feed?event_id=' + encodeURIComponent(eventId) + '&stream=personal&golden=1', {
    waitUntil: 'networkidle',
    timeout: 60000
  });
  const feedSelector = '#blocks [data-real-smart-note][data-event-id="' + eventId + '"]';
  await page.locator(feedSelector).waitFor({ state: 'visible', timeout: 30000 });
  const feedMatch = await page.locator(feedSelector).count();
  if (feedMatch !== 1) throw new Error('FEED_EVENT_NOT_RENDERED');
  mark('FEED_VERIFIED', { eventId, count: feedMatch });

  const activity = page.locator('.feedNav button[data-feed="activity"]');
  await activity.waitFor({ state: 'visible', timeout: 30000 });
  await activity.click();
  await page.waitForFunction(
    () => document.querySelector('.feedNav button[data-feed="activity"]')?.classList.contains('active'),
    { timeout: 30000 }
  );
  await page.locator(feedSelector).waitFor({ state: 'visible', timeout: 30000 });
  const activityMatch = await page.locator(feedSelector).count();
  if (activityMatch !== 1) throw new Error('ACTIVITY_EVENT_NOT_RENDERED');
  mark('ACTIVITY_VERIFIED', { eventId, count: activityMatch });

  const proof = {
    status: 'VERIFIED',
    auth_user_id: auth.userId,
    smart_note: { title, event_id: eventId, transaction_id: transactionId, intelligent_block_id: ibId },
    db_provenance: db.data,
    deep_link: deep,
    reload,
    feed_match: feedMatch,
    activity_match: activityMatch,
    checks: {
      capture: 'PASS',
      persistence: 'PASS',
      canonical_ib_identity: 'PASS',
      source_event_provenance: 'PASS',
      deep_link_resolved: 'PASS',
      deep_link_dom_identity: 'PASS',
      reload_identity: 'PASS',
      feed: 'PASS',
      activity: 'PASS'
    },
    trace
  };
  fs.writeFileSync(process.env.PROOF_PATH || 'canonical-smart-note-deep-link-proof.json', JSON.stringify(proof, null, 2) + '\n');
  console.log(JSON.stringify(proof));
} finally {
  await context.close();
  await browser.close();
}
