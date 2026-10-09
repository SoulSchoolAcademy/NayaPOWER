/* Smart Block: ship-gate — byte-true from Naya Epic Elements - Lego pieces N5.html */
/* Ship gate — launch sequence */
(function () {
  var boxes = document.querySelectorAll('.check input');
  var fill = document.getElementById('gateFill');
  var status = document.getElementById('gateStatus');
  var count = document.getElementById('gateCount');
  function update() {
    var n = 0; boxes.forEach(function (b) { if (b.checked) n++; });
    fill.style.width = (n / boxes.length * 100) + '%';
    if (n === boxes.length) {
      status.classList.add('open');
      status.innerHTML = '<span class="gate-lock">✓</span> CLEARED FOR LAUNCH';
    } else {
      status.classList.remove('open');
      status.innerHTML = '<span class="gate-lock">◈</span> GATE CLOSED · <b id="gateCount">' + n + ' / ' + boxes.length + '</b> checks cleared';
    }
  }
  boxes.forEach(function (b) { b.addEventListener('change', update); });
  update();
})();
