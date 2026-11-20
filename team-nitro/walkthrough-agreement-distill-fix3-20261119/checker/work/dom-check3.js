// CHECKER COPY of the fix-1 dom-harness.js — identical except the selector engine
// gains *= ^= $= ~= attribute operators (see patch note in dom-harness2.js).
// dom-harness.js — DOM harness proof for the agreement-distill fix round.
// Hand-rolled minimal DOM (no jsdom in this VM; npm install EPERM-blocked).
// Parses the page's REAL html, runs its REAL <script> blocks in a vm context,
// then drives the REAL handlers tap by tap and asserts the observable state:
// exactly one board visible, the progress pill/jewel tracking the board on
// screen, buttons, stage routing, and the hold. No render is claimed: this
// proves the state machine over the real code paths, not pixels.
// Usage: node dom-harness.js  (exit 0 = all assertions pass)
var vm = require('vm');
var cp = require('child_process');
var path = require('path');

var T = path.join(__dirname, 'transform-fix.js');
function fixed() {
  var r = cp.spawnSync(process.execPath, [T], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) throw new Error('transform-fix failed: ' + r.stderr);
  var d = JSON.parse(r.stdout);
  return {
    unfold: Buffer.from(d.unfold_b64, 'base64').toString('utf8'),
    welcome: Buffer.from(d.welcome_b64, 'base64').toString('utf8')
  };
}

// ---------- entities ----------
var ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: '\u00a0', mdash: '\u2014', ndash: '\u2013', ldquo: '\u201c', rdquo: '\u201d', lsquo: '\u2018', rsquo: '\u2019', hellip: '\u2026', middot: '\u00b7', bull: '\u2022', copy: '\u00a9', reg: '\u00ae', trade: '\u2122', laquo: '\u00ab', raquo: '\u00bb', times: '\u00d7', divide: '\u00f7', plusmn: '\u00b1', deg: '\u00b0', prime: '\u2032', Prime: '\u2033', dagger: '\u2020', Dagger: '\u2021', permil: '\u2030', euro: '\u20ac', pound: '\u00a3', yen: '\u00a5', cent: '\u00a2', curren: '\u00a4', sect: '\u00a7', para: '\u00b6', micro: '\u00b5', shy: '\u00ad' };
function decodeEnt(s) {
  return s.replace(/&(#x[0-9a-fA-F]+|#\d+|[a-zA-Z]+);/g, function (m, e) {
    if (e[0] === '#') {
      var n = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return isNaN(n) ? m : String.fromCodePoint(n);
    }
    return ENT[e] !== undefined ? ENT[e] : m;
  });
}

var VOID = { area: 1, base: 1, br: 1, col: 1, embed: 1, hr: 1, img: 1, input: 1, link: 1, meta: 1, source: 1, track: 1, wbr: 1, param: 1 };

