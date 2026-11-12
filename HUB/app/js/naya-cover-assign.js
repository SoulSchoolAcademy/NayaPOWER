/*
 * naya-cover-assign.js — Manifest-driven cover assignment at page creation.
 * (PI item cover-library-wiring, Cover library, order rank 6; naya-power.)
 *
 * The seam this file wires, end to end:
 *
 *   page creation (any path: walkthrough birth, Smart Factory template,
 *   any future creator)
 *     → THIS FILE: assignCoverForPage({pageType, page, manifest, seed})
 *         → the manifest's assignment table by page type
 *           (area/personal, area/business, area/spaces, area/events…)
 *         → else the best-matching cover for the page card (≥ 2 signals)
 *         → else the next rotating cover, cycling deterministically
 *         → else the built-in default cover. NEVER blank, NEVER null.
 *     → cover_url lands on the born page (page_about.cover_url).
 *
 * What is HARVESTED, not invented:
 * - The manifest itself: HUB/covers/manifest.json on main (blob sha
 *   fd2ed9444978dfaebe65053904953f4479724971, 89 assets, read live this
 *   pass). The assignment table, the asset cards, the typical_terms map,
 *   the slot (1920x640, 3:1) all come from it. This file never copies
 *   the manifest: the caller passes it in, and the file reads it by key.
 * - The default chain + serving rules from FEATURE.ai.md / the
 *   cover-chooser contract (workspace/system/
 *   cover-chooser-every-page-2026-11-11.py, 28/28 tests): area default
 *   if ready → recommend (≥ 2 signal families) → rotation → default;
 *   no card, no entry; retired never served; citizens never see
 *   exclusive / house-signature / house-area covers except a Naya's own
 *   page; a failed save never strips the existing cover (this file only
 *   assigns at creation — it never un-assigns).
 * - The match model from smart_match_v1_1.score() (weights topics .40 /
 *   goals .25 / offers_needs .20 / wants .15; governed taxonomy v1,
 *   ported verbatim below): the same scoring the chooser uses, so the
 *   born cover and the chooser's recommendation agree with each other.
 * - The birth module's cover seam (walkthrough-page-birth-wiring,
 *   naya-page-birth.js): its assignCover assumed a shorthand manifest
 *   {areas, rotating} that the real manifest.json does NOT have. This
 *   file accepts BOTH shapes (normalizeManifest) and is the single
 *   engine the birth module delegates to — one assignment, every path.
 *
 * URL base (a deployment fact, not an assignment fact):
 * The worker serves static assets from HUB/app/ only (HUB/wrangler.toml
 * [assets] directory = "./app"; no /covers route exists in
 * HUB/hub-worker.js), while the library ships at HUB/covers/. So a
 * cover URL of /covers/<file> would hit the SPA fallback, not the
 * image. The URL that provably serves the assets today is the repo raw
 * base — the same base hub-worker.js itself fetches the Smart Note
 * registry from (RAW_BASE). DEFAULT_ASSET_BASE is that raw base, and it
 * is overridable per call (opts.assetBase): the production gate switches
 * it to https://nayanet.app/covers the moment a /covers route lands,
 * with zero change to the assignment logic. Asset files are versioned
 * with the code, per the manifest's hosting decision — no manual
 * Cloudflare upload step, ever.
 *
 * What this file does NOT do (owed steps, other lanes — never claimed):
 * - It does not mount itself into any live page. The mount is one line
 *   at the intake mount site (see SPEC.md): the production gate supplies
 *   the real store + the live manifest and wires onFinished. Until then
 *   this file is proven in tests + landed in the repo, never claimed live.
 * - It does not supply the 3 missing area covers (area/booking,
 *   area/templates, area/intel-today are 'designed', not 'ready').
 *   Resolve's owed supply; this file routes around them (fallback chain)
 *   and flags them in validateManifest.
 * - It does not render anything. Rendered proof at the real address is
 *   owed (parent / browser lane). Never claim live/AAA from these tests.
 *
 * Dual runtime like naya-intake.js / naya-page-birth.js: browser
 * (window.NayaCoverAssign) and Node (module.exports) share this one file.
 */
