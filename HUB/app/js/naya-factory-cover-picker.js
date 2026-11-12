/*
 * naya-factory-cover-picker.js — the cover step inside the Smart Factory
 * build flow: choose template and cover together, born with its cover.
 *
 * PI item factory-cover-picker-20261027 (Cover library, order rank 6) ·
 * naya-power · 2026-11-12. Landed direct to main under the PI Code (no
 * PR workflow, ever). The Python spec/test harness is
 * workspace/system/factory-cover-picker-2026-11-12.py — same contract,
 * same rules, same test names; the two must never disagree.
 *
 * The seam this file wires, end to end:
 *
 *   Factory build flow (process-build-queue.py process_build):
 *     (a) template selection from contract['template'] via the registry
 *     (a1/2) THIS STEP: openFactoryCoverStep({template, manifest, ...})
 *         -> the SAME chooser the other pages use (create mode, born
 *            cover pre-selected, one-tap skip, Recommended / Library /
 *            Upload doors)
 *         -> builder picks / uploads / skips
 *         -> resolveFactoryCoverAction(step, action, manifest)
 *         -> applyCoverToContract(contract, state, manifest)
 *            stores contract['cover'] = {cover_key|upload_ref, cover_url,
 *            cover_source, cover_via, set_by, offset_y}
 *     (b)+(c) branding + pieces -> (d) worker -> artifact -> gate ->
 *     deploy -> receipt carries the cover block (factoryCoverReceipt).
 *   The page is born with that cover (page_about.cover_url); Change
 *   cover after birth reuses the creation-time session shape (chooser C6).
 *
 * What is HARVESTED, not invented:
 * - The canonical born-cover engine HUB/app/js/naya-cover-assign.js:
 *   assignCoverForPage() (area default -> recommendation -> rotation ->
 *   builtin default) and recommend() are used when the engine is present
 *   beside this file. When it is absent the built-in chain below runs
 *   (same order, same `via` names) — the guarantees hold either way, and
 *   no behavior changes when the engine is absent. Same pattern as
 *   naya-page-birth.js.
 * - The live manifest HUB/covers/manifest.json (assets[] + assignment
 *   table). Template keys come from the registry (12, named); cover keys
 *   come from the manifest's servable set; page types come from the
 *   assignment table. An unknown template is a named error, never a
 *   silent substitution.
 * - The asset base that provably serves HUB/covers/ today is the assign
 *   engine's default (repo raw base); it takes assetBase as an override,
 *   so the gate switches to https://nayanet.app/covers the moment a
 *   /covers route lands, with zero change to step logic.
 *
 * Guarantees this file keeps:
 * - A step NEVER opens blank: the born cover always resolves (area
 *   default, else recommendation, else rotation, else the built-in
 *   default cover) and `via` names which step chose it.
 * - A failed pick NEVER strips the existing cover: resolve returns
 *   {state: null, error} and the caller KEEPS the current cover.
 * - A build NEVER stores a blank cover: applyCoverToContract with no
 *   state resolves the born default for the contract's template.
 * - A failed store is REPORTED ({contract: null, error}), never thrown
 *   and never reported as stored.
 *
 * What this file does NOT do (owed steps, other lanes — never claimed):
 * - It does not mount itself into process-build-queue.py: the step-(a1/2)
 *   call-site patch is specified in the item spec (production build
 *   pipeline — gated apply). No build calls this file yet.
 * - It does not render anything. Rendered proof at the real address is
 *   owed (parent / browser lane). Never claim live/AAA from these tests.
 *
 * Dual runtime like naya-cover-assign.js: browser
 * (window.NayaFactoryCoverPicker) and Node (module.exports) share this
 * one file. `node naya-factory-cover-picker.js --selftest` prints one
 * JSON line {ok, tests} for the built-in smoke checks.
 */
