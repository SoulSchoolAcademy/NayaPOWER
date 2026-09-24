import { chromium } from 'playwright';
import crypto from 'node:crypto';
import fs from 'node:fs';

const hub = process.env.HUB_URL;
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_PUBLISHABLE_KEY;
const run = process.env.GITHUB_RUN_ID || 'local-disposition-audit';
const alias = ('disposition' + run + '-' + crypto.randomBytes(4).toString('hex')).toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 48);

if (!hub || !supabaseUrl || !supabaseKey) {
  console.error('Missing env: HUB_URL / SUPABASE_URL / SUPABASE_PUBLISHABLE_KEY');
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  let ownerId = null;
  let audit = null;
  try {
    await page.goto(hub + '/?disposition_audit_run=' + encodeURIComponent(run), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForFunction(() => !!window.NayaNETNameFirstAuth?.establish, { timeout: 30000 });
    const identity = await page.evaluate(async ({ alias }) =>
      await window.NayaNETNameFirstAuth.establish({ name: 'Legacy Cognition Disposition Audit', alias }), { alias });
    if (!identity?.authenticated || !identity?.userId) throw new Error('OWNER_IDENTITY_NOT_ESTABLISHED');
    ownerId = identity.userId;

    const session = await page.evaluate(async () => {
      const c = window.__NayaNETSupabaseClient;
      const s = c ? (await c.auth.getSession()).data.session : null;
      return s ? { userId: s.user.id, access_token: s.access_token } : null;
    });
    if (!session?.access_token || session.userId !== ownerId) throw new Error('OWNER_SESSION_NOT_ESTABLISHED');

    const rpc = await fetch(supabaseUrl + '/rest/v1/rpc/nayanet_legacy_cognition_disposition_audit', {
      method: 'POST',
      headers: {
        apikey: supabaseKey,
        Authorization: 'Bearer ' + session.access_token,
        'Content-Type': 'application/json',
      },
      body: '{}',
    });
    if (!rpc.ok) throw new Error('DISPOSITION_RPC_FAILED:' + rpc.status + ':' + (await rpc.text()).slice(0, 300));
    audit = await rpc.json();
    if (!audit || typeof audit.cohort_total !== 'number') throw new Error('DISPOSITION_RPC_BAD_SHAPE:' + JSON.stringify(audit));

    const total = audit.cohort_total;
    const classified = audit.classified;
    const unclassified = audit.unclassified;
    if (classified + unclassified !== total) throw new Error('DISPOSITION_INCONSISTENT:classified+unclassified!=total');
    if (typeof audit.cohort_fingerprint_sha256 !== 'string' || audit.cohort_fingerprint_sha256.length !== 64) throw new Error('COHORT_FINGERPRINT_INVALID');

    console.log('LEGACY_COGNITION_DISPOSITION_AUDIT ' + JSON.stringify({
      run_id: run,
      owner_id: ownerId,
      schema: audit.schema,
      generated_at: audit.generated_at,
      cohort_fingerprint_sha256: audit.cohort_fingerprint_sha256,
      cohort_total: total,
      classified: classified,
      unclassified: unclassified,
      complete: audit.complete,
      groups: audit.groups,
    }));
    fs.writeFileSync('legacy-cognition-disposition-audit.json', JSON.stringify({
      schema: audit.schema,
      status: 'VERIFIED',
      run_id: run,
      source_head: process.env.GITHUB_SHA || null,
      owner_id: ownerId,
      audit,
    }, null, 2));
  } finally {
    await ctx.close();
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });