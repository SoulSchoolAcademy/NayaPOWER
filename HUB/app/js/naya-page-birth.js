/*
 * naya-page-birth.js — Walkthrough completion → page birth wiring
 * (PI item walkthrough-page-birth-wiring, Birth chain, order rank 5).
 *
 * The seam this file wires, end to end:
 *
 *   Welcome walkthrough completes
 *     → NayaIntake.joinRecord(session, emailHash)   [harvested: HUB/app/js/naya-intake.js]
 *     → store.submit(session) saves the join         [harvested: same file]
 *     → opts.onFinished(joinRecord) fires           [harvested: same file, renderReview]
 *     → THIS FILE: birthPage(joinRecord, kind, deps)
 *         → citizen_worlds row (the citizen's world) [harvested: live schema, read 2026-11-11]
 *         → page_about row with cover_url            [harvested: live schema, read 2026-11-11]
 *         → cover from the cover manifest            [harvested: cover-library-wiring c2]
 *
 * What is HARVESTED, not invented:
 * - The intake engine, its join record shape, and its onFinished hook.
 *   This file changes nothing in naya-intake.js; it consumes the hook.
 * - The live tables citizen_worlds (alias, name, answers, topics,
 *   settings) and page_about (page_kind, page_alias, owner_alias,
 *   headline, body, cover_url). There is NO pages table and NO covers
 *   table in production (read 2026-11-11) — so the write transport is
 *   INJECTED as `deps.store`, exactly like intake's createStore pattern.
 *   The production gate supplies the real store; this file never talks
 *   to Supabase directly and never hard-codes a table that does not exist.
 * - The cover manifest seam from cover-library-wiring c2: manifest.json
 *   keyed by page type (area/personal, area/business, area/spaces,
 *   area/events); other pages draw the next rotating cover. The manifest
 *   itself is Resolve's supply (3 area covers still owed there); this
 *   file only CONSUMES it by key, with a deterministic fallback chain,
 *   so a missing key can never produce a blank page.
 *   2026-11-12 (cover-library-wiring): the consumption is now delegated
 *   to the canonical engine naya-cover-assign.js (same directory in the
 *   repo: HUB/app/js/), which accepts the REAL manifest.json shape
 *   (assets[] + assignment table) as well as this file's shorthand
 *   {areas, rotating}. assignCover() below calls the engine when it is
 *   present and falls back to the built-in chain when it is not — the
 *   guarantees hold either way, and no behavior changes when the engine
 *   is absent.
 * - Page Settings Law, SN-0852: visibility defaults personal PRIVATE,
 *   business PUBLIC, space PUBLIC; discoverability FINDABLE for all
 *   three. Installable has NO settled default in the record — this file
 *   defaults it to false (install is a citizen choice, not a birth
 *   default) and the spec flags it as open law rather than inventing one.
 *
 * Guarantees this file keeps:
 * - A half-finished walkthrough NEVER births a page: birthPage refuses
 *   any record that fails validateJoinRecord (bad/missing email hash,
 *   missing name, unknown flow). The intake already refuses incomplete
 *   sessions; this is the second gate, at the birth seam.
 * - A page is NEVER born twice: birthPage looks up (email hash, kind)
 *   first and returns the existing page (already:true) with zero writes.
 *   A retry after a partial Trinity birth resumes per kind, no duplicates.
 * - A page NEVER has a blank cover: assignCover always returns a cover —
 *   area key, else next rotating cover, else the built-in default cover.
 *   It never returns null.
 * - A failed store write is REPORTED ({born:false, reason}), never thrown
 *   and never reported as born.
 *
 * What this file does NOT do (owed steps, other lanes — never claimed):
 * - It does not land itself anywhere live. Landing behind the production
 *   gate is owed (Nitro lane / production gate).
 * - It does not render anything. Rendered proof at the real address is
 *   owed (parent / browser lane). Never claim live/AAA from these tests.
 *
 * Dual runtime like naya-intake.js: browser (window.NayaPageBirth) and
 * Node (module.exports) share this one file.
 */
