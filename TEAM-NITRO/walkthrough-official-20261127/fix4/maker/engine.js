  var idx = 0;
  /* FIX4 — ONE PHONE PER SCREEN. No groups, no trio, no grouping header.
     One phone at a time in #bdSingle; the ball advances (tap 1 flashes the
     picture where the step has one, tap 2 moves on; steps with no picture
     advance on the first tap); the foot arrows move back / forward. */
  var singleEl = document.getElementById('bdSingle');
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function fieldLabel(f){ return f.label || f.id; }
  function currentPhone(){ return singleEl ? singleEl.querySelector('.bd-phone') : null; }
  function fieldValue(phone, f){
    if (!f || !phone) return '';
    var fieldsEl = phone.querySelector('.bd-fields');
    if (!fieldsEl) return '';
    if (f.t === 'checks') {
      var vals = [];
      fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[type=checkbox]').forEach(function(b){ if (b.checked) vals.push(b.value); });
      return vals;
    }
    if (f.t === 'subs') {
      var cats = [];
      fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[data-cat]').forEach(function(b){ if (b.checked) cats.push(b.value); });
      var subs = [];
      fieldsEl.querySelectorAll('input[data-sub]').forEach(function(b){ if (b.checked) subs.push(b.getAttribute('data-cat-label') + ': ' + b.value); });
      return {cats: cats, subs: subs};
    }
    /* FIX4 — never save the placeholder text as an answer. An unchosen
       select's first option is 'Choose…' (value ''); returning its TEXT
       saved 'Choose…' as the answer, and the cascade restore then read
       that back as a real choice — province flipped to '__other' with
       'Choose…' in its text box, and the city got pv='Choose…' (no map
       entry) and fell back to a free-text input. An unchosen select is
       an empty answer, full stop. */
    if (f.cascadeFrom) {
      var selC = fieldsEl.querySelector('[data-fid="' + f.id + '"]');
      var otherC = fieldsEl.querySelector('[data-fid="' + f.id + '-other"]');
      var wrapC = selC ? selC.closest('.bd-field') : null;
      var modeC = wrapC ? wrapC.getAttribute('data-cascade-mode') : 'select';
      if (modeC === 'text') return otherC ? (otherC.value || '') : '';
      if (!selC) return '';
      if (!selC.value) return '';
      if (selC.value === '__other') return otherC ? (otherC.value || '') : '';
      var optC = selC.options[selC.selectedIndex];
      return optC ? optC.text : '';
    }
    var el = fieldsEl.querySelector('[data-fid="' + f.id + '"]');
    if (!el) return '';
    if (f.t === 'select') {
      if (!el.value) return '';
      var opt = el.options[el.selectedIndex];
      return opt ? opt.text : '';
    }
    return el.value || '';
  }
  function collectPhone(phone, step){
    if (!phone || !step) return '';
    if (step.video) { S.answers[step.key] = ''; save(); return ''; }
    if (step.fields) {
      var parts = [];
      step.fields.forEach(function(f){
        var v = fieldValue(phone, f);
        if (f.t === 'checks') {
          S.answers[f.id] = v;
          if (v.length) parts.push(fieldLabel(f) + ': ' + v.join(', '));
        } else if (f.t === 'subs') {
          S.answers[f.id] = v.cats;
          S.answers[f.id + '_subs'] = v.subs;
          if (v.cats.length) parts.push(fieldLabel(f) + ': ' + v.cats.join(', '));
          v.subs.forEach(function(s){ parts.push(s); });
        } else {
          S.answers[f.id] = v;
          if (v) parts.push(fieldLabel(f) + ': ' + v);
        }
      });
      var summary = parts.join('\n');
      var collides = step.fields.some(function(f){ return f.id === step.key; });
      if (!collides) S.answers[step.key] = summary;
      save();
      return summary;
    }
    var ta = phone.querySelector('.bd-answer');
    var val = ta ? ta.value : '';
    S.answers[step.key] = val;
    save();
    return val;
  }
  function buildFields(step, phone){
    var fieldsEl = phone.querySelector('.bd-fields');
    var ta = phone.querySelector('.bd-answer');
    if (!fieldsEl || !ta) return;
    if (!step.fields) { fieldsEl.hidden = true; ta.hidden = false; ta.value = S.answers[step.key] || ''; return; }
    ta.hidden = true;
    fieldsEl.hidden = false;
    fieldsEl.innerHTML = '';
    var box = null;
    step.fields.forEach(function(f){
      var wrap = fieldsEl;
      if (f.box) {
        if (!box || box.getAttribute('data-box') !== String(f.box)) {
          box = document.createElement('div');
          box.className = 'bd-field-box';
          box.setAttribute('data-box', String(f.box));
          fieldsEl.appendChild(box);
        }
        wrap = box;
      } else { box = null; }
      var d = document.createElement('div');
      d.className = 'bd-field';
      if (f.t === 'text') {
        d.innerHTML = '<label>' + esc(fieldLabel(f)) + '</label><input type="text" data-fid="' + esc(f.id) + '" placeholder="' + esc(f.ph || '') + '" value="' + esc(S.answers[f.id] || '') + '">';
      } else if (f.t === 'select') {
        /* FIX3 — CASCADE: a cascade field starts as an empty select plus a
           hidden free-text "Other…" input; wireCascade fills it once its
           parent is chosen, and hides the whole field until then. */
        var opts = '';
        if (!f.cascadeFrom) {
          opts = f.options.map(function(o){
            return '<option value="' + esc(o[0]) + '"' + ((S.answers[f.id] || '') === o[1] ? ' selected' : '') + '>' + esc(o[1]) + '</option>';
          }).join('');
        }
        d.innerHTML = '<label>' + esc(fieldLabel(f)) + '</label><select data-fid="' + esc(f.id) + '">' + opts + '</select>' + (f.cascadeFrom ? '<input type="text" data-fid="' + esc(f.id) + '-other" placeholder="' + esc(f.otherText || 'Type it in your own words') + '" hidden>' : '');
        if (f.cascadeFrom) d.classList.add('bd-cascade-hidden');
      } else if (f.t === 'checks') {
        var chips = f.options.map(function(o){
          var on = (S.answers[f.id] || []).indexOf(o[1]) >= 0;
          return '<label class="bd-check"><input type="checkbox" value="' + esc(o[1]) + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + '</span></label>';
        }).join('');
        d.innerHTML = '<label>' + esc(fieldLabel(f)) + '</label><div class="bd-checks" data-fid="' + esc(f.id) + '">' + chips + '</div>';
      } else if (f.t === 'subs') {
        var cats = f.options.map(function(o){
          var on = (S.answers[f.id] || []).indexOf(o[1]) >= 0;
          return '<label class="bd-check"><input type="checkbox" data-cat="' + esc(o[0]) + '" value="' + esc(o[1]) + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + '</span></label>';
        }).join('');
        d.innerHTML = '<label>' + esc(fieldLabel(f)) + '</label><div class="bd-checks" data-fid="' + esc(f.id) + '">' + cats + '</div><div class="bd-subs" data-subs-for="' + esc(f.id) + '"></div>';
      }
      wrap.appendChild(d);
    });
    renderSubs(step, phone);
    wireCascade(step, phone);
    markChosen(phone);
    if (!fieldsEl._bdWired) {
      fieldsEl._bdWired = true;
      /* Collect FIRST, then re-render subs: re-rendering first destroys the
         just-clicked sub checkbox before its state is saved (v2 carry-over). */
      fieldsEl.addEventListener('change', function(ev){
        collectPhone(phone, step);
        /* Only re-render the sub list when a CATEGORY changed: a sub tap
           must not rebuild the list under the finger (it detaches the
           just-tapped checkbox). */
        if (!ev.target || !ev.target.hasAttribute('data-sub')) renderSubs(step, phone);
        markChosen(phone);
      });
      fieldsEl.addEventListener('input', function(){ collectPhone(phone, step); markChosen(phone); });
    }
  }
  /* FIX3 — CASCADING DROPDOWNS (country -> province -> city, where-you-are
     phone) + SELECTION HIGHLIGHT. The next dropdown appears only after the
     previous choice is made; a chosen value highlights and lifts in royal
     purple (.bd-chosen, purple first). A parent with no map for the child
     (e.g. country "Other") turns the child into a free-text input instead
     of a dead dropdown; a child with no map for the typed parent does the
     same. Saved answers restore the whole chain on re-render. */
  function markChosen(phone){
    if (!phone) return;
    phone.querySelectorAll('.bd-field').forEach(function(wrap){
      var chosen = false;
      var sel = wrap.querySelector('select');
      var txt = wrap.querySelector('input[type=text]:not([data-fid$="-other"])');
      var other = wrap.querySelector('input[data-fid$="-other"]');
      if (sel && sel.value && sel.value !== '__other') chosen = true;
      if (other && !other.hidden && other.value.trim()) chosen = true;
      if (txt && txt.value.trim()) chosen = true;
      if (wrap.querySelector('input[type=checkbox]:checked')) chosen = true;
      if (chosen) wrap.classList.add('bd-chosen'); else wrap.classList.remove('bd-chosen');
    });
  }
  function wireCascade(step, phone){
    var fieldsEl = phone.querySelector('.bd-fields');
    if (!fieldsEl || !step.fields) return;
    var byId = {};
    step.fields.forEach(function(f){ byId[f.id] = f; });
    var hasCascade = step.fields.some(function(f){ return !!f.cascadeFrom; });
    if (!hasCascade) return;
    function wrapFor(fid){
      var el = fieldsEl.querySelector('[data-fid="' + fid + '"]');
      return el ? el.closest('.bd-field') : null;
    }
    function parentValue(fid){
      var pf = byId[fid]; if (!pf) return '';
      var sel = fieldsEl.querySelector('[data-fid="' + fid + '"]');
      if (!sel) return '';
      if (pf.cascadeFrom) {
        var wrap = sel.closest('.bd-field');
        var mode = wrap ? wrap.getAttribute('data-cascade-mode') : 'select';
        var o = fieldsEl.querySelector('[data-fid="' + fid + '-other"]');
        if (mode === 'text') return o ? o.value.trim() : '';
        if (sel.value === '__other') return o ? o.value.trim() : '';
        return sel.value || '';
      }
      return sel.value || '';
    }
    function cascadeChildren(fid){
      step.fields.forEach(function(g){ if (g.cascadeFrom === fid) refreshChild(g.id); });
    }
    function refreshChild(childId){
      var f = byId[childId]; if (!f) return;
      var wrap = wrapFor(childId); if (!wrap) return;
      var sel = wrap.querySelector('select[data-fid="' + childId + '"]');
      var other = wrap.querySelector('input[data-fid="' + childId + '-other"]');
      var pv = parentValue(f.cascadeFrom);
      /* FIX4 — self-heal: answers saved by the old fieldValue carried the
         placeholder text 'Choose…' as if it were a choice. Treat it as
         unchosen, so a stale save can never poison the chain again. */
      var saved = S.answers[childId] || '';
      if (saved === 'Choose…') saved = '';
      if (!pv) {
        wrap.classList.add('bd-cascade-hidden');
        wrap.setAttribute('data-cascade-mode', 'select');
        if (sel) { sel.hidden = false; sel.innerHTML = '<option value="">Choose…</option>'; sel.value = ''; }
        if (other) { other.hidden = true; other.value = ''; }
        S.answers[childId] = '';
        cascadeChildren(childId);
        return;
      }
      wrap.classList.remove('bd-cascade-hidden');
      var list = (f.cascadeMap || {})[pv];
      if (list && list.length) {
        wrap.setAttribute('data-cascade-mode', 'select');
        if (sel) sel.hidden = false;
        var html = '<option value="">Choose…</option>';
        var inList = false, savedVal = '';
        list.forEach(function(o){ if (o[1] === saved) { inList = true; savedVal = o[0]; } html += '<option value="' + esc(o[0]) + '">' + esc(o[1]) + '</option>'; });
        html += '<option value="__other">Other…</option>';
        if (sel) sel.innerHTML = html;
        if (saved && inList && sel) sel.value = savedVal;
        else if (saved && sel) { sel.value = '__other'; if (other) { other.hidden = false; other.value = saved; } }
        else if (sel) { sel.value = ''; if (other) { other.hidden = true; other.value = ''; } }
      } else {
        wrap.setAttribute('data-cascade-mode', 'text');
        if (sel) sel.hidden = true;
        if (other) { other.hidden = false; other.value = saved; }
      }
      cascadeChildren(childId);
    }
    step.fields.forEach(function(f){
      if (!f.cascadeFrom) return;
      refreshChild(f.id);
      /* FIX4 — the parent listener and the field's OWN listener are two
         different jobs on (sometimes) the same element: the province
         select is BOTH the city's parent AND a field of its own. The old
         code shared one _bdCascadeWired flag for both, so whichever wired
         first won and the other never attached — the province change never
         refreshed the city. Separate flags per job; the parent listener
         refreshes ALL of that parent's children, so shared parents work. */
      var parentSel = fieldsEl.querySelector('[data-fid="' + f.cascadeFrom + '"]');
      if (parentSel && !parentSel._bdParentWired) {
        parentSel._bdParentWired = true;
        parentSel.addEventListener('change', function(){ cascadeChildren(f.cascadeFrom); markChosen(phone); });
      }
      var parentOther = fieldsEl.querySelector('[data-fid="' + f.cascadeFrom + '-other"]');
      if (parentOther && !parentOther._bdParentWired) {
        parentOther._bdParentWired = true;
        parentOther.addEventListener('input', function(){ cascadeChildren(f.cascadeFrom); markChosen(phone); });
      }
      var sel = fieldsEl.querySelector('[data-fid="' + f.id + '"]');
      if (sel && !sel._bdOwnWired) {
        sel._bdOwnWired = true;
        sel.addEventListener('change', function(){
          var other = fieldsEl.querySelector('[data-fid="' + f.id + '-other"]');
          if (other) other.hidden = (sel.value !== '__other');
          markChosen(phone);
        });
      }
    });
  }
  function renderSubs(step, phone){
    var f = null;
    (step.fields || []).forEach(function(x){ if (x.t === 'subs') f = x; });
    if (!f || !phone) return;
    var fieldsEl = phone.querySelector('.bd-fields');
    var host = fieldsEl ? fieldsEl.querySelector('[data-subs-for="' + f.id + '"]') : null;
    if (!host) return;
    var picked = [];
    fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[data-cat]').forEach(function(b){
      if (b.checked) picked.push(b.getAttribute('data-cat'));
    });
    var html = '';
    picked.forEach(function(cat){
      var catLabel = '';
      f.options.forEach(function(o){ if (o[0] === cat) catLabel = o[1]; });
      var subs = (f.subs[cat] || []).map(function(o){
        var saved = S.answers[f.id + '_subs'] || [];
        var on = saved.indexOf(catLabel + ': ' + o[1]) >= 0;
        return '<label class="bd-check"><input type="checkbox" data-sub="' + esc(o[0]) + '" data-cat-label="' + esc(catLabel) + '" value="' + esc(o[1]) + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + '</span></label>';
      }).join('');
      html += '<p class="bd-subs-label">' + esc(catLabel) + '</p><div class="bd-checks">' + subs + '</div>';
    });
    host.innerHTML = html;
  }
  function advance(){
    var step = QUESTIONS[idx];
    collectPhone(currentPhone(), step);
    if (idx < QUESTIONS.length - 1) { idx++; render(true); return; }
    complete();
  }
  function goBack(){
    if (idx > 0) {
      collectPhone(currentPhone(), QUESTIONS[idx]);
      idx--; render(true);
    }
  }
  function render(scroll){
    /* Tear the video down before the phone re-renders: a video element
       destroyed mid-download logs a failed request, and a playing video
       would keep its audio going from a hidden phone. */
    singleEl.querySelectorAll('video').forEach(function(v){ try { v.pause(); v.removeAttribute('src'); v.load(); } catch(e){} });
    singleEl.innerHTML = '';
    var step = QUESTIONS[idx];
    var n = idx + 1;
    var phone = window.bdPhone.buildPhone(step, n, QUESTIONS.length);
    singleEl.appendChild(phone);
    buildFields(step, phone);
    var ta = phone.querySelector('.bd-answer');
    if (ta && !step.fields && !step.video) {
      ta.addEventListener('input', function(){
        S.answers[step.key] = ta.value;
        save();
      });
    }
    /* The foot arrows are built fresh with the phone: re-capture backBtn
       (the portal captured it once at load, when no phone existed yet)
       and wire both arrows every render. */
    var back = phone.querySelector('#fpWalkBack');
    if (back) {
      backBtn = back;
      back.hidden = idx === 0;
      back.addEventListener('click', function(){ goBack(); });
    }
    var next = phone.querySelector('#fpWalkNext');
    if (next) next.addEventListener('click', function(){ advance(); });
    if (scroll) { try { document.getElementById('bdSingle').scrollIntoView({block: 'start'}); } catch(e){} }
  }
  if (window.bdPhone) window.bdPhone.onBall = function(phone, step, n){
    if (step.video) return; /* the video phone has no answer to reveal — the ball just spins, the video plays; arrows advance */
    if (step.pic && !phone.classList.contains('bd-revealed')) {
      /* Tap 1: flash the related image. */
      var summary = collectPhone(phone, step);
      window.bdPhone.reveal(phone, step.q, summary, step.def);
      return;
    }
    /* Tap 2 (or first tap on a picture-less step): move to the next input. */
    advance();
  };
  /* NO SKIP — his ~10:41 count: no skip button anywhere. They click forward
     to advance, enter or not. The fpWalkSkip element stays in the DOM hidden
     (finish() still touches it); there is no skip handler and no skip pill. */
  render(false);
