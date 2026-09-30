// nayanet-github-dispatch
// Governed GitHub projection for canonical Smart Note transactions.
//
// Called ONLY by v7-smart-note-canonical, and only with a narrow,
// single-transaction authority grant (action "smart_note_github_projection").
// This function creates no standing GitHub authority: every projection is
// scoped to exactly one transaction, one IB identity, one commit.
//
// Contract (must match v7-smart-note-canonical's expectations exactly):
//   request:  { operation:"project_smart_note", transaction_id, authority_grant_id,
//               approval:"EXPLICIT_APPROVAL_GRANTED", idempotency_key }
//   success:  { ok:true, pipeline:"PROJECTION_VERIFIED", smart_link,
//               receipt:{id}, projection_verification:{completed_at, run_url, commit_sha} }
//   smart_link must match:
//     https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.+/IB-\d{6}/smart-note.md
//
// Failure posture is fail-closed and receipted: a missing GitHub credential,
// a refused grant, or a GitHub API error never produces a guessed link and
// never fails silently. Replays with the same idempotency key return the
// original receipt without a duplicate commit.

import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { SignJWT, importPKCS8 } from "https://esm.sh/jose@6.0.10";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-idempotency-key",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

const REPO_OWNER = "SoulSchoolAcademy";
const REPO_NAME = "NayaPOWER";
const REPO = REPO_OWNER + "/" + REPO_NAME;
const ACTION = "smart_note_github_projection";
const IB_RE = /^IB-\d{6}$/;
const LINK_RE = /^https:\/\/github\.com\/SoulSchoolAcademy\/NayaPOWER\/blob\/main\/.+\/IB-\d{6}\/smart-note\.md$/;

function normalizedText(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function slugify(value: string, max: number): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, max);
}

function b64encode(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

function ghHeaders(token: string): Record<string, string> {
  return {
    Authorization: "Bearer " + token,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
  };
}


type GitHubCredential = {
  token: string;
  mode: "GITHUB_APP_INSTALLATION_TOKEN" | "STATIC_GITHUB_TOKEN_DEPRECATED";
};

async function resolveGitHubCredential(): Promise<GitHubCredential> {
  const appId = normalizedText(Deno.env.get("GITHUB_APP_ID"));
  const installationId = normalizedText(Deno.env.get("GITHUB_APP_INSTALLATION_ID"));
  const privateKeyRaw = Deno.env.get("GITHUB_APP_PRIVATE_KEY") || "";
  const legacyToken = Deno.env.get("GITHUB_TOKEN") || "";

  if (appId && installationId && privateKeyRaw) {
    const privateKey = privateKeyRaw.includes("\\n") ? privateKeyRaw.replace(/\\n/g, "\n") : privateKeyRaw;
    const key = await importPKCS8(privateKey, "RS256");
    const now = Math.floor(Date.now() / 1000);
    const appJwt = await new SignJWT({})
      .setProtectedHeader({ alg: "RS256" })
      .setIssuedAt(now - 60)
      .setExpirationTime(now + 540)
      .setIssuer(appId)
      .sign(key);

    const tokenRes = await fetch(
      `https://api.github.com/app/installations/${encodeURIComponent(installationId)}/access_tokens`,
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + appJwt,
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ repositories: [REPO_NAME], permissions: { contents: "write" } }),
      },
    );
    const tokenJson: any = await tokenRes.json().catch(() => ({}));
    const token = normalizedText(tokenJson?.token);
    if (!tokenRes.ok || !token) {
      throw new Error("GITHUB_APP_TOKEN_MINT_FAILED:" + tokenRes.status);
    }
    return { token, mode: "GITHUB_APP_INSTALLATION_TOKEN" };
  }

  if (legacyToken) {
    return { token: legacyToken, mode: "STATIC_GITHUB_TOKEN_DEPRECATED" };
  }

  throw new Error("GITHUB_CREDENTIAL_NOT_CONFIGURED");
}