(function (global) {
  'use strict';

  // ── Settled law, encoded ────────────────────────────────────────────
  // SN-0852 Page Settings Law: three independent switches per page.
  // Visibility defaults: personal PRIVATE, business PUBLIC, space PUBLIC.
  // Discoverability: FINDABLE for all three (the acceptance criteria's
  // own words: "personal private + findable, business/space public +
  // findable"). Installable: NO settled default in the record — false
  // here, flagged as open law in SPEC.md, never invented.

  var PAGE_KINDS = ['personal', 'business', 'space'];

  var SETTINGS_DEFAULTS = {
    personal: { installable: false, visibility: 'private', discoverability: 'findable' },
    business: { installable: false, visibility: 'public', discoverability: 'findable' },
    space: { installable: false, visibility: 'public', discoverability: 'findable' },
  };

  // Cover manifest keys, from cover-library-wiring c2. 'events' is a
  // cover key only, not a birth kind: no page is born as kind 'events'.
  var AREA_COVER_KEYS = {
    personal: 'area/personal',
    business: 'area/business',
    space: 'area/spaces',
    events: 'area/events',
  };

  // Built-in last resort: the house cover. Named, visible, never blank.
  // The app renders this key as the house gradient; it is a fallback,
  // not a cover from the library, and the cover_source says so.
  var DEFAULT_COVER = 'naya:default-cover';

  var FLOWS = { welcome: true, invite_accept: true };

  var INTENT_LINES = {
    learn: 'Here to learn what NayaNET is.',
    build: 'Here to build my own app.',
    community: 'Here to join the community.',
    team: 'Here to work with the team.',
  };

  function isNonEmptyString(v) {
    return typeof v === 'string' && v.trim().length > 0;
  }

  // ── Page alias ──────────────────────────────────────────────────────
  // The citizen's page alias is a slug of their own display name — NOT
  // the join record's owner_alias, which is the AMBASSADOR whose link
  // they joined through. Confusing the two would put the new citizen's
  // page under someone else's name; the spec keeps them distinct as
  // citizen_alias vs ambassador_alias.

  function slugifyName(name) {
    if (!isNonEmptyString(name)) return null;
    var slug = String(name).trim().toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .replace(/-{2,}/g, '-');
    return slug || null;
  }

  // ── Join-record validation (second gate at the birth seam) ──────────
  // The join record is NayaIntake.joinRecord's shape: {flow,
  // owner_alias, invitee_email_hash, display_name, intent, note}.
  // A record passes only if it could have come from a COMPLETE session:
  // known flow, 64-hex email hash, non-empty display name.

  function validateJoinRecord(record) {
    if (!record || typeof record !== 'object') return { ok: false, reason: 'no_record' };
    if (!FLOWS[record.flow]) return { ok: false, reason: 'bad_flow' };
    if (!/^[0-9a-f]{64}$/.test(record.invitee_email_hash || '')) {
      return { ok: false, reason: 'bad_email_hash' };
    }
    if (!isNonEmptyString(record.display_name)) return { ok: false, reason: 'no_display_name' };
    return { ok: true };
  }

  // ── Cover assignment (never blank) ──────────────────────────────────
  // Delegated to the canonical engine (cover-library-wiring):
  // naya-cover-assign.js, loaded when present beside this file (repo:
  // HUB/app/js/; workspace twin beside this file). The engine accepts
  // the REAL manifest.json shape (assets[] + assignment table) and this
  // file's shorthand {areas, rotating}, and runs the same chain:
  // area key → recommend (≥ 2 signals, when a page card is given) →
  // next rotating cover → built-in default. Never returns null.
  // Absent engine (or any engine error) → the built-in chain below,
  // byte-identical to the original implementation, keeps every guarantee.
  var CoverAssign = null;
  try {
    if (typeof module !== 'undefined' && module.exports && typeof require === 'function') {
      CoverAssign = require('./naya-cover-assign.js');
    } else if (typeof window !== 'undefined' && window.NayaCoverAssign) {
      CoverAssign = window.NayaCoverAssign;
    }
  } catch (e) { CoverAssign = null; }

  function assignCover(pageKind, manifest, rotationIndex) {
    if (CoverAssign && typeof CoverAssign.assignCoverLegacy === 'function') {
      try {
        var delegated = CoverAssign.assignCoverLegacy(pageKind, manifest, rotationIndex);
        if (delegated && isNonEmptyString(delegated.cover)) return delegated;
      } catch (e) { /* fall through to the built-in chain */ }
    }
    return assignCoverBuiltIn(pageKind, manifest, rotationIndex);
  }

  function assignCoverBuiltIn(pageKind, manifest, rotationIndex) {
    var m = manifest || {};
    var areas = m.areas || {};
    var key = AREA_COVER_KEYS[pageKind] || null;
    var areaCover = key ? areas[key] : null;
    if (isNonEmptyString(areaCover)) {
      return { cover: areaCover, source: 'area', key: key };
    }
    var rotating = m.rotating || [];
    if (rotating.length) {
      var idx = ((rotationIndex || 0) % rotating.length + rotating.length) % rotating.length;
      if (isNonEmptyString(rotating[idx])) {
        return { cover: rotating[idx], source: 'rotating', key: 'rotating[' + idx + ']' };
      }
    }
    return { cover: DEFAULT_COVER, source: 'default', key: null };
  }

  // ── Page spec (pure) ────────────────────────────────────────────────
  // Builds the born page's full spec from a validated join record. Pure:
  // no I/O, so the settings law and the cover rule are testable alone.

  function buildPageSpec(record, pageKind, manifest, rotationIndex) {
    var v = validateJoinRecord(record);
    if (!v.ok) return { ok: false, reason: v.reason };
    if (PAGE_KINDS.indexOf(pageKind) < 0) return { ok: false, reason: 'bad_page_kind' };
    var alias = slugifyName(record.display_name);
    if (!alias) return { ok: false, reason: 'bad_display_name' };
    var cover = assignCover(pageKind, manifest, rotationIndex);
    var settings = SETTINGS_DEFAULTS[pageKind];
    var headline = String(record.display_name).trim();
    var body = isNonEmptyString(record.note)
      ? String(record.note).trim()
      : (INTENT_LINES[record.intent] || 'New to NayaNET.');
    return {
      ok: true,
      spec: {
        page_alias: alias,
        page_kind: pageKind,
        citizen_alias: alias,
        ambassador_alias: isNonEmptyString(record.owner_alias)
          ? String(record.owner_alias).trim() : null,
        headline: headline,
        body: body,
        settings: {
          installable: settings.installable,
          visibility: settings.visibility,
          discoverability: settings.discoverability,
        },
        cover: cover.cover,
        cover_source: cover.source,
        cover_key: cover.key,
        source: {
          flow: record.flow,
          invitee_email_hash: record.invitee_email_hash,
        },
      },
    };
  }

  // ── Birth (orchestration, store injected) ───────────────────────────
  // deps.store seam (the production gate supplies the real one):
  //   findPage(emailHash, pageKind) -> page row | null   (idempotency)
  //   findWorld(alias)              -> world row | null
  //   createWorld(worldRow)         -> world row
  //   createPage(pageRow)           -> page row
  //   countPages(emailHash)         -> number (optional; rotation index)
  // Each may return a value or a Promise. World row shape follows the
  // live citizen_worlds columns (alias, name, answers, topics,
  // settings); page row shape follows live page_about columns
  // (page_kind, page_alias, owner_alias, headline, body, cover_url).
  // findPage(hash, kind) resolves through the world row: the hash lives
  // in citizen_worlds.answers.invitee_email_hash (hash-only canon),
  // since page_about carries no hash column of its own.
  // A store failure is reported as {born:false, reason:'store_error'},
  // never thrown, never reported as born.

  function toPromise(v) {
    return (v && typeof v.then === 'function') ? v : Promise.resolve(v);
  }

  function birthPage(record, pageKind, deps) {
    deps = deps || {};
    var store = deps.store;
    if (!store) return Promise.resolve({ born: false, reason: 'no_store', writes: 0 });
    var v = validateJoinRecord(record);
    if (!v.ok) return Promise.resolve({ born: false, reason: v.reason, writes: 0 });
    if (PAGE_KINDS.indexOf(pageKind) < 0) {
      return Promise.resolve({ born: false, reason: 'bad_page_kind', writes: 0 });
    }
    var hash = record.invitee_email_hash;
    return toPromise(typeof store.countPages === 'function'
      ? store.countPages(hash) : 0).then(function (count) {
      var built = buildPageSpec(record, pageKind, deps.manifest || null, count || 0);
      if (!built.ok) return { born: false, reason: built.reason, writes: 0 };
      var spec = built.spec;
      return toPromise(store.findPage(hash, pageKind)).then(function (existing) {
        if (existing) {
          return { born: false, already: true, page: existing, cover: spec.cover,
                   cover_source: spec.cover_source, writes: 0 };
        }
        var worldRow = {
          alias: spec.citizen_alias,
          name: spec.headline,
          answers: {
            intent: record.intent || null,
            note: record.note || null,
            flow: record.flow,
            // Hash-only, like the intake: the raw email never lands here.
            // The hash is the idempotency key — findPage(hash, kind)
            // resolves through the world row, since page_about carries
            // no hash column of its own.
            invitee_email_hash: hash,
          },
          topics: record.intent ? [record.intent] : [],
          settings: spec.settings,
        };
        return toPromise(store.findWorld(spec.citizen_alias)).then(function (world) {
          var worldP = world ? Promise.resolve(world)
            : toPromise(store.createWorld(worldRow));
          return worldP.then(function (worldRowOut) {
            var pageRow = {
              page_kind: spec.page_kind,
              page_alias: spec.page_alias,
              owner_alias: spec.citizen_alias,
              headline: spec.headline,
              body: spec.body,
              cover_url: spec.cover,
            };
            return toPromise(store.createPage(pageRow)).then(function (pageRowOut) {
              return { born: true, page: pageRowOut, world: worldRowOut,
                       cover: spec.cover, cover_source: spec.cover_source,
                       writes: world ? 1 : 2 };
            });
          });
        });
      });
    }).catch(function () {
      return { born: false, reason: 'store_error', writes: 0 };
    });
  }

  // Trinity birth: the reveal shows pages already filled (SN-0846), so
  // one completed walkthrough births the whole Trinity — personal first,
  // then business, then space — each through the same birthPage, so a
  // retry after a partial birth resumes per kind with no duplicates.
  // Per-kind results are collected; one kind failing never blocks the
  // others, and the caller sees exactly which kinds landed.

  function birthTrinity(record, deps) {
    var results = {};
    var kinds = ['personal', 'business', 'space'];
    var chain = Promise.resolve();
    kinds.forEach(function (kind) {
      chain = chain.then(function () {
        return birthPage(record, kind, deps).then(function (r) { results[kind] = r; });
      });
    });
    return chain.then(function () {
      var bornCount = kinds.filter(function (k) { return results[k].born; }).length;
      return { results: results, bornCount: bornCount };
    });
  }

  // ── Walkthrough hook ────────────────────────────────────────────────
  // The one-line wiring at the intake mount site — no intake change:
  //
  //   mountIntake(el, {
  //     store: intakeStore,
  //     onFinished: NayaPageBirth.wireWalkthroughCompletion({ store: birthStore, manifest: coverManifest })
  //   });
  //
  // opts.trinity true births the whole Trinity on completion; false
  // (default) births the personal page only.

  function wireWalkthroughCompletion(deps, opts) {
    opts = opts || {};
    if (opts.trinity) {
      return function onWalkthroughFinished(record) { return birthTrinity(record, deps); };
    }
    return function onWalkthroughFinished(record) {
      return birthPage(record, 'personal', deps);
    };
  }

  var api = {
    PAGE_KINDS: PAGE_KINDS,
    SETTINGS_DEFAULTS: SETTINGS_DEFAULTS,
    AREA_COVER_KEYS: AREA_COVER_KEYS,
    DEFAULT_COVER: DEFAULT_COVER,
    slugifyName: slugifyName,
    validateJoinRecord: validateJoinRecord,
    assignCover: assignCover,
    assignCoverBuiltIn: assignCoverBuiltIn,
    buildPageSpec: buildPageSpec,
    birthPage: birthPage,
    birthTrinity: birthTrinity,
    wireWalkthroughCompletion: wireWalkthroughCompletion,
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    global.NayaPageBirth = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
