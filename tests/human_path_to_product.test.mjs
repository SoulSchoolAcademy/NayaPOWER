import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

/**
 * The path a human takes to actually use NayaNET.
 *
 * Every defect locked here was shipped and invisible to every other gate in this
 * repository, because the Hub and the identity surfaces are only ever executed in
 * a browser. A cold run of the 14-question acceptance interface on 2026-10-08
 * found all of them by reading source.
 *
 * These assertions deliberately EXECUTE the real expressions lifted out of the
 * source instead of regex-matching the source text. tools/edge-typecheck/README.md
 * records the failure mode this avoids: "Every assertion ... regex-matched the
 * handler's source text rather than executing it", which is how a completely
 * broken OTP validator can sit in a file full of passing tests.
 */

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (...p) => readFileSync(join(ROOT, ...p), "utf8");

const IDENTITY_PAGE = "NAYANET BRIDGE INDENITY CODE.html";
const SMART_LINK_VIEWER = join("supabase", "functions", "nayanet-smart-note-viewer", "index.ts");
const HUB_APP = join("HUB", "app", "index.html");

/** Evaluate a regex literal against a value the way the browser would. */
function inlineGuard(source, variableName) {
  const m = source.match(new RegExp(`!\\s*(/\\^[^\\n]*?/)\\s*\\.test\\(${variableName}\\)`));
  assert.ok(
    m,
    `could not find an inline /^\s*$ /-style guard testing ${variableName} — ` +
    `the test must fail loudly rather than skip`
  );
  return new RegExp(m[1].slice(1, m[1].lastIndexOf("/")));
}

/* ------------------------------------------------------------------ *
 * 1. Authentication must be able to succeed.
 * ------------------------------------------------------------------ */

test("the OTP validator actually accepts a six-digit code", () => {
  const src = read(IDENTITY_PAGE);
  const re = inlineGuard(src, "token");

  for (const code of ["123456", "000000", "999999", "424242"]) {
    assert.ok(re.test(code), `a legitimate six-digit code ${code} must pass validation`);
  }
  for (const bad of ["12345", "1234567", "abcdef", "", "12345a"]) {
    assert.ok(!re.test(bad), `${JSON.stringify(bad)} must be rejected`);
  }
});

test("the Smart Link viewer normalizes the OTP before verifying it", () => {
  const src = read(SMART_LINK_VIEWER);
  const m = src.match(/\.replace\((\/\\D\/g)/);
  assert.ok(m, "the Smart Link viewer must strip non-digits from the OTP");
  const strip = new RegExp("\\D", "g");
  for (const pasted of ["123456", "123 456", "123-456", "1 2 3 4 5 6"]) {
    assert.equal(
      pasted.replace(strip, "").slice(0, 6),
      "123456",
      `a human pasting ${JSON.stringify(pasted)} must still produce a usable code`
    );
  }
});

test("no double-escaped regex literal remains in any shipped browser surface", () => {
  // "/\\d/" is an escaped backslash followed by 'd': it matches a literal "\" then
  // six "d"s, so a real OTP can never validate. This class of bug was present in
  // both auth surfaces and is invisible to every non-browser gate.
  const surfaces = [IDENTITY_PAGE, SMART_LINK_VIEWER];
  const offender = /\/[^/\n]*?\\\\[dDsSwWbBnrt][^/\n]*?\//;
  for (const rel of surfaces) {
    const src = read(rel);
    const hit = src.match(offender);
    // The Smart Link viewer legitimately rewrites a literal backslash-n from raw
    // JSON; that is a string operation, not a regex character class.
    if (hit && /privateKeyRaw|\\\\n/.test(hit[0])) continue;
    assert.equal(
      hit,
      null,
      `${rel} contains a double-escaped regex literal ${hit?.[0] ?? ""} — ` +
      `character classes must be written /\\d/ not /\\\\d/`
    );
  }
});

/* ------------------------------------------------------------------ *
 * 2. Navigation must not lead a human to a 404.
 * ------------------------------------------------------------------ */

test("the Hub never redirects a room to a file that does not exist", () => {
  const src = read(HUB_APP);
  const map = src.match(/EXTERNAL_ROOMS\s*=\s*\{([^}]*)\}/);
  if (!map) {
    // No external-room map at all: every room renders in-app. This is the fixed
    // state. Assert the router actually forwards rooms to HubView instead.
    assert.match(
      src,
      /Router\.on\('hub\/:room',\s*params\s*=>\s*window\.HubView\(params\)\)/,
      "rooms must render in-app via HubView"
    );
    return;
  }
  // If an external map is ever reintroduced, every target must be a real file.
  const dir = join(ROOT, "HUB", "app");
  for (const [, room, file] of map[1].matchAll(/(\w+)\s*:\s*'([^']+\.html)'/g)) {
    assert.ok(
      existsSync(join(dir, file)),
      `room "${room}" redirects to ${file}, which does not exist — that is a hard 404`
    );
  }
});