// ---------- Element ----------
var observers = []; // MutationObserver registry: {cb}
function notifyObservers() {
  var list = observers.slice();
  for (var i = 0; i < list.length; i++) {
    try { list[i]([{ type: 'attributes', attributeName: 'class' }]); } catch (e) {}
  }
}
function ClassList(el) { this.el = el; }
ClassList.prototype = {
  _set: function () { return this.el._cls; },
  add: function () { var c = arguments, ch = false; for (var i = 0; i < c.length; i++) if (!this.el._cls.has(c[i])) { this.el._cls.add(c[i]); ch = true; } if (ch) { this.el._syncClass(); notifyObservers(); } },
  remove: function () { var c = arguments, ch = false; for (var i = 0; i < c.length; i++) if (this.el._cls.has(c[i])) { this.el._cls.delete(c[i]); ch = true; } if (ch) { this.el._syncClass(); notifyObservers(); } },
  toggle: function (name, force) {
    var has = this.el._cls.has(name);
    var want = force === undefined ? !has : !!force;
    if (want) this.el._cls.add(name); else this.el._cls.delete(name);
    if (want !== has) { this.el._syncClass(); notifyObservers(); }
    return want;
  },
  contains: function (name) { return this.el._cls.has(name); }
};
function Style(el) { this.el = el; this._props = {}; }
Style.prototype = {
  setProperty: function (k, v) { this._props[k] = String(v); },
  getPropertyValue: function (k) { return this._props[k] || ''; },
  removeProperty: function (k) { delete this._props[k]; }
};
var styleProxyHandler = {
  get: function (t, p) {
    if (p === 'setProperty' || p === 'getPropertyValue' || p === 'removeProperty' || p === 'el' || p === '_props') return t[p];
    return t._props[p] || '';
  },
  set: function (t, p, v) { t._props[p] = String(v); return true; }
};
function El(tag, attrs) {
  this.nodeType = 1;
  this.tagName = tag.toUpperCase();
  this.attributes = attrs || {};
  this.children = [];
  this.parentNode = null;
  this._cls = new Set(((this.attributes['class'] || '').split(/\s+/).filter(Boolean)));
  this.classList = new ClassList(this);
  this.style = new Proxy(new Style(this), styleProxyHandler);
  this._listeners = {};
  this._text = null; // for text nodes use a plain object instead
  this._hidden = this.attributes.hasOwnProperty('hidden');
}
El.prototype = {
  get id() { return this.attributes.id || ''; },
  set id(v) { this.attributes.id = v; },
  get className() { return this.attributes['class'] || ''; },
  set className(v) { this.attributes['class'] = v; this._cls = new Set(v.split(/\s+/).filter(Boolean)); },
  _syncClass: function () { this.attributes['class'] = Array.from(this._cls).join(' '); },
  get hidden() { return this._hidden; },
  set hidden(v) { this._hidden = !!v; if (this._hidden) this.attributes.hidden = ''; else delete this.attributes.hidden; },
  getAttribute: function (k) { var v = this.attributes[k]; return v === undefined ? null : v; },
  setAttribute: function (k, v) { this.attributes[k] = String(v); if (k === 'class') this._cls = new Set(String(v).split(/\s+/).filter(Boolean)); if (k === 'hidden') this._hidden = true; },
  removeAttribute: function (k) { delete this.attributes[k]; if (k === 'hidden') this._hidden = false; if (k === 'class') this._cls = new Set(); },
  hasAttribute: function (k) { return this.attributes.hasOwnProperty(k); },
  appendChild: function (c) { if (c.parentNode) c.parentNode.removeChild(c); c.parentNode = this; this.children.push(c); return c; },
  insertBefore: function (c, ref) { if (c.parentNode) c.parentNode.removeChild(c); c.parentNode = this; var i = ref ? this.children.indexOf(ref) : -1; if (i === -1) this.children.push(c); else this.children.splice(i, 0, c); return c; },
  removeChild: function (c) { var i = this.children.indexOf(c); if (i !== -1) this.children.splice(i, 1); c.parentNode = null; return c; },
  replaceChild: function (nc, oc) { var i = this.children.indexOf(oc); if (i === -1) throw new Error('replaceChild: not a child'); if (nc.parentNode) nc.parentNode.removeChild(nc); nc.parentNode = this; this.children[i] = nc; oc.parentNode = null; return oc; },
  remove: function () { if (this.parentNode) this.parentNode.removeChild(this); },
  get firstChild() { return this.children[0] || null; },
  get lastChild() { return this.children[this.children.length - 1] || null; },
  get childNodes() { return this.children; },
  cloneNode: function (deep) {
    var c = new El(this.tagName.toLowerCase(), Object.assign({}, this.attributes));
    c._cls = new Set(this._cls);
    c.classList = new ClassList(c);
    c.style = new Proxy(new Style(c), styleProxyHandler);
    Object.keys(this.style._props).forEach(function (k) { c.style._props[k] = this.style._props[k]; }, this);
    c._hidden = this._hidden;
    if (deep) {
      this.children.forEach(function (ch) {
        if (ch.nodeType === 3) c.children.push({ nodeType: 3, data: ch.data, parentNode: c });
        else c.appendChild(ch.cloneNode(true));
      });
    }
    return c;
  },
  get nextSibling() { if (!this.parentNode) return null; var i = this.parentNode.children.indexOf(this); return this.parentNode.children[i + 1] || null; },
  get previousSibling() { if (!this.parentNode) return null; var i = this.parentNode.children.indexOf(this); return this.parentNode.children[i - 1] || null; },
  get textContent() {
    var s = '';
    for (var i = 0; i < this.children.length; i++) {
      var c = this.children[i];
      s += c.nodeType === 3 ? c.data : c.textContent;
    }
    return s;
  },
  set textContent(v) { this.children = [{ nodeType: 3, data: String(v), parentNode: this }]; },
  get innerHTML() { return this.children.map(serialize).join(''); },
  set innerHTML(v) { this.children = parseFragment(v, this); },
  addEventListener: function (type, fn) { (this._listeners[type] = this._listeners[type] || []).push(fn); },
  removeEventListener: function (type, fn) { var l = this._listeners[type]; if (!l) return; var i = l.indexOf(fn); if (i !== -1) l.splice(i, 1); },
  dispatchEvent: function (ev) {
    ev.target = this;
    var path = [], n = this;
    while (n) { path.push(n); n = n.parentNode; }
    if (ev.bubbles !== false) {
      for (var i = 0; i < path.length; i++) {
        ev.currentTarget = path[i];
        var l = path[i]._listeners && path[i]._listeners[ev.type];
        if (l) for (var j = 0; j < l.slice().length; j++) { try { l[j].call(path[i], ev); } catch (e) { if (global.__harnessOnError) global.__harnessOnError(e); } if (ev._stopped) return !ev.defaultPrevented; }
        if (ev._stopped) return !ev.defaultPrevented;
      }
    } else {
      ev.currentTarget = this;
      var l2 = this._listeners[ev.type];
      if (l2) for (var k = 0; k < l2.slice().length; k++) l2[k].call(this, ev);
    }
    return !ev.defaultPrevented;
  },
  click: function () {
    var ev = { type: 'click', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    this.dispatchEvent(ev);
  },
  focus: function () { if (global.__doc) global.__doc.activeElement = this; },
  scrollIntoView: function () {},
  closest: function (sel) { var n = this; while (n) { if (n.nodeType === 1 && matchesSel(n, sel)) return n; n = n.parentNode; } return null; },
  matches: function (sel) { return matchesSel(this, sel); },
  querySelector: function (sel) { var r = this.querySelectorAll(sel); return r.length ? r[0] : null; },
  querySelectorAll: function (sel) { return selectAll(this, sel); },
  getBoundingClientRect: function () {
    var vis = isVisible(this);
    if (!vis) return { top: 0, left: 0, bottom: 0, right: 0, width: 0, height: 0, x: 0, y: 0 };
    return { top: 0, left: 0, bottom: 600, right: 800, width: 800, height: 600, x: 0, y: 0 };
  },
  get offsetHeight() { return isVisible(this) ? 600 : 0; },
  get offsetWidth() { return isVisible(this) ? 800 : 0; },
  get scrollHeight() { return 600; },
  get clientHeight() { return 600; },
  get clientWidth() { return 800; },
  get scrollTop() { return this._scrollTop || 0; },
  set scrollTop(v) { this._scrollTop = v; },
  get value() { return this.attributes.value || ''; },
  set value(v) { this.attributes.value = String(v); },
  get src() { return this.attributes.src || ''; },
  set src(v) { this.attributes.src = String(v); },
  get href() { return this.attributes.href || ''; },
  set href(v) { this.attributes.href = String(v); }
};
function isVisible(el) {
  var n = el;
  while (n) {
    if (n.nodeType === 1 && (n.hidden || (n.style && n.style.display === 'none'))) return false;
    n = n.parentNode;
  }
  return true;
}
function serialize(node) {
  if (node.nodeType === 3) return node.data;
  var attrs = Object.keys(node.attributes).map(function (k) { return ' ' + k + '="' + node.attributes[k] + '"'; }).join('');
  if (VOID[node.tagName.toLowerCase()]) return '<' + node.tagName.toLowerCase() + attrs + '>';
  return '<' + node.tagName.toLowerCase() + attrs + '>' + node.children.map(serialize).join('') + '</' + node.tagName.toLowerCase() + '>';
}

// ---------- selector engine (subset: tag, #id, .class, [attr], [attr=val], descendant, >, comma, :not()) ----------
function parseSimple(sel) {
  var out = { tag: null, id: null, classes: [], attrs: [], nots: [], firstChild: false, lastChild: false };
  var s = sel.trim();
  var m;
  while ((m = /^:not\(([^()]*)\)/.exec(s))) { out.nots.push(parseSimple(m[1])); s = s.slice(m[0].length); }
  m = /^([a-zA-Z][a-zA-Z0-9-]*|\*)/.exec(s);
  if (m) { out.tag = m[1].toLowerCase(); s = s.slice(m[0].length); }
  while (s.length) {
    if (s[0] === '#') { m = /^#([A-Za-z0-9\-_]+)/.exec(s); if (!m) break; out.id = m[1]; s = s.slice(m[0].length); }
    else if (s[0] === '.') { m = /^\.([A-Za-z0-9\-_]+)/.exec(s); if (!m) break; out.classes.push(m[1]); s = s.slice(m[0].length); }
    else if (s[0] === '[') {
      m = /^\[([A-Za-z0-9\-_]+)(?:([*^$~]?=)(?:"([^"]*)"|'([^']*)'|([^\]]*)))?\]/.exec(s);
      if (!m) break;
      out.attrs.push({ k: m[1], op: m[2] ? m[2].charAt(0) : "=", v: m[3] !== undefined ? m[3] : (m[4] !== undefined ? m[4] : m[5]) });
      s = s.slice(m[0].length);
    }
    else if ((m = /^:not\(([^()]*)\)/.exec(s))) { out.nots.push(parseSimple(m[1])); s = s.slice(m[0].length); }
    else if (s.indexOf(':first-child') === 0) { out.firstChild = true; s = s.slice(12); }
    else if (s.indexOf(':last-child') === 0) { out.lastChild = true; s = s.slice(11); }
    else if ((m = /^:[A-Za-z\-]+(\([^)]*\))?/.exec(s))) { s = s.slice(m[0].length); /* state pseudo (:hover etc.) — ignored: no hover in the harness */ }
    else break;
  }
  if (s.trim()) throw new Error('unsupported selector part: ' + sel);
  return out;
}
function matchSimple(el, p) {
  if (el.nodeType !== 1) return false;
  if (p.tag && p.tag !== '*' && el.tagName.toLowerCase() !== p.tag) return false;
  if (p.id && el.id !== p.id) return false;
  for (var i = 0; i < p.classes.length; i++) if (!el.classList.contains(p.classes[i])) return false;
  for (var j = 0; j < p.attrs.length; j++) {
    var a = p.attrs[j];
    if (!el.hasAttribute(a.k)) return false;
    if (a.v !== undefined) { var av = el.getAttribute(a.k); if (a.op === "*") { if (av.indexOf(a.v) === -1) return false; } else if (a.op === "^") { if (av.indexOf(a.v) !== 0) return false; } else if (a.op === "$") { if (av.slice(-a.v.length) !== a.v) return false; } else if (a.op === "~") { if (av.split(/\s+/).indexOf(a.v) === -1) return false; } else if (av !== a.v) return false; }
  }
  if (p.firstChild || p.lastChild) {
    var sibs = el.parentNode ? el.parentNode.children.filter(function (c) { return c.nodeType === 1; }) : [el];
    if (p.firstChild && sibs[0] !== el) return false;
    if (p.lastChild && sibs[sibs.length - 1] !== el) return false;
  }
  for (var k = 0; k < p.nots.length; k++) if (matchSimple(el, p.nots[k])) return false;
  return true;
}
function splitSelector(sel) {
  // returns [{comb:' '|'>'|'+'|'~'|null, simple}] left to right
  var parts = [], cur = '', depth = 0, i;
  var br = 0, qq = null;
  for (i = 0; i < sel.length; i++) {
    var ch = sel[i];
    if (qq) { if (ch === qq) qq = null; cur += ch; continue; }
    if (ch === '"' || ch === "'") { qq = ch; cur += ch; continue; }
    if (ch === '(') depth++;
    if (ch === ')') depth--;
    if (ch === '[') br++;
    if (ch === ']') br--;
    if (depth === 0 && br === 0 && (ch === ' ' || ch === '>' || ch === '+' || ch === '~')) {
      if (cur.trim()) parts.push({ comb: null, simple: cur.trim() });
      if (ch !== ' ') parts.push({ comb: ch, simple: '' });
      else if (parts.length && parts[parts.length - 1].comb === null) parts[parts.length - 1].comb = ' ';
      cur = '';
      while (sel[i + 1] === ' ') i++;
    } else cur += ch;
  }
  if (cur.trim()) parts.push({ comb: null, simple: cur.trim() });
  var res = [], pending = null;
  for (var k = 0; k < parts.length; k++) {
    if (parts[k].simple === '') { pending = parts[k].comb; continue; }
    res.push({ comb: pending, simple: parts[k].simple });
    pending = parts[k].comb;
  }
  return res;
}
function matchesSel(el, sel) {
  var groups = sel.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  for (var g = 0; g < groups.length; g++) {
    var chain = splitSelector(groups[g]).map(function (p) { return { comb: p.comb, simple: parseSimple(p.simple) }; });
    if (matchChain(el, chain, chain.length - 1)) return true;
  }
  return false;
}
function matchChain(el, chain, idx) {
  if (!matchSimple(el, chain[idx].simple)) return false;
  if (idx === 0) return true;
  var comb = chain[idx].comb || ' ';
  if (comb === '>') {
    return el.parentNode ? matchChain(el.parentNode, chain, idx - 1) : false;
  }
  if (comb === '+') {
    var prev = el.previousSibling;
    while (prev && prev.nodeType !== 1) prev = prev.previousSibling;
    return prev ? matchChain(prev, chain, idx - 1) : false;
  }
  if (comb === '~') {
    var p = el.previousSibling;
    while (p) {
      if (p.nodeType === 1 && matchChain(p, chain, idx - 1)) return true;
      p = p.previousSibling;
    }
    return false;
  }
  var n = el.parentNode;
  while (n) {
    if (n.nodeType === 1 && matchChain(n, chain, idx - 1)) return true;
    n = n.parentNode;
  }
  return false;
}
function selectAll(root, sel) {
  var out = [];
  (function walk(n) {
    for (var i = 0; i < n.children.length; i++) {
      var c = n.children[i];
      if (c.nodeType === 1) {
        if (matchesSel(c, sel)) out.push(c);
        walk(c);
      }
    }
  })(root);
  return out;
}

// ---------- HTML parser ----------
function parseAttrs(str) {
  var attrs = {}, re = /([A-Za-z0-9\-_:]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g, m;
  while ((m = re.exec(str)) !== null) {
    attrs[m[1]] = m[2] !== undefined ? decodeEnt(m[2]) : (m[3] !== undefined ? decodeEnt(m[3]) : (m[4] !== undefined ? decodeEnt(m[4]) : ''));
  }
  return attrs;
}
function parseHTML(html) {
  var root = new El('html', {});
  var doc = { documentElement: root, body: null, head: null };
  var stack = [root];
  var i = 0, n = html.length;
  function top() { return stack[stack.length - 1]; }
  function addText(t) {
    if (!t) return;
    top().children.push({ nodeType: 3, data: decodeEnt(t), parentNode: top() });
  }
  while (i < n) {
    var lt = html.indexOf('<', i);
    if (lt === -1) { addText(html.slice(i)); break; }
    if (lt > i) addText(html.slice(i, lt));
    if (html.startsWith('<!--', lt)) {
      var end = html.indexOf('-->', lt + 4);
      i = end === -1 ? n : end + 3;
      continue;
    }
    if (html.startsWith('<!', lt) || html.startsWith('<?', lt)) {
      var gt = html.indexOf('>', lt);
      i = gt === -1 ? n : gt + 1;
      continue;
    }
    if (html.startsWith('</', lt)) {
      var m = /^<\/([A-Za-z0-9\-]+)\s*>/.exec(html.slice(lt));
      if (!m) { i = lt + 2; continue; }
      var tag = m[1].toLowerCase();
      for (var s = stack.length - 1; s > 0; s--) {
        if (stack[s].tagName.toLowerCase() === tag) { stack.length = s; break; }
      }
      i = lt + m[0].length;
      continue;
    }
    var om = /^<([A-Za-z0-9\-]+)((?:\s+[^>]*?)?)\s*(\/?)>/.exec(html.slice(lt));
    if (!om) { i = lt + 1; continue; }
    var tname = om[1].toLowerCase();
    var attrs = parseAttrs(om[2] || '');
    var selfClose = !!om[3] || !!VOID[tname];
    var el = new El(tname, attrs);
    top().appendChild(el);
    i = lt + om[0].length;
    if (tname === 'script' || tname === 'style') {
      var close = html.indexOf('</' + tname, i);
      var raw = close === -1 ? html.slice(i) : html.slice(i, close);
      el.children.push({ nodeType: 3, data: raw, parentNode: el });
      if (close === -1) { i = n; break; }
      var cm = /^<\/[A-Za-z0-9\-]+\s*>/.exec(html.slice(close));
      i = close + (cm ? cm[0].length : 0);
      continue;
    }
    if (!selfClose) stack.push(el);
    if (tname === 'body') doc.body = el;
    if (tname === 'head') doc.head = el;
  }
  return { root: root, doc: doc };
}
function parseFragment(html, parent) {
  var frag = parseHTML(html);
  var kids = frag.root.children;
  kids.forEach(function (c) { c.parentNode = parent; });
  return kids;
}

// ---------- document / window ----------
function makeStorage() {
  var m = new Map();
  return {
    getItem: function (k) { return m.has(k) ? m.get(k) : null; },
    setItem: function (k, v) { m.set(String(k), String(v)); },
    removeItem: function (k) { m.delete(k); },
    clear: function () { m.clear(); }
  };
}
function makeEnv(html, search, preset) {
  var parsed = parseHTML(html);
  var root = parsed.root, docObj = parsed.doc;
  var navigations = [];
  var loc = {
    href: 'https://naya-walk-beginning-staging.nayapower.workers.dev/' + (search ? '?' + search.replace(/^\?/, '') : ''),
    search: search || '',
    pathname: '/',
    replace: function (u) { navigations.push({ kind: 'replace', url: u }); loc.href = u; },
    assign: function (u) { navigations.push({ kind: 'assign', url: u }); loc.href = u; },
    reload: function () { navigations.push({ kind: 'reload' }); }
  };
  Object.defineProperty(loc, 'href', {
    get: function () { return this._href; },
    set: function (v) { this._href = v; navigations.push({ kind: 'href', url: v }); },
    configurable: true
  });
  loc._href = 'https://naya-walk-beginning-staging.nayapower.workers.dev/' + (search ? '?' + search.replace(/^\?/, '') : '');
  var storage = makeStorage();
  var sstorage = makeStorage();
  if (preset) {
    if (preset.local) Object.keys(preset.local).forEach(function (k) { storage.setItem(k, preset.local[k]); });
    if (preset.session) Object.keys(preset.session).forEach(function (k) { sstorage.setItem(k, preset.session[k]); });
  }
  var docListeners = {};
  var document = {
    nodeType: 9,
    documentElement: root,
    body: docObj.body,
    head: docObj.head,
    activeElement: null,
    hidden: false,
    readyState: 'complete',
    _listeners: docListeners,
    children: [root],
    parentNode: null,
    getElementById: function (id) {
      var found = null;
      (function walk(n) {
        if (found) return;
        for (var i = 0; i < n.children.length; i++) {
          var c = n.children[i];
          if (c.nodeType === 1) {
            if (c.id === id) { found = c; return; }
            walk(c);
          }
        }
      })(root);
      return found;
    },
    querySelector: function (s) { var r = selectAll(root, s); return r.length ? r[0] : null; },
    querySelectorAll: function (s) { return selectAll(root, s); },
    createElement: function (tag) { return new El(tag, {}); },
    createTextNode: function (t) { return { nodeType: 3, data: String(t), parentNode: null }; },
    addEventListener: function (type, fn) { (docListeners[type] = docListeners[type] || []).push(fn); },
    removeEventListener: function (type, fn) { var l = docListeners[type]; if (!l) return; var i = l.indexOf(fn); if (i !== -1) l.splice(i, 1); },
    dispatchEvent: function (ev) {
      ev.target = document; ev.currentTarget = document;
      var l = docListeners[ev.type] || [];
      for (var i = 0; i < l.slice().length; i++) l[i].call(document, ev);
      return !ev.defaultPrevented;
    },
    title: ''
  };
  root.parentNode = document;
  global.__doc = document;
  var fetchCalls = [];
  function fetchStub() {
    fetchCalls.push(Array.prototype.slice.call(arguments));
    // CHECKER PATCH (only change vs dom-harness3-dom.js): preset.fetch==='pending'
    // returns a never-settling promise, so the checker can prove causally whether
    // the walk's fetch verdict (vs the 4s timer) is what advances the walk.
    if (preset && preset.fetch === 'pending') return new Promise(function () {});
    return Promise.resolve({ ok: false, status: 404, json: function () { return Promise.resolve(null); }, text: function () { return Promise.resolve(''); } });
  }
  function MutationObserver(cb) { this._cb = cb; }
  MutationObserver.prototype.observe = function () { observers.push(this._cb); };
  MutationObserver.prototype.disconnect = function () { var i = observers.indexOf(this._cb); if (i !== -1) observers.splice(i, 1); };
  function NoopObserver() {}
  NoopObserver.prototype.observe = function () {};
  NoopObserver.prototype.unobserve = function () {};
  NoopObserver.prototype.disconnect = function () {};
  var env = {
    console: console,
    setTimeout: setTimeout, clearTimeout: clearTimeout,
    setInterval: setInterval, clearInterval: clearInterval,
    requestAnimationFrame: function (fn) { return setTimeout(fn, 16); },
    cancelAnimationFrame: function (id) { clearTimeout(id); },
    URL: URL, URLSearchParams: URLSearchParams, JSON: JSON, Math: Math, Date: Date,
    Promise: Promise, RegExp: RegExp, Array: Array, Object: Object, String: String,
    Number: Number, Boolean: Boolean, Error: Error, Map: Map, Set: Set, Symbol: Symbol,
    parseInt: parseInt, parseFloat: parseFloat, isNaN: isNaN, isFinite: isFinite,
    document: document,
    location: loc,
    history: { scrollRestoration: 'auto', back: function () {}, pushState: function () {}, replaceState: function () {} },
    localStorage: storage, sessionStorage: sstorage,
    navigator: { userAgent: 'harness', language: 'en-US' },
    screen: { width: 1920, height: 1080 },
    innerWidth: 1920, innerHeight: 1080,
    fetch: fetchStub,
    MutationObserver: MutationObserver,
    IntersectionObserver: NoopObserver,
    ResizeObserver: NoopObserver,
    getComputedStyle: function (el) {
      return {
        position: (el.style && el.style.position) || 'static',
        display: (el.style && el.style.display) || '',
        getPropertyValue: function (p) { return (el.style && el.style.getPropertyValue) ? el.style.getPropertyValue(p) : ''; }
      };
    },
    matchMedia: function () { return { matches: false, addListener: function () {}, removeListener: function () {}, addEventListener: function () {}, removeEventListener: function () {} }; },
    scrollTo: function () {},
    addEventListener: function (t, f) { (env._wl = env._wl || {})[t] = ((env._wl || {})[t] || []).concat([f]); },
    removeEventListener: function () {},
    alert: function () {},
    __navigations: navigations,
    __fetchCalls: fetchCalls,
    __env: null
  };
  env.window = env;
  env.globalThis = env;
  env.self = env;
  env.__env = env;
  var ctx = vm.createContext(env);
  var errors = [];
  global.__harnessOnError = function (e) { errors.push(e); };
  // run every inline script in document order
  var scripts = selectAll(root, 'script').filter(function (s) { return !s.getAttribute('src'); });
  var ran = 0;
  scripts.forEach(function (s, idx) {
    var code = s.children.map(function (c) { return c.nodeType === 3 ? c.data : ''; }).join('');
    if (!code.trim()) return;
    try {
      vm.runInContext(code, ctx, { filename: 'script-' + idx + '.js' });
      ran++;
    } catch (e) {
      errors.push({ script: idx, error: String(e && e.stack || e), head: code.slice(0, 120) });
    }
  });
  // fire DOMContentLoaded + load
  try {
    var ev = { type: 'DOMContentLoaded', bubbles: false, target: document, currentTarget: document, defaultPrevented: false, preventDefault: function () { this.defaultPrevented = true; } };
    document.dispatchEvent(ev);
  } catch (e) { errors.push(e); }
  return { env: env, document: document, root: root, navigations: navigations, errors: errors, scriptsRun: ran, storage: storage, sstorage: sstorage, ctx: ctx };
}

// ---------- CSS cascade (display only, for the unfold proof) ----------
function parseCSS(css) {
  var rules = [];
  css = css.replace(/\/\*[\s\S]*?\*\//g, '');
  function parseBlock(text, media) {
    var i = 0;
    while (i < text.length) {
      var ob = text.indexOf('{', i);
      if (ob === -1) break;
      var sel = text.slice(i, ob).trim();
      var depth = 1, j = ob + 1;
      while (j < text.length && depth > 0) { if (text[j] === '{') depth++; if (text[j] === '}') depth--; j++; }
      var body = text.slice(ob + 1, j - 1);
      if (sel.indexOf('@media') === 0) {
        parseBlock(body, sel);
      } else if (sel && sel.indexOf('@') !== 0) {
        rules.push({ sel: sel, body: body, media: media || null, order: rules.length });
      }
      i = j;
    }
  }
  parseBlock(css, null);
  return rules;
}
function specificity(sel) {
  var a = (sel.match(/#[A-Za-z0-9\-_]+/g) || []).length;
  var b = (sel.match(/\.[A-Za-z0-9\-_]+/g) || []).length + (sel.match(/\[[^\]]+\]/g) || []).length + (sel.match(/:[A-Za-z\-]+(\([^)]*\))?/g) || []).length;
  var c = (sel.replace(/[#\.:\[][^\s]*/g, '').match(/[A-Za-z][A-Za-z0-9\-]*/g) || []).length;
  return [a, b, c];
}
function cmpSpec(x, y) {
  for (var i = 0; i < 3; i++) { if (x[i] !== y[i]) return x[i] - y[i]; }
  return 0;
}
function mediaApplies(media, width) {
  if (!media) return true;
  var m;
  if ((m = /max-width\s*:\s*(\d+)px/.exec(media))) return width <= parseInt(m[1], 10);
  if ((m = /min-width\s*:\s*(\d+)px/.exec(media))) return width >= parseInt(m[1], 10);
  if (/prefers-reduced-motion/.test(media)) return false;
  return true;
}
function cascadeDisplay(el, rules, width) {
  var best = null; // {spec, order, important, value}
  rules.forEach(function (r) {
    if (!mediaApplies(r.media, width)) return;
    var dm = /display\s*:\s*([^;!]+)(\s*!important)?/.exec(r.body);
    if (!dm) return;
    var groups = r.sel.split(',').map(function (s) { return s.trim(); });
    for (var g = 0; g < groups.length; g++) {
      var ok = false;
      try { ok = matchesSel(el, groups[g]); } catch (e) { ok = false; }
      if (!ok) continue;
      var spec = specificity(groups[g]);
      var imp = !!dm[2];
      var cand = { spec: spec, order: r.order, important: imp, value: dm[1].trim() };
      if (!best) { best = cand; continue; }
      if (cand.important !== best.important) { if (cand.important) best = cand; continue; }
      var c = cmpSpec(cand.spec, best.spec);
      if (c > 0 || (c === 0 && cand.order > best.order)) best = cand;
    }
  });
  return best ? best.value : null;
}

// ---------- assertions ----------
var PASS = 0, FAIL = 0, FAILURES = [];
function check(name, cond, detail) {
  if (cond) { PASS++; console.log('  PASS ' + name + (detail ? ' — ' + detail : '')); }
  else { FAIL++; FAILURES.push(name); console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); }
}
function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
function q(doc, sel) { return doc.querySelector(sel); }
function qa(doc, sel) { return doc.querySelectorAll(sel); }

// ---------- scenarios ----------
async function scenarioUnfold(F) {
  console.log('\n== SCENARIO 1: /agreement (unfold, plain) ==');
  var e = makeEnv(F.unfold, '');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 3).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var beats = qa(doc, '#deckBody .letter-beat');
  check('unfold: 37 boards', beats.length === 37, 'found ' + beats.length);
  var now = beats.filter(function (b) { return b.classList.contains('frame-now'); });
  check('unfold: exactly one frame-now at load', now.length === 1, 'found ' + now.length);
  check('unfold: first board is current', now.length === 1 && now[0].getAttribute('data-beat') === '1');
  var pill = q(doc, '.af-prog-num');
  check('unfold: pill reads 1 / 37', pill && pill.textContent.trim() === '1 / 37', pill ? JSON.stringify(pill.textContent) : 'no pill');
  // CSS cascade: exactly one board displays, the rest none.
  var cssText = qa(doc, 'style').map(function (s) { return s.textContent; }).join('\n');
  var rules = parseCSS(cssText);
  function visibleBeats() {
    return beats.filter(function (b) { return cascadeDisplay(b, rules, 1920) !== 'none'; });
  }
  var vis = visibleBeats();
  check('unfold: cascade shows exactly one board', vis.length === 1, 'visible=' + vis.length);
  check('unfold: cascade shows board 1', vis.length === 1 && vis[0].getAttribute('data-beat') === '1');
  check('unfold: cascade hides board 2', cascadeDisplay(beats[1], rules, 1920) === 'none', 'board2=' + cascadeDisplay(beats[1], rules, 1920));
  // Tap Keep reading through all 37.
  var ok = true;
  for (var step = 2; step <= 37; step++) {
    var cur = qa(doc, '#deckBody .letter-beat.frame-now')[0];
    if (!cur) { ok = false; check('unfold: frame-now present at step ' + step, false); break; }
    var btn = cur.querySelector('.deck-next[data-beat]');
    if (!btn) { ok = false; check('unfold: Keep reading present on board ' + (step - 1), false, 'no .deck-next'); break; }
    btn.click();
    await sleep(10);
    var now2 = qa(doc, '#deckBody .letter-beat.frame-now');
    var pill2 = q(doc, '.af-prog-num');
    if (now2.length !== 1 || now2[0].getAttribute('data-beat') !== String(step) || !pill2 || pill2.textContent.trim() !== step + ' / 37') {
      ok = false;
      check('unfold: step ' + step, false, 'frame-now=' + now2.length + ' beat=' + (now2[0] ? now2[0].getAttribute('data-beat') : '?') + ' pill=' + (pill2 ? pill2.textContent : '?'));
      break;
    }
    var v = visibleBeats();
    if (v.length !== 1 || v[0].getAttribute('data-beat') !== String(step)) {
      ok = false;
      check('unfold: cascade at step ' + step, false, 'visible=' + v.length);
      break;
    }
  }
  if (ok) check('unfold: Next walks 1..37, one board at a time, pill in sync', true, '36 taps');
  // Back from 37 to 36.
  var b37 = qa(doc, '#deckBody .letter-beat.frame-now')[0];
  var back = b37 ? b37.querySelector('.deck-back') : null;
  if (back) {
    back.click();
    await sleep(10);
    var now3 = qa(doc, '#deckBody .letter-beat.frame-now');
    check('unfold: Back 37 -> 36', now3.length === 1 && now3[0].getAttribute('data-beat') === '36', now3.length ? now3[0].getAttribute('data-beat') : '?');
  } else check('unfold: Back button present on board 37', false);
  // Board text checks (one story).
  var b1 = beats[0], b11 = beats[10], b34 = beats[33], b37 = beats[36];
  check('unfold: board 1 drops the 99/100 claim', b1.textContent.indexOf('99 out of 100') === -1);
  check('unfold: board 11 says superhighway', b11.textContent.indexOf('superhighway') !== -1 && b11.textContent.indexOf('supercomputer') === -1);
  check('unfold: board 34 title is Your card', (b34.querySelector('.ib-title') || {}).textContent === 'Your card');
  check('unfold: board 37 keeps Congratulations — you\u2019re hired', b37.textContent.indexOf('Congratulations') !== -1 && b37.textContent.indexOf('you\u2019re hired') !== -1);
  check('unfold: internal audio note is gone', F.unfold.indexOf('Waiting on the captioned video') === -1 && F.unfold.indexOf('Nothing is wired here yet') === -1);
  check('unfold: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioUnfoldStage(F) {
  console.log('\n== SCENARIO 2: /agreement?stage=deck|letter|bridge ==');
  ['deck', 'letter', 'bridge'].forEach(function (st) {
    var e = makeEnv(F.unfold, '?stage=' + st);
    var rep = e.navigations.filter(function (n) { return n.kind === 'replace'; });
    check('unfold: ?stage=' + st + ' redirects to /?stage=' + st, rep.length === 1 && rep[0].url === '/?stage=' + st, JSON.stringify(rep));
  });
}

async function scenarioDeck(F) {
  console.log('\n== SCENARIO 3: /?stage=deck ==');
  var e = makeEnv(F.welcome, '?stage=deck');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var body = doc.body;
  check('deck: stage is on', body.classList.contains('fp-stage-on'));
  var agreeSec = q(doc, '#fpAgreement');
  check('deck: view is deck', agreeSec.classList.contains('fp-view-deck'));
  var jewel = q(doc, '#fpStageJewelNum');
  var jewelText = function () {
    var j = q(doc, '#fpStageJewelNum');
    return j ? j.textContent.trim() : '?';
  };
  var deckBeats = qa(doc, '#deckBody .letter-beat');
  check('deck: 37 deck boards', deckBeats.length === 37, 'found ' + deckBeats.length);
  function shownDeck() { return deckBeats.filter(function (b) { return !b.hidden; }); }
  var s0 = shownDeck();
  check('deck: exactly one board shown at 1/37', s0.length === 1, 'shown=' + s0.length);
  check('deck: board 1 shown', s0.length === 1 && s0[0].getAttribute('data-beat') === '1');
  check('deck: jewel reads 1 / 37', jewelText() === '1 / 37', jewelText());
  check('deck: board 1 is talk, never visual', s0.length === 1 && s0[0].classList.contains('fp-smart-talk') && !s0[0].classList.contains('fp-smart-visual'));
  check('deck: no subtitles (one story)', qa(doc, '#deckBody .ib-subtitle').length === 0, qa(doc, '#deckBody .ib-subtitle').length + ' found');
  var nextBtn = q(doc, '#fpNextBtn');
  check('deck: mirror button present', !!nextBtn);
  // Walk 1..37 with the mirror button; Back at step 5.
  var ok = true;
  for (var step = 2; step <= 37; step++) {
    if (step === 5) {
      var cur5 = shownDeck()[0];
      var back5 = cur5 ? cur5.querySelector('.deck-back') : null;
      if (!back5) { ok = false; check('deck: Back present at step 5', false); break; }
      back5.click();
      await sleep(10);
      var sBack = shownDeck();
      if (sBack.length !== 1 || sBack[0].getAttribute('data-beat') !== '3' || jewelText() !== '3 / 37') {
        // Back from board 4 goes to board 3; jewel 3/37.
        ok = false; check('deck: Back decrements', false, 'shown=' + (sBack[0] ? sBack[0].getAttribute('data-beat') : '?') + ' jewel=' + jewelText()); break;
      }
      // re-walk 4 -> 5
      nextBtn.click(); await sleep(10);
      var s5 = shownDeck();
      if (s5.length !== 1 || s5[0].getAttribute('data-beat') !== '4') { ok = false; check('deck: re-walk after Back', false); break; }
      // note: the loop's step counter is now off by one tap; continue from 5
      step = 5;
    }
    nextBtn.click();
    await sleep(10);
    var s = shownDeck();
    if (s.length !== 1 || s[0].getAttribute('data-beat') !== String(step) || jewelText() !== step + ' / 37') {
      ok = false;
      check('deck: step ' + step, false, 'shown=' + s.length + ' beat=' + (s[0] ? s[0].getAttribute('data-beat') : '?') + ' jewel=' + jewelText());
      break;
    }
    if (s[0].classList.contains('fp-smart-visual')) { ok = false; check('deck: step ' + step + ' never visual', false); break; }
  }
  if (ok) check('deck: mirror Next walks 1..37 one tap per board, jewel in sync', true, '36 taps + 1 Back');
  check('deck: board 37 mirror reads Enter NayaNET', nextBtn.textContent.indexOf('Enter NayaNET') !== -1, JSON.stringify(nextBtn.textContent));
  nextBtn.click();
  await sleep(50);
  var hold = q(doc, '#fpNHold');
  check('deck: Enter NayaNET shows the N hold', hold && hold.hidden === false);
  await sleep(3300);
  check('deck: hold releases to the bridge', hold.hidden === true && agreeSec.classList.contains('fp-view-bridge'), 'hold.hidden=' + hold.hidden + ' bridge=' + agreeSec.classList.contains('fp-view-bridge'));
  check('deck: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioLetter(F) {
  console.log('\n== SCENARIO 4: /?stage=letter ==');
  var e = makeEnv(F.welcome, '?stage=letter');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var agreeSec = q(doc, '#fpAgreement');
  check('letter: stage is on', doc.body.classList.contains('fp-stage-on'));
  check('letter: view is letterPage (?stage=letter opens it by design)', agreeSec.classList.contains('fp-view-letterpage'), agreeSec.className);
  var jewelText = function () { var j = q(doc, '#fpStageJewelNum'); return j ? j.textContent.trim() : '?'; };
  var letterBeats = qa(doc, '#letterBody .letter-beat[data-distilled]');
  check('letter: 37 letter boards', letterBeats.length === 37, 'found ' + letterBeats.length);
  function shownLetter() { return letterBeats.filter(function (b) { return !b.hidden; }); }
  var s0 = shownLetter();
  check('letter: exactly one board shown at 1/37', s0.length === 1, 'shown=' + s0.length);
  check('letter: jewel reads 1 / 37', jewelText() === '1 / 37', jewelText());
  // One story: the letter carries the same 37 boards in the same order as
  // the deck (compared by INDEX — the letter's data-beat is 0-based for its
  // dots, the deck's 1-based; the reader-facing order and words match).
  var deckBeats = qa(doc, '#deckBody .letter-beat');
  function nutshell(b) { var n = b ? b.querySelector('.ib-nutshell') : null; return n ? n.textContent.trim() : '?'; }
  check('letter: board 1 words match the deck', nutshell(deckBeats[0]) === nutshell(letterBeats[0]));
  check('letter: board 11 words match the deck', nutshell(deckBeats[10]) === nutshell(letterBeats[10]));
  check('letter: board 37 words match the deck', nutshell(deckBeats[36]) === nutshell(letterBeats[36]));
  var nextBtn = q(doc, '#fpNextBtn');
  var ok = true;
  for (var step = 2; step <= 37; step++) {
    nextBtn.click();
    await sleep(10);
    var s = shownLetter();
    // The letter's data-beat is 0-based (for its dots); compare by INDEX.
    if (s.length !== 1 || s[0] !== letterBeats[step - 1] || jewelText() !== step + ' / 37') {
      ok = false;
      check('letter: step ' + step, false, 'shown=' + s.length + ' idx=' + letterBeats.indexOf(s[0]) + ' jewel=' + jewelText());
      break;
    }
  }
  if (ok) check('letter: mirror Next walks 1..37 one tap per board', true, '36 taps');
  check('letter: board 37 mirror reads I agree', nextBtn.textContent.indexOf('I agree') !== -1, JSON.stringify(nextBtn.textContent));
  nextBtn.click();
  await sleep(50);
  var agreeBox = q(doc, '#dealAgree') || q(doc, '#fpAgreeBox');
  check('letter: I agree opens the agree view', agreeSec.classList.contains('fp-view-agree'), agreeSec.className);
  var agreeBtn = q(doc, '#dealAgreeBtn');
  check('letter: agree button present', !!agreeBtn);
  if (agreeBtn) {
    agreeBtn.click();
    await sleep(50);
    var hold = q(doc, '#fpNHold');
    check('letter: agree shows the N hold', hold && hold.hidden === false);
    await sleep(3300);
    check('letter: hold releases to the bridge', agreeSec.classList.contains('fp-view-bridge'), agreeSec.className);
  }
  check('letter: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioWelcomePlain(F) {
  console.log('\n== SCENARIO 5: / plain — hero button, name form, reload restore ==');
  var e = makeEnv(F.welcome, '');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var enterBtn = q(doc, '#fpEnterDeal');
  check('plain: hero Read button present', !!enterBtn);
  if (enterBtn) {
    enterBtn.click();
    await sleep(10);
    var nav = e.navigations.filter(function (n) { return n.kind === 'href'; });
    check('plain: hero Read goes to /agreement', nav.length >= 1 && nav[nav.length - 1].url === '/agreement', JSON.stringify(nav));
  }
  // Name form with the agreed flag: Enter shows the hold, then identity.
  var e2 = makeEnv(F.welcome, '', { local: { nayanet_fp_agreed: '1' } });
  var doc2 = e2.document;
  var form = q(doc2, '#entryForm');
  var name = q(doc2, '#userName');
  check('plain: name form present', !!form && !!name);
  if (form && name) {
    name.value = 'Test Name';
    var ev = { type: 'submit', bubbles: true, target: form, currentTarget: form, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    form.dispatchEvent(ev);
    await sleep(50);
    var hold2 = q(doc2, '#fpNHold');
    check('plain: agreed submit shows the N hold', hold2 && hold2.hidden === false);
    await sleep(3300);
    var nav2 = e2.navigations.filter(function (n) { return n.kind === 'href'; });
    check('plain: hold releases to identity with the name', nav2.length >= 1 && nav2[nav2.length - 1].url === '/identity.html?name=Test%20Name', JSON.stringify(nav2));
  }
  // Reload restore: the fromBridge flag re-opens the name form.
  var e3 = makeEnv(F.welcome, '', { session: { nayanet_fp_from_bridge: '1' } });
  var doc3 = e3.document;
  var form3 = q(doc3, '#entryForm');
  check('plain: reload with fromBridge re-opens the name form', form3 && form3.hidden === false);
  check('plain: no script errors after driving', e.errors.length === 0 && e2.errors.length === 0 && e3.errors.length === 0,
    'e=' + e.errors.length + ' e2=' + e2.errors.length + ' e3=' + e3.errors.length);
}

async function main() {
  var F = fixed();
  console.log('fixed unfold bytes=' + Buffer.byteLength(F.unfold) + ' welcome bytes=' + Buffer.byteLength(F.welcome));
  await scenarioUnfold(F);
  await scenarioUnfoldStage(F);
  await scenarioDeck(F);
  await scenarioLetter(F);
  await scenarioWelcomePlain(F);
  console.log('\nHARNESS RESULT: ' + PASS + ' pass / ' + FAIL + ' fail');
  if (FAIL) { console.log('failures: ' + FAILURES.join(' | ')); process.exit(1); }
}
if (require.main === module) {
  main().catch(function (e) { console.error('HARNESS CRASH: ' + (e && e.stack || e)); process.exit(2); });
}
module.exports = { fixed: fixed, makeEnv: makeEnv, parseCSS: parseCSS, cascadeDisplay: cascadeDisplay, check: check, sleep: sleep, q: q, qa: qa };
