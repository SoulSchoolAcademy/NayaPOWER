/* ============================================================================
   THE AUTO ORGANIZER — the automatic categorization engine
   ============================================================================
   Shawn's order, voice call 2026-11-26 ~21:35-21:43 MST ("Okay, so let's
   get her done"): "write an algorithm that using like just simple logic
   even categorization even as simple as a library, you should be able to
   auto organize these feeds... it just knows how to categorize it because
   it looks oh this goes with this, let's put those together."
   "Everything the whole system just auto organizes with intelligence and
   you can choose to always change those categories or move one thing from
   another... Like by default."
   "Auto organizer is sort of auto match... one's doing organizing, one's
   doing matching... they work together... in sync with the Smart Vault or
   the Nanonode."

   HARVESTED, NOT INVENTED (copy don't create):
   - Scoring is intelClusterOf, byte-for-byte the same logic, from the Hub
     (hub-unified-20261124/r20/hub-live-R12-BASE.html, smartTabStrip area)
     and its server twin (team-nitro/public-blog-seo-20261112/
     hub-worker-intel-today.js:451): a note scores each cluster by keyword
     hits in its topics + title + opening text; most hits wins; no hits
     lands in the home cluster. Weights: phrase longer than 12 chars = 3,
     phrase with a space = 2, single word = 1.
   - ONE HARDENING over the harvested pattern: keywords match on word
     boundaries, not raw substrings. The harvested indexOf would let the
     2-letter key "ai" match "said", "again", "training", and "tv" match
     "active". Same weights, same scoring — safer matching. Documented here
     so the next seat does not "fix" it back to indexOf.
   - Override storage follows the harvested human-tabs pattern
     (localStorage key nayanet.feed.smartTabs.v1): device-local JSON,
     in-memory fallback when storage is unavailable (Node, private mode).
   - The move UI follows the harvested category picker
     (openCategoryPicker): a .tab-menu panel of .mi items, outside click /
     Escape dismisses, picking files the entry under that category.

   WHAT IT DOES, IN PLAIN WORDS (the library):
   Every new thing — smart note, post, contact, list, or the citizen's
   own note — is a book arriving at the library. The Organizer reads its
   cover and its first page (title + opening words), looks at the words on
   the shelves (the taxonomy below), and puts the book on the shelf where
   the most words match. The shelf labels the citizen already picked win
   ties. If the citizen moves a book to another shelf, the move always
   wins — and the Organizer remembers which words taught it, so the next
   similar book goes to the right shelf the first time. If no words match
   at all, the book goes home (the citizen's first picked interest, or
   General) with a note saying so, so the citizen can place it.

   STRUCTURE: categories -> subcategories -> topics (the Q14 restructure).
   The 6 major categories and 25 subcategories are SETTLED (his list, web
   2026-11-26 ~18:49 MST; MEMORY.md "INTEREST CATEGORIES — FULL
   STRUCTURED LIST"). Keyword lists are built ONLY from his two word
   lists: that structured list and the first-10 list (chat 2026-11-26
   ~18:44 MST) — label words + description words + their plurals. Two
   words were deliberately LEFT OUT with reasons, in the spec.
   The TOPICS level is NOT settled: TOPICS starts empty; setTopics(list)
   loads it the moment he gives the list. Nothing about topics is invented.
   Until then every placement carries topic: null, topicReady: true.

   WHERE IT LIVES: this file is the engine. The Hub's Smart Tabs are its
   face: at note-load time the feed calls organize(item, ctx) and stores
   the result on the note as note.organizer = {category, subcategory,
   topic, confidence, reasons, source}. The tab strip then shows the
   item under its category tab. Placement is COMPUTED ON READ, not stored
   in the database — hub_smart_notes has no category column, and no
   schema change is needed or made. The only stored piece is the citizen's
   override (device-local, like human tabs).
   ========================================================================== */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.AutoOrganizer = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* --- THE TAXONOMY (settled; his list, 2026-11-26 ~18:49 MST) ------------
     6 majors, 25 subcategories. Keyword lists: label words + description
     words + plurals, from his structured list and his first-10 list
     (2026-11-26 ~18:44 MST). Shared words (journaling, writing, film,
     gardening, camping...) are listed in EVERY subcategory whose
     description contains them — each subcategory scores independently,
     exactly like the harvested clusters. Ties break by taxonomy order,
     then citizen picks, then learned rules. */
  var TAXONOMY = [
    { id: 'entertainment-media', label: 'Entertainment & Media', subs: [
      { id: 'music', label: 'Music', keys: ['music', 'listening', 'concert', 'concerts', 'playing instruments', 'singing', 'dance', 'dancing'] },
      { id: 'movies-television', label: 'Movies & Television', keys: ['movies', 'movie', 'television', 'streaming', 'series', 'films', 'film', 'pop culture', 'franchise', 'franchises', 'entertainment'] },
      { id: 'gaming', label: 'Gaming', keys: ['gaming', 'video games', 'video game', 'tabletop board games', 'board games', 'board game', 'role-playing games', 'role-playing game', 'console', 'online competitive', 'competitive'] },
      { id: 'reading-literature', label: 'Reading & Literature', keys: ['reading', 'literature', 'fiction', 'non-fiction', 'nonfiction', 'audiobooks', 'audiobook', 'book clubs', 'book club', 'journaling', 'journal', 'creative writing', 'writing', 'book', 'books'] },
      { id: 'podcasts-audio', label: 'Podcasts & Audio', keys: ['podcasts', 'podcast', 'audio', 'true crime', 'comedy', 'educational', 'conversational'] }
    ]},
    { id: 'food-drink', label: 'Food & Drink', subs: [
      { id: 'cooking-baking', label: 'Cooking & Baking', keys: ['cooking', 'baking', 'home cooking', 'recipe', 'recipes', 'recipe swaps', 'culinary', 'culinary exploration', 'food'] },
      { id: 'dining-out', label: 'Dining Out & Food Culture', keys: ['dining out', 'dining', 'restaurants', 'restaurant', 'street food', 'local cafes', 'cafe', 'cafes', 'food culture'] },
      { id: 'coffee-tea', label: 'Coffee, Tea & Craft Beverages', keys: ['coffee', 'tea', 'craft beverages', 'craft beverage', 'specialty coffee', 'mixology', 'wine tasting', 'wine', 'craft beer', 'beer', 'beverages', 'beverage'] }
    ]},
    { id: 'health-fitness-sports', label: 'Health, Fitness & Sports', subs: [
      { id: 'fitness-working-out', label: 'Fitness & Working Out', keys: ['fitness', 'working out', 'workout', 'workouts', 'strength', 'yoga', 'pilates', 'home workouts', 'swimming'] },
      { id: 'spectator-sports', label: 'Spectator Sports', keys: ['spectator sports', 'pro leagues', 'league', 'leagues', 'live matches', 'live match', 'fantasy sports', 'fantasy', 'sports'] },
      { id: 'recreational-team-sports', label: 'Recreational & Team Sports', keys: ['recreational team sports', 'team sports', 'pickleball', 'soccer', 'basketball', 'tennis', 'golf', 'recreational'] },
      { id: 'mental-health-mindfulness', label: 'Mental Health & Mindfulness', keys: ['mental health', 'mindfulness', 'meditation', 'journaling', 'journal', 'self-improvement', 'self improvement'] }
    ]},
    { id: 'outdoors-travel', label: 'Outdoors & Travel', subs: [
      { id: 'travel-exploration', label: 'Travel & Exploration', keys: ['travel', 'exploration', 'vacationing', 'vacation', 'road trips', 'road trip', 'cultural tourism', 'tourism', 'local trips', 'international travel', 'cultural festivals', 'festival', 'festivals', 'sightseeing', 'trip', 'trips'] },
      { id: 'hiking-nature', label: 'Hiking & Nature', keys: ['hiking', 'hike', 'nature', 'trail walking', 'trail', 'trails', 'camping', 'birding', 'birdwatching', 'parks', 'park', 'fishing', 'outdoors', 'outdoor'] },
      { id: 'gardening-houseplants', label: 'Gardening & Houseplants', keys: ['gardening', 'garden', 'houseplants', 'houseplant', 'indoor plants', 'indoor plant', 'backyard vegetables', 'vegetables', 'flower beds', 'flower bed'] },
      { id: 'pets-animals', label: 'Pets & Animals', keys: ['pets', 'pet', 'animals', 'animal', 'dogs', 'dog', 'cats', 'cat', 'exotic pets', 'caring for pets'] }
    ]},
    { id: 'arts-crafts-making', label: 'Arts, Crafts & Making', subs: [
      { id: 'visual-arts', label: 'Visual Arts', keys: ['visual arts', 'drawing', 'painting', 'digital illustration', 'illustration', 'sculpture'] },
      { id: 'photography-videography', label: 'Photography & Videography', keys: ['photography', 'photograph', 'videography', 'video', 'street photography', 'content creation', 'filmmaking', 'film'] },
      { id: 'fiber-textile-arts', label: 'Fiber & Textile Arts', keys: ['fiber', 'textile arts', 'textile', 'crocheting', 'crochet', 'knitting', 'knit', 'sewing', 'sew', 'embroidery'] },
      { id: 'writing-storytelling', label: 'Writing & Storytelling', keys: ['writing', 'storytelling', 'story', 'stories', 'creative writing', 'poetry', 'poem', 'poems', 'blogging', 'blog', 'journaling', 'journal'] },
      { id: 'diy-woodworking', label: 'DIY & Woodworking', keys: ['diy', 'do it yourself', 'woodworking', 'wood', 'home improvement', 'furniture building', 'furniture', 'pottery', 'candle making', 'candles', 'crafts', 'craft'] }
    ]},
    { id: 'lifestyle-tech-knowledge', label: 'Lifestyle, Tech & Knowledge', subs: [
      { id: 'fashion-personal-style', label: 'Fashion & Personal Style', keys: ['fashion', 'personal style', 'style', 'thrifting', 'thrift', 'streetwear', 'skincare', 'skin care', 'makeup'] },
      { id: 'home-decor', label: 'Home Decor & Interior Design', keys: ['home decor', 'decor', 'interior design', 'organizing', 'decorating', 'curating living spaces', 'living spaces', 'curating'] },
      { id: 'technology-gadgets', label: 'Technology & Gadgets', keys: ['technology', 'gadgets', 'gadget', 'consumer tech', 'tech', 'ai tools', 'pc building', 'smart home'] },
      { id: 'history-science-learning', label: 'History, Science & Learning', keys: ['history', 'science', 'language learning', 'astronomy', 'genealogy', 'trivia'] }
    ]}
  ];

  /* Topics level — NOT settled, NOT invented. Starts empty; setTopics(list)
     loads it the moment he gives the list. Each topic names its
     subcategory id; validation rejects any topic that does not. */
  var TOPICS = [];
  var TOPIC_BY_ID = {};

  var OVERRIDE_KEY = 'nayanet.organizer.overrides.v1';
  var RULE_KEY = 'nayanet.organizer.learned-rules.v1';
  var MAX_RULES = 50;

  /* --- stores (localStorage when available, memory fallback) --- */
  function makeStore(key) {
    var mem = null;
    function read() {
      try {
        var raw = (typeof localStorage !== 'undefined') ? localStorage.getItem(key) : null;
        if (raw) return JSON.parse(raw);
      } catch (e) {}
      return mem;
    }
    function write(v) {
      mem = v;
      try { if (typeof localStorage !== 'undefined') localStorage.setItem(key, JSON.stringify(v)); } catch (e) {}
    }
    return { read: read, write: write };
  }
  var overrideStore = makeStore(OVERRIDE_KEY);
  var ruleStore = makeStore(RULE_KEY);

  function readOverrides() { var o = overrideStore.read(); return (o && typeof o === 'object') ? o : {}; }
  function readRules() { var r = ruleStore.read(); return Array.isArray(r) ? r : []; }

  /* --- matching (harvested weights; word-boundary hardening, see header) --- */
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function wordHit(hay, key) {
    var re = new RegExp('\\b' + escRe(key) + '\\b', 'i');
    return re.test(hay);
  }
  function keyWeight(k) {
    if (k.length > 12) return 3;           /* long phrase, harvested */
    if (k.indexOf(' ') !== -1) return 2;   /* phrase, harvested */
    return 1;                              /* single word, harvested */
  }

  /* --- haystack per item type: cover + first page, nothing else --- */
  function haystackFor(item) {
    var parts = [];
    function add(v) { if (v !== undefined && v !== null && v !== '') parts.push(String(v)); }
    function addList(a) { if (Array.isArray(a)) a.forEach(add); }
    var t = item.type || 'note';
    addList(item.topics);
    if (t === 'contact') {
      add(item.name); add(item.alias); add(item.about);
      addList(item.interests); addList(item.sharedInterests);
    } else if (t === 'list') {
      add(item.name); add(item.title);
      addList(item.items);
    } else if (t === 'post') {
      add(item.title); add(item.body ? String(item.body).slice(0, 1200) : '');
    } else { /* note, own note, default */
      add(item.title); add(item.nutshell); add(item.subtitle);
      add(item.body ? String(item.body).slice(0, 1200) : '');
      add(item.human_note ? String(item.human_note).slice(0, 600) : '');
    }
    return parts.join(' ');
  }

  function findSub(id) {
    for (var i = 0; i < TAXONOMY.length; i++) {
      var subs = TAXONOMY[i].subs;
      for (var j = 0; j < subs.length; j++) {
        if (subs[j].id === id) return { major: TAXONOMY[i], sub: subs[j] };
      }
    }
    return null;
  }
  function findMajor(id) {
    for (var i = 0; i < TAXONOMY.length; i++) if (TAXONOMY[i].id === id) return TAXONOMY[i];
    return null;
  }

  /* Score every subcategory. Returns [{major, sub, score, hits[]}] in
     taxonomy order — order IS the tie-break, deterministic, like the
     harvested clusters' priority order. */
  function scoreAll(item, hay, ctx) {
    var picks = (ctx && ctx.picks) || [];
    var rules = readRules();
    var out = [];
    TAXONOMY.forEach(function (major) {
      major.subs.forEach(function (sub) {
        var score = 0, hits = [];
        sub.keys.forEach(function (k) {
          if (wordHit(hay, k)) { score += keyWeight(k); hits.push(k); }
        });
        /* Explicit topic naming this subcategory: a direct hit. */
        if (Array.isArray(item.topics)) {
          item.topics.forEach(function (tp) {
            var low = String(tp).toLowerCase();
            if (low === sub.label.toLowerCase() || low === sub.id) { score += 10; hits.push('topic:' + sub.label); }
          });
        }
        /* Citizen's declared picks win ties: +2 to a picked subcategory. */
        if (picks.indexOf(sub.label) !== -1 || picks.indexOf(sub.id) !== -1) {
          if (score > 0) { score += 2; hits.push('pick:' + sub.label); }
        }
        /* Learned rules: words a past move taught us, +2 each. */
        rules.forEach(function (r) {
          if (r.subcategory === sub.id) {
            r.keywords.forEach(function (k) { if (wordHit(hay, k)) { score += 2; hits.push('learned:' + k); } });
          }
        });
        out.push({ major: major, sub: sub, score: score, hits: hits });
      });
    });
    return out;
  }

  function confidenceFor(score) {
    if (score >= 6) return 'high';
    if (score >= 3) return 'medium';
    if (score >= 1) return 'low';
    return 'none';
  }

  /* --- the Organizer: place one item --- */
  function organize(item, ctx) {
    item = item || {};
    ctx = ctx || {};
    var id = item.id || item.ib_id || item.title || 'unknown';
    /* 1. The citizen's override ALWAYS wins. */
    var ov = readOverrides()[id];
    if (ov) {
      var placed = findSub(ov.subcategory);
      if (placed) {
        /* Override = the citizen said so: full certainty, not "none". */
        return finish(item, placed.major, placed.sub, 10, 'override',
          ['you placed this under ' + placed.sub.label], ctx);
      }
    }
    var hay = haystackFor(item);
    /* 2. An explicit major in the item's topics narrows the shelf first. */
    var narrowed = null;
    if (Array.isArray(item.topics)) {
      item.topics.forEach(function (tp) {
        var low = String(tp).toLowerCase();
        TAXONOMY.forEach(function (m) {
          if (low === m.label.toLowerCase() || low === m.id) narrowed = m;
        });
      });
    }
    var scored = scoreAll(item, hay, ctx);
    if (narrowed) scored = scored.filter(function (s) { return s.major.id === narrowed.id; });
    var best = null;
    scored.forEach(function (s) { if (!best || s.score > best.score) best = s; });
    /* EVIDENCE THRESHOLD (measured, proof run 2, 2026-11-26 21:53 MST):
       a single generic word is NOT evidence — hand-checking 27 score-1
       placements on real notes found 26 wrong (metaphor or passing
       mention: "reading" the response, "story" as metaphor, "travel" in
       passing). A placement needs REAL evidence: total score >= 3, or
       one real phrase hit (weight >= 2). Otherwise the item goes home
       with the best subcategory recorded as a SUGGESTION the citizen can
       confirm or move — the system suggests, it does not fake. */
    var hasPhrase = false;
    if (best) {
      best.hits.forEach(function (h) {
        var k = h.replace(/^(topic|pick|learned):/, '');
        if (keyWeight(k) >= 2) hasPhrase = true;
      });
    }
    if (!best || (best.score < 3 && !hasPhrase)) {
      return homePlacement(item, narrowed, ctx, best);
    }
    return finish(item, best.major, best.sub, best.score, best.hits.some(function (h) { return h.indexOf('topic:') === 0; }) ? 'explicit' : (best.hits.some(function (h) { return h.indexOf('learned:') === 0; }) ? 'learned' : 'keywords'),
      best.hits.slice(0, 4), ctx);
  }

  /* Home placement: an explicitly named major is home; else the citizen's
     first pick's major; else General. The best-scoring subcategory (if
     any) is recorded as a SUGGESTION — the system suggests, the citizen
     confirms or moves. Nothing is faked into a subcategory without
     evidence. */
  function homePlacement(item, narrowed, ctx, best) {
    var id = item.id || item.ib_id || item.title || 'unknown';
    var homeMajor = narrowed || null;
    var picks = (ctx && ctx.picks) || [];
    if (!homeMajor && picks.length) {
      var first = findSub(picks[0]) || null;
      if (first) homeMajor = first.major;
      else TAXONOMY.forEach(function (m) { if (!homeMajor && (m.label === picks[0] || m.id === picks[0])) homeMajor = m; });
    }
    var suggestion = null;
    if (best && best.score > 0) {
      suggestion = { category: best.major.label, categoryId: best.major.id,
        subcategory: best.sub.label, subcategoryId: best.sub.id,
        score: best.score, reasons: best.hits.slice(0, 4) };
    }
    return {
      itemId: id, type: item.type || 'note',
      category: homeMajor ? homeMajor.label : 'General',
      categoryId: homeMajor ? homeMajor.id : 'general',
      subcategory: null, subcategoryId: null,
      topic: null, topicReady: true,
      score: 0, confidence: 'none', source: 'home',
      reasons: [best && best.score > 0
        ? 'too little evidence to file — best guess was ' + best.sub.label + ' (' + best.score + '), confirm it or move it'
        : 'no keyword hit — placed at home, move it if you like'],
      suggestion: suggestion,
      matchInput: null
    };
  }

  function finish(item, major, sub, score, source, reasons, ctx) {
    var id = item.id || item.ib_id || item.title || 'unknown';
    var p = {
      itemId: id, type: item.type || 'note',
      category: major.label, categoryId: major.id,
      subcategory: sub.label, subcategoryId: sub.id,
      topic: null, topicReady: true,
      score: score, confidence: confidenceFor(score), source: source,
      reasons: reasons,
      matchInput: null
    };
    p.matchInput = matchInput(p, item, ctx);
    return p;
  }

  /* --- the handoff to Smart Match: the placed item + its reasons.
     The Organizer does NOT compute match percentages — Match owns that,
     through the privacy gate, with reasons attached. This object is the
     exact input Match receives. --- */
  function matchInput(placement, item, ctx) {
    if (!placement || !placement.subcategoryId) return null;
    var keywords = (placement.reasons || []).filter(function (r) {
      return r.indexOf('topic:') !== 0 && r.indexOf('pick:') !== 0 && r.indexOf('you placed') !== 0;
    }).map(function (r) { return r.replace(/^learned:/, ''); });
    if (!keywords.length) {
      /* Override placement: the reasons are the citizen's words, not
         keywords — fall back to the item's own top scored keywords so
         Match still receives what the item is about. */
      var hay = haystackFor(item);
      var scored = scoreAll(item, hay, ctx || {});
      var top = null;
      scored.forEach(function (s) { if (s.subcategoryId === undefined && s.sub && s.sub.id === placement.subcategoryId) top = s; });
      scored.forEach(function (s) { if (!top || s.score > top.score) top = s; });
      if (top) {
        keywords = top.hits.filter(function (h) { return h.indexOf(':') === -1; }).slice(0, 4);
      }
    }
    return {
      itemId: placement.itemId,
      type: placement.type,
      category: placement.category,
      categoryId: placement.categoryId,
      subcategory: placement.subcategory,
      subcategoryId: placement.subcategoryId,
      keywords: keywords,
      owner: (ctx && ctx.owner) || item.owner || item.author || null,
      reasons: placement.reasons.slice()
    };
  }

  /* --- the citizen's move: override always wins, and teaches ---
     moveItem places the item under the chosen subcategory, records the
     override, and learns: the item's top 2 matched keywords (by weight)
     gain +2 toward the new subcategory for future items. A later move of
     the same item retracts its old rule. Rules cap at 50, oldest first. */
  function moveItem(item, categoryId, subcategoryId) {
    var found = findSub(subcategoryId);
    if (!found || found.major.id !== categoryId) return null;
    var id = item.id || item.ib_id || item.title || 'unknown';
    var hay = haystackFor(item);
    var scored = scoreAll(item, hay, {});
    var top = null;
    scored.forEach(function (s) { if (!top || s.score > top.score) top = s; });
    var teachKeys = [];
    if (top && top.hits.length) {
      teachKeys = top.hits
        .filter(function (h) { return h.indexOf(':') === -1; })
        .sort(function (a, b) { return keyWeight(b) - keyWeight(a); })
        .slice(0, 2);
    }
    var ovs = readOverrides();
    ovs[id] = { category: categoryId, subcategory: subcategoryId, at: new Date().toISOString() };
    overrideStore.write(ovs);
    var rules = readRules().filter(function (r) { return r.taughtBy !== id; });
    if (teachKeys.length) {
      rules.push({ subcategory: subcategoryId, keywords: teachKeys, taughtBy: id, at: new Date().toISOString() });
      while (rules.length > MAX_RULES) rules.shift();
    }
    ruleStore.write(rules);
    return organize(item, {});
  }

  function clearOverride(itemId) {
    var ovs = readOverrides();
    delete ovs[itemId];
    overrideStore.write(ovs);
    var rules = readRules().filter(function (r) { return r.taughtBy !== itemId; });
    ruleStore.write(rules);
  }

  /* --- topics level: ready, empty until he gives the list --- */
  function setTopics(list) {
    if (!Array.isArray(list)) return { ok: false, error: 'topics must be an array' };
    for (var i = 0; i < list.length; i++) {
      var t = list[i];
      if (!t || !t.id || !t.label || !t.subcategory || !findSub(t.subcategory)) {
        return { ok: false, error: 'topic ' + (t && t.id) + ' does not name a real subcategory' };
      }
    }
    TOPICS = list.slice();
    TOPIC_BY_ID = {};
    TOPICS.forEach(function (t) { TOPIC_BY_ID[t.id] = t; });
    return { ok: true, count: TOPICS.length };
  }

  function organizeAll(items, ctx) {
    var out = (items || []).map(function (it) { return organize(it, ctx); });
    var dist = {};
    out.forEach(function (p) {
      var k = p.subcategoryId || 'general';
      dist[k] = (dist[k] || 0) + 1;
    });
    return { placements: out, distribution: dist, total: out.length };
  }

  return {
    TAXONOMY: TAXONOMY,
    organize: organize,
    organizeAll: organizeAll,
    moveItem: moveItem,
    clearOverride: clearOverride,
    matchInput: matchInput,
    setTopics: setTopics,
    topics: function () { return TOPICS.slice(); },
    learnedRules: readRules,
    overrides: readOverrides,
    haystackFor: haystackFor,
    VERSION: '1.0.0-20261126'
  };
});
