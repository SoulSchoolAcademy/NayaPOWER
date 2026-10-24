// WALK WORKER FIX — JOINING block, /api/welcome/complete.
// BEFORE (bug, named by Nitro): link_url built with the raw alias.
// AFTER: encodeURIComponent(alias), idempotent by primary key, one wire.
async function issueAmbassadorLink(alias) {
  const link = "https://nayanet.live/joinus?ref=" + encodeURIComponent(alias);
  const existing = await db.from("ambassador_links").select("*").eq("alias", alias).maybeSingle();
  if (existing.data) return existing.data;
  const { data } = await db.from("ambassador_links")
    .insert({ alias, link_url: link })
    .select().single();
  return data;
}
// End slide renders from THIS response's ambassador_link — no second issuance call.
// Dashboard row reads the same ambassador_links row.