(function (global) {
  'use strict';

  // ── Settled law, encoded ────────────────────────────────────────────
  // Shawn lock 2026-10-27: template AND cover in one flow; library or
  // upload; stored with the build; born with its cover; changeable after.
  // Same picker as every other page, never a Factory-only version.

  // Registry template -> chooser page type. The 12 keys are the live
  // registry's templates table (templates-registry.json). menu / portfolio
  // / product / signup have no dedicated page type: any_other_page
  // (recommendation, then rotation) — the step says so, never silently.
  var TEMPLATE_PAGE_TYPES = {
    'personal': 'personal_page',
    'personal-hub': 'personal_page',
    'business': 'business_page',
    'business-hub': 'business_page',
    'community': 'space',
    'event': 'events_page',
    'booking': 'booking_page',
    'dashboard': 'dashboard_intel',
    'menu': 'any_other_page',
    'portfolio': 'any_other_page',
    'product': 'any_other_page',
    'signup': 'any_other_page'
  };
  var REGISTRY_TEMPLATES = Object.keys(TEMPLATE_PAGE_TYPES).sort();
  var CATCH_ALL_TEMPLATES = { 'menu': true, 'portfolio': true, 'product': true, 'signup': true };

  // The asset base that provably serves HUB/covers/ today (same default
  // as the assign engine — harvested, not invented).
  var DEFAULT_ASSET_BASE =
    'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/HUB/covers/';
  var DEFAULT_COVER = 'naya:default-cover';
  var DOORS = ['recommended', 'library', 'upload'];
  var SHELF_CAP = 8;
  var SUGGEST_LIMIT = 12;
  var UPLOAD_EXTS = { '.jpg': true, '.jpeg': true, '.png': true, '.webp': true, '.gif': true, '.avif': true };
  var HOUSE_CATEGORIES = { 'house-signature': true, 'house-area': true };
  var MATCH_CARD_REQUIRED = ['key', 'name', 'category', 'tier', 'suits', 'status', 'credit', 'file'];
  var ROTATION_KINDS = { 'rotation': true, 'rotating': true };

  function isNonEmptyString(v) {
    return typeof v === 'string' && v.trim().length > 0;
  }

  function assignEngine() {
    if (global && global.NayaCoverAssign) return global.NayaCoverAssign;
    try {
      if (typeof require === 'function') return require('./naya-cover-assign.js');
    } catch (e) { /* engine absent: built-in chain below */ }
    return null;
  }

  // ── Template -> page type (F6) ──────────────────────────────────────
  function templatePageType(template) {
    if (!isNonEmptyString(template)) {
      throw new Error('unknown factory template: ' + JSON.stringify(template) +
        ' (want one of ' + REGISTRY_TEMPLATES.join(', ') + ')');
    }
    var key = template.trim();
    var pageType = TEMPLATE_PAGE_TYPES[key];
    if (!pageType) {
      throw new Error('unknown factory template: ' + JSON.stringify(key) +
        ' (not in the registry: ' + REGISTRY_TEMPLATES.join(', ') + ')');
    }
    var note = CATCH_ALL_TEMPLATES[key]
      ? ('template ' + JSON.stringify(key) + ' has no dedicated page type; treated as ' +
         'any_other_page (recommendation, then rotation)')
      : null;
    return { pageType: pageType, note: note };
  }

  // ── Manifest helpers (same semantics as the assign engine) ──────────
  function assetByKey(manifest, key) {
    var assets = (manifest && manifest.assets) || [];
    for (var i = 0; i < assets.length; i++) if (assets[i].key === key) return assets[i];
    return null;
  }

  function isCompleteCard(asset) {
    if (!asset) return false;
    for (var i = 0; i < MATCH_CARD_REQUIRED.length; i++) if (!asset[MATCH_CARD_REQUIRED[i]]) return false;
    return true;
  }

  function servable(asset, ownerIsNaya) {
    if (!asset || asset.status !== 'ready') return false;
    if (!isCompleteCard(asset)) return false;
    if (!ownerIsNaya) {
      if (asset.featured_class === 'exclusive') return false;
      if (HOUSE_CATEGORIES[asset.category]) return false;
    }
    return true;
  }

  function coverUrl(manifest, coverKey, assetBase) {
    var engine = assignEngine();
    if (engine && engine.coverUrl) {
      var viaEngine = engine.coverUrl(manifest, coverKey, assetBase);
      if (viaEngine) return viaEngine;
    }
    var asset = assetByKey(manifest, coverKey);
    if (!asset) return null;
    if (isNonEmptyString(asset.url)) return asset.url;
    if (!isNonEmptyString(asset.file)) return null;
    var base = assetBase || DEFAULT_ASSET_BASE;
    if (base.slice(-1) !== '/') base += '/';
    return base + asset.file;
  }

  // The rotating set: kind rotation/rotating, status ready, BY KEY —
  // the same rule as the chooser (rotation_set) and the assign engine
  // (rotationSet). Sorting matters: seed 0 must pick the same cover in
  // every runtime ('11-her-kingdom-tree' sorts before 'rotation/...').
  function rotationPick(manifest, seed) {
    var assets = (manifest && manifest.assets) || [];
    var set = [];
    for (var i = 0; i < assets.length; i++) {
      if (ROTATION_KINDS[assets[i].kind] && assets[i].status === 'ready') set.push(assets[i]);
    }
    set.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : 0; });
    if (!set.length) return null;
    var idx = ((seed || 0) % set.length + set.length) % set.length;
    return { asset: set[idx], index: idx };
  }

  // The born cover (F4: never blank). Chain: area default -> recommendation
  // -> rotation -> builtin default. `via` names the step, never magic.
  function bornCoverForTemplate(opts) {
    opts = opts || {};
    var mapped = templatePageType(opts.template);
    var engine = assignEngine();
    if (engine && engine.assignCoverForPage) {
      var r = engine.assignCoverForPage({
        pageType: mapped.pageType, page: opts.page || null,
        manifest: opts.manifest, seed: opts.seed || 0,
        assetBase: opts.assetBase
      });
      return { cover_key: r.cover_key, name: r.name, cover_url: r.cover_url,
        source: r.source, via: r.via, set_by: 'system', why: r.why || null,
        rotation_index: (r.rotation_index === undefined ? null : r.rotation_index) };
    }
    var manifest = opts.manifest || {};
    var assignment = manifest.assignment_on_page_creation || {};
    var named = assignment[mapped.pageType];
    if (named) {
      var areaAsset = assetByKey(manifest, named);
      if (areaAsset && areaAsset.status === 'ready') {
        return { cover_key: named, name: areaAsset.name,
          cover_url: coverUrl(manifest, named, opts.assetBase),
          source: 'library', via: 'area_default', set_by: 'system', why: null, rotation_index: null };
      }
    }
    var pick = rotationPick(manifest, opts.seed || 0);
    if (pick) {
      return { cover_key: pick.asset.key, name: pick.asset.name,
        cover_url: coverUrl(manifest, pick.asset.key, opts.assetBase),
        source: 'library', via: 'rotation', set_by: 'system', why: null,
        rotation_index: pick.index };
    }
    return { cover_key: DEFAULT_COVER, name: 'Naya default cover',
      cover_url: DEFAULT_COVER, source: 'default', via: 'builtin_default',
      set_by: 'system', why: null, rotation_index: null };
  }

  function newCoverState(source, coverKey, uploadRef, offsetY, setBy) {
    return { source: source, cover_key: coverKey || null,
      upload_ref: uploadRef || null,
      offset_y: (typeof offsetY === 'number' ? offsetY : 0),
      set_by: setBy || 'system', updated_at: 'set-by-persistence-layer' };
  }

  function validUploadRef(ref) {
    if (!isNonEmptyString(ref)) return false;
    if (ref.indexOf('..') !== -1 || ref.indexOf('\\') !== -1 ||
        ref.charAt(0) === '/' || ref.indexOf('\x00') !== -1) return false;
    if (ref.length > 512) return false;
    var dot = ref.lastIndexOf('.');
    if (dot < 0) return false;
    return !!UPLOAD_EXTS[ref.slice(dot).toLowerCase()];
  }

  function clampOffset(value) {
    if (typeof value === 'boolean' || typeof value !== 'number' || isNaN(value)) {
      throw new Error('offset_y must be a number');
    }
    return Math.max(-1, Math.min(1, value));
  }

  // Category shelves for the Library door (chooser C3): featured first,
  // at most SHELF_CAP shown per category, `more` counts the rest. Never
  // the whole shelf dumped. Servable set only (F6).
  function categoryShelves(manifest, ownerIsNaya) {
    var assets = (manifest && manifest.assets) || [];
    var byCat = {};
    for (var i = 0; i < assets.length; i++) {
      var a = assets[i];
      if (!servable(a, ownerIsNaya)) continue;
      if (!a.category) continue;
      (byCat[a.category] = byCat[a.category] || []).push(a);
    }
    var cats = Object.keys(byCat);
    cats.sort(function (x, y) {
      var fx = byCat[x].some(function (a) { return a.featured_class === 'citizen'; }) ? 0 : 1;
      var fy = byCat[y].some(function (a) { return a.featured_class === 'citizen'; }) ? 0 : 1;
      return fx - fy || (x < y ? -1 : 1);
    });
    var out = {};
    cats.forEach(function (cat) {
      var list = byCat[cat].slice().sort(function (a, b) {
        var fa = (a.featured_class === 'citizen' ? (a.featured_order || 0) : 1e9);
        var fb = (b.featured_class === 'citizen' ? (b.featured_order || 0) : 1e9);
        return fa - fb || (a.key < b.key ? -1 : 1);
      });
      var featured = list.filter(function (a) { return a.featured_class === 'citizen'; })
        .map(function (a) { return a.key; });
      var shown = list.slice(0, SHELF_CAP).map(function (a) { return a.key; });
      out[cat] = { featured: featured, covers: shown, total: list.length,
        more: Math.max(0, list.length - shown.length) };
    });
    return out;
  }

  function suggestionsFor(manifest, page, ownerIsNaya) {
    var engine = assignEngine();
    if (engine && engine.recommend) {
      var rec = engine.recommend(page || null, manifest, ownerIsNaya);
      if (rec && rec.top_pick) {
        var list = [{ cover_key: rec.top_pick, name: rec.top_name,
          why: rec.why || null, rank: 1, featured: false }];
        (rec.alternates || []).slice(0, SUGGEST_LIMIT - 1).forEach(function (a, i) {
          list.push({ cover_key: a.cover_key, name: a.name || null,
            why: a.why || null, rank: i + 2, featured: false });
        });
        return { top_pick: rec.top_pick, top_name: rec.top_name,
          why: rec.why || null, suggestions: list };
      }
    }
    return { top_pick: null, top_name: null, why: null, suggestions: [] };
  }

  // ── The step (F1, F2) ───────────────────────────────────────────────
  function openFactoryCoverStep(opts) {
    opts = opts || {};
    if (!opts.manifest) throw new Error('openFactoryCoverStep needs a manifest');
    var mapped = templatePageType(opts.template);
    var ownerIsNaya = !!(opts.owner_is_naya || (opts.page && opts.page.owner_is_naya));
    var page = opts.page || {};
    page.page_type = mapped.pageType;
    var born = bornCoverForTemplate({
      template: opts.template, manifest: opts.manifest, page: page,
      seed: opts.seed || 0, assetBase: opts.assetBase
    });
    var preselected = newCoverState('library', born.cover_key, null, 0, 'system');
    var sugg = suggestionsFor(opts.manifest, page, ownerIsNaya);
    var step = {
      step: 'factory_cover',
      template: opts.template,
      page_type: mapped.pageType,
      mode: 'create',
      doors: DOORS.slice(),
      preselected: preselected,
      born_cover: born,
      born_default: born,
      suggestions: sugg,
      shelves: categoryShelves(opts.manifest, ownerIsNaya),
      search_hint: "Try 'dog' or 'office' — or browse a category below.",
      skip: { action: 'skip', keeps: born.cover_key, taps: 1,
        note: 'Skip keeps ' + born.cover_key + ' — closing changes nothing.' },
      build: opts.build || {}
    };
    if (mapped.note) step.page_type_note = mapped.note;
    return step;
  }

  // ── Resolve one builder action (F4, C4, C5) ─────────────────────────
  // Returns {state, error, meta}: on ANY invalid pick state is null and
  // the caller KEEPS the current cover. skip / close / keep_default keep
  // the born cover, changed=false, in one tap.
  function resolveFactoryCoverAction(step, action, manifest, opts) {
    opts = opts || {};
    if (!step) return { state: null, error: 'no factory cover step open', meta: {} };
    var ownerIsNaya = !!(opts.owner_is_naya || step.owner_is_naya);
    var kind = (action || {}).action;
    var meta = { template: step.template, page_type: step.page_type };
    var born = step.born_cover || step.born_default || {};
    if (kind === 'skip' || kind === 'close' || kind === 'keep_default') {
      var kept = newCoverState('library', born.cover_key, null, 0, 'system');
      kept.via = born.via;
      meta.action = kind; meta.changed = false; meta.kept = born.cover_key; meta.taps = 1;
      return { state: kept, error: null, meta: meta };
    }
    if (kind === 'pick') {
      var current = step.preselected || newCoverState('library', born.cover_key, null, 0, 'system');
      var offset = 0;
      try { offset = clampOffset(action.offset_y === undefined ? (current.offset_y || 0) : action.offset_y); }
      catch (e) { return { state: null, error: 'invalid offset_y: ' + e.message,
        meta: Object.assign(meta, { action: 'pick', changed: false, kept: born.cover_key }) }; }
      if (action.source === 'library') {
        var asset = assetByKey(manifest, action.cover_key);
        if (!asset) return { state: null, error: 'unknown library cover: ' + JSON.stringify(action.cover_key),
          meta: Object.assign(meta, { action: 'pick', changed: false, kept: born.cover_key }) };
        if (!servable(asset, ownerIsNaya)) {
          return { state: null, error: 'cover ' + action.cover_key + ' is not servable to this owner (status=' + asset.status + ')',
            meta: Object.assign(meta, { action: 'pick', changed: false, kept: born.cover_key }) };
        }
        var picked = newCoverState('library', action.cover_key, null, offset, 'owner');
        picked.via = 'owner_pick';
        meta.action = 'pick'; meta.changed = true; meta.cover_key = action.cover_key;
        return { state: picked, error: null, meta: meta };
      }
      if (action.source === 'upload') {
        if (!validUploadRef(action.upload_ref)) {
          return { state: null, error: 'invalid upload_ref: ' + JSON.stringify(action.upload_ref),
            meta: Object.assign(meta, { action: 'pick', changed: false, kept: born.cover_key }) };
        }
        var up = newCoverState('upload', null, action.upload_ref, offset, 'owner');
        up.via = 'owner_pick';
        meta.action = 'pick'; meta.changed = true; meta.upload_ref = action.upload_ref;
        return { state: up, error: null, meta: meta };
      }
      return { state: null, error: "unknown source: " + JSON.stringify(action.source) + " (want 'library' or 'upload')",
        meta: Object.assign(meta, { action: 'pick', changed: false, kept: born.cover_key }) };
    }
    if (kind === 'adjust') {
      var cur = step.preselected || newCoverState('library', born.cover_key, null, 0, 'system');
      var off;
      try { off = clampOffset(action.offset_y); }
      catch (e) { return { state: null, error: 'invalid offset_y: ' + e.message,
        meta: Object.assign(meta, { action: 'adjust', changed: false }) }; }
      var adj = newCoverState(cur.source, cur.cover_key, cur.upload_ref, off, cur.set_by);
      adj.via = cur.via;
      meta.action = 'adjust'; meta.changed = true; meta.offset_y = off;
      return { state: adj, error: null, meta: meta };
    }
    return { state: null, error: "unknown chooser action: " + JSON.stringify(kind) +
      " (want 'pick', 'skip', 'close', 'keep_default' or 'adjust')", meta: meta };
  }

  // ── Store with the build (F3, F4) ───────────────────────────────────
  function coverFieldsForBuild(coverState, manifest, assetBase) {
    if (!coverState || (!coverState.cover_key && !coverState.upload_ref)) {
      return { fields: null, error: 'no cover to store (blank cover state)' };
    }
    var url;
    if (coverState.source === 'upload') {
      url = coverState.upload_ref;
    } else if (coverState.source === 'default' ||
               coverState.cover_key === DEFAULT_COVER) {
      // The built-in default is a render key, not a library asset: the
      // app renders it as the house gradient (same as the assign engine).
      url = DEFAULT_COVER;
    } else {
      url = coverUrl(manifest, coverState.cover_key, assetBase);
    }
    if (!url) {
      return { fields: null, error: 'cover ' +
        JSON.stringify(coverState.cover_key || coverState.upload_ref) +
        ' resolves to no URL in this manifest' };
    }
    return { fields: {
      cover_key: coverState.cover_key || null,
      upload_ref: coverState.upload_ref || null,
      cover_url: url,
      cover_source: coverState.source,
      cover_via: coverState.via || 'owner_pick',
      set_by: coverState.set_by,
      offset_y: (typeof coverState.offset_y === 'number' ? coverState.offset_y : 0)
    }, error: null };
  }

  // Pure: the input contract is never mutated. coverState null -> the born
  // default for the contract's template is resolved and stored (never
  // blank). An existing different cover is refused unless opts.replace.
  function applyCoverToContract(contract, coverState, manifest, opts) {
    opts = opts || {};
    if (!contract || typeof contract !== 'object') {
      return { contract: null, fields: null, error: 'build contract is not an object' };
    }
    var mapped;
    try { mapped = templatePageType(contract.template); }
    catch (e) { return { contract: null, fields: null, error: e.message }; }
    var state = coverState;
    if (!state) {
      var born = bornCoverForTemplate({ template: contract.template, manifest: manifest,
        page: null, seed: opts.seed || 0, assetBase: opts.assetBase });
      state = { source: born.source, cover_key: born.cover_key, upload_ref: null,
        offset_y: 0, set_by: 'system', via: born.via };
    }
    var existing = contract.cover;
    if (existing && !opts.replace) {
      var existingKey = existing.cover_key || existing.upload_ref;
      var newKey = state.cover_key || state.upload_ref;
      if (existingKey && newKey && existingKey !== newKey) {
        return { contract: null, fields: null,
          error: 'contract already carries cover ' + JSON.stringify(existingKey) +
            ' (refusing to overwrite with ' + JSON.stringify(newKey) + ' without replace:true)' };
      }
    }
    var shaped = coverFieldsForBuild(state, manifest, opts.assetBase);
    if (shaped.error) return { contract: null, fields: null, error: shaped.error };
    var next = Object.assign({}, contract);
    next.cover = shaped.fields;
    return { contract: next, fields: shaped.fields, error: null };
  }

  function factoryCoverReceipt(buildId, template, coverFields, workerName, url) {
    return { build_id: buildId, template: template, worker: workerName || null,
      url: url || null, cover: coverFields || null };
  }

  // ── Self-test (node naya-factory-cover-picker.js --selftest) ─────────
  function selftest() {
    var fixture = {
      assignment_on_page_creation: {
        personal_page: 'area/personal', business_page: 'area/business',
        space: 'area/spaces', events_page: 'area/events',
        any_other_page: 'rotation set'
      },
      assets: [
        { key: 'area/personal', file: 'areas/personal.jpg', kind: 'area', status: 'ready', name: 'Area — Personal', category: 'house-area', suits: 'personal pages', credit: 'Naya Resolve', tier: 'signature' },
        { key: 'area/business', file: 'areas/business.jpg', kind: 'area', status: 'ready', name: 'Area — Business', category: 'house-area', suits: 'business pages', credit: 'Naya Resolve', tier: 'signature' },
        { key: 'area/events', file: 'areas/events.jpg', kind: 'area', status: 'ready', name: 'Area — Events', category: 'house-area', suits: 'event pages', credit: 'Naya Resolve', tier: 'signature' },
        { key: 'open/companion-golden', file: 'open/companion-golden.jpg', kind: 'open', status: 'ready', name: 'Companion Golden', category: 'companions', suits: 'a golden retriever at dawn, for dog lovers', credit: 'Naya Resolve', tier: 'open', featured_class: 'citizen', featured_order: 1 },
        { key: 'open/quiet-office', file: 'open/quiet-office.jpg', kind: 'open', status: 'ready', name: 'Quiet Office', category: 'craft', suits: 'a clean minimal office for professionals', credit: 'Naya Resolve', tier: 'open' },
        { key: 'open/retired-one', file: 'open/retired.jpg', kind: 'open', status: 'retired', name: 'Retired One', category: 'abstract', suits: 'retired', credit: 'Naya Resolve', tier: 'open' },
        { key: 'rotation/her-kingdom-tree', file: 'rotation/her-kingdom-tree.jpg', kind: 'rotation', status: 'ready', name: 'Her Kingdom Tree', category: 'house-signature', suits: 'kingdom tree', credit: 'Naya Resolve', tier: 'signature' }
      ]
    };
    var checks = [];
    function check(name, cond) { checks.push({ name: name, ok: !!cond }); }
    var step = openFactoryCoverStep({ template: 'personal', manifest: fixture });
    check('personal born is area/personal via area_default',
      step.born_cover.cover_key === 'area/personal' && step.born_cover.via === 'area_default');
    check('skip keeps born', (function () {
      var r = resolveFactoryCoverAction(step, { action: 'skip' }, fixture);
      return !r.error && r.state.cover_key === 'area/personal' && r.meta.changed === false;
    })());
    check('pick stores chosen cover', (function () {
      var r = resolveFactoryCoverAction(step, { action: 'pick', source: 'library', cover_key: 'open/companion-golden' }, fixture);
      return !r.error && r.state.cover_key === 'open/companion-golden' && r.state.set_by === 'owner';
    })());
    check('retired pick refused, born kept', (function () {
      var r = resolveFactoryCoverAction(step, { action: 'pick', source: 'library', cover_key: 'open/retired-one' }, fixture);
      return !!r.error && r.state === null && r.meta.kept === 'area/personal';
    })());
    check('apply stores cover in contract', (function () {
      var r = resolveFactoryCoverAction(step, { action: 'pick', source: 'library', cover_key: 'open/companion-golden' }, fixture);
      var a = applyCoverToContract({ template: 'personal', handle: 'alex' }, r.state, fixture);
      return !a.error && a.contract.cover.cover_key === 'open/companion-golden' &&
        a.contract.cover.cover_url.indexOf('open/companion-golden.jpg') !== -1;
    })());
    check('no-state apply resolves born default', (function () {
      var a = applyCoverToContract({ template: 'event' }, null, fixture);
      return !a.error && a.contract.cover.cover_key === 'area/events';
    })());
    check('unknown template refused', (function () {
      try { openFactoryCoverStep({ template: 'today', manifest: fixture }); return false; }
      catch (e) { return e.message.indexOf('unknown factory template') === 0; }
    })());
    var failed = checks.filter(function (c) { return !c.ok; });
    return { ok: failed.length === 0, tests: checks.length,
      failed: failed.map(function (c) { return c.name; }) };
  }

  var api = {
    TEMPLATE_PAGE_TYPES: TEMPLATE_PAGE_TYPES,
    REGISTRY_TEMPLATES: REGISTRY_TEMPLATES,
    CATCH_ALL_TEMPLATES: CATCH_ALL_TEMPLATES,
    DOORS: DOORS,
    DEFAULT_ASSET_BASE: DEFAULT_ASSET_BASE,
    DEFAULT_COVER: DEFAULT_COVER,
    templatePageType: templatePageType,
    bornCoverForTemplate: bornCoverForTemplate,
    openFactoryCoverStep: openFactoryCoverStep,
    resolveFactoryCoverAction: resolveFactoryCoverAction,
    coverFieldsForBuild: coverFieldsForBuild,
    applyCoverToContract: applyCoverToContract,
    factoryCoverReceipt: factoryCoverReceipt,
    categoryShelves: categoryShelves,
    selftest: selftest
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    if (require.main === module && process.argv.indexOf('--selftest') !== -1) {
      process.stdout.write(JSON.stringify(selftest()) + '\n');
    }
  }
  if (global) {
    global.NayaFactoryCoverPicker = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
