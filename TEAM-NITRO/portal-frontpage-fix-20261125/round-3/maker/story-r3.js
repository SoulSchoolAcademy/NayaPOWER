/* ROUND 3 — the visual story, in place. Data (FP_SLIDES, FP_SLIDE_IMGS,
   FP_FINAL, FP_PORTRAITS) is injected by build-fix-r3.mjs, harvested verbatim
   from the live agreement v25. No navigation away: every entry opens the
   story at slide 0 ("The Old Way"); closing or agreeing returns to the front
   page, to the name box. */
(function () {
  var story = document.getElementById('fpStory');
  if (!story) return;
  var img = document.getElementById('fpStoryImg');
  var titleEl = document.getElementById('fpStoryTitle');
  var textEl = document.getElementById('fpStoryText');
  var stationEl = document.getElementById('fpStoryStation');
  var countEl = document.getElementById('fpStoryCount');
  var faceEl = document.getElementById('fpStoryFace');
  var nEl = document.getElementById('fpStoryN');
  var backBtn = document.getElementById('fpStoryBack');
  var nextBtn = document.getElementById('fpStoryNext');
  var closeBtn = document.getElementById('fpStoryClose');
  var agreeWrap = document.getElementById('fpStoryAgreeWrap');
  var agreeBtn = document.getElementById('fpStoryAgree');
  var linksBar = document.getElementById('fpStoryLinks');
  var endBox = document.getElementById('fpStoryEnd');
  var finalReader = document.getElementById('fpStoryFinal');
  var finalTitle = document.getElementById('fpStoryFinalTitle');
  var finalBody = document.getElementById('fpStoryFinalBody');
  var finalClose = document.getElementById('fpStoryFinalClose');
  var TOTAL = FP_SLIDES.length;
  var current = 0;
  var dec = document.createElement('div');

  function plain(s) { dec.innerHTML = s; return dec.textContent || s; }
  function nameInput() {
    return document.querySelector('input[autocomplete="name"]') ||
      document.getElementById('fpName') ||
      document.querySelector('.content input');
  }
  function render() {
    var s = FP_SLIDES[current];
    img.src = FP_SLIDE_IMGS[current];
    img.alt = s.a || '';
    titleEl.textContent = plain(s.t);
    textEl.innerHTML = s.x;
    stationEl.textContent = plain(s.t).toUpperCase();
    countEl.textContent = (current + 1) + ' of ' + TOTAL;
    faceEl.src = FP_PORTRAITS[current % FP_PORTRAITS.length];
    backBtn.disabled = current === 0;
    /* CONFIRMED live behaviour (2026-11-25 17:42-17:55 MST): forward from
       slide 27 EXITS to the name entry — so Next is never disabled; on the
       last slide it is the agree action (close to the name box). */
    nextBtn.disabled = false;
    var last = current === TOTAL - 1;
    agreeWrap.hidden = !last;
    linksBar.hidden = !last;
    endBox.hidden = !last;
    var board = story.querySelector('.fp-story-board');
    if (board) board.scrollTop = 0;
    story.querySelector('.fp-story-frame').scrollTop = 0;
    story.scrollTop = 0;
  }
  function openStory(i) {
    current = Math.max(0, Math.min(TOTAL - 1, i || 0));
    render();
    story.hidden = false;
    document.body.classList.add('fp-story-open');
    closeBtn.focus();
  }
  function closeStory() {
    story.hidden = true;
    finalReader.hidden = true;
    document.body.classList.remove('fp-story-open');
    var n = nameInput();
    if (n) { try { n.focus(); } catch (e) {} }
  }
  function openFinal(key) {
    var e = FP_FINAL[key];
    if (!e) return;
    finalTitle.textContent = e.t;
    finalBody.textContent = e.body;
    finalReader.hidden = false;
    finalClose.focus();
  }
  /* entries: the red N in the circle, both corner Ns, "Read the agreement" */
  var circleN = document.getElementById('fpCircleN');
  if (circleN) circleN.addEventListener('click', function () { openStory(0); });
  var corners = document.querySelectorAll('.ncorner');
  for (var c = 0; c < corners.length; c++) {
    corners[c].addEventListener('click', function (ev) {
      ev.preventDefault();
      openStory(0);
    });
  }
  var deal = document.getElementById('fpEnterDeal');
  if (deal) deal.addEventListener('click', function () { openStory(0); });
  backBtn.addEventListener('click', function () {
    if (current > 0) { current--; render(); }
  });
  nextBtn.addEventListener('click', function () {
    if (current < TOTAL - 1) { current++; render(); }
    else closeStory(); /* forward from slide 27 exits to the name entry */
  });
  closeBtn.addEventListener('click', closeStory);
  agreeBtn.addEventListener('click', closeStory);
  finalClose.addEventListener('click', function () {
    finalReader.hidden = true;
    closeBtn.focus();
  });
  var links = linksBar.querySelectorAll('[data-final]');
  for (var l = 0; l < links.length; l++) {
    links[l].addEventListener('click', function () {
      openFinal(this.getAttribute('data-final'));
    });
  }
  document.addEventListener('keydown', function (ev) {
    if (story.hidden) return;
    if (ev.key === 'Escape') {
      if (!finalReader.hidden) { finalReader.hidden = true; closeBtn.focus(); }
      else closeStory();
    } else if (ev.key === 'ArrowRight' && finalReader.hidden) {
      if (current < TOTAL - 1) { current++; render(); }
      else closeStory();
    } else if (ev.key === 'ArrowLeft' && finalReader.hidden && current > 0) {
      current--; render();
    }
  });
  /* the circle N and the board N reuse the harvested red ball already on the
     page (corner img) — same bytes, no duplicate 182 KB data URI. */
  var ball = document.querySelector('.ncorner-right img');
  if (ball) {
    var circleImg = document.getElementById('fpCircleNImg');
    if (circleImg) circleImg.src = ball.src;
    if (nEl) nEl.src = ball.src;
  }
  window.fpOpenStory = openStory;
})();
