

/* =========================================================
   NAYANET ORBITAL JEWEL GENERATOR
   ---------------------------------------------------------
   12 color families × 3 shades × 3 repetitions
   = 108 individually colored luxury crystal jewels.
   ========================================================= */

(function(){

  const orbit =
    document.getElementById('nayaColorOrbit');

  const orbitFrame =
    document.querySelector('.naya-orbit');

  if(!orbit || !orbitFrame){
    return;
  }

  /* =======================================================
     FULL SPECTRUM
     ======================================================= */

  const palette = [

    /* 01 — PEARL / WHITE */
    '#ffffff',
    '#fff5fb',
    '#ffe7f3',

    /* 02 — ROSE */
    '#ffb6d9',
    '#ff78bb',
    '#ff3f9f',

    /* 03 — MAGENTA */
    '#ff36c8',
    '#e91caf',
    '#c91a9e',

    /* 04 — PURPLE */
    '#c56bff',
    '#a94dff',
    '#8735e8',

    /* 05 — VIOLET */
    '#7b4dff',
    '#6634e6',
    '#5125bd',

    /* 06 — INDIGO */
    '#4c3bd4',
    '#3f42b9',
    '#343b98',

    /* 07 — BLUE */
    '#3f68e8',
    '#3d8cff',
    '#55adff',

    /* 08 — CYAN / TEAL */
    '#54d9ff',
    '#45d5d2',
    '#38c5b4',

    /* 09 — GREEN */
    '#40cf91',
    '#49d878',
    '#63df61',

    /* 10 — LIME / YELLOW */
    '#91e94f',
    '#c4ee4b',
    '#e9ed55',

    /* 11 — GOLD / ORANGE */
    '#f4d14e',
    '#f5ad45',
    '#f48a3e',

    /* 12 — RED */
    '#f05a46',
    '#ed3d50',
    '#d82f61'

  ];

  /*
    Three complete passes through the spectrum.

    This does not merely add random dots.
    It deliberately creates three full color cycles
    around the ring so every range of the spectrum is
    represented evenly.

    36 colors × 3 passes = 108 jewels.
  */

  const repeats = 3;

  const total =
    palette.length * repeats;

  /*
    All jewels remain tightly controlled in scale.
    The visual hierarchy comes from:

      - facet geometry
      - spectral color
      - white highlights
      - restrained glow
      - density
      - continuous motion

    Not from cheap random blinking or oversized lights.
  */

  const jewelSize = 4.9;

  /*
    The radius is calculated in real pixels.
    The orbit has been moved upward 8px to follow
    the vault center.

    44% keeps the jewel ring just outside the
    silver vault while preserving the elegant
    separation toward the white unity light.
  */

  function positionJewels(){

    const orbitSize =
      orbitFrame.getBoundingClientRect().width;

    const radius =
      orbitSize * .44;

    orbit.style.setProperty(
      '--computed-orbit-radius',
      radius + 'px'
    );

    const jewels =
      orbit.querySelectorAll('.naya-jewel');

    jewels.forEach(function(jewel){

      jewel.style.setProperty(
        '--orbit-radius',
        radius + 'px'
      );

    });

  }

  /*
    Generate all 108 jewels.
  */

  for(let i = 0; i < total; i++){

    const jewel =
      document.createElement('span');

    /*
      Every jewel receives an exact position around
      the 360-degree circle.

      108 jewels means approximately 3.33 degrees
      between each jewel — a much more continuous,
      finely crafted ring.
    */

    const angle =
      (360 / total) * i;

    const colorIndex =
      i % palette.length;

    jewel.className =
      'naya-jewel';

    jewel.style.setProperty(
      '--jewel',
      palette[colorIndex]
    );

    jewel.style.setProperty(
      '--angle',
      angle + 'deg'
    );

    jewel.style.setProperty(
      '--size',
      jewelSize + 'px'
    );

    jewel.style.setProperty(
      '--size-mobile',
      '4.25px'
    );

    /*
      Consistent scale creates the appearance of
      precision-cut fine jewelry rather than
      decorative random particles.
    */

    jewel.style.setProperty(
      '--scale',
      '1'
    );

    jewel.style.setProperty(
      '--opacity',
      '.9'
    );

    orbit.appendChild(jewel);

  }

  /*
    Position after the jewels exist and the browser
    has rendered the responsive orbit dimensions.
  */

  positionJewels();

  window.addEventListener(
    'resize',
    positionJewels,
    {passive:true}
  );

})();