test("every room declared in the Hub has a renderer or an honest fallback", () => {
  const src = read(HUB_APP);
  const rooms = [...src.matchAll(/\{\s*id:\s*'([\w-]+)',\s*name:/g)].map((m) => m[1]);
  assert.ok(rooms.length >= 11, `expected the Hub's rooms to be declared, found ${rooms.length}`);

  // The shell must degrade honestly rather than render blank when a room has no
  // renderer, and it must NOT hard-redirect to a missing page as a substitute.
  assert.match(src, /notVerified\(room\)/, "a room without a renderer must show an honest state");
  assert.ok(
    !/location\.href\s*=\s*EXTERNAL_ROOMS/.test(src),
    "rooms must not be redirected out of the app"
  );
});

test("the Hub can be opened locally for inspection", () => {
  const src = read(HUB_APP);
  assert.match(
    src,
    /get\('dev'\)\s*===\s*'1'/,
    "the Hub must expose ?dev=1 so a reviewer can open it without a live identity"
  );
  // The production front-door behavior must be preserved, not quietly removed.
  assert.match(src, /location\.href\s*=\s*WELCOME_URL/);
});

/* ------------------------------------------------------------------ *
 * 4. The Hub must not present a snapshot as if it were live.
 * ------------------------------------------------------------------ */

test("the feed states when its intelligence was captured", () => {
  const src = read(HUB_APP);

  // The snapshot date exists in the content model...
  const meta = src.match(/as_of\s*:\s*"([^"]+)"/);
  assert.ok(meta, "the content model must carry the snapshot capture time");

  // ...and it must reach the human, not just sit in a comment.
  assert.match(
    src,
    /Intelligence as of/,
    "the Hub must render the intelligence's own capture date to the person reading it"
  );
  // The hero prints today's date, so a stale snapshot needs an explicit age.
  assert.match(src, /day/, "the provenance line must express how old the snapshot is");
  assert.match(src, /feed-provenance/, "the provenance must be styled, not ad-hoc inline");

  // It must be sourced from the snapshot metadata, never hardcoded, so a
  // re-baked snapshot updates the label without a second manual edit.
  assert.match(
    src,
    /NayaContent\.meta\.as_of/,
    "the label must read its date from the snapshot metadata"
  );
});

/* ------------------------------------------------------------------ *
 * 5. The Hub bundle must keep parsing.
 * ------------------------------------------------------------------ */

test("every inline script block in the Hub parses", () => {
  const src = read(HUB_APP);
  const blocks = [...src.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
  assert.ok(blocks.length >= 20, `expected the Hub's inline blocks, found ${blocks.length}`);
  for (const [i, m] of blocks.entries()) {
    try {
      // Function constructor throws SyntaxError on invalid source.
      new Function(m[1]);
    } catch (e) {
      assert.fail(`Hub inline script block ${i + 1} does not parse: ${e.message}`);
    }
  }
});