(function (global) {
  'use strict';

  // ── Settled law, encoded ────────────────────────────────────────────
  // Shawn 2026-10-25: pages are born with an impressive cover, never
  // blank. Manifest hosting decision: the library ships as assets inside
  // the app, versioned with the code. Page creation assigns by key.

  // The asset base that provably serves HUB/covers/ today (see header).
  var DEFAULT_ASSET_BASE =
    'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/HUB/covers/';

  // Built-in last resort: the house cover. Named, visible, never blank.
  // The app renders this key as the house gradient; it is a fallback,
  // not a cover from the library. Same key as naya-page-birth.js.
  var DEFAULT_COVER = 'naya:default-cover';

  var MATCH_CARD_REQUIRED = ['key', 'name', 'category', 'tier', 'suits', 'status', 'credit', 'file'];
  var HOUSE_CATEGORIES = { 'house-signature': true, 'house-area': true };
  var ROTATION_KINDS = { 'rotation': true, 'rotating': true };
  var ALTERNATES_MAX = 11;
  var SURFACE_SIGNALS = 2;

  // Page type -> birth kind (walkthrough-page-birth-wiring kinds).
  var KIND_TO_PAGE_TYPE = {
    personal: 'personal_page',
    business: 'business_page',
    space: 'space',
    events: 'events_page',
  };

  // ── Word helpers (ported from the chooser contract) ────────────────
  var STOPWORDS = {
    a: true, an: true, the: true, and: true, or: true, of: true, for: true,
    to: true, in: true, on: true, with: true, my: true, our: true,
    your: true, is: true, it: true, its: true, i: true, me: true, we: true,
    you: true, that: true, this: true, at: true, by: true, from: true,
    as: true, are: true, be: true, am: true, do: true, so: true, her: true,
    his: true, their: true, was: true, were: true, will: true,
    would: true, can: true, could: true, page: true, cover: true,
    naya: true, nayanet: true,
  };

  function normalize(text) {
    return String(text || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').replace(/^\s+|\s+$/g, '');
  }

  function tokenize(text) {
    var out = {};
    if (!text) return out;
    var words = String(text).toLowerCase().match(/[a-z0-9]+/g) || [];
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (!STOPWORDS[w] && w.length > 1) out[w] = true;
    }
    return out;
  }

  function setToArray(set) {
    var out = [];
    for (var k in set) if (set[k]) out.push(k);
    return out.sort();
  }

  function isNonEmptyString(v) {
    return typeof v === 'string' && v.trim().length > 0;
  }

  // ── Smart-match scoring (ported verbatim from smart_match_v1_1.py) ──
  // Weights topics .40 / goals .25 / offers_needs .20 / wants .15.
  // Governed taxonomy v1: concept -> member terms. Matching runs over
  // raw terms + concepts. A % without reasons is a bug; reasons ride along.
  var WEIGHTS = { topics: 0.40, goals: 0.25, offers_needs: 0.20, wants: 0.15 };
  var TAXONOMY = {
    MAKING: ['building', 'creation', 'templates', 'apps', 'step 7', 'app creation'],
    SHIPPING: ['execution', 'delivery', 'ship', 'waves', 'build loop'],
    PROVING: ['testing', 'validation', 'quality', 'quality control', 'evidence', 'proof', 'verification', 'audit'],
    CONNECTING: ['integration', 'systems', 'network', 'coordination', 'the platform'],
    SPEAKING: ['voice', 'speech', 'audio', 'streaming', 'synthesis', 'ear test'],
    TALKING: ['mail', 'messaging', 'communication', 'conversation', 'questions', 'answers', 'listening', 'scheduling'],
    THINKING: ['distillation', 'essence', 'reflection', 'learning', 'analysis', 'critical thinking', 'root cause', 'derivation', 'project intelligence'],
    CLEARING: ['blockers', 'problem solving', 'conflict resolution', 'risk', 'risk review', 'reliability', 'unblocking'],
    GUIDING: ['strategy', 'project leadership', 'orientation', 'home', 'long-term strategy', 'design'],
    DECIDING: ['performance rulings', 'governance', 'decisions'],
    PUBLISHING: ['smart notes', 'feed', 'publishing', 'flow', 'publishing path', 'notes'],
    PEOPLE: ['citizens', 'usage', 'readers', 'material'],
  };
  var TERM2CONCEPTS = {};
  (function () {
    for (var concept in TAXONOMY) {
      var terms = TAXONOMY[concept];
      for (var i = 0; i < terms.length; i++) {
        if (!TERM2CONCEPTS[terms[i]]) TERM2CONCEPTS[terms[i]] = [];
        TERM2CONCEPTS[terms[i]].push(concept);
      }
    }
  })();

  function expand(terms) {
    var sig = {};
    var list = terms || [];
    for (var i = 0; i < list.length; i++) {
      var t = list[i];
      sig[t] = true;
      var concepts = TERM2CONCEPTS[t] || [];
      for (var j = 0; j < concepts.length; j++) sig[concepts[j]] = true;
    }
    return sig;
  }

  function overlap(aTerms, bTerms) {
    var A = expand(aTerms);
    var B = expand(bTerms);
    var aKeys = setToArray(A);
    var bKeys = setToArray(B);
    if (!aKeys.length || !bKeys.length) return { ratio: 0, shared: [] };
    var shared = [];
    for (var i = 0; i < aKeys.length; i++) if (B[aKeys[i]]) shared.push(aKeys[i]);
    var denom = Math.min(aKeys.length, bKeys.length);
    return { ratio: shared.length / denom, shared: shared };
  }

  function matchScore(a, b) {
    var t = overlap(a.topics, b.topics);
    var g = overlap(a.goals, b.goals);
    var on1 = overlap(a.offers, b.needs);
    var on2 = overlap(b.offers, a.needs);
    var on = (on1.ratio + on2.ratio) / 2;
    var w1 = overlap(a.wants, (b.topics || []).concat(b.offers || []));
    var w2 = overlap(b.wants, (a.topics || []).concat(a.offers || []));
    var w = (w1.ratio + w2.ratio) / 2;
    var parts = { topics: t.ratio, goals: g.ratio, offers_needs: on, wants: w };
    var relevance = Math.round(100 * (WEIGHTS.topics * parts.topics +
      WEIGHTS.goals * parts.goals + WEIGHTS.offers_needs * parts.offers_needs +
      WEIGHTS.wants * parts.wants));
    var signals = [];
    for (var k in parts) if (parts[k] > 0) signals.push(k);
    var reasons = [];
    if (t.shared.length) reasons.push('shared: ' + t.shared.slice(0, 5).join(', '));
    if (g.shared.length) reasons.push('shared goals: ' + g.shared.slice(0, 3).join(', '));
    var fits = {};
    on1.shared.concat(on2.shared).forEach(function (s) { fits[s] = true; });
    var fitList = setToArray(fits);
    if (fitList.length) reasons.push('offer/need fit: ' + fitList.slice(0, 3).join(', '));
    var wants = {};
    w1.shared.concat(w2.shared).forEach(function (s) { wants[s] = true; });
    var wantList = setToArray(wants);
    if (wantList.length) reasons.push('wanted connection: ' + wantList.slice(0, 3).join(', '));
    return { score: relevance, rank: relevance, signals: signals, surface: signals.length >= 2, parts: parts, reasons: reasons };
  }

  // ── Manifest normalization (real shape AND birth shorthand) ─────────
  // Real manifest.json: {assets: [{key, file, kind, status, ...}],
  // assignment_on_page_creation: {pageType: coverKey}, typical_terms}.
  // Birth shorthand (naya-page-birth.js tests + deps): {areas:
  // {coverKey: coverUrl}, rotating: [coverUrl, ...]}. Both normalize to
  // {assets, assignment, typical_terms} so one chain serves every path.
  // Shorthand assets carry url verbatim (they ARE the cover string the
  // birth module promised); real assets resolve via the asset base.

  function normalizeManifest(manifest) {
    var m = manifest || {};
    if (Array.isArray(m.assets)) {
      return {
        assets: m.assets,
        assignment: m.assignment_on_page_creation || {},
        typical_terms: m.typical_terms || {},
        shorthand: false,
      };
    }
    var assets = [];
    var assignment = {};
    var areas = m.areas || {};
    var kindFor = { personal: 'personal_page', business: 'business_page', space: 'space', events: 'events_page' };
    var areaToKind = { 'area/personal': 'personal', 'area/business': 'business', 'area/spaces': 'space', 'area/events': 'events' };
    for (var key in areas) {
      assets.push({ key: key, file: areas[key], url: areas[key], kind: 'area',
        status: 'ready', name: key, category: 'house-area',
        suits: '', credit: '', tier: 'signature' });
      var kind = areaToKind[key];
      if (kind && kindFor[kind]) assignment[kindFor[kind]] = key;
    }
    var rotating = m.rotating || [];
    for (var i = 0; i < rotating.length; i++) {
      if (!isNonEmptyString(rotating[i])) continue;
      assets.push({ key: 'rotating[' + i + ']', file: rotating[i], url: rotating[i],
        kind: 'rotation', status: 'ready', name: 'Rotating ' + i,
        category: 'house-signature', suits: '', credit: '', tier: 'signature' });
    }
    return { assets: assets, assignment: assignment, typical_terms: {}, shorthand: true };
  }

  // ── Asset lookup + URL ──────────────────────────────────────────────
  function assetByKey(manifest, key) {
    var assets = (manifest && manifest.assets) || [];
    for (var i = 0; i < assets.length; i++) if (assets[i].key === key) return assets[i];
    return null;
  }

  function coverUrl(manifest, coverKey, assetBase) {
    var asset = assetByKey(manifest, coverKey);
    if (!asset) return null;
    if (isNonEmptyString(asset.url)) return asset.url;
    if (!isNonEmptyString(asset.file)) return null;
    var base = assetBase || DEFAULT_ASSET_BASE;
    if (base.slice(-1) !== '/') base += '/';
    return base + asset.file;
  }

  // ── Shelf + rotation ────────────────────────────────────────────────
  function isCompleteCard(asset) {
    for (var i = 0; i < MATCH_CARD_REQUIRED.length; i++) {
      if (!asset[MATCH_CARD_REQUIRED[i]]) return false;
    }
    return true;
  }

  function incompleteFields(asset) {
    var out = [];
    for (var i = 0; i < MATCH_CARD_REQUIRED.length; i++) {
      if (!asset[MATCH_CARD_REQUIRED[i]]) out.push(MATCH_CARD_REQUIRED[i]);
    }
    return out;
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

  function citizenShelf(norm, ownerIsNaya) {
    var assets = [];
    for (var i = 0; i < norm.assets.length; i++) {
      if (servable(norm.assets[i], ownerIsNaya)) assets.push(norm.assets[i]);
    }
    var featured = [];
    var rest = [];
    for (var j = 0; j < assets.length; j++) {
      if (assets[j].featured_class === 'citizen') featured.push(assets[j]);
      else rest.push(assets[j]);
    }
    featured.sort(function (a, b) {
      var ao = (typeof a.featured_order === 'number') ? a.featured_order : 1000000;
      var bo = (typeof b.featured_order === 'number') ? b.featured_order : 1000000;
      return (ao - bo) || (a.key < b.key ? -1 : a.key > b.key ? 1 : 0);
    });
    rest.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : 0; });
    return featured.concat(rest);
  }

  function rotationSet(norm) {
    var out = [];
    for (var i = 0; i < norm.assets.length; i++) {
      var a = norm.assets[i];
      if (ROTATION_KINDS[a.kind] && a.status === 'ready') out.push(a);
    }
    out.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : 0; });
    return out;
  }

  function rotationPick(norm, seed) {
    var rot = rotationSet(norm);
    if (!rot.length) return null;
    var idx = ((seed || 0) % rot.length + rot.length) % rot.length;
    return { asset: rot[idx], index: idx };
  }

  // ── Page + cover vectors (chooser contract) ─────────────────────────
  function termAreas(norm) {
    return (norm.typical_terms && norm.typical_terms.areas) || {};
  }

  function coverAreaKeys(norm, coverKey) {
    var areas = termAreas(norm);
    var suffix = String(coverKey).split('/').pop();
    var found = [];
    for (var ak in areas) {
      var refs = (areas[ak] && areas[ak].covers) || [];
      for (var i = 0; i < refs.length; i++) {
        if (refs[i] === coverKey || refs[i] === suffix) { found.push(ak); break; }
      }
    }
    return found;
  }

  function buildCoverVector(asset, norm) {
    var areas = termAreas(norm);
    var areaKeys = coverAreaKeys(norm, asset.key);
    var topics = {};
    if (asset.category) topics[asset.category] = true;
    for (var i = 0; i < areaKeys.length; i++) {
      var ak = areaKeys[i];
      var terms = (areas[ak] && areas[ak].terms) || [];
      for (var j = 0; j < terms.length; j++) topics[normalize(terms[j])] = true;
      topics[ak] = true;
      var akTokens = tokenize(ak);
      for (var t in akTokens) topics[t] = true;
    }
    var nameTokens = tokenize(asset.name || '');
    for (var n in nameTokens) topics[n] = true;
    var suitsTokens = tokenize(asset.suits || '');
    for (var s in suitsTokens) topics[s] = true;
    delete topics[''];
    return { topics: setToArray(topics), goals: areaKeys.slice().sort(), offers: [], needs: [], wants: [] };
  }

  function buildPageVector(page, norm) {
    page = page || {};
    var words = tokenize(page.purpose || '');
    var topicsList = page.topics || [];
    for (var i = 0; i < topicsList.length; i++) words[normalize(topicsList[i])] = true;
    delete words[''];
    var goals = {};
    var goalsList = page.goals || [];
    for (var j = 0; j < goalsList.length; j++) {
      var g = normalize(goalsList[j]);
      if (g) goals[g] = true;
    }
    var areas = termAreas(norm);
    for (var ak in areas) {
      var terms = (areas[ak] && areas[ak].terms) || [];
      for (var k = 0; k < terms.length; k++) {
        if (words[normalize(terms[k])]) { goals[ak] = true; break; }
      }
    }
    return {
      topics: setToArray(words),
      goals: setToArray(goals),
      offers: (page.offers || []).slice(),
      needs: (page.needs || []).slice(),
      wants: (page.wants || []).slice(),
    };
  }

  function whySentence(cover, result) {
    var reasons = result.reasons || [];
    if (!reasons.length) return 'Chosen for ' + (cover.name || cover.key) + '.';
    var detail = reasons.join('; ').replace(/\.+$/g, '');
    return 'Fits ' + (cover.name || cover.key) + ' — ' + detail + '.';
  }

  // ── Recommend (chooser contract, ≥ 2 signal families) ──────────────
  function recommend(page, manifest, ownerIsNaya) {
    var norm = normalizeManifest(manifest);
    var pv = buildPageVector(page, norm);
    var shelf = citizenShelf(norm, ownerIsNaya);
    var scored = [];
    for (var i = 0; i < shelf.length; i++) {
      var cv = buildCoverVector(shelf[i], norm);
      var r = matchScore(pv, cv);
      if (r.signals.length >= SURFACE_SIGNALS) {
        scored.push({ rank: r.rank, key: shelf[i].key, asset: shelf[i], result: r });
      }
    }
    scored.sort(function (a, b) { return (b.rank - a.rank) || (a.key < b.key ? -1 : a.key > b.key ? 1 : 0); });
    if (!scored.length) {
      return { top_pick: null, alternates: [], surfaced: 0, why: null, reason: 'no cover shares >= 2 signals with this page' };
    }
    var top = scored[0];
    var alternates = [];
    for (var j = 1; j < scored.length && alternates.length < ALTERNATES_MAX; j++) {
      alternates.push({ cover_key: scored[j].key, name: scored[j].asset.name,
        rank: scored[j].rank, signals: scored[j].result.signals,
        why: whySentence(scored[j].asset, scored[j].result) });
    }
    return { top_pick: top.key, top_name: top.asset.name, rank: top.rank,
      signals: top.result.signals, why: whySentence(top.asset, top.result),
      alternates: alternates, surfaced: scored.length };
  }

  // ── The assignment (the born cover — never blank) ───────────────────
  // Chain, in order: (1) the manifest's assignment-table area cover for
  // the page type, if it exists AND is ready; (2) recommend() top pick
  // (≥ 2 signals); (3) the rotation set, cycling deterministically by
  // seed; (4) the built-in default cover. `via` names which step chose
  // it, so the default is auditable, never magic.
  function assignCoverForPage(opts) {
    opts = opts || {};
    var norm = normalizeManifest(opts.manifest);
    var pageType = opts.pageType || 'any_other_page';
    var ownerIsNaya = !!((opts.page || {}).owner_is_naya);
    var assetBase = opts.assetBase || DEFAULT_ASSET_BASE;
    var named = norm.assignment[pageType];
    if (named) {
      var areaAsset = assetByKey(norm, named);
      if (areaAsset && areaAsset.status === 'ready') {
        return { cover_key: named, name: areaAsset.name,
          cover_url: coverUrl(norm, named, assetBase),
          source: 'library', via: 'area_default', set_by: 'system',
          rotation_index: null };
      }
    }
    var rec = recommend(opts.page, opts.manifest, ownerIsNaya);
    if (rec.top_pick) {
      return { cover_key: rec.top_pick, name: rec.top_name,
        cover_url: coverUrl(norm, rec.top_pick, assetBase),
        source: 'library', via: 'recommendation', set_by: 'system',
        why: rec.why, rotation_index: null };
    }
    var pick = rotationPick(norm, opts.seed || 0);
    if (pick) {
      return { cover_key: pick.asset.key, name: pick.asset.name,
        cover_url: coverUrl(norm, pick.asset.key, assetBase),
        source: 'library', via: 'rotation', set_by: 'system',
        rotation_index: pick.index };
    }
    return { cover_key: DEFAULT_COVER, name: 'Naya default cover',
      cover_url: DEFAULT_COVER, source: 'default', via: 'builtin_default',
      set_by: 'system', rotation_index: null };
  }

  // Birth-module adapter: naya-page-birth.js assignCover(kind, manifest,
  // rotationIndex) delegates here and keeps its exact return shape
  // {cover, source, key}. `source` vocabulary: area | recommendation |
  // rotating | default.
  function assignCoverLegacy(pageKind, manifest, rotationIndex) {
    var pageType = KIND_TO_PAGE_TYPE[pageKind] || 'any_other_page';
    var r = assignCoverForPage({ pageType: pageType, page: null, manifest: manifest, seed: rotationIndex || 0 });
    var source = r.via === 'area_default' ? 'area'
      : r.via === 'rotation' ? 'rotating'
      : r.via === 'recommendation' ? 'recommendation' : 'default';
    var key = r.cover_key === DEFAULT_COVER ? null
      : r.via === 'rotation' ? 'rotating[' + r.rotation_index + ']' : r.cover_key;
    return { cover: r.cover_url, source: source, key: key };
  }

  // ── Page types ──────────────────────────────────────────────────────
  function pageTypes(manifest) {
    var norm = normalizeManifest(manifest);
    var types = [];
    for (var k in norm.assignment) types.push(k);
    if (types.indexOf('membership_page') < 0) types.push('membership_page');
    if (types.indexOf('any_other_page') < 0) types.push('any_other_page');
    return types;
  }

  // ── Manifest validation (mirrors the chooser's validate_manifest) ───
  function validateManifest(manifest) {
    var norm = normalizeManifest(manifest);
    var assets = norm.assets;
    var report = {
      assets: assets.length,
      ready: 0,
      retired: [],
      incomplete_cards: {},
      citizen_servable: citizenShelf(norm, false).length,
      featured_citizen: 0,
      rotation_size: rotationSet(norm).length,
      mood_tagged: 0,
      dangling_term_refs: [],
      defaults_not_ready: [],
      defaults_missing: [],
      rotation_instruction: false,
      page_types: pageTypes(manifest),
    };
    var keys = {};
    var names = {};
    for (var i = 0; i < assets.length; i++) {
      var a = assets[i];
      keys[a.key] = true;
      names[normalize(a.name || '')] = true;
      if (a.status === 'ready') report.ready++;
      if (a.status === 'retired') report.retired.push(a.key);
      if (!isCompleteCard(a)) report.incomplete_cards[a.key] = incompleteFields(a);
      if (a.featured_class === 'citizen') report.featured_citizen++;
      if (a.mood_tags && a.mood_tags.length) report.mood_tagged++;
    }
    var areas = termAreas(norm);
    for (var ak in areas) {
      var refs = (areas[ak] && areas[ak].covers) || [];
      for (var j = 0; j < refs.length; j++) {
        var ref = refs[j];
        var suffix = String(ref).split('/').pop();
        if (keys[ref] || keys['open/' + ref] || keys['area/' + ref] ||
            keys['rotation/' + ref] || names[normalize(ref)]) continue;
        report.dangling_term_refs.push([ak, ref]);
      }
    }
    for (var pt in norm.assignment) {
      var named = norm.assignment[pt];
      if (String(named).indexOf(' ') >= 0) { report.rotation_instruction = true; continue; }
      var asset = assetByKey(norm, named);
      if (!asset) report.defaults_missing.push([pt, named]);
      else if (asset.status !== 'ready') report.defaults_not_ready.push([pt, named, asset.status]);
    }
    return report;
  }

  var api = {
    DEFAULT_ASSET_BASE: DEFAULT_ASSET_BASE,
    DEFAULT_COVER: DEFAULT_COVER,
    KIND_TO_PAGE_TYPE: KIND_TO_PAGE_TYPE,
    normalizeManifest: normalizeManifest,
    assetByKey: assetByKey,
    coverUrl: coverUrl,
    rotationSet: function (manifest) { return rotationSet(normalizeManifest(manifest)); },
    rotationPick: function (manifest, seed) {
      var p = rotationPick(normalizeManifest(manifest), seed);
      return p ? p.asset : null;
    },
    servable: servable,
    citizenShelf: function (manifest, ownerIsNaya) { return citizenShelf(normalizeManifest(manifest), ownerIsNaya); },
    recommend: recommend,
    assignCoverForPage: assignCoverForPage,
    assignCoverLegacy: assignCoverLegacy,
    pageTypes: pageTypes,
    validateManifest: validateManifest,
    matchScore: matchScore,
    buildPageVector: function (page, manifest) { return buildPageVector(page, normalizeManifest(manifest)); },
    buildCoverVector: function (asset, manifest) { return buildCoverVector(asset, normalizeManifest(manifest)); },
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    global.NayaCoverAssign = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
