/* Optional, isolated executable RLS regression for GT-039 / PR #3345.
 * Data is synthetic. No production database, keys, API, or tenant content.
 * Tested with PGlite 0.5.16 (real Postgres in WASM, but NOT Supabase runtime).
 * Install package into an isolated TEMP directory (do not change repo deps),
 * set NAYA_PGLITE_MODULE to its dist/index.js, then run:
 *   node tests/mail_rls_synthetic_pglite.mjs candidate       # expects 13/13 PASS, exit 0
 *   node tests/mail_rls_synthetic_pglite.mjs unsafe-thread   # expected fail, exit 2; spoofed thread visible
 *   node tests/mail_rls_synthetic_pglite.mjs unsafe-delete   # expected fail, exit 2; unauthorized delete
 * This is a supplementary local proof, not independent security review.
 */
import { pathToFileURL } from 'node:url';
const modulePath=process.env.NAYA_PGLITE_MODULE;
if (!modulePath) throw new Error('Set NAYA_PGLITE_MODULE to the installed @electric-sql/pglite/dist/index.js. This test never downloads packages or contacts a database.');
const { PGlite } = await import(pathToFileURL(modulePath).href);
import fs from 'node:fs';
const root = new URL('../supabase/migrations/', import.meta.url);
const fixture = new URL('./fixtures/mail_rls_synthetic.sql', import.meta.url);
const db = await PGlite.create();
const mode = process.argv[2] || 'candidate';
const Alice = '11111111-1111-4111-8111-111111111111';
const Bob = '22222222-2222-4222-8222-222222222222';
let tests = 0, fail = 0;
function assert(name, got, expected) {
  tests++;
  if (JSON.stringify(got) !== JSON.stringify(expected)) {
    fail++; console.log('FAIL', name, 'got', JSON.stringify(got), 'expected', JSON.stringify(expected));
  } else console.log('PASS', name, JSON.stringify(got));
}
async function as(role, claims, statement) {
  const encoded = JSON.stringify(claims).replaceAll("'", "''");
  await db.exec("SET request.jwt.claims = '" + encoded + "';");
  await db.exec("SET request.jwt.claim.sub = '" + (claims.sub || '') + "';");
  await db.exec("SET ROLE " + role + ";");
  try { return await db.query(statement); }
  finally { await db.exec('RESET ROLE;'); }
}
async function denied(name, role, claims, query) {
  let pass = false, detail = '';
  try { const r = await as(role, claims, query); detail = JSON.stringify(r.rows); }
  catch (e) { pass = /permission denied/.test(e.message); detail=e.message.slice(0,180); }
  assert(name, pass, true);
  if (!pass) console.log('DETAIL', detail);
}
try {
  await db.exec(fs.readFileSync(fixture,'utf8'));
  console.log('FIXTURE_CREATED');
  for (const filename of [
    '20261023190000_smart_mail_legacy_rls_hardening.sql',
    '20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql',
  ]) {
    let sql=fs.readFileSync(new URL(filename, root),'utf8');
    if(filename.startsWith('20261024194500') && mode==='unsafe-thread') sql=sql.replace('drop policy if exists smart_mail_threads_owner_select on public.smart_mail_threads;', '');
    if(filename.startsWith('20261024194500') && mode==='unsafe-delete') sql=sql.replace('drop policy if exists smart_mail_messages_owner_delete on public.smart_mail_messages;', '');
    await db.exec(sql);
    console.log('MIGRATION_APPLIED_TO_SYNTHETIC_PGLITE',filename,'mode',mode);
  }
  const names=(await db.query("select tablename,policyname from pg_policies where schemaname='public' and tablename in ('smart_mail_messages','smart_mail_threads') order by tablename,policyname")).rows;
  assert('final mail policy inventory', names.map(x=>x.policyname), ['smart_mail_messages_participant_select','smart_mail_threads_participant_select']);
  const grants=(await db.query("select has_table_privilege('anon','public.smart_mail_messages','SELECT') as ams,has_table_privilege('anon','public.smart_mail_threads','INSERT') as ati,has_table_privilege('authenticated','public.smart_mail_messages','SELECT') as rms")).rows[0];
  assert('anonymous grants revoked; authenticated read retained', grants, {ams:false,ati:false,rms:true});
  await denied('anonymous cannot select message content', 'anon', {user_metadata:{smart_alias:'alice'}}, "SELECT count(*) FROM public.smart_mail_messages");
  await denied('anonymous cannot insert thread', 'anon', {}, "INSERT INTO public.smart_mail_threads VALUES('00000000-0000-4000-8000-000000009999','bob')");
  const spoof=await as('authenticated',{user_metadata:{smart_alias:'alice'},sub:Bob},"SELECT count(*)::integer AS n FROM public.smart_mail_messages");
  assert('user-editable metadata spoof alone denied',spoof.rows[0].n,0);
  const ownAlice=await as('authenticated',{app_metadata:{smart_alias:'alice'},sub:Alice},"SELECT count(*)::integer AS n FROM public.smart_mail_messages");
  assert('alice sender message read',ownAlice.rows[0].n,1);
  const recvBob=await as('authenticated',{app_metadata:{smart_alias:'bob'},sub:Bob},"SELECT count(*)::integer AS n FROM public.smart_mail_messages");
  assert('bob recipient message read',recvBob.rows[0].n,1);
  const bobThread=await as('authenticated',{app_metadata:{smart_alias:'bob'},sub:Bob},"SELECT count(*)::integer AS n FROM public.smart_mail_threads");
  assert('bob recipient thread read',bobThread.rows[0].n,1);
  const senderThread=await as('authenticated',{app_metadata:{smart_alias:'alice'},sub:Alice},"SELECT count(*)::integer AS n FROM public.smart_mail_threads");
  assert('alice sender thread read via helper',senderThread.rows[0].n,1);
  const stranger=await as('authenticated',{app_metadata:{smart_alias:'eve'},sub:Alice},"SELECT count(*)::integer AS n FROM public.smart_mail_messages");
  assert('nonparticipant mail read denied',stranger.rows[0].n,0);
  const noDelete=await as('authenticated',{app_metadata:{smart_alias:'alice'},sub:Alice},"DELETE FROM public.smart_mail_messages WHERE from_alias='alice' RETURNING id");
  assert('authenticated cannot delete legacy messages',noDelete.rows.length,0);
  const intakeAlice=await as('authenticated',{app_metadata:{smart_alias:'eve'},sub:Alice},"SELECT count(*)::integer AS n FROM public.intake_events");
  assert('intake owner scoped by auth.uid',intakeAlice.rows[0].n,1);
  const intakeStranger=await as('authenticated',{app_metadata:{smart_alias:'alice'},sub:'33333333-3333-4333-8333-333333333333'},"SELECT count(*)::integer AS n FROM public.intake_events");
  assert('intake alias spoof denied',intakeStranger.rows[0].n,0);
  if(mode==='unsafe-thread') {
    const vulnerable=await as('authenticated',{user_metadata:{smart_alias:'bob'},sub:Alice},'SELECT count(*)::integer AS n FROM public.smart_mail_threads');
    assert('sabotage: restored legacy thread policy leaks to user_metadata spoof',vulnerable.rows[0].n,1);
  }
  if(mode==='unsafe-delete') {
    const vulnerable=await as('authenticated',{app_metadata:{smart_alias:'charlie'},user_metadata:{smart_alias:'carol'},sub:Bob},"DELETE FROM public.smart_mail_messages WHERE from_alias='carol' RETURNING id");
    assert('sabotage: restored legacy delete policy allows forged sender deletion',vulnerable.rows.length,1);
  }
  console.log('SUMMARY',JSON.stringify({tests,fail,mode,engine:'PGlite WASM PostgreSQL',data:'synthetic only',production:'NOT TOUCHED'}));
}catch(e){fail++; console.error('UNEXPECTED_ERROR',e.message,e.stack?.slice(0,1400));}
finally{await db.close();}
if(fail)process.exit(2);