/* =========================================================
   ENTRY-FLOW CONFIG — the one deployment seam.
   ---------------------------------------------------------
   HUB_APP_URL: where the Intelligent Hub app is hosted.
   Set it to the Hub's address (an absolute URL is safest
   once the pages and the Hub live on different hosts).

   The Hub entry URL carries the one-time identity handoff
   (?name=…&alias=…) so the Hub — a separate site — can
   recognize the visitor. The Hub consumes it once and
   scrubs it from the address bar.
   ========================================================= */

var HUB_APP_URL = 'hub/';

function hubEntryUrl(){

  var name = '';
  var alias = '';

  try{

    name =
      localStorage.getItem(
        'nayanet_smart_name'
      ) || '';

    alias =
      localStorage.getItem(
        'nayanet_smart_alias'
      ) || '';

  }catch(e){}

  var url = HUB_APP_URL;

  if(name || alias){

    url +=
      (url.indexOf('?') === -1 ? '?' : '&') +
      'name=' +
      encodeURIComponent(name) +
      '&alias=' +
      encodeURIComponent(alias);

  }

  return url;

}



/* =========================================================
   AUTO LOGIN — a saved identity jumps straight into the Hub.
   ========================================================= */

function checkAutoLogin(){

  var alias = null;

  try{

    alias =
      localStorage.getItem(
        'nayanet_smart_alias'
      );

  }catch(e){}

  if(alias){

    location.href = hubEntryUrl();

  }else{

    alert(
      'No saved key found. Enter your name to generate your NayaNET key.'
    );

  }

}



/* =========================================================
   EXISTING ENTRY FLOW
   ========================================================= */

document
  .getElementById('entryForm')
  .addEventListener(
    'submit',
    function(e){

      e.preventDefault();

      const input =
        document.getElementById('userName');

      const name =
        input.value.trim();

      if(!name){
        return;
      }

      sessionStorage.setItem(
        'nayanet_user_name',
        name
      );

      document.body.classList.add(
        'entering'
      );

      document
        .getElementById('presence')
        .textContent =
        'Naya Responding';

      input.blur();

      setTimeout(
        function(){

          location.href =
            'identity.html?name=' +
            encodeURIComponent(name);

        },
        1350
      );

    }
  );



/* =========================================================
   WELCOME BACK
   ---------------------------------------------------------
   A remembered identity skips the form: the portal greets
   the visitor by name with a one-tap jump back into the Hub.
   "Use a different identity" clears the saved profile and
   restores the name entry. Nothing here is a verified
   credential — it is a remembered profile on this device.
   ========================================================= */

(function welcomeBack(){

  var alias = null;
  var name = '';

  try{

    alias =
      localStorage.getItem(
        'nayanet_smart_alias'
      );

    name =
      localStorage.getItem(
        'nayanet_smart_name'
      ) || '';

  }catch(e){}

  if(!alias){
    return;
  }

  var form =
    document.getElementById('entryForm');

  var presence =
    document.getElementById('presence');

  var content =
    document.querySelector('.content');

  if(!content){
    return;
  }

  if(form){
    form.style.display = 'none';
  }

  if(presence){
    presence.textContent = 'Welcome back';
  }

  var safeName =
    String(name).replace(/[<>&"']/g, '');

  var back =
    document.createElement('div');

  back.id = 'welcomeBack';

  back.innerHTML =
    '<div class="wb-name">' +
      (safeName
        ? 'Good to see you,<br><strong>' +
          safeName +
          '</strong>'
        : 'Good to see you') +
    '</div>' +
    '<button class="enter" type="button" id="wbJump">' +
      'Jump back in →' +
    '</button>' +
    '<button class="wb-switch" type="button" id="wbSwitch">' +
      'Use a different identity' +
    '</button>';

  content.appendChild(back);

  document
    .getElementById('wbJump')
    .addEventListener(
      'click',
      function(){
        location.href = hubEntryUrl();
      }
    );

  document
    .getElementById('wbSwitch')
    .addEventListener(
      'click',
      function(){

        try{

          localStorage.removeItem(
            'nayanet_smart_alias'
          );

          localStorage.removeItem(
            'nayanet_smart_name'
          );

          localStorage.removeItem(
            'nayanet_vault_key'
          );

        }catch(e){}

        back.remove();

        if(form){
          form.style.display = '';
        }

        if(presence){
          presence.textContent =
            'Naya Listening';
        }

      }
    );

})();

