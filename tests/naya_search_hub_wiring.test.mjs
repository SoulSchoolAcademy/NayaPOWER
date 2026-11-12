import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { runInNewContext } from "node:vm";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const INDEX = readFileSync(join(ROOT, "HUB/app/index.html"), "utf8");
const match = INDEX.match(/<script src="js\/naya-search\.js"><\/script>\s*<script>([\s\S]*?)<\/script>/);
assert.ok(match, "the public Hub must load the existing search module before initializing it");
const APP_WIRING = match[1];

function createHarness() {
  const state = {
    openCount: 0, mounted: 0, store: null, created: [], button: null,
    network: 0, hotkey: null,
  };
  const fakeDocument = {
    body: { appendChild(node) { if (node.tagName === "button") state.button = node; } },
    head: { appendChild() {} },
    createElement(name) {
      return {
        tagName: name,
        className: "",
        textContent: "",
        setAttribute() {},
        addEventListener(event, fn) { if (event === "click") this.click = fn; },
      };
    },
  };
  const fakeSearch = {
    mountPalette(body, opts) {
      assert.equal(body, fakeDocument.body);
      state.mounted += 1;
      state.store = opts.store;
      return { open() { state.openCount += 1; } };
    },
    installHotkey(doc, open) {
      assert.equal(doc, fakeDocument);
      state.hotkey = open;
    },
    createStore(opts) {
      state.created.push(opts);
      return {
        search(q) {
          state.network += 1;
          return Promise.resolve({ results: [{ title: q }] });
        },
      };
    },
  };
  const context = { window: { NayaSearch: fakeSearch }, document: fakeDocument, Promise };
  runInNewContext(APP_WIRING, context, { filename: "hub-search-wiring.js" });
  assert.equal(state.mounted, 1, "exactly one palette, no competing search UI");
  assert.ok(state.hotkey, "keyboard search must work");
  assert.ok(state.button, "mobile search needs a visible, operable entry");
  return { state, context };
}

test("missing authentication never creates transport or performs private search", async () => {
  const { state } = createHarness();
  const result = await state.store.search("Maria");
  assert.equal(result.not_verified, true);
  assert.equal(result.reason, "no_session");
  assert.equal(state.created.length, 0);
  assert.equal(state.network, 0);
});

test("opening the palette on phone/keyboard does not silently issue network calls", () => {
  const { state } = createHarness();
  state.hotkey();
  state.button.click();
  assert.equal(state.openCount, 2);
  assert.equal(state.network, 0);
});

test("login occurring AFTER page load is read at query time, never on initial mount", async () => {
  const { state, context } = createHarness();
  assert.equal(state.created.length, 0);
  context.window.NayaSearchSession = {
    supabaseUrl: "https://example.supabase.co",
    anonKey: "public-anon-key",
    getAccessToken() { return "authenticated-session-token"; },
  };
  const result = await state.store.search("Maria");
  assert.equal(result.results[0].title, "Maria");
  assert.equal(state.created.length, 1);
  assert.equal(state.created[0].supabaseUrl, "https://example.supabase.co");
  assert.equal(state.created[0].getAccessToken(), "authenticated-session-token");
  assert.equal(state.network, 1);
});

test("missing token, invalid URL or throwing session getter fails closed", async () => {
  for (const session of [
    { supabaseUrl: "https://example.supabase.co", anonKey: "public", getAccessToken: () => "" },
    { supabaseUrl: "http://insecure.local", anonKey: "public", getAccessToken: () => "token" },
    { supabaseUrl: "https://example.supabase.co", anonKey: "", getAccessToken: () => "token" },
    { supabaseUrl: "https://example.supabase.co", anonKey: "public", getAccessToken() { throw Error("denied"); } },
  ]) {
    const { state, context } = createHarness();
    context.window.NayaSearchSession = session;
    const result = await state.store.search("Maria");
    assert.equal(result.not_verified, true, "invalid auth must never search");
    assert.equal(state.network, 0);
    assert.equal(state.created.length, 0);
  }
});

test("Hub never embeds a JWT, service role or dev bypass into search bootstrap", () => {
  assert.doesNotMatch(APP_WIRING, /service_role|bearer\s+eyJ|localStorage\.getItem\(['"]access_token|\?dev=1/i);
  assert.match(APP_WIRING, /NayaSearchSession/);
  assert.match(APP_WIRING, /NayaSearch\.mountPalette/);
  assert.match(APP_WIRING, /NayaSearch\.installHotkey/);
});
