  var idx = 0;
  var gidx = 0;
  var GROUPS = [];
  for (var gi = 0; gi < QUESTIONS.length; gi += 3) GROUPS.push(QUESTIONS.slice(gi, gi + 3));
  var trioEl = document.getElementById('bdTrio');
  var groupProgEl = document.getElementById('bdGroupProg');
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function fieldLabel(f){ return f.label || f.id; }
  function phoneOf(step){ return trioEl.querySelector('[data-key="' + step.key + '"]'); }
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
    var el = fieldsEl.querySelector('[data-fid="' + f.id + '"]');
    if (!el) return '';
    if (f.t === 'select') {
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
  function collectGroup(){
    var out = [];
    GROUPS[gidx].forEach(function(step){
      out.push(collectPhone(phoneOf(step), step));
    });
    return out;
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
        var opts = f.options.map(function(o){
          return '<option value="' + esc(o[0]) + '"' + ((S.answers[f.id] || '') === o[1] ? ' selected' : '') + '>' + esc(o[1]) + '</option>';
        }).join('');
        d.innerHTML = '<label>' + esc(fieldLabel(f)) + '</label><select data-fid="' + esc(f.id) + '">' + opts + '</select>';
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
      });
      fieldsEl.addEventListener('input', function(){ collectPhone(phone, step); });
    }
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
  function render(scroll){
    /* Tear the video down before the trio re-renders: a video element
       destroyed mid-download logs a failed request, and a playing video
       would keep its audio going from a hidden phone. */
    trioEl.querySelectorAll('video').forEach(function(v){ try { v.pause(); v.removeAttribute('src'); v.load(); } catch(e){} });
    trioEl.innerHTML = '';
    var group = GROUPS[gidx];
    var first = gidx * 3 + 1;
    var last = gidx * 3 + group.length;
    group.forEach(function(step, i){
      var n = gidx * 3 + i + 1;
      idx = n - 1;
      var phone = window.bdPhone.buildPhone(step, n, QUESTIONS.length);
      trioEl.appendChild(phone);
      buildFields(step, phone);
      var ta = phone.querySelector('.bd-answer');
      if (ta && !step.fields && !step.video) {
        ta.addEventListener('input', function(){
          S.answers[step.key] = ta.value;
          save();
        });
      }
    });
    if (groupProgEl) groupProgEl.textContent = 'Group ' + (gidx + 1) + ' of ' + GROUPS.length + ' — Steps ' + first + '–' + last + ' of ' + QUESTIONS.length;
    backBtn.hidden = gidx === 0;
    if (scroll) { try { document.getElementById('bdTrioWrap').scrollIntoView({block: 'start'}); } catch(e){} }
  }
  if (window.bdPhone) window.bdPhone.onBall = function(phone, step, n){
    if (step.video) return; /* the video phone has no answer to reveal — the ball just spins, the video plays */
    if (phone.classList.contains('bd-revealed')) { window.bdPhone.unreveal(phone); return; }
    var summary = collectPhone(phone, step);
    window.bdPhone.reveal(phone, step.q, summary, step.def);
  };
  backBtn.addEventListener('click', function(){
    if (gidx > 0) { collectGroup(); gidx--; render(true); }
  });
  var nextBtn = document.getElementById('fpWalkNext');
  if (nextBtn) nextBtn.addEventListener('click', function(){
    collectGroup();
    if (gidx < GROUPS.length - 1) { gidx++; render(true); return; }
    complete();
  });
  /* NO SKIP — his ~10:41 count: no skip button anywhere. They click forward
     to advance, enter or not. The fpWalkSkip element stays in the DOM hidden
     (finish() still touches it); there is no skip handler and no skip pill. */
  render(false);