async function sha256Hex(text: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function renderSmartNoteMarkdown(args: {
  block: any;
  ibId: string;
  transactionId: string;
  grantId: string;
  projectedAt: string;
  contentHash: string;
  userId: string;
}): string {
  const { block, ibId, transactionId, grantId, projectedAt, contentHash, userId } = args;
  const meaning = block?.meaning || {};
  const perspectives = block?.perspectives || {};
  const provenance = block?.provenance || {};
  const truth = block?.truth || {};
  const authority = block?.authority || {};
  const evidence = block?.evidence || {};
  const learning = block?.learning || {};
  const line = (v: unknown): string => normalizedText(v) || "—";
  return (
    `# Smart Note — ${ibId}\n\n` +
    `> Governed repository projection of a canonical Intelligent Block.\n` +
    `> Canonical receiver: \`v7-smart-note-canonical\` · Transaction: \`${transactionId}\`\n` +
    `> Authority grant: \`${grantId}\` (single-transaction, action \`smart_note_github_projection\`)\n` +
    `> Projected at: ${projectedAt} · Content SHA-256: \`${contentHash}\`\n` +
    `> Owner: \`${userId}\` · Epistemic state: ${line(truth.state)}\n\n` +
    `## Subject\n\n${line(meaning.subject)}\n\n` +
    `## In a nutshell\n\n${line(meaning.in_a_nutshell || meaning.summary)}\n\n` +
    `## Human view\n\n${line(perspectives.human)}\n\n` +
    `## Naya view\n\n${line(perspectives.naya)}\n\n` +
    `## Simple view\n\n${line(perspectives.child)}\n\n` +
    `## Everyday view\n\n${line(perspectives.grandma)}\n\n` +
    `## Machine view\n\n${line(perspectives.machine)}\n\n` +
    `## What it means\n\n${line(perspectives.meaning)}\n\n` +
    `## How it connects\n\n${line(perspectives.connections)}\n\n` +
    `## How to apply\n\n${line(perspectives.application)}\n\n` +
    `## Value\n\n${line(perspectives.value)}\n\n` +
    `## Learning\n\n${line(learning.lesson || learning.what_changed)}\n\n` +
    `## Provenance\n\n` +
    `- Source: ${line(provenance.source)} (${line(provenance.source_ref)})\n` +
    `- Captured by: \`${line(provenance.captured_by)}\`\n` +
    `- Evidence state: ${line(evidence.evidence_state)} · Verification: ${line(evidence.verification)}\n` +
    `- Authority: ${line(authority.state)} (${line(authority.authority_ref)})\n` +
    `- Constraints: ${(Array.isArray(authority.constraints) ? authority.constraints : []).join(", ") || "—"}\n\n` +
    `---\n\n` +
    `*Projected by \`nayanet-github-dispatch\` under a narrow single-transaction grant. ` +
    `The authoritative record is the \`v7_smart_note_transactions\` row for transaction \`${transactionId}\`; ` +
    `this file is a projection, not the source of truth.*\n`
  );
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);

  let transactionId: string | null = null;
  let idempotencyKey: string | null = null;

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY");
    const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    if (!supabaseUrl || !supabaseAnonKey || !serviceKey) throw new Error("SUPABASE_RUNTIME_NOT_CONFIGURED");

    const auth = req.headers.get("Authorization");
    if (!auth) return json({ ok: false, error: "AUTHORIZATION_REQUIRED" }, 401);
    const supabase = createClient(supabaseUrl, supabaseAnonKey, { global: { headers: { Authorization: auth } } });
    const admin = createClient(supabaseUrl, serviceKey);
    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser();
    if (userError || !user) return json({ ok: false, error: "AUTHENTICATED_USER_REQUIRED" }, 401);

    const body = await req.json().catch(() => ({}));
    const operation = normalizedText(body?.operation);
    transactionId = normalizedText(body?.transaction_id);
    const grantId = normalizedText(body?.authority_grant_id);
    const approval = normalizedText(body?.approval);
    idempotencyKey =
      normalizedText(body?.idempotency_key) || normalizedText(req.headers.get("x-idempotency-key"));

    if (operation !== "project_smart_note") return json({ ok: false, error: "UNKNOWN_OPERATION" }, 400);
    if (!transactionId) return json({ ok: false, error: "TRANSACTION_ID_REQUIRED" }, 400);
    if (!grantId) return json({ ok: false, error: "AUTHORITY_GRANT_REQUIRED" }, 400);
    if (approval !== "EXPLICIT_APPROVAL_GRANTED")
      return json({ ok: false, error: "EXPLICIT_APPROVAL_REQUIRED" }, 403);
    if (!idempotencyKey) return json({ ok: false, error: "IDEMPOTENCY_KEY_REQUIRED" }, 400);

    const receipts = admin.from("nayanet_github_dispatch_receipts");

    // Idempotency claim: exactly one row per key. A concurrent duplicate either
    // replays the completed receipt or takes over a non-completed claim.
    const claimInsert = await receipts
      .insert({ idempotency_key: idempotencyKey, transaction_id: transactionId, user_id: user.id, status: "processing" })
      .select("id,status,smart_link,commit_sha,completed_at")
      .maybeSingle();
    if (claimInsert.error && claimInsert.error.code !== "23505") throw claimInsert.error;
    if (!claimInsert.error && !claimInsert.data) throw new Error("DISPATCH_RECEIPT_CLAIM_FAILED");
    let claimRow: any = claimInsert.error ? null : claimInsert.data;
    if (!claimRow) {
      const existing = await receipts
        .select("id,status,smart_link,commit_sha,completed_at,intelligent_block_id,repo_path")
        .eq("idempotency_key", idempotencyKey)
        .maybeSingle();
      if (existing.error) throw existing.error;
      claimRow = existing.data;
      if (!claimRow) throw new Error("DISPATCH_RECEIPT_CLAIM_FAILED");
    }
    if (claimRow.status === "completed" && claimRow.smart_link) {
      return json({
        ok: true,
        pipeline: "PROJECTION_VERIFIED",
        smart_link: claimRow.smart_link,
        receipt: { id: claimRow.id },
        replayed: true,
        projection_verification: {
          completed_at: claimRow.completed_at,
          run_url: null,
          commit_sha: claimRow.commit_sha || null,
          credential_mode: null,
        },
      });
    }
    const failReceipt = async (failure: string): Promise<void> => {
      const upd = await receipts
        .update({ status: "failed", failure })
        .eq("idempotency_key", idempotencyKey);
      if (upd.error) throw upd.error;
    };

    // Authority: the grant must be live, owner-issued, owner-held, carry the
    // projection action, and be scoped to exactly this transaction.
    const grantRes = await supabase
      .from("nayanet_authority_grants")
      .select("grant_id,status,expires_at,actions,scope,issuer_id,subject_id")
      .eq("grant_id", grantId)
      .maybeSingle();
    if (grantRes.error) throw grantRes.error;
    const g: any = grantRes.data;
    const grantOk =
      g &&
      g.status === "ACTIVE" &&
      String(g.issuer_id) === user.id &&
      String(g.subject_id) === user.id &&
      Array.isArray(g.actions) &&
      g.actions.includes(ACTION) &&
      String(g.scope?.target || "") === transactionId &&
      (!g.expires_at || new Date(g.expires_at) > new Date());
    if (!grantOk) {
      await failReceipt("PROJECTION_AUTHORITY_REFUSED");
      return json({ ok: false, pipeline: "PROJECTION_REFUSED", error: "PROJECTION_AUTHORITY_REFUSED" }, 403);
    }

    // Load the canonical transaction (owner-scoped read; RLS enforces ownership).
    const txRes = await supabase
      .from("v7_smart_note_transactions")
      .select("id,user_id,intelligent_block,created_at")
      .eq("id", transactionId)
      .maybeSingle();
    if (txRes.error) throw txRes.error;
    const tx: any = txRes.data;
    if (!tx || String(tx.user_id) !== user.id) {
      await failReceipt("TRANSACTION_NOT_FOUND");
      return json({ ok: false, pipeline: "PROJECTION_REFUSED", error: "TRANSACTION_NOT_FOUND" }, 404);
    }
    const block: any = tx.intelligent_block || {};
    const ibId = normalizedText(block?.identity?.intelligent_block_id);
    if (!IB_RE.test(ibId)) {
      await failReceipt("INTELLIGENT_BLOCK_ID_INVALID");
      return json({ ok: false, pipeline: "PROJECTION_REFUSED", error: "INTELLIGENT_BLOCK_ID_INVALID" }, 422);
    }

    const meta: any = block?.metadata || {};
    const category = slugify(normalizedText(meta.projection_category) || "system", 64) || "system";
    const topicSlug = slugify(normalizedText(meta.projection_topic) || "smart-note", 96) || "smart-note";
    const created = tx.created_at ? new Date(tx.created_at) : new Date();
    const datePath = created.toISOString().slice(0, 10).replace(/-/g, "/");
    const repoPath = `BRAIN/05-MEMORY/SMART-NOTES/${datePath}/${category}/${topicSlug}/${ibId}/smart-note.md`;
    const smartLink = `https://github.com/${REPO}/blob/main/${repoPath}`;
    if (!LINK_RE.test(smartLink)) throw new Error("SMART_LINK_CONTRACT_VIOLATION");

    let githubCredential: GitHubCredential;
    try {
      githubCredential = await resolveGitHubCredential();
    } catch (credentialError) {
      const credentialFailure = String((credentialError as Error)?.message || credentialError);
      const isMissing = credentialFailure === "GITHUB_CREDENTIAL_NOT_CONFIGURED";
      const failure = isMissing ? "GITHUB_CREDENTIAL_NOT_CONFIGURED" : credentialFailure;
      const upd = await receipts
        .update({
          status: isMissing ? "blocked" : "failed",
          failure,
          authority_grant_id: grantId,
          intelligent_block_id: ibId,
          repo_path: repoPath,
          smart_link: smartLink,
        })
        .eq("idempotency_key", idempotencyKey);
      if (upd.error) throw upd.error;
      return json(
        {
          ok: false,
          pipeline: isMissing ? "PROJECTION_BLOCKED" : "PROJECTION_FAILED",
          error: isMissing ? "GITHUB_CREDENTIAL_NOT_CONFIGURED" : "GITHUB_APP_TOKEN_MINT_FAILED",
          detail: isMissing
            ? "Configure a repo-scoped GitHub App (preferred) or temporary legacy GITHUB_TOKEN, then replay the same idempotency key."
            : credentialFailure,
          transaction_id: transactionId,
        },
        isMissing ? 503 : 502,
      );
    }
    const githubToken = githubCredential.token;

    const projectedAt = new Date().toISOString();
    const markdown = renderSmartNoteMarkdown({
      block,
      ibId,
      transactionId,
      grantId,
      projectedAt,
      contentHash: await sha256Hex(JSON.stringify(block)),
      userId: user.id,
    });

    // Commit via the GitHub Contents API. Same deterministic content re-PUT to
    // the same path returns the existing blob without a duplicate commit.
    const apiUrl = `https://api.github.com/repos/${REPO}/contents/${repoPath}`;
    const headRes = await fetch(apiUrl + "?ref=main", { headers: ghHeaders(githubToken) });
    let sha: string | null = null;
    if (headRes.status === 200) {
      const headJson: any = await headRes.json().catch(() => ({}));
      sha = typeof headJson?.sha === "string" ? headJson.sha : null;
    } else if (headRes.status !== 404) {
      await failReceipt("GITHUB_READ_FAILED:" + headRes.status);
      return json(
        { ok: false, pipeline: "PROJECTION_FAILED", error: "GITHUB_READ_FAILED", status: headRes.status },
        502
      );
    }
    const putBody: Record<string, unknown> = {
      message:
        `projection(smart-note): ${ibId} canonical Smart Note projection\n\n` +
        `Transaction: ${transactionId}\nAuthority grant: ${grantId}\nIdempotency: ${idempotencyKey}`,
      content: b64encode(markdown),
      branch: "main",
    };
    if (sha) putBody.sha = sha;
    const putRes = await fetch(apiUrl, {
      method: "PUT",
      headers: ghHeaders(githubToken),
      body: JSON.stringify(putBody),
    });
    const putJson: any = await putRes.json().catch(() => ({}));
    const commitSha: string | null = typeof putJson?.content?.sha === "string" ? putJson.content.sha : null;
    if (!putRes.ok || !commitSha) {
      await failReceipt("GITHUB_COMMIT_FAILED:" + putRes.status);
      return json(
        {
          ok: false,
          pipeline: "PROJECTION_FAILED",
          error: "GITHUB_COMMIT_FAILED",
          status: putRes.status,
          detail: normalizedText(putJson?.message).slice(0, 300) || "UNKNOWN",
        },
        502
      );
    }

    // Verify: read back and confirm the blob at the expected path.
    const verifyRes = await fetch(apiUrl + "?ref=main", { headers: ghHeaders(githubToken) });
    const verifyJson: any = await verifyRes.json().catch(() => ({}));
    if (!verifyRes.ok || verifyJson?.sha !== commitSha) {
      await failReceipt("PROJECTION_UNVERIFIED");
      return json({ ok: false, pipeline: "PROJECTION_FAILED", error: "PROJECTION_UNVERIFIED" }, 502);
    }

    const completedAt = new Date().toISOString();
    const doneUpd = await receipts
      .update({
        status: "completed",
        failure: null,
        authority_grant_id: grantId,
        intelligent_block_id: ibId,
        repo_path: repoPath,
        smart_link: smartLink,
        commit_sha: commitSha,
        completed_at: completedAt,
      })
      .eq("idempotency_key", idempotencyKey)
      .select("id")
      .single();
    if (doneUpd.error) throw doneUpd.error;

    return json({
      ok: true,
      pipeline: "PROJECTION_VERIFIED",
      smart_link: smartLink,
      receipt: { id: doneUpd.data.id },
      projection_verification: {
        completed_at: completedAt,
        run_url: null,
        commit_sha: commitSha,
        credential_mode: githubCredential.mode,
      },
    });
  } catch (error) {
    console.error(error);
    return json(
      {
        ok: false,
        pipeline: "failed",
        error: "GITHUB_DISPATCH_FAILED",
        detail: String(error && (error as Error).message ? (error as Error).message : error).slice(0, 500),
        transaction_id: transactionId,
        idempotency_key: idempotencyKey,
      },
      500
    );
  }
});
