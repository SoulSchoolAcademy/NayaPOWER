  var idx = 0;
  var fieldsEl = document.getElementById('bdFields');
  function fieldLabel(f){ return f.label || f.id; }
  function fieldValue(f){
    if (!f) return '';
    var el = fieldsEl.querySelector('[data-fid="' + f.id + '"]');
    if (!el) return '';
    if (f.t === 'checks') {
      var vals = [];
      var boxes = fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[type=checkbox]');
      boxes.forEach(function(b){ if (b.checked) vals.push(b.value); });
      return vals;
    }
    if (f.t === 'subs') {
      var cats = [];
      var cboxes = fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[data-cat]');
      cboxes.forEach(function(b){ if (b.checked) cats.push(b.value); });
      var subs = [];
      var sboxes = fieldsEl.querySelectorAll('[data-fid="' + f.id + '"] input[data-sub]');
      sboxes.forEach(function(b){ if (b.checked) subs.push(b.getAttribute('data-cat-label') + ': ' + b.value); });
      return {cats: cats, subs: subs};
    }
    if (f.t === 'select') {
      var opt = el.options[el.selectedIndex];
      return opt ? opt.text : '';
    }
    return el.value || '';
  }
  function collect(){
    var step = QUESTIONS[idx];
    if (!step.fields) {
      S.answers[step.key] = ansEl.value;
      save();
      return ansEl.value || '';
    }
    var parts = [];
    step.fields.forEach(function(f){
      var v = fieldValue(f);
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
    /* The step summary lives under the step key — UNLESS a field already
       owns that key (gender, connect): the field's own answer wins, and
       the summary would clobber it. finish() still counts the step via
       the field value, which is truthy when anything was answered. */
    var collides = step.fields.some(function(f){ return f.id === step.key; });
    if (!collides) S.answers[step.key] = summary;
    save();
    return summary;
  }
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function buildFields(step){
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
    renderSubs(step);
    if (!fieldsEl._bdWired) {
      fieldsEl._bdWired = true;
      fieldsEl.addEventListener('change', onFieldChange);
      fieldsEl.addEventListener('input', onFieldChange);
    }
  }
  function renderSubs(step){
    var f = null;
    (step.fields || []).forEach(function(x){ if (x.t === 'subs') f = x; });
    if (!f) return;
    var host = fieldsEl.querySelector('[data-subs-for="' + f.id + '"]');
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
  function onFieldChange(){
    var step = QUESTIONS[idx];
    if (step.fields) renderSubs(step);
    collect();
  }
  function render(){
    var step = QUESTIONS[idx];
    qEl.textContent = '\u201C' + step.q + '\u201D';
    progEl.textContent = (idx + 1) + ' of ' + QUESTIONS.length;
    backBtn.hidden = idx === 0;
    endEl.hidden = true;
    if (step.fields) {
      ansEl.hidden = true;
      fieldsEl.hidden = false;
      buildFields(step);
    } else {
      fieldsEl.hidden = true;
      ansEl.hidden = false;
      ansEl.value = S.answers[step.key] || '';
      ansEl.placeholder = step.ph || '';
    }
    if (window.bdPhone) window.bdPhone.showInput(step.pic || '');
    var first = fieldsEl.querySelector('input,select');
    if (first && step.fields) { try { first.focus({preventScroll:true}); } catch(e){} }
    else { try { ansEl.focus({preventScroll:true}); } catch(e){} }
  }
  ansEl.addEventListener('input', function(){
    S.answers[QUESTIONS[idx].key] = ansEl.value;
    save();
  });
  backBtn.addEventListener('click', function(){
    if (idx > 0) { idx--; render(); }
  });
  var nextBtn = document.getElementById('fpWalkNext');
  if (nextBtn) nextBtn.addEventListener('click', function(){
    collect();
    if (idx < QUESTIONS.length - 1) { idx++; render(); return; }
    complete();
  });
  enterBtn.addEventListener('click', function(){
    if (!endEl.hidden) return; /* the ball is Enter: it reveals, it never navigates */
    var step = QUESTIONS[idx];
    var summary = collect();
    if (window.bdPhone) window.bdPhone.reveal(step.q, summary, step.def, step.pic || '');
  });
  /* NO SKIP — his ~10:41 count: no skip button anywhere. They click forward
     to advance, enter or not. The fpWalkSkip element stays in the DOM hidden
     (finish() still touches it); there is no skip handler and no skip pill. */
  render();
