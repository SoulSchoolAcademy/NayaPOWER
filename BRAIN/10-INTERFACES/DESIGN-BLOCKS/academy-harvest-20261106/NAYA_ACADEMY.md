\<\!-- \============================================================  
     NAYANET — ICONIC CINEMATIC CONVERSION PAGE  
       
     DESIGN PRINCIPLE:  
     Premium technology \+ human potential \+ cinematic luxury.  
       
     NO EXTERNAL LIBRARIES  
     RESPONSIVE  
     MOBILE-FIRST  
     ACCESSIBLE  
     REDUCED-MOTION FRIENDLY  
     \============================================================ \--\>

\<style\>

/\* \============================================================  
   01 — GLOBAL FOUNDATION  
   \============================================================ \*/

html,  
body {  
    width: 100% \!important;  
    min-width: 100% \!important;  
    margin: 0 \!important;  
    padding: 0 \!important;  
    overflow-x: hidden \!important;  
    background: \#030305 \!important;  
    color: \#fff \!important;  
}

html {  
    min-height: 100%;  
}

body {  
    min-height: 100vh;  
    font-family:  
        Inter,  
        \-apple-system,  
        BlinkMacSystemFont,  
        "Segoe UI",  
        Roboto,  
        Helvetica,  
        Arial,  
        sans-serif;  
    \-webkit-font-smoothing: antialiased;  
    \-moz-osx-font-smoothing: grayscale;  
}

\*,  
\*::before,  
\*::after {  
    box-sizing: border-box;  
}

body \> \*,  
main,  
section,  
article,  
header,  
footer,  
div {  
    max-width: none;  
}

/\* \============================================================  
   02 — MASTER ATMOSPHERE  
   \============================================================ \*/

body {  
    background:  
        radial-gradient(  
            ellipse 100% 48% at 50% \-5%,  
            rgba(196, 100, 255, 0.48) 0%,  
            rgba(125, 42, 226, 0.32) 26%,  
            rgba(45, 14, 83, 0.28) 52%,  
            transparent 76%  
        ),  
        linear-gradient(  
            180deg,  
            \#130622 0%,  
            \#09050e 31%,  
            \#040407 67%,  
            \#020203 100%  
        ) \!important;  
}

body::before {  
    content: "";  
    position: fixed;  
    inset: 0;  
    pointer-events: none;  
    z-index: \-10;

    background:  
        radial-gradient(  
            ellipse 45% 30% at 8% 24%,  
            rgba(118, 35, 255, 0.13),  
            transparent 72%  
        ),  
        radial-gradient(  
            ellipse 45% 30% at 92% 24%,  
            rgba(36, 112, 255, 0.10),  
            transparent 72%  
        ),  
        radial-gradient(  
            ellipse 55% 35% at 50% 100%,  
            rgba(31, 180, 117, 0.07),  
            transparent 75%  
        );  
}

/\* \============================================================  
   03 — PAGE CONTAINER  
   \============================================================ \*/

.ny-page-inner {  
    position: relative;  
    width: 100%;  
    min-height: 100vh;  
    isolation: isolate;  
}

/\* \============================================================  
   04 — CINEMATIC THEATER  
   \============================================================ \*/

.ny-theater {  
    position: relative;  
    width: 100%;  
    display: flex;  
    justify-content: center;  
    align-items: center;

    padding:  
        clamp(12px, 1.7vw, 26px)  
        clamp(10px, 2.6vw, 44px)  
        clamp(9px, 1.4vw, 20px);

    overflow: hidden;  
}

.ny-theater::before {  
    content: "";  
    position: absolute;

    width: min(1500px, 100%);  
    height: 90%;

    top: 0;  
    left: 50%;

    transform: translateX(-50%);

    pointer-events: none;

    background:  
        radial-gradient(  
            ellipse at center,  
            rgba(132, 50, 240, 0.20),  
            transparent 68%  
        );

    filter: blur(12px);  
}

/\* \============================================================  
   05 — VIDEO FRAME OUTER JEWEL  
   \============================================================ \*/

.ny-screen-frame {  
    position: relative;  
    z-index: 2;

    width: min(1500px, 100%);

    padding: clamp(2px, 0.18vw, 4px);

    border-radius:  
        clamp(13px, 1.45vw, 23px);

    background:  
        linear-gradient(  
            135deg,  
            rgba(255,255,255,0.68),  
            rgba(194,135,255,0.68) 18%,  
            rgba(93,32,175,0.65) 48%,  
            rgba(255,255,255,0.25) 76%,  
            rgba(132,70,230,0.60)  
        );

    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.16),  
        0 15px 45px rgba(0,0,0,0.74),  
        0 25px 90px rgba(71,17,142,0.30),  
        0 0 90px rgba(130,53,244,0.18);  
}

/\* \============================================================  
   06 — VIDEO SCREEN  
   \============================================================ \*/

.ny-screen {  
    position: relative;

    width: 100%;  
    aspect-ratio: 16 / 9;

    overflow: hidden;

    background: \#000;

    border-radius:  
        clamp(11px, 1.25vw, 20px);

    box-shadow:  
        inset 0 1px 0 rgba(255,255,255,0.15),  
        inset 0 0 0 1px rgba(255,255,255,0.04);  
}

.ny-screen::after {  
    content: "";  
    position: absolute;  
    inset: 0;

    pointer-events: none;  
    z-index: 4;

    background:  
        linear-gradient(  
            180deg,  
            rgba(255,255,255,0.035),  
            transparent 18%,  
            transparent 82%,  
            rgba(0,0,0,0.15)  
        );  
}

\#ny-youtube-player {  
    position: absolute;  
    inset: 0;

    width: 100%;  
    height: 100%;

    border: 0 \!important;  
    display: block;

    background: \#000;  
}

/\* \============================================================  
   07 — PRIMARY CTA AREA  
   \============================================================ \*/

.ny-primary-zone {  
    position: relative;  
    z-index: 5;

    width: 100%;

    display: flex;  
    justify-content: center;  
    align-items: center;

    padding:  
        clamp(9px, 1.15vw, 18px)  
        clamp(12px, 2.4vw, 36px)  
        clamp(8px, 1vw, 15px);  
}

/\* \============================================================  
   08 — UNIVERSAL BUTTON  
   \============================================================ \*/

.ny-button {  
    position: relative;

    display: flex;  
    align-items: center;  
    justify-content: center;

    text-decoration: none \!important;  
    color: \#fff \!important;

    cursor: pointer;  
    isolation: isolate;

    \-webkit-tap-highlight-color: transparent;

    transition:  
        transform 220ms cubic-bezier(.2,.8,.2,1),  
        filter 220ms ease,  
        box-shadow 220ms ease;  
}

.ny-button:hover {  
    transform: translateY(-4px);  
    filter: brightness(1.07);  
}

.ny-button:active {  
    transform: translateY(1px) scale(0.995);  
}

.ny-button:focus-visible {  
    outline: 3px solid rgba(222,190,255,0.96);  
    outline-offset: 5px;  
}

.ny-button-face {  
    position: absolute;  
    inset: 0;  
    z-index: \-2;  
    pointer-events: none;  
}

.ny-button-content {  
    position: relative;  
    width: 100%;  
    height: 100%;

    display: flex;  
    align-items: center;  
    justify-content: center;

    gap: clamp(10px, 1vw, 18px);

    padding:  
        clamp(12px, 1.3vw, 20px)  
        clamp(16px, 2vw, 30px);

    text-align: center;  
}

/\* \============================================================  
   09 — PRIMARY CTA  
   \============================================================ \*/

.ny-primary {  
    width: min(700px, 95vw);

    min-height:  
        clamp(78px, 7.3vw, 112px);

    padding: 2px;

    border-radius:  
        clamp(18px, 1.55vw, 25px);

    background:  
        linear-gradient(  
            135deg,  
            \#fff6ff 0%,  
            \#e5baff 9%,  
            \#b565ff 23%,  
            \#7a32e5 42%,  
            \#42118d 63%,  
            \#8f42ee 82%,  
            \#e8c0ff 100%  
        );

    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.28),  
        0 8px 22px rgba(55,14,119,0.52),  
        0 20px 55px rgba(74,20,157,0.30),  
        0 0 65px rgba(150,69,255,0.28),  
        inset 0 1px 1px rgba(255,255,255,0.82);  
}

.ny-primary .ny-button-face {  
    border-radius:  
        clamp(16px, 1.4vw, 23px);

    background:  
        linear-gradient(  
            145deg,  
            \#29222d 0%,  
            \#151117 27%,  
            \#09080b 58%,  
            \#030305 100%  
        );

    box-shadow:  
        inset 0 1px 2px rgba(255,255,255,0.20),  
        inset 0 \-18px 30px rgba(0,0,0,0.60);  
}

.ny-primary::before {  
    content: "";

    position: absolute;  
    top: 2px;  
    left: 12%;

    width: 76%;  
    height: 1px;

    background:  
        linear-gradient(  
            90deg,  
            transparent,  
            rgba(255,255,255,0.75),  
            transparent  
        );

    opacity: 0.78;  
    pointer-events: none;  
}

/\* \============================================================  
   10 — PRIMARY ICON  
   \============================================================ \*/

.ny-primary .ny-icon {  
    position: relative;

    width: clamp(43px, 4vw, 59px);  
    height: clamp(43px, 4vw, 59px);

    flex: 0 0 auto;

    display: flex;  
    align-items: center;  
    justify-content: center;

    border-radius: 50%;

    background:  
        radial-gradient(  
            circle at 30% 20%,  
            \#ffffff 0%,  
            \#f4ddff 12%,  
            \#d28cff 29%,  
            \#9747ff 47%,  
            \#5518a7 68%,  
            \#22043f 100%  
        );

    border: 1px solid rgba(241,217,255,0.98);

    color: \#fff \!important;

    font-size:  
        clamp(18px, 2vw, 27px);

    font-weight: 900;

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.90),  
        inset 0 \-8px 13px rgba(37,4,77,0.72),  
        0 0 19px rgba(167,80,255,0.48),  
        0 5px 14px rgba(0,0,0,0.58);

    text-shadow:  
        0 2px 4px rgba(0,0,0,0.75);  
}

/\* \============================================================  
   11 — BUTTON COPY  
   \============================================================ \*/

.ny-copy {  
    display: flex;  
    flex-direction: column;

    align-items: center;  
    justify-content: center;

    min-width: 0;  
}

.ny-title {  
    display: block;

    color: \#fff \!important;

    font-size:  
        clamp(15px, 1.42vw, 22px);

    line-height: 1.08;

    font-weight: 780;

    letter-spacing: \-0.025em;

    text-shadow:  
        0 2px 9px rgba(0,0,0,0.95);  
}

.ny-sub {  
    display: block;

    margin-top: 6px;

    color:  
        rgba(255,255,255,0.78) \!important;

    font-size:  
        clamp(10px, 0.84vw, 13px);

    line-height: 1.15;

    font-weight: 500;

    letter-spacing: 0.025em;

    text-shadow:  
        0 1px 6px rgba(0,0,0,0.95);  
}

/\* \============================================================  
   12 — SECONDARY GRID  
   \============================================================ \*/

.ny-secondary-grid {  
    position: relative;  
    z-index: 5;

    width: 100%;

    display: grid;

    grid-template-columns:  
        repeat(4, minmax(0, 1fr));

    gap:  
        clamp(9px, 1.25vw, 19px);

    padding:  
        clamp(7px, 0.9vw, 14px)  
        clamp(12px, 2.5vw, 42px)  
        clamp(10px, 1.3vw, 21px);  
}

/\* \============================================================  
   13 — SECONDARY BUTTON FOUNDATION  
   \============================================================ \*/

.ny-secondary {  
    min-width: 0;

    min-height:  
        clamp(94px, 8vw, 124px);

    padding: 2px;

    border-radius:  
        clamp(17px, 1.35vw, 22px);

    background:  
        linear-gradient(  
            135deg,  
            \#ffffff 0%,  
            \#e7eaf0 11%,  
            \#9da4ae 31%,  
            \#ffffff 50%,  
            \#c7ccd4 72%,  
            \#6e757e 100%  
        );

    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.55),  
        0 10px 28px rgba(0,0,0,0.54),  
        0 0 28px rgba(255,255,255,0.06),  
        inset 0 1px 1px rgba(255,255,255,0.94);  
}

.ny-secondary .ny-button-face {  
    border-radius:  
        clamp(15px, 1.18vw, 20px);

    background:  
        linear-gradient(  
            145deg,  
            \#25272d 0%,  
            \#131519 29%,  
            \#08090b 62%,  
            \#020203 100%  
        );

    box-shadow:  
        inset 0 1px 2px rgba(255,255,255,0.18),  
        inset 0 \-14px 27px rgba(0,0,0,0.63);  
}

.ny-secondary::before {  
    content: "";

    position: absolute;  
    top: 2px;  
    left: 9%;

    width: 82%;  
    height: 1px;

    background:  
        linear-gradient(  
            90deg,  
            transparent,  
            rgba(255,255,255,0.55),  
            transparent  
        );

    pointer-events: none;  
    z-index: 3;  
}

/\* \============================================================  
   14 — ICON PLATFORM  
   \============================================================ \*/

.ny-secondary .ny-icon {  
    position: relative;

    width: clamp(43px, 4vw, 58px);  
    height: clamp(43px, 4vw, 58px);

    flex: 0 0 auto;

    display: flex;  
    align-items: center;  
    justify-content: center;

    border-radius: 17px;

    color: \#fff \!important;

    font-size:  
        clamp(18px, 1.8vw, 25px);

    font-weight: 900;

    border: 1px solid rgba(255,255,255,0.82);

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.72),  
        inset 0 \-7px 13px rgba(0,0,0,0.58),  
        0 5px 14px rgba(0,0,0,0.62);

    text-shadow:  
        0 2px 4px rgba(0,0,0,0.82);

    overflow: hidden;  
}

.ny-secondary .ny-icon::after {  
    content: "";

    position: absolute;  
    top: 5%;  
    left: 14%;

    width: 45%;  
    height: 25%;

    border-radius: 50%;

    background:  
        linear-gradient(  
            180deg,  
            rgba(255,255,255,0.72),  
            transparent  
        );

    filter: blur(2px);

    opacity: 0.7;  
}

/\* \============================================================  
   15 — FREE GIFTS ICON  
   MAGENTA / CROWN-ENERGY  
   \============================================================ \*/

.ny-secondary:nth-child(1) .ny-icon {  
    border-radius: 15px;

    background:  
        linear-gradient(  
            145deg,  
            \#ffdcfa 0%,  
            \#ff77dc 18%,  
            \#e62ab8 39%,  
            \#9d1680 64%,  
            \#470635 100%  
        );

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.82),  
        inset 0 \-8px 14px rgba(70,0,48,0.65),  
        0 0 24px rgba(241,42,190,0.34),  
        0 5px 14px rgba(0,0,0,0.62);  
}

/\* Gift box \*/

.ny-gift-symbol {  
    position: relative;

    width: 25px;  
    height: 21px;

    border: 2px solid rgba(255,255,255,0.94);

    border-radius: 3px;

    background:  
        linear-gradient(  
            90deg,  
            transparent 42%,  
            rgba(255,255,255,0.9) 43%,  
            rgba(255,255,255,0.9) 57%,  
            transparent 58%  
        );  
}

.ny-gift-symbol::before {  
    content: "";

    position: absolute;

    left: \-3px;  
    top: \-6px;

    width: 29px;  
    height: 8px;

    border: 2px solid rgba(255,255,255,0.94);

    border-radius: 3px;

    background:  
        linear-gradient(  
            90deg,  
            transparent 40%,  
            rgba(255,255,255,0.9) 41%,  
            rgba(255,255,255,0.9) 59%,  
            transparent 60%  
        );  
}

.ny-gift-symbol::after {  
    content: "";

    position: absolute;

    width: 11px;  
    height: 7px;

    left: 5px;  
    top: \-11px;

    border-top: 2px solid \#fff;  
    border-radius: 50%;  
}

/\* \============================================================  
   16 — PROMAX PLAYER ICON  
   SAPPHIRE BLUE  
   \============================================================ \*/

.ny-secondary:nth-child(2) .ny-icon {  
    border-radius: 50%;

    background:  
        radial-gradient(  
            circle at 30% 20%,  
            \#d9f7ff 0%,  
            \#6bdcff 20%,  
            \#1689ed 43%,  
            \#0755a9 68%,  
            \#032550 100%  
        );

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.85),  
        inset 0 \-8px 15px rgba(0,22,64,0.70),  
        0 0 25px rgba(30,158,255,0.38),  
        0 5px 14px rgba(0,0,0,0.62);  
}

/\* Play jewel \*/

.ny-play-symbol {  
    position: relative;

    width: 0;  
    height: 0;

    margin-left: 4px;

    border-top:  
        10px solid transparent;

    border-bottom:  
        10px solid transparent;

    border-left:  
        16px solid \#ffffff;

    filter:  
        drop-shadow(  
            0 2px 3px rgba(0,0,0,0.55)  
        );  
}

/\* \============================================================  
   17 — AI MASTERCLASS ICON  
   INDIGO / ELECTRIC VIOLET  
   \============================================================ \*/

.ny-secondary:nth-child(3) .ny-icon {  
    border-radius: 18px;

    background:  
        linear-gradient(  
            145deg,  
            \#d8d7ff 0%,  
            \#7674ff 18%,  
            \#4b42d6 40%,  
            \#29228e 68%,  
            \#100b45 100%  
        );

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.82),  
        inset 0 \-8px 14px rgba(12,7,61,0.72),  
        0 0 26px rgba(91,81,255,0.38),  
        0 5px 14px rgba(0,0,0,0.62);  
}

/\* AI neural symbol \*/

.ny-ai-symbol {  
    position: relative;

    width: 30px;  
    height: 30px;  
}

.ny-ai-symbol::before,  
.ny-ai-symbol::after {  
    content: "";

    position: absolute;

    inset: 4px;

    border: 2px solid rgba(255,255,255,0.92);

    border-radius: 50%;  
}

.ny-ai-symbol::after {  
    inset: 9px;

    border-radius: 6px;

    transform: rotate(45deg);

    border-color:  
        rgba(255,255,255,0.84);  
}

.ny-ai-node {  
    position: absolute;

    width: 6px;  
    height: 6px;

    border-radius: 50%;

    background: \#fff;

    box-shadow:  
        0 0 7px rgba(255,255,255,0.95);  
}

.ny-ai-node.n1 {  
    top: 0;  
    left: 12px;  
}

.ny-ai-node.n2 {  
    top: 12px;  
    left: 0;  
}

.ny-ai-node.n3 {  
    top: 12px;  
    right: 0;  
}

.ny-ai-node.n4 {  
    bottom: 0;  
    left: 12px;  
}

/\* \============================================================  
   18 — TAKE YOUR POWER BACK ICON  
   EMERALD  
   \============================================================ \*/

.ny-secondary:nth-child(4) .ny-icon {  
    border-radius: 50%;

    background:  
        radial-gradient(  
            circle at 30% 20%,  
            \#dffff2 0%,  
            \#63efb4 19%,  
            \#19bd79 42%,  
            \#08744a 68%,  
            \#023624 100%  
        );

    box-shadow:  
        inset 0 2px 4px rgba(255,255,255,0.88),  
        inset 0 \-8px 15px rgba(0,48,29,0.70),  
        0 0 26px rgba(27,221,137,0.32),  
        0 5px 14px rgba(0,0,0,0.62);  
}

/\* Power crown / MAX symbol \*/

.ny-power-symbol {  
    position: relative;

    width: 29px;  
    height: 28px;

    transform: rotate(45deg);  
}

.ny-power-symbol::before {  
    content: "";

    position: absolute;

    inset: 3px;

    border:  
        3px solid rgba(255,255,255,0.94);

    border-radius: 7px;

    box-shadow:  
        inset 0 0 5px rgba(255,255,255,0.32);  
}

.ny-power-symbol::after {  
    content: "";

    position: absolute;

    width: 11px;  
    height: 11px;

    left: 9px;  
    top: 9px;

    background: \#fff;

    clip-path:  
        polygon(  
            50% 0%,  
            100% 100%,  
            0% 100%  
        );

    transform: rotate(-45deg);  
}

/\* \============================================================  
   19 — INDIVIDUAL HOVER GLOW  
   \============================================================ \*/

.ny-secondary:nth-child(1):hover {  
    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.58),  
        0 12px 30px rgba(0,0,0,0.56),  
        0 0 35px rgba(235,36,185,0.22);  
}

.ny-secondary:nth-child(2):hover {  
    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.58),  
        0 12px 30px rgba(0,0,0,0.56),  
        0 0 35px rgba(30,160,255,0.22);  
}

.ny-secondary:nth-child(3):hover {  
    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.58),  
        0 12px 30px rgba(0,0,0,0.56),  
        0 0 35px rgba(88,76,255,0.24);  
}

.ny-secondary:nth-child(4):hover {  
    box-shadow:  
        0 0 0 1px rgba(255,255,255,0.58),  
        0 12px 30px rgba(0,0,0,0.56),  
        0 0 35px rgba(25,220,130,0.22);  
}

/\* \============================================================  
   20 — MEMBERSHIP SECTION  
   \============================================================ \*/

.ny-membership {  
    position: relative;  
    z-index: 5;

    width: 100%;

    display: flex;  
    justify-content: center;  
    align-items: center;

    padding:  
        clamp(14px, 2.4vw, 38px)  
        clamp(12px, 3vw, 45px)  
        clamp(24px, 3.2vw, 48px);  
}

/\* \============================================================  
   21 — MEMBERSHIP PLAQUE  
   \============================================================ \*/

.ny-membership-inner {  
    position: relative;

    width: min(1120px, 100%);

    padding:  
        clamp(28px, 3vw, 48px)  
        clamp(20px, 4vw, 62px);

    text-align: center;

    border-radius:  
        clamp(20px, 1.6vw, 27px);

    background:  
        linear-gradient(  
            145deg,  
            rgba(255,255,255,0.115),  
            rgba(255,255,255,0.045) 40%,  
            rgba(0,0,0,0.22) 100%  
        );

    border:  
        1px solid rgba(255,255,255,0.18);

    box-shadow:  
        inset 0 1px 0 rgba(255,255,255,0.17),  
        inset 0 \-25px 50px rgba(0,0,0,0.18),  
        0 18px 50px rgba(0,0,0,0.44),  
        0 0 50px rgba(112,45,220,0.13);

    backdrop-filter: blur(14px);  
    \-webkit-backdrop-filter: blur(14px);  
}

.ny-membership-inner::before {  
    content: "";

    position: absolute;

    top: 0;  
    left: 12%;

    width: 76%;  
    height: 1px;

    background:  
        linear-gradient(  
            90deg,  
            transparent,  
            rgba(255,255,255,0.56),  
            transparent  
        );  
}

/\* \============================================================  
   22 — MEMBERSHIP KICKER  
   \============================================================ \*/

.ny-membership-kicker {  
    margin-bottom: 10px;

    color:  
        rgba(255,255,255,0.72) \!important;

    font-size:  
        clamp(10px, 0.95vw, 15px);

    line-height: 1.1;

    font-weight: 800;

    letter-spacing:  
        0.25em;

    text-shadow:  
        0 0 16px rgba(165,82,255,0.34);  
}

/\* \============================================================  
   23 — MEMBERSHIP TITLE  
   \============================================================ \*/

.ny-membership-title {  
    color: \#fff \!important;

    font-family:  
        Georgia,  
        "Times New Roman",  
        serif;

    font-size:  
        clamp(30px, 4vw, 55px);

    line-height: 1.05;

    font-weight: 700;

    letter-spacing: \-0.025em;

    text-shadow:  
        0 3px 18px rgba(0,0,0,0.62);  
}

/\* \============================================================  
   24 — MEMBERSHIP DIVIDER  
   \============================================================ \*/

.ny-membership-divider {  
    display: flex;

    align-items: center;  
    justify-content: center;

    gap: 13px;

    width:  
        min(430px, 82%);

    margin:  
        clamp(15px, 1.8vw, 23px)  
        auto;  
}

.ny-membership-divider span {  
    flex: 1;

    height: 1px;

    background:  
        linear-gradient(  
            90deg,  
            transparent,  
            rgba(220,198,255,0.58),  
            transparent  
        );  
}

.ny-membership-divider i {  
    color:  
        \#ffffff;

    font-size: 16px;

    font-style: normal;

    text-shadow:  
        0 0 15px rgba(160,82,255,0.90);  
}

/\* \============================================================  
   25 — MEMBERSHIP SUBTITLE  
   \============================================================ \*/

.ny-membership-sub {  
    color:  
        rgba(255,255,255,0.91) \!important;

    font-family:  
        Georgia,  
        "Times New Roman",  
        serif;

    font-size:  
        clamp(18px, 2vw, 28px);

    line-height: 1.2;

    font-style: italic;

    text-shadow:  
        0 2px 10px rgba(0,0,0,0.50);  
}

/\* \============================================================  
   26 — MAX STATEMENT  
   \============================================================ \*/

.ny-membership-max {  
    margin-top:  
        clamp(17px, 2vw, 28px);

    color:  
        \#fff \!important;

    font-size:  
        clamp(15px, 1.5vw, 23px);

    line-height: 1.3;

    font-weight: 800;

    letter-spacing:  
        clamp(0.08em, 0.15vw, 0.16em);

    text-shadow:  
        0 2px 10px rgba(0,0,0,0.82);  
}

.ny-membership-max span {  
    color:  
        \#ffffff \!important;

    text-shadow:  
        0 0 18px rgba(145,72,255,0.38);  
}

/\* \============================================================  
   27 — TABLET  
   \============================================================ \*/

@media (max-width: 900px) {

    .ny-secondary-grid {  
        grid-template-columns:  
            repeat(2, minmax(0, 1fr));  
    }

    .ny-theater {  
        padding-left: 14px;  
        padding-right: 14px;  
    }

}

/\* \============================================================  
   28 — MOBILE  
   \============================================================ \*/

@media (max-width: 600px) {

    .ny-theater {  
        padding:  
            9px  
            9px  
            7px;  
    }

    .ny-screen-frame {  
        border-radius: 14px;  
    }

    .ny-screen {  
        border-radius: 12px;  
    }

    .ny-primary-zone {  
        padding:  
            7px  
            10px;  
    }

    .ny-primary {  
        width: 100%;  
        min-height: 84px;  
        border-radius: 19px;  
    }

    .ny-primary .ny-button-content {  
        gap: 10px;

        padding:  
            10px  
            14px;  
    }

    .ny-primary .ny-icon {  
        width: 45px;  
        height: 45px;

        font-size: 18px;  
    }

    .ny-primary .ny-title {  
        font-size: 17px;  
    }

    .ny-primary .ny-sub {  
        font-size: 10px;  
    }

    .ny-secondary-grid {  
        grid-template-columns:  
            repeat(2, minmax(0, 1fr));

        gap: 9px;

        padding:  
            6px  
            10px  
            8px;  
    }

    .ny-secondary {  
        min-height: 91px;  
        border-radius: 17px;  
    }

    .ny-secondary .ny-button-content {  
        flex-direction: column;

        gap: 5px;

        padding:  
            8px  
            5px;  
    }

    .ny-secondary .ny-icon {  
        width: 40px;  
        height: 40px;

        font-size: 16px;  
    }

    .ny-title {  
        font-size: 13px;  
    }

    .ny-sub {  
        margin-top: 2px;  
        font-size: 9px;  
    }

    .ny-membership {  
        padding:  
            10px  
            10px  
            22px;  
    }

    .ny-membership-inner {  
        padding:  
            29px  
            18px  
            32px;

        border-radius: 20px;  
    }

    .ny-membership-kicker {  
        font-size: 10px;  
        letter-spacing: 0.18em;  
    }

    .ny-membership-title {  
        font-size: 30px;  
    }

    .ny-membership-sub {  
        font-size: 19px;  
    }

    .ny-membership-max {  
        font-size: 14px;  
        line-height: 1.4;  
    }  
}

/\* \============================================================  
   29 — SMALL MOBILE  
   \============================================================ \*/

@media (max-width: 380px) {

    .ny-theater {  
        padding-left: 7px;  
        padding-right: 7px;  
    }

    .ny-secondary-grid {  
        gap: 7px;

        padding-left: 7px;  
        padding-right: 7px;  
    }

    .ny-secondary {  
        min-height: 84px;  
    }

    .ny-secondary .ny-icon {  
        width: 36px;  
        height: 36px;  
    }

    .ny-secondary .ny-title {  
        font-size: 12px;  
    }

    .ny-secondary .ny-sub {  
        display: none;  
    }

    .ny-membership-inner {  
        padding:  
            25px  
            15px  
            29px;  
    }  
}

/\* \============================================================  
   30 — LANDSCAPE MOBILE  
   \============================================================ \*/

@media (max-width: 900px) and (orientation: landscape) {

    .ny-theater {  
        padding-top: 7px;  
        padding-bottom: 5px;  
    }

    .ny-screen {  
        max-height: 58vh;  
    }

    .ny-primary {  
        min-height: 68px;  
    }

    .ny-secondary {  
        min-height: 70px;  
    }

    .ny-secondary .ny-button-content {  
        flex-direction: row;  
    }

    .ny-secondary .ny-icon {  
        width: 36px;  
        height: 36px;  
    }

    .ny-membership {  
        padding-top: 8px;  
    }  
}

/\* \============================================================  
   31 — LARGE DESKTOP  
   \============================================================ \*/

@media (min-width: 1600px) {

    .ny-theater {  
        padding-left: 3vw;  
        padding-right: 3vw;  
    }

    .ny-secondary-grid {  
        padding-left: 3vw;  
        padding-right: 3vw;  
    }  
}

/\* \============================================================  
   32 — REDUCED MOTION  
   \============================================================ \*/

@media (prefers-reduced-motion: reduce) {

    .ny-button {  
        transition: none \!important;  
    }

    .ny-button:hover,  
    .ny-button:active {  
        transform: none \!important;  
    }  
}

/\* \============================================================  
   33 — EMBED / GROOVE SAFETY  
   \============================================================ \*/

.ny-theater,  
.ny-primary-zone,  
.ny-secondary-grid,  
.ny-membership {  
    float: none \!important;  
    clear: both \!important;  
}

\</style\>

\<div class="ny-page-inner"\>

    \<\!-- \========================================================  
         CINEMATIC VIDEO  
         \======================================================== \--\>

    \<section  
        class="ny-theater"  
        aria-label="NayaNET cinematic introduction"  
    \>

        \<div class="ny-screen-frame"\>

            \<div class="ny-screen"\>

                \<iframe  
                    id="ny-youtube-player"  
                    src="https\://www\.youtube-nocookie.com/embed/8tApdV0UpRs?rel=0\&modestbranding=1\&playsinline=1\&enablejsapi=1\&vq=hd1080"  
                    title="NayaNET — The Network of Human Potential and AI Mastery"  
                    allow="  
                        accelerometer;  
                        autoplay;  
                        clipboard-write;  
                        encrypted-media;  
                        gyroscope;  
                        picture-in-picture;  
                        web-share;  
                        fullscreen  
                    "  
                    allowfullscreen  
                    loading="eager"  
                    referrerpolicy="strict-origin-when-cross-origin"  
                \>\</iframe\>

            \</div\>

        \</div\>

    \</section\>

    \<\!-- \========================================================  
         PRIMARY CTA  
         \======================================================== \--\>

    \<section  
        class="ny-primary-zone"  
        aria-label="Primary action"  
    \>

        \<a  
            class="ny-button ny-primary"  
            href="https\://takeyourpowerback.xyz/services"  
            aria-label="Start your free trial"  
        \>

            \<span  
                class="ny-button-face"  
                aria-hidden="true"  
            \>\</span\>

            \<span class="ny-button-content"\>

                \<span  
                    class="ny-icon"  
                    aria-hidden="true"  
                \>  
                    ★  
                \</span\>

                \<span class="ny-copy"\>

                    \<span class="ny-title"\>  
                        Start Your Free Trial  
                    \</span\>

                    \<span class="ny-sub"\>  
                        Step Into AI Mastery \+ Human Empowerment  
                    \</span\>

                \</span\>

            \</span\>

        \</a\>

    \</section\>

    \<\!-- \========================================================  
         DESTINATION PORTALS  
         \======================================================== \--\>

    \<nav  
        class="ny-secondary-grid"  
        aria-label="NayaNET destinations"  
    \>

        \<\!-- \====================================================  
             FREE GIFTS  
             \==================================================== \--\>

        \<a  
            class="ny-button ny-secondary"  
            href="https\://d4caeb1f.sibforms.com/serve/MUIFAHZEqs40zTV64qB6TJ3trIfgjO-7ifv\_cwA8Ua9BM\_ZWkkGMHIqLouO50nmRIpU7PfCmTRRO4O0s0nGQfi7t6ToHyQzbMT7iUzmDHZtsD5tx6jc73HxU-foqyiPhBEP8x3cPoVDmowa6zho13-C2BMEL97y1KYyYPYlNelzoBgNwtrgGW5ieJ\_v\_i\_eKEGWIvxw1NNUVnKpa"  
            aria-label="Free Gifts"  
        \>

            \<span  
                class="ny-button-face"  
                aria-hidden="true"  
            \>\</span\>

            \<span class="ny-button-content"\>

                \<span  
                    class="ny-icon"  
                    aria-hidden="true"  
                \>  
                    \<span class="ny-gift-symbol"\>\</span\>  
                \</span\>

                \<span class="ny-copy"\>

                    \<span class="ny-title"\>  
                        Free Gifts  
                    \</span\>

                    \<span class="ny-sub"\>  
                        Begin Here  
                    \</span\>

                \</span\>

            \</span\>

        \</a\>

        \<\!-- \====================================================  
             PROMAX PLAYER  
             \==================================================== \--\>

        \<a  
            class="ny-button ny-secondary"  
            href="https\://promaxplayer.takeyourpowerback.xyz/"  
            aria-label="ProMax Player"  
        \>

            \<span  
                class="ny-button-face"  
                aria-hidden="true"  
            \>\</span\>

            \<span class="ny-button-content"\>

                \<span  
                    class="ny-icon"  
                    aria-hidden="true"  
                \>  
                    \<span class="ny-play-symbol"\>\</span\>  
                \</span\>

                \<span class="ny-copy"\>

                    \<span class="ny-title"\>  
                        ProMax Player  
                    \</span\>

                    \<span class="ny-sub"\>  
                        Experience  
                    \</span\>

                \</span\>

            \</span\>

        \</a\>

        \<\!-- \====================================================  
             AI MASTERCLASS  
             \==================================================== \--\>

        \<a  
            class="ny-button ny-secondary"  
            href="https\://aimasterclass.takeyourpowerback.xyz/"  
            aria-label="AI Masterclass"  
        \>

            \<span  
                class="ny-button-face"  
                aria-hidden="true"  
            \>\</span\>

            \<span class="ny-button-content"\>

                \<span  
                    class="ny-icon"  
                    aria-hidden="true"  
                \>

                    \<span class="ny-ai-symbol"\>

                        \<span class="ny-ai-node n1"\>\</span\>  
                        \<span class="ny-ai-node n2"\>\</span\>  
                        \<span class="ny-ai-node n3"\>\</span\>  
                        \<span class="ny-ai-node n4"\>\</span\>

                    \</span\>

                \</span\>

                \<span class="ny-copy"\>

                    \<span class="ny-title"\>  
                        AI Masterclass  
                    \</span\>

                    \<span class="ny-sub"\>  
                        Master The Engine  
                    \</span\>

                \</span\>

            \</span\>

        \</a\>

        \<\!-- \====================================================  
             TAKE YOUR POWER BACK  
             \==================================================== \--\>

        \<a  
            class="ny-button ny-secondary"  
            href="https\://takeyourpowerback.xyz/"  
            aria-label="Take Your Power Back"  
        \>

            \<span  
                class="ny-button-face"  
                aria-hidden="true"  
            \>\</span\>

            \<span class="ny-button-content"\>

                \<span  
                    class="ny-icon"  
                    aria-hidden="true"  
                \>

                    \<span class="ny-power-symbol"\>\</span\>

                \</span\>

                \<span class="ny-copy"\>

                    \<span class="ny-title"\>  
                        Take Your Power Back  
                    \</span\>

                    \<span class="ny-sub"\>  
                        Become Your Max  
                    \</span\>

                \</span\>

            \</span\>

        \</a\>

    \</nav\>

    \<\!-- \========================================================  
         MEMBERSHIP / BRAND SEAL  
         \======================================================== \--\>

    \<section  
        class="ny-membership"  
        aria-label="NayaNET membership statement"  
    \>

        \<div class="ny-membership-inner"\>

            \<div class="ny-membership-kicker"\>  
                ONE MEMBERSHIP  
            \</div\>

            \<div class="ny-membership-title"\>  
                Everything Included.  
            \</div\>

            \<div class="ny-membership-divider"\>

                \<span\>\</span\>

                \<i aria-hidden="true"\>  
                    ✦  
                \</i\>

                \<span\>\</span\>

            \</div\>

            \<div class="ny-membership-sub"\>  
                Your next level starts here.  
            \</div\>

            \<div class="ny-membership-max"\>

                \<span\>  
                    LEARN AI.  
                \</span\>

                \<span\>  
                    BECOME YOUR MAX.  
                \</span\>

            \</div\>

        \</div\>

    \</section\>

\</div\>  
\<style\>

/\* \============================================================  
   NAYANET — FINAL MEMBERSHIP SIGNATURE POLISH  
   Add at the END of the existing code  
   \============================================================ \*/

.ny-membership {  
    position: relative;  
    z-index: 4;  
    display: flex;  
    align-items: center;  
    justify-content: center;  
    width: 100% \!important;  
    max-width: none \!important;  
    padding:  
        clamp(18px, 2.8vw, 42px)  
        clamp(12px, 3vw, 46px)  
        clamp(28px, 4vw, 58px);  
    overflow: hidden;  
}

.ny-membership::before {  
    content: "";  
    position: absolute;  
    left: 50%;  
    top: 50%;  
    width: min(900px, 90vw);  
    height: 420px;  
    transform: translate(-50%, \-50%);  
    pointer-events: none;  
    background:  
        radial-gradient(  
            ellipse at 50% 42%,  
            rgba(184, 72, 255, 0.16) 0%,  
            rgba(105, 52, 220, 0.10) 28%,  
            rgba(38, 103, 255, 0.055) 46%,  
            transparent 72%  
        );  
    filter: blur(10px);  
}

.ny-membership-inner {  
    position: relative;  
    width: min(1120px, 100%);  
    padding:  
        clamp(34px, 4.2vw, 64px)  
        clamp(22px, 5vw, 76px)  
        clamp(38px, 4.8vw, 70px);  
    text-align: center;  
    border-radius:  
        clamp(20px, 1.8vw, 30px);  
    background:  
        linear-gradient(  
            145deg,  
            rgba(255,255,255,0.105) 0%,  
            rgba(255,255,255,0.045) 24%,  
            rgba(80,38,122,0.065) 55%,  
            rgba(0,0,0,0.34) 100%  
        );  
    border: 1px solid rgba(255,255,255,0.20);  
    box-shadow:  
        0 0 0 1px rgba(153,78,255,0.10),  
        inset 0 1px 0 rgba(255,255,255,0.18),  
        inset 0 \-30px 60px rgba(0,0,0,0.20),  
        0 18px 55px rgba(0,0,0,0.48),  
        0 0 70px rgba(117,46,224,0.12);  
    backdrop-filter: blur(16px);  
    \-webkit-backdrop-filter: blur(16px);  
    overflow: hidden;  
    isolation: isolate;  
}

.ny-membership-inner::before {  
    content: "";  
    position: absolute;  
    top: 0;  
    left: 8%;  
    width: 84%;  
    height: 1px;  
    background:  
        linear-gradient(  
            90deg,  
            transparent 0%,  
            rgba(255,255,255,0.18) 18%,  
            rgba(215,154,255,0.78) 38%,  
            rgba(255,255,255,0.92) 50%,  
            rgba(215,154,255,0.78) 62%,  
            rgba(255,255,255,0.18) 82%,  
            transparent 100%  
        );  
    box-shadow: 0 0 12px rgba(181,91,255,0.45);  
    pointer-events: none;  
}

.ny-membership-inner::after {  
    content: "";  
    position: absolute;  
    left: 50%;  
    top: 0;  
    width: 65%;  
    height: 100%;  
    transform: translateX(-50%);  
    pointer-events: none;  
    background:  
        radial-gradient(  
            ellipse at 50% 0%,  
            rgba(218,76,255,0.12),  
            transparent 62%  
        );  
    z-index: \-1;  
}

/\* ONE MEMBERSHIP \*/

.ny-membership-kicker {  
    position: relative;  
    display: inline-block;  
    margin-bottom: clamp(12px, 1.4vw, 18px);  
    padding: 7px clamp(15px, 1.8vw, 23px);  
    color: \#f0d9ff \!important;  
    font-family:  
        Inter,  
        \-apple-system,  
        BlinkMacSystemFont,  
        "Segoe UI",  
        Roboto,  
        Helvetica,  
        Arial,  
        sans-serif;  
    font-size: clamp(13px, 1.05vw, 17px);  
    line-height: 1;  
    font-weight: 800;  
    letter-spacing: clamp(0.14em, 0.22vw, 0.24em);  
    text-shadow: 0 0 18px rgba(193,83,255,0.42);  
}

.ny-membership-kicker::before,  
.ny-membership-kicker::after {  
    content: "◆";  
    position: absolute;  
    top: 50%;  
    transform: translateY(-50%);  
    font-size: 5px;  
    color: \#b66cff;  
    text-shadow: 0 0 9px rgba(182,108,255,0.9);  
}

.ny-membership-kicker::before {  
    left: 0;  
}

.ny-membership-kicker::after {  
    right: 0;  
}

/\* EVERYTHING INCLUDED \*/

.ny-membership-title {  
    position: relative;  
    color: \#ffffff \!important;  
    font-family:  
        Georgia,  
        "Times New Roman",  
        serif;  
    font-size: clamp(34px, 4.5vw, 62px);  
    line-height: 1.02;  
    font-weight: 700;  
    letter-spacing: \-0.035em;  
    text-shadow:  
        0 3px 22px rgba(0,0,0,0.70),  
        0 0 32px rgba(255,255,255,0.045);  
}

/\* DIVIDER \*/

.ny-membership-divider {  
    display: flex;  
    align-items: center;  
    justify-content: center;  
    gap: 14px;  
    width: min(500px, 88%);  
    margin:  
        clamp(18px, 2.1vw, 27px)  
        auto  
        clamp(17px, 2vw, 25px);  
}

.ny-membership-divider span {  
    flex: 1;  
    height: 1px;  
    background:  
        linear-gradient(  
            90deg,  
            transparent,  
            rgba(205,163,255,0.62),  
            rgba(255,255,255,0.22)  
        );  
    box-shadow:  
        0 0 8px rgba(161,78,255,0.20);  
}

.ny-membership-divider span:last-child {  
    background:  
        linear-gradient(  
            90deg,  
            rgba(255,255,255,0.22),  
            rgba(205,163,255,0.62),  
            transparent  
        );  
}

/\* CENTRAL PURPLE DIAMOND \*/

.ny-membership-divider i {  
    position: relative;  
    display: flex;  
    align-items: center;  
    justify-content: center;  
    width: 31px;  
    height: 31px;  
    flex: 0 0 31px;  
    color: \#ffffff;  
    font-size: 11px;  
    font-style: normal;  
    transform: rotate(45deg);  
    border-radius: 7px;  
    background:  
        linear-gradient(  
            145deg,  
            \#ffdfff 0%,  
            \#ef9cff 18%,  
            \#c346ff 38%,  
            \#7d2be0 62%,  
            \#3c117e 100%  
        );  
    border: 1px solid rgba(255,255,255,0.82);  
    box-shadow:  
        inset 1px 1px 3px rgba(255,255,255,0.75),  
        inset \-3px \-4px 8px rgba(42,5,78,0.50),  
        0 0 15px rgba(201,76,255,0.70),  
        0 0 32px rgba(128,47,226,0.30);  
}

/\* YOUR NEXT LEVEL STARTS HERE \*/

.ny-membership-sub {  
    position: relative;  
    color: rgba(255,255,255,0.97) \!important;  
    font-family:  
        Georgia,  
        "Times New Roman",  
        serif;  
    font-size: clamp(20px, 2.35vw, 31px);  
    line-height: 1.2;  
    font-style: italic;  
    letter-spacing: 0.005em;  
    text-shadow:  
        0 2px 12px rgba(0,0,0,0.60);  
}

.ny-membership-sub::before {  
    content: "“";  
    color: \#b96aff;  
    font-size: 1.35em;  
    margin-right: 3px;  
    text-shadow:  
        0 0 14px rgba(188,92,255,0.50);  
}

.ny-membership-sub::after {  
    content: "”";  
    color: \#6c9dff;  
    font-size: 1.35em;  
    margin-left: 3px;  
    text-shadow:  
        0 0 14px rgba(84,132,255,0.42);  
}

/\* LEARN AI / BECOME YOUR MAX \*/

.ny-membership-max {  
    position: relative;  
    margin-top: clamp(20px, 2.3vw, 31px);  
    color: \#ffffff \!important;  
    font-family:  
        Inter,  
        \-apple-system,  
        BlinkMacSystemFont,  
        "Segoe UI",  
        Roboto,  
        Helvetica,  
        Arial,  
        sans-serif;  
    font-size: clamp(16px, 1.65vw, 24px);  
    line-height: 1.35;  
    font-weight: 850;  
    letter-spacing: clamp(0.08em, 0.14vw, 0.15em);  
    text-shadow:  
        0 2px 12px rgba(0,0,0,0.80);  
}

.ny-membership-max span {  
    display: inline-block;  
    margin-left: 7px;  
    color: \#dca4ff \!important;  
    text-shadow:  
        0 0 18px rgba(181,73,255,0.46),  
        0 2px 12px rgba(0,0,0,0.75);  
}

/\* FOUR-COLOR SIGNATURE \*/

.ny-membership-max::after {  
    content: "";  
    display: block;  
    width: min(180px, 35vw);  
    height: 2px;  
    margin:  
        clamp(14px, 1.6vw, 20px)  
        auto  
        0;  
    border-radius: 999px;  
    background:  
        linear-gradient(  
            90deg,  
            \#e14cff 0%,  
            \#674cff 34%,  
            \#48a8ff 66%,  
            \#45d99a 100%  
        );  
    box-shadow:  
        0 0 12px rgba(150,82,255,0.32);  
    opacity: 0.72;  
}

/\* \============================================================  
   MOBILE  
   \============================================================ \*/

@media (max-width: 600px) {

    .ny-membership {  
        padding:  
            12px  
            10px  
            25px;  
    }

    .ny-membership-inner {  
        padding:  
            31px  
            17px  
            34px;  
        border-radius: 21px;  
    }

    .ny-membership-kicker {  
        margin-bottom: 14px;  
        font-size: 13px;  
        letter-spacing: 0.16em;  
        padding: 7px 14px;  
    }

    .ny-membership-title {  
        font-size: clamp(31px, 9vw, 39px);  
        line-height: 1.02;  
    }

    .ny-membership-divider {  
        width: 90%;  
        gap: 10px;  
        margin: 18px auto;  
    }

    .ny-membership-divider i {  
        width: 28px;  
        height: 28px;  
        flex-basis: 28px;  
        border-radius: 6px;  
        font-size: 10px;  
    }

    .ny-membership-sub {  
        font-size: clamp(19px, 5.5vw, 23px);  
        line-height: 1.25;  
    }

    .ny-membership-max {  
        margin-top: 21px;  
        font-size: clamp(14px, 4vw, 17px);  
        line-height: 1.5;  
        letter-spacing: 0.08em;  
    }

    .ny-membership-max span {  
        display: block;  
        margin: 3px 0 0;  
    }

    .ny-membership-max::after {  
        width: 145px;  
        margin-top: 15px;  
    }  
}

/\* \============================================================  
   SMALL MOBILE  
   \============================================================ \*/

@media (max-width: 380px) {

    .ny-membership-inner {  
        padding:  
            27px  
            14px  
            30px;  
    }

    .ny-membership-kicker {  
        font-size: 12px;  
        letter-spacing: 0.13em;  
    }

    .ny-membership-title {  
        font-size: 29px;  
    }

    .ny-membership-sub {  
        font-size: 18px;  
    }

    .ny-membership-max {  
        font-size: 13px;  
    }  
}

\</style\>  
\<\!-- \============================================================  
 🔱 NAYANET — NAYA POWER ACADEMY  
 FIVE-DAY EXPERIENCE — AAA JEWEL EDITION

 DROP-IN RULE:  
 Paste this ENTIRE block once at the very END of the existing  
 working page code.

 This block:  
 • Preserves the existing page.  
 • Preserves the existing feature player.  
 • Preserves the five Academy videos.  
 • Preserves the checkout destination.  
 • Adds the Academy experience below the existing page.  
 • Creates MAXIS-inspired living jewel boards.  
 • Uses a five-color spectrum across every lesson.  
 • Does NOT require a second patch.  
 \============================================================ \--\>

\<style\>

/\* \============================================================  
   01 — ACADEMY ROOT  
   \============================================================ \*/

.ny-academy-experience {  
  position: relative;  
  width: 100%;  
  margin: 0 auto;  
  padding: clamp(28px, 4vw, 62px) 0 clamp(30px, 4vw, 58px);  
  overflow: hidden;  
  isolation: isolate;  
  color: \#fff;  
}

/\* \============================================================  
   02 — ATMOSPHERE  
   \============================================================ \*/

.ny-academy-experience::before {  
  content: "";  
  position: absolute;  
  z-index: \-2;  
  top: 8%;  
  left: 50%;  
  width: min(1200px, 100%);  
  height: 900px;  
  transform: translateX(-50%);

  background:  
    radial-gradient(  
      ellipse at 50% 15%,  
      rgba(148, 67, 255, .13),  
      transparent 55%  
    ),  
    radial-gradient(  
      ellipse at 15% 55%,  
      rgba(0, 112, 255, .055),  
      transparent 42%  
    ),  
    radial-gradient(  
      ellipse at 85% 80%,  
      rgba(255, 0, 180, .055),  
      transparent 42%  
    );

  pointer-events: none;  
}

.ny-academy-experience::after {  
  content: "";  
  position: absolute;  
  z-index: \-1;  
  inset: 0;

  background:  
    linear-gradient(  
      180deg,  
      transparent 0%,  
      rgba(0,0,0,.08) 30%,  
      rgba(0,0,0,.22) 100%  
    );

  pointer-events: none;  
}

/\* \============================================================  
   03 — INTRO  
   \============================================================ \*/

.ny-academy-intro {  
  width: min(1380px, calc(100% \- 30px));  
  margin: 0 auto clamp(38px, 5vw, 66px);  
  text-align: center;  
}

.ny-academy-eyebrow {  
  display: inline-flex;  
  align-items: center;  
  justify-content: center;

  color: rgba(221, 190, 255, .95);  
  font-size: clamp(10px, .82vw, 13px);  
  line-height: 1.2;  
  font-weight: 900;  
  letter-spacing: .26em;  
  text-transform: uppercase;

  text-shadow:  
    0 0 18px rgba(166, 76, 255, .48);  
}

.ny-academy-title {  
  margin: 13px auto 0;  
  max-width: 1050px;

  color: \#fff;  
  font-size: clamp(32px, 4.5vw, 64px);  
  line-height: .99;  
  font-weight: 900;  
  letter-spacing: \-.052em;

  text-shadow:  
    0 4px 28px rgba(0,0,0,.78),  
    0 0 55px rgba(144, 65, 255, .20);  
}

.ny-academy-title span {  
  display: block;  
  margin-top: 15px;

  color: rgba(231, 211, 255, .94);  
  font-size: clamp(17px, 1.65vw, 25px);  
  line-height: 1.3;  
  font-weight: 650;  
  letter-spacing: \-.018em;  
}

.ny-academy-intro-copy {  
  max-width: 820px;  
  margin: 21px auto 0;

  color: rgba(255,255,255,.76);  
  font-size: clamp(14px, 1.05vw, 17px);  
  line-height: 1.68;  
  font-weight: 500;

  text-shadow: 0 2px 12px rgba(0,0,0,.65);  
}

/\* \============================================================  
   04 — LESSON STACK  
   \============================================================ \*/

.ny-academy-lessons {  
  width: 100%;

  display: flex;  
  flex-direction: column;

  gap: clamp(70px, 8vw, 118px);  
}

/\* \============================================================  
   05 — LESSON  
   \============================================================ \*/

.ny-academy-lesson {  
  width: 100%;  
  margin: 0 auto;

  display: flex;  
  flex-direction: column;  
  align-items: center;  
}

/\* \============================================================  
   06 — LESSON HEADER  
   \============================================================ \*/

.ny-academy-lesson-header {  
  width: min(1500px, calc(100% \- 24px));  
  margin: 0 auto 16px;

  text-align: center;  
}

.ny-academy-day {  
  position: relative;

  display: inline-flex;  
  align-items: center;  
  justify-content: center;

  min-height: 32px;  
  padding: 7px 16px;

  border-radius: 999px;

  background:  
    linear-gradient(  
      135deg,  
      rgba(179, 92, 255, .19),  
      rgba(255,255,255,.035)  
    );

  border: 1px solid rgba(216, 178, 255, .30);

  color: rgba(230, 205, 255, .97);

  font-size: clamp(10px, .75vw, 12px);  
  font-weight: 900;  
  letter-spacing: .22em;  
  text-transform: uppercase;

  box-shadow:  
    inset 0 1px 0 rgba(255,255,255,.11),  
    0 0 28px rgba(138, 58, 238, .10);  
}

.ny-academy-lesson-title {  
  margin: 14px 0 0;

  color: \#fff;  
  font-size: clamp(27px, 3vw, 46px);  
  line-height: 1.03;  
  font-weight: 900;  
  letter-spacing: \-.042em;

  text-shadow:  
    0 4px 25px rgba(0,0,0,.72),  
    0 0 34px rgba(152, 72, 255, .14);  
}

/\* \============================================================  
   07 — CINEMATIC VIDEO  
   \============================================================ \*/

.ny-academy-video-shell {  
  position: relative;

  width: min(1500px, calc(100% \- 24px));

  padding: clamp(2px, .18vw, 4px);

  border-radius: clamp(14px, 1.45vw, 24px);

  background:  
    linear-gradient(  
      135deg,  
      rgba(255,255,255,.78),  
      rgba(199,137,255,.70) 17%,  
      rgba(94,33,178,.72) 48%,  
      rgba(255,255,255,.30) 75%,  
      rgba(139,72,236,.66)  
    );

  box-shadow:  
    0 0 0 1px rgba(255,255,255,.17),  
    0 20px 58px rgba(0,0,0,.74),  
    0 30px 105px rgba(74,18,147,.30),  
    0 0 95px rgba(135,55,245,.16);  
}

.ny-academy-video {  
  position: relative;

  width: 100%;  
  aspect-ratio: 16 / 9;

  overflow: hidden;

  border-radius: clamp(12px, 1.25vw, 21px);

  background: \#000;

  box-shadow:  
    inset 0 1px 0 rgba(255,255,255,.15),  
    inset 0 0 0 1px rgba(255,255,255,.045);  
}

.ny-academy-video::before {  
  content: "";  
  position: absolute;  
  z-index: 2;  
  inset: 0;

  pointer-events: none;

  background:  
    linear-gradient(  
      180deg,  
      rgba(255,255,255,.045),  
      transparent 18%,  
      transparent 82%,  
      rgba(0,0,0,.17)  
    );  
}

.ny-academy-video iframe {  
  position: absolute;  
  inset: 0;

  width: 100%;  
  height: 100%;

  display: block;

  border: 0 \!important;  
  background: \#000;  
}

/\* \============================================================  
   08 — JEWEL BOARD  
   \============================================================ \*/

.ny-jewel-panel {  
  \--board-accent: \#a15cff;  
  \--board-accent-soft: rgba(161,92,255,.22);  
  \--board-accent-bright: rgba(195,143,255,.95);

  position: relative;  
  isolation: isolate;

  width: min(1250px, calc(100% \- 34px));

  margin: clamp(22px, 2.7vw, 36px) auto 0;

  padding:  
    clamp(29px, 3.4vw, 52px)  
    clamp(22px, 3.5vw, 52px)  
    clamp(27px, 3.2vw, 46px);

  overflow: hidden;

  border-radius: 30px;

  background:  
    radial-gradient(  
      circle at 12% 0%,  
      var(--board-accent-soft),  
      transparent 32%  
    ),  
    radial-gradient(  
      circle at 92% 100%,  
      var(--board-accent-soft),  
      transparent 36%  
    ),  
    linear-gradient(  
      145deg,  
      \#211727 0%,  
      \#100c14 43%,  
      \#07070a 100%  
    );

  border: 1px solid rgba(225,205,255,.22);

  box-shadow:  
    0 25px 78px rgba(0,0,0,.52),  
    0 0 85px var(--board-accent-soft),  
    inset 0 1px 0 rgba(255,255,255,.10),  
    inset 0 \-1px 0 rgba(0,0,0,.85);

  text-align: center;  
}

.ny-jewel-panel::before {  
  content: "";

  position: absolute;  
  z-index: \-1;

  top: 0;  
  left: 9%;

  width: 82%;  
  height: 2px;

  background:  
    linear-gradient(  
      90deg,  
      transparent,  
      rgba(255,255,255,.90) 18%,  
      var(--board-accent-bright) 50%,  
      rgba(255,255,255,.90) 82%,  
      transparent  
    );

  box-shadow:  
    0 0 16px var(--board-accent),  
    0 0 38px var(--board-accent-soft);  
}

.ny-jewel-panel::after {  
  content: "";

  position: absolute;  
  z-index: \-1;

  left: 0;  
  top: 15%;

  width: 2px;  
  height: 70%;

  background:  
    linear-gradient(  
      180deg,  
      transparent,  
      var(--board-accent),  
      transparent  
    );

  box-shadow:  
    0 0 18px var(--board-accent),  
    0 0 40px var(--board-accent-soft);  
}

/\* \============================================================  
   09 — BOARD HEADER  
   \============================================================ \*/

.ny-jewel-kicker {  
  color: var(--board-accent-bright);

  font-size: clamp(10px, .78vw, 12px);  
  line-height: 1.2;  
  font-weight: 900;  
  letter-spacing: .25em;  
  text-transform: uppercase;

  text-shadow:  
    0 0 18px var(--board-accent-soft);  
}

.ny-jewel-title {  
  margin: 10px auto 0;

  color: \#fff;

  font-size: clamp(27px, 2.7vw, 41px);  
  line-height: 1.04;  
  font-weight: 900;  
  letter-spacing: \-.042em;

  text-shadow:  
    0 3px 20px rgba(0,0,0,.75),  
    0 0 35px var(--board-accent-soft);  
}

.ny-jewel-summary {  
  max-width: 900px;

  margin: 15px auto 0;

  color: rgba(255,255,255,.82);

  font-size: clamp(14px, 1.04vw, 17px);  
  line-height: 1.65;  
  font-weight: 520;

  text-shadow: 0 2px 10px rgba(0,0,0,.65);  
}

/\* \============================================================  
   10 — FIVE JEWEL CARDS  
   \============================================================ \*/

.ny-jewel-points {  
  width: 100%;  
  max-width: 1120px;

  margin: clamp(29px, 3.2vw, 42px) auto 0;

  display: grid;  
  grid-template-columns: repeat(5, minmax(0, 1fr));

  gap: 12px;  
}

/\* \============================================================  
   11 — INDIVIDUAL JEWEL  
   \============================================================ \*/

.ny-jewel-point {  
  \--jewel: \#a15cff;  
  \--jewel-rgb: 161,92,255;

  position: relative;

  min-height: 190px;

  padding:  
    21px 13px 18px;

  display: flex;  
  flex-direction: column;  
  align-items: center;  
  justify-content: flex-start;

  overflow: hidden;

  border-radius: 20px;

  background:  
    radial-gradient(  
      circle at 50% \-10%,  
      rgba(var(--jewel-rgb), .18),  
      transparent 58%  
    ),  
    linear-gradient(  
      145deg,  
      rgba(255,255,255,.095),  
      rgba(255,255,255,.025)  
    );

  border: 1px solid rgba(var(--jewel-rgb), .42);

  box-shadow:  
    0 12px 34px rgba(0,0,0,.30),  
    0 0 26px rgba(var(--jewel-rgb), .10),  
    inset 0 1px 0 rgba(255,255,255,.10),  
    inset 0 \-1px 0 rgba(0,0,0,.55);

  transition:  
    transform .28s ease,  
    border-color .28s ease,  
    box-shadow .28s ease,  
    filter .28s ease;  
}

.ny-jewel-point::before {  
  content: "";

  position: absolute;

  top: 0;  
  left: 10%;  
  right: 10%;

  height: 1px;

  background:  
    linear-gradient(  
      90deg,  
      transparent,  
      rgba(255,255,255,.72),  
      var(--jewel),  
      rgba(255,255,255,.72),  
      transparent  
    );

  box-shadow:  
    0 0 12px var(--jewel);

  opacity: .90;  
}

.ny-jewel-point::after {  
  content: "";

  position: absolute;

  width: 130px;  
  height: 130px;

  top: \-82px;  
  right: \-62px;

  border-radius: 50%;

  background: var(--jewel);

  filter: blur(55px);

  opacity: .12;

  pointer-events: none;  
}

.ny-jewel-point:hover {  
  transform: translateY(-7px) scale(1.015);

  border-color: rgba(var(--jewel-rgb), .78);

  box-shadow:  
    0 19px 42px rgba(0,0,0,.42),  
    0 0 32px rgba(var(--jewel-rgb), .23),  
    0 0 65px rgba(var(--jewel-rgb), .10),  
    inset 0 1px 0 rgba(255,255,255,.14);

  filter: brightness(1.08);  
}

/\* \============================================================  
   12 — FACETED JEWEL ICON  
   \============================================================ \*/

.ny-jewel-icon {  
  position: relative;

  width: 54px;  
  height: 54px;

  flex: 0 0 auto;

  display: flex;  
  align-items: center;  
  justify-content: center;

  transform: rotate(45deg);

  border-radius: 13px;

  background:  
    linear-gradient(  
      135deg,  
      rgba(255,255,255,.98) 0%,  
      var(--jewel) 28%,  
      color-mix(in srgb, var(--jewel) 68%, \#000 32%) 68%,  
      \#08050d 100%  
    );

  border: 1px solid rgba(255,255,255,.78);

  box-shadow:  
    inset 3px 3px 8px rgba(255,255,255,.55),  
    inset \-7px \-8px 15px rgba(0,0,0,.48),  
    0 0 20px rgba(var(--jewel-rgb), .48),  
    0 7px 18px rgba(0,0,0,.58);

  overflow: hidden;  
}

.ny-jewel-icon::before {  
  content: "";

  position: absolute;

  top: 5px;  
  left: 7px;

  width: 22px;  
  height: 11px;

  border-radius: 50%;

  background: rgba(255,255,255,.78);

  filter: blur(5px);

  opacity: .72;  
}

.ny-jewel-icon::after {  
  content: "";

  position: absolute;  
  inset: 8px;

  border: 1px solid rgba(255,255,255,.34);

  border-radius: 9px;  
}

.ny-jewel-icon span {  
  position: relative;  
  z-index: 2;

  transform: rotate(-45deg);

  color: \#fff;

  font-size: 14px;  
  line-height: 1;  
  font-weight: 950;

  text-shadow:  
    0 2px 5px rgba(0,0,0,.75),  
    0 0 8px rgba(255,255,255,.40);  
}

/\* \============================================================  
   13 — CARD TYPOGRAPHY  
   \============================================================ \*/

.ny-jewel-point-title {  
  margin-top: 17px;

  color: \#fff;

  font-size: clamp(12px, .90vw, 15px);  
  line-height: 1.12;  
  font-weight: 900;  
  letter-spacing: \-.015em;

  text-shadow:  
    0 2px 10px rgba(0,0,0,.72);  
}

.ny-jewel-point-text {  
  margin-top: 8px;

  color: rgba(255,255,255,.70);

  font-size: clamp(10px, .73vw, 12px);  
  line-height: 1.48;  
  font-weight: 500;

  text-shadow:  
    0 1px 7px rgba(0,0,0,.68);  
}

/\* \============================================================  
   14 — BIG IDEA  
   \============================================================ \*/

.ny-nutshell-line {  
  max-width: 920px;

  margin: 29px auto 0;  
  padding-top: 21px;

  border-top:  
    1px solid rgba(255,255,255,.11);

  position: relative;  
}

.ny-nutshell-line::before {  
  content: "";

  position: absolute;

  top: \-1px;  
  left: 34%;

  width: 32%;  
  height: 1px;

  background:  
    linear-gradient(  
      90deg,  
      transparent,  
      var(--board-accent),  
      transparent  
    );

  box-shadow:  
    0 0 12px var(--board-accent);  
}

.ny-nutshell-line-label {  
  color: var(--board-accent-bright);

  font-size: 10px;  
  line-height: 1.2;  
  font-weight: 900;  
  letter-spacing: .22em;  
  text-transform: uppercase;  
}

.ny-nutshell-line-text {  
  margin-top: 8px;

  color: rgba(255,255,255,.94);

  font-size: clamp(14px, 1.03vw, 17px);  
  line-height: 1.52;  
  font-weight: 700;

  text-shadow:  
    0 2px 12px rgba(0,0,0,.65);  
}

/\* \============================================================  
   15 — CTA  
   \============================================================ \*/

.ny-academy-cta {  
  position: relative;

  width: min(700px, calc(100% \- 34px));  
  min-height: clamp(80px, 7vw, 110px);

  margin: clamp(18px, 2.2vw, 27px) auto 0;  
  padding: 2px;

  display: flex;  
  align-items: center;  
  justify-content: center;

  border-radius: 23px;

  background:  
    linear-gradient(  
      135deg,  
      \#fff6ff 0%,  
      \#e7baff 9%,  
      \#b565ff 23%,  
      \#7a32e5 42%,  
      \#42118d 63%,  
      \#8f42ee 82%,  
      \#e8c0ff 100%  
    );

  border: 1px solid rgba(255,255,255,.44);

  color: \#fff \!important;  
  text-decoration: none \!important;

  box-shadow:  
    0 10px 28px rgba(55,14,119,.52),  
    0 24px 62px rgba(74,20,157,.30),  
    0 0 70px rgba(150,69,255,.25),  
    inset 0 1px 1px rgba(255,255,255,.86);

  transition:  
    transform .24s ease,  
    filter .24s ease,  
    box-shadow .24s ease;  
}

.ny-academy-cta::before {  
  content: "";

  position: absolute;  
  inset: 2px;

  border-radius: 21px;

  background:  
    linear-gradient(  
      145deg,  
      \#302733 0%,  
      \#171119 28%,  
      \#09080b 62%,  
      \#030305 100%  
    );

  box-shadow:  
    inset 0 1px 2px rgba(255,255,255,.18),  
    inset 0 \-18px 30px rgba(0,0,0,.58);  
}

.ny-academy-cta:hover {  
  transform: translateY(-5px);

  filter: brightness(1.08);

  box-shadow:  
    0 14px 34px rgba(55,14,119,.60),  
    0 28px 76px rgba(105,37,220,.40),  
    0 0 86px rgba(170,80,255,.34),  
    inset 0 1px 1px rgba(255,255,255,.96);  
}

.ny-academy-cta-content {  
  position: relative;  
  z-index: 2;

  width: 100%;  
  min-height: 76px;

  display: flex;  
  align-items: center;  
  justify-content: center;

  gap: 14px;

  padding: 13px 25px;

  text-align: center;  
}

.ny-academy-cta-icon {  
  position: relative;

  width: 48px;  
  height: 48px;

  flex: 0 0 auto;

  display: flex;  
  align-items: center;  
  justify-content: center;

  border-radius: 50%;

  background:  
    radial-gradient(  
      circle at 30% 20%,  
      \#fff 0%,  
      \#f4ddff 12%,  
      \#d28cff 29%,  
      \#9747ff 47%,  
      \#5518a7 68%,  
      \#22043f 100%  
    );

  border: 1px solid rgba(241,217,255,.98);

  color: \#fff;

  font-size: 20px;

  box-shadow:  
    inset 0 2px 4px rgba(255,255,255,.90),  
    inset 0 \-8px 13px rgba(37,4,77,.72),  
    0 0 19px rgba(167,80,255,.45),  
    0 5px 14px rgba(0,0,0,.58);  
}

.ny-academy-cta-copy {  
  display: flex;  
  flex-direction: column;  
  align-items: center;  
}

.ny-academy-cta-title {  
  color: \#fff;

  font-size: clamp(16px, 1.4vw, 21px);  
  line-height: 1.12;  
  font-weight: 850;  
  letter-spacing: \-.02em;

  text-shadow:  
    0 2px 10px rgba(0,0,0,.60);  
}

.ny-academy-cta-sub {  
  margin-top: 5px;

  color: rgba(255,255,255,.72);

  font-size: clamp(10px, .78vw, 12px);  
  line-height: 1.2;  
  letter-spacing: .025em;  
}

/\* \============================================================  
   16 — FINAL FEEDBACK  
   \============================================================ \*/

.ny-feel-power {  
  position: relative;

  width: min(1200px, calc(100% \- 30px));

  margin: clamp(72px, 9vw, 120px) auto 0;

  padding:  
    clamp(42px, 5vw, 72px)  
    clamp(20px, 5vw, 70px);

  overflow: hidden;

  border-radius: 32px;

  text-align: center;

  background:  
    radial-gradient(  
      circle at 50% \-15%,  
      rgba(180,100,255,.32),  
      transparent 50%  
    ),  
    radial-gradient(  
      circle at 10% 100%,  
      rgba(92,34,173,.19),  
      transparent 42%  
    ),  
    linear-gradient(  
      145deg,  
      \#18101f,  
      \#08070b 65%,  
      \#11091a  
    );

  border: 1px solid rgba(220,188,255,.26);

  box-shadow:  
    0 25px 90px rgba(0,0,0,.57),  
    0 0 100px rgba(112,44,207,.14),  
    inset 0 1px 0 rgba(255,255,255,.09);  
}

.ny-feel-power::before {  
  content: "";

  position: absolute;

  top: 0;  
  left: 9%;

  width: 82%;  
  height: 2px;

  background:  
    linear-gradient(  
      90deg,  
      transparent,  
      rgba(240,220,255,.96),  
      rgba(166,86,255,.95),  
      rgba(240,220,255,.96),  
      transparent  
    );

  box-shadow:  
    0 0 20px rgba(169,91,255,.50);  
}

.ny-feel-eyebrow {  
  color: rgba(215,181,255,.95);

  font-size: clamp(10px, .9vw, 13px);  
  font-weight: 900;  
  letter-spacing: .25em;  
  text-transform: uppercase;  
}

.ny-feel-title {  
  margin: 13px auto 0;

  color: \#fff;

  font-size: clamp(32px, 4.5vw, 61px);  
  line-height: 1.01;  
  font-weight: 900;  
  letter-spacing: \-.05em;

  text-shadow:  
    0 4px 30px rgba(0,0,0,.76),  
    0 0 48px rgba(158,75,255,.22);  
}

.ny-feel-subtitle {  
  max-width: 720px;

  margin: 17px auto 0;

  color: rgba(229,204,255,.92);

  font-size: clamp(16px, 1.45vw, 21px);  
  line-height: 1.35;  
  font-weight: 700;  
}

.ny-feel-copy {  
  max-width: 740px;

  margin: 19px auto 0;

  color: rgba(255,255,255,.72);

  font-size: clamp(13px, 1vw, 16px);  
  line-height: 1.66;  
}

.ny-feel-question {  
  margin: 29px auto 0;

  color: rgba(255,255,255,.94);

  font-size: clamp(15px, 1.15vw, 18px);  
  line-height: 1.5;  
  font-weight: 700;  
}

/\* \============================================================  
   17 — FINAL DAY JEWELS  
   \============================================================ \*/

.ny-feel-days {  
  max-width: 950px;

  margin: 30px auto 0;

  display: grid;  
  grid-template-columns: repeat(5, 1fr);

  gap: 11px;  
}

.ny-feel-day {  
  \--feel: \#a15cff;  
  \--feel-rgb: 161,92,255;

  position: relative;

  min-height: 118px;

  padding: 16px 9px;

  display: flex;  
  flex-direction: column;  
  align-items: center;  
  justify-content: center;

  overflow: hidden;

  border-radius: 19px;

  background:  
    radial-gradient(  
      circle at 50% 0%,  
      rgba(var(--feel-rgb), .18),  
      transparent 68%  
    ),  
    linear-gradient(  
      145deg,  
      rgba(255,255,255,.075),  
      rgba(255,255,255,.018)  
    );

  border: 1px solid rgba(var(--feel-rgb), .40);

  color: \#fff;  
  text-decoration: none;

  box-shadow:  
    inset 0 1px 0 rgba(255,255,255,.065),  
    0 10px 29px rgba(0,0,0,.27),  
    0 0 24px rgba(var(--feel-rgb), .08);

  transition:  
    transform .22s ease,  
    border-color .22s ease,  
    box-shadow .22s ease,  
    filter .22s ease;  
}

.ny-feel-day::before {  
  content: "";

  position: absolute;

  top: 0;  
  left: 12%;  
  width: 76%;  
  height: 1px;

  background:  
    linear-gradient(  
      90deg,  
      transparent,  
      var(--feel),  
      transparent  
    );

  box-shadow:  
    0 0 13px var(--feel);  
}

.ny-feel-day:hover {  
  transform: translateY(-6px);

  border-color: rgba(var(--feel-rgb), .76);

  box-shadow:  
    0 17px 38px rgba(0,0,0,.37),  
    0 0 35px rgba(var(--feel-rgb), .20),  
    inset 0 1px 0 rgba(255,255,255,.10);

  filter: brightness(1.08);  
}

.ny-feel-day-number {  
  color: var(--feel);

  font-size: 12px;  
  font-weight: 900;  
  letter-spacing: .18em;

  text-shadow:  
    0 0 14px rgba(var(--feel-rgb), .40);  
}

.ny-feel-day-question {  
  margin-top: 9px;

  color: \#fff;

  font-size: clamp(12px, .88vw, 14px);  
  line-height: 1.25;  
  font-weight: 800;  
}

.ny-feel-footer {  
  margin-top: 13px;

  color: rgba(255,255,255,.46);

  font-size: 11px;  
  line-height: 1.5;  
}

/\* \============================================================  
   18 — COLOR SPECTRUM  
   \============================================================ \*/

/\* DAY 1 — MAGENTA \*/

.ny-jewel-panel\[data-day="1"\] {  
  \--board-accent: \#ff3eb5;  
  \--board-accent-soft: rgba(255,62,181,.18);  
  \--board-accent-bright: \#ff8ad5;  
}

.ny-jewel-panel\[data-day="1"\] .ny-jewel-point:nth-child(1),  
.ny-feel-day:nth-child(1) {  
  \--jewel: \#ff3eb5;  
  \--jewel-rgb: 255,62,181;  
  \--feel: \#ff3eb5;  
  \--feel-rgb: 255,62,181;  
}

.ny-jewel-panel\[data-day="1"\] .ny-jewel-point:nth-child(2) {  
  \--jewel: \#d94bdc;  
  \--jewel-rgb: 217,75,220;  
}

.ny-jewel-panel\[data-day="1"\] .ny-jewel-point:nth-child(3) {  
  \--jewel: \#b04fff;  
  \--jewel-rgb: 176,79,255;  
}

.ny-jewel-panel\[data-day="1"\] .ny-jewel-point:nth-child(4) {  
  \--jewel: \#7e62ff;  
  \--jewel-rgb: 126,98,255;  
}

.ny-jewel-panel\[data-day="1"\] .ny-jewel-point:nth-child(5) {  
  \--jewel: \#5c8dff;  
  \--jewel-rgb: 92,141,255;  
}

/\* DAY 2 — INDIGO \*/

.ny-jewel-panel\[data-day="2"\] {  
  \--board-accent: \#725cff;  
  \--board-accent-soft: rgba(114,92,255,.18);  
  \--board-accent-bright: \#aaa0ff;  
}

.ny-jewel-panel\[data-day="2"\] .ny-jewel-point:nth-child(1) {  
  \--jewel: \#9a62ff;  
  \--jewel-rgb: 154,98,255;  
}

.ny-jewel-panel\[data-day="2"\] .ny-jewel-point:nth-child(2) {  
  \--jewel: \#725cff;  
  \--jewel-rgb: 114,92,255;  
}

.ny-jewel-panel\[data-day="2"\] .ny-jewel-point:nth-child(3) {  
  \--jewel: \#536fff;  
  \--jewel-rgb: 83,111,255;  
}

.ny-jewel-panel\[data-day="2"\] .ny-jewel-point:nth-child(4) {  
  \--jewel: \#428cff;  
  \--jewel-rgb: 66,140,255;  
}

.ny-jewel-panel\[data-day="2"\] .ny-jewel-point:nth-child(5) {  
  \--jewel: \#43a9ff;  
  \--jewel-rgb: 67,169,255;  
}

/\* DAY 3 — SAPPHIRE \*/

.ny-jewel-panel\[data-day="3"\] {  
  \--board-accent: \#24a9ff;  
  \--board-accent-soft: rgba(36,169,255,.18);  
  \--board-accent-bright: \#86d5ff;  
}

.ny-jewel-panel\[data-day="3"\] .ny-jewel-point:nth-child(1) {  
  \--jewel: \#37b8ff;  
  \--jewel-rgb: 55,184,255;  
}

.ny-jewel-panel\[data-day="3"\] .ny-jewel-point:nth-child(2) {  
  \--jewel: \#238fff;  
  \--jewel-rgb: 35,143,255;  
}

.ny-jewel-panel\[data-day="3"\] .ny-jewel-point:nth-child(3) {  
  \--jewel: \#3f70ff;  
  \--jewel-rgb: 63,112,255;  
}

.ny-jewel-panel\[data-day="3"\] .ny-jewel-point:nth-child(4) {  
  \--jewel: \#5860ff;  
  \--jewel-rgb: 88,96,255;  
}

.ny-jewel-panel\[data-day="3"\] .ny-jewel-point:nth-child(5) {  
  \--jewel: \#7654ff;  
  \--jewel-rgb: 118,84,255;  
}

/\* DAY 4 — GREEN \*/

.ny-jewel-panel\[data-day="4"\] {  
  \--board-accent: \#35d98b;  
  \--board-accent-soft: rgba(53,217,139,.16);  
  \--board-accent-bright: \#8ff5bf;  
}

.ny-jewel-panel\[data-day="4"\] .ny-jewel-point:nth-child(1) {  
  \--jewel: \#48e3a0;  
  \--jewel-rgb: 72,227,160;  
}

.ny-jewel-panel\[data-day="4"\] .ny-jewel-point:nth-child(2) {  
  \--jewel: \#35d98b;  
  \--jewel-rgb: 53,217,139;  
}

.ny-jewel-panel\[data-day="4"\] .ny-jewel-point:nth-child(3) {  
  \--jewel: \#63d95e;  
  \--jewel-rgb: 99,217,94;  
}

.ny-jewel-panel\[data-day="4"\] .ny-jewel-point:nth-child(4) {  
  \--jewel: \#a6dc45;  
  \--jewel-rgb: 166,220,69;  
}

.ny-jewel-panel\[data-day="4"\] .ny-jewel-point:nth-child(5) {  
  \--jewel: \#d0e343;  
  \--jewel-rgb: 208,227,67;  
}

/\* DAY 5 — GOLD \*/

.ny-jewel-panel\[data-day="5"\] {  
  \--board-accent: \#f2bd45;  
  \--board-accent-soft: rgba(242,189,69,.16);  
  \--board-accent-bright: \#ffe39a;  
}

.ny-jewel-panel\[data-day="5"\] .ny-jewel-point:nth-child(1) {  
  \--jewel: \#ffd15a;  
  \--jewel-rgb: 255,209,90;  
}

.ny-jewel-panel\[data-day="5"\] .ny-jewel-point:nth-child(2) {  
  \--jewel: \#f2bd45;  
  \--jewel-rgb: 242,189,69;  
}

.ny-jewel-panel\[data-day="5"\] .ny-jewel-point:nth-child(3) {  
  \--jewel: \#f5a83c;  
  \--jewel-rgb: 245,168,60;  
}

.ny-jewel-panel\[data-day="5"\] .ny-jewel-point:nth-child(4) {  
  \--jewel: \#e98c39;  
  \--jewel-rgb: 233,140,57;  
}

.ny-jewel-panel\[data-day="5"\] .ny-jewel-point:nth-child(5) {  
  \--jewel: \#ffdf78;  
  \--jewel-rgb: 255,223,120;  
}

/\* \============================================================  
   19 — FINAL FEEDBACK SPECTRUM  
   \============================================================ \*/

.ny-feel-day:nth-child(1) {  
  \--feel: \#ff3eb5;  
  \--feel-rgb: 255,62,181;  
}

.ny-feel-day:nth-child(2) {  
  \--feel: \#725cff;  
  \--feel-rgb: 114,92,255;  
}

.ny-feel-day:nth-child(3) {  
  \--feel: \#24a9ff;  
  \--feel-rgb: 36,169,255;  
}

.ny-feel-day:nth-child(4) {  
  \--feel: \#35d98b;  
  \--feel-rgb: 53,217,139;  
}

.ny-feel-day:nth-child(5) {  
  \--feel: \#f2bd45;  
  \--feel-rgb: 242,189,69;  
}

/\* \============================================================  
   20 — RESPONSIVE  
   \============================================================ \*/

@media (max-width: 1050px) {

  .ny-jewel-points {  
    grid-template-columns: repeat(3, 1fr);  
  }

  .ny-jewel-point:last-child {  
    grid-column: auto;  
  }

  .ny-feel-days {  
    grid-template-columns: repeat(3, 1fr);  
  }

}

@media (max-width: 760px) {

  .ny-jewel-points {  
    grid-template-columns: repeat(2, 1fr);  
  }

  .ny-feel-days {  
    grid-template-columns: repeat(2, 1fr);  
  }

  .ny-jewel-point {  
    min-height: 175px;  
  }

}

@media (max-width: 600px) {

  .ny-academy-experience {  
    padding-top: 24px;  
  }

  .ny-academy-intro,  
  .ny-academy-lesson-header {  
    width: calc(100% \- 18px);  
  }

  .ny-academy-video-shell {  
    width: calc(100% \- 18px);  
    border-radius: 15px;  
  }

  .ny-academy-video {  
    border-radius: 13px;  
  }

  .ny-jewel-panel {  
    width: calc(100% \- 18px);  
    padding: 27px 15px;  
    border-radius: 23px;  
  }

  .ny-jewel-points {  
    grid-template-columns: 1fr;  
    gap: 10px;  
  }

  .ny-jewel-point {  
    min-height: 0;  
    padding: 20px 18px;  
  }

  .ny-jewel-point-text {  
    max-width: 310px;  
  }

  .ny-academy-cta {  
    width: calc(100% \- 18px);  
  }

  .ny-academy-cta-content {  
    padding: 12px 15px;  
  }

  .ny-academy-cta-icon {  
    width: 43px;  
    height: 43px;  
  }

  .ny-feel-power {  
    width: calc(100% \- 18px);  
    padding: 39px 15px;  
    border-radius: 25px;  
  }

  .ny-feel-days {  
    grid-template-columns: 1fr;  
  }

  .ny-feel-day {  
    min-height: 72px;  
    flex-direction: row;  
    justify-content: flex-start;  
    gap: 15px;  
    padding: 13px 18px;  
    text-align: left;  
  }

}

/\* \============================================================  
   21 — REDUCED MOTION  
   \============================================================ \*/

@media (prefers-reduced-motion: reduce) {

  .ny-jewel-point,  
  .ny-academy-cta,  
  .ny-feel-day {  
    transition: none \!important;  
  }

  .ny-jewel-point:hover,  
  .ny-academy-cta:hover,  
  .ny-feel-day:hover {  
    transform: none \!important;  
    filter: none \!important;  
  }

}

\</style\>

\<script\>  
(function () {

  "use strict";

  /\* \==========================================================  
     CANONICAL CHECKOUT  
     \========================================================== \*/

  const CHECKOUT\_URL \=  
    "https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab";

  /\* \==========================================================  
     FEATURE VIDEO  
     \========================================================== \*/

  const FEATURE\_VIDEO\_ID \= "wnjvDqEhBCY";

  /\* \==========================================================  
     FIVE-DAY ACADEMY DATA  
     \========================================================== \*/

  const LESSONS \= \[

    {  
      day: "DAY 1",  
      dayNumber: "1",  
      title: "ACTIVATE / EXPERIENCE",  
      video: "ZRIfvxCsYWY",

      summary:  
        "Meet Naya. Activate the relationship. Feel the difference immediately by letting Naya understand who you are, what matters to you, and where you want to go.",

      points: \[  
        \["01","MEET NAYA","Begin a relationship instead of another disconnected AI conversation."\],  
        \["02","BE UNDERSTOOD","Give Naya your identity, story, goals, priorities and direction."\],  
        \["03","SOLVE THE FIVE","See how Naya addresses directive, consistency, overwhelm, context and quality problems."\],  
        \["04","CAPTURE WHAT MATTERS","Begin making human and Naya notes so important experience is not lost."\],  
        \["05","FIRST PROOF","End the day with your Daily Intelligence Briefing and experience intelligence beginning to compound."\]  
      \],

      nutshell:  
        "Day 1 is about becoming known — and discovering what changes when AI starts with you."  
    },

    {  
      day: "DAY 2",  
      dayNumber: "2",  
      title: "REMEMBER / COMPOUND",  
      video: "j0YwJsC6Q4Y",

      summary:  
        "Stop starting over. Turn useful experience into intelligence that can be remembered, retrieved, reviewed and carried forward.",

      points: \[  
        \["01","SMART NOTES","Capture the moments, lessons, decisions and breakthroughs actually worth remembering."\],  
        \["02","CONTEXT","Preserve the information that helps future conversations start further ahead."\],  
        \["03","RETRIEVE","Turn past experience into something useful instead of something forgotten."\],  
        \["04","REVIEW","Use daily, weekly, monthly and longer-term reviews to see what changed."\],  
        \["05","COMPOUND","Build a personal intelligence savings account where useful experience becomes more valuable over time."\]  
      \],

      nutshell:  
        "Day 2 changes the relationship from conversations that end to intelligence that carries forward."  
    },

    {  
      day: "DAY 3",  
      dayNumber: "3",  
      title: "LEARN / MASTER",  
      video: "PtYW43cIZng",

      summary:  
        "Learn meaningful AI and Human Maximus subjects with Naya, then prove what you know and discover exactly where you can improve.",

      points: \[  
        \["01","CHOOSE","Select a meaningful AI or Human Maximus subject worth mastering."\],  
        \["02","LEARN","Ask Naya to teach, explain, explore and build the subject with you."\],  
        \["03","TEST","Use MAXIS to measure where your understanding actually is."\],  
        \["04","IMPROVE","Discover gaps, learn more and return without judgment."\],  
        \["05","MASTER","Retest your knowledge and watch your capability develop through evidence."\]  
      \],

      nutshell:  
        "Day 3 turns AI from an answer machine into a learning and mastery partner."  
    },

    {  
      day: "DAY 4",  
      dayNumber: "4",  
      title: "CREATE / EXECUTE",  
      video: "3c0q\_NjM3i8",

      summary:  
        "Turn intelligence into extraordinary work. Think with Naya, create with Naya, review with Naya, score it, improve it and execute.",

      points: \[  
        \["01","THINK","Use Naya to clarify ideas, problems, strategy and direction."\],  
        \["02","CREATE","Write, plan, research, design, analyze, organize and build."\],  
        \["03","REVIEW","Ask Naya to challenge the work instead of simply accepting the first result."\],  
        \["04","SCORE","Define what excellent looks like and identify the gaps."\],  
        \["05","EXECUTE","Move from idea to finished result through deliberate improvement."\]  
      \],

      nutshell:  
        "Day 4 is where intelligence becomes action — and better action becomes better results."  
    },

    {  
      day: "DAY 5",  
      dayNumber: "5",  
      title: "BECOME / COMPOUND",  
      video: "T9Pi1BftCZk",

      summary:  
        "This is not simply the end of five lessons. It is the beginning of a new way to operate: learn, remember, create, reflect, improve and compound.",

      points: \[  
        \["01","PERSONALIZE","Naya becomes increasingly useful because the relationship carries context."\],  
        \["02","REMEMBER","Your valuable experiences remain available instead of disappearing."\],  
        \["03","LEARN","Lessons and assessments create a path for continuous development."\],  
        \["04","CREATE","Your intelligence becomes a practical force for better work and better decisions."\],  
        \["05","COMPOUND","The value grows because every meaningful day can become part of the next."\]  
      \],

      nutshell:  
        "Day 5 reveals the bigger idea — Naya Power is not a five-day course. It is a new way to operate."  
    }

  \];

  /\* \==========================================================  
     PREVENT DUPLICATE ACADEMY  
     \========================================================== \*/

  if (  
    document.querySelector(".ny-academy-experience")  
  ) {  
    return;  
  }

  /\* \==========================================================  
     FEATURE PLAYER  
     ONLY MODIFY AN EXISTING NON-ACADEMY IFRAME  
     \========================================================== \*/

  const existingIframes \=  
    Array.from(document.querySelectorAll("iframe"));

  let featureIframe \=  
    existingIframes.find(function (iframe) {

      const src \=  
        (iframe.getAttribute("src") \|\| "").toLowerCase();

      const title \=  
        (iframe.getAttribute("title") \|\| "").toLowerCase();

      return (  
        src.includes("youtube.com/embed") \|\|  
        src.includes("youtube-nocookie.com/embed") \|\|  
        title.includes("welcome") \|\|  
        title.includes("ai mastery") \|\|  
        title.includes("human empowerment")  
      );

    });

  if (featureIframe) {

    featureIframe.src \=  
      "https\://www\.youtube-nocookie.com/embed/" \+  
      FEATURE\_VIDEO\_ID \+  
      "?rel=0\&modestbranding=1\&playsinline=1\&vq=hd1080";

    featureIframe.setAttribute(  
      "title",  
      "Naya Power — Meet Naya. Experience the Future."  
    );

    featureIframe.setAttribute(  
      "allow",  
      "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen"  
    );

    featureIframe.setAttribute(  
      "allowfullscreen",  
      ""  
    );

    featureIframe.setAttribute(  
      "loading",  
      "eager"  
    );

    featureIframe.setAttribute(  
      "referrerpolicy",  
      "strict-origin-when-cross-origin"  
    );

  }

  /\* \==========================================================  
     ACADEMY ROOT  
     \========================================================== \*/

  const academy \=  
    document.createElement("section");

  academy.className \=  
    "ny-academy-experience";

  academy.setAttribute(  
    "aria-label",  
    "Naya Power Academy Five-Day Experience"  
  );

  /\* \==========================================================  
     INTRO  
     \========================================================== \*/

  academy.innerHTML \=

    '\<div class="ny-academy-intro"\>' \+

      '\<div class="ny-academy-eyebrow"\>' \+  
        "NAYA POWER ACADEMY" \+  
      "\</div\>" \+

      '\<h2 class="ny-academy-title"\>' \+  
        "Five Days. Five Experiences. One New Way to Operate." \+  
        '\<span\>See what you will experience inside Naya Power.\</span\>' \+  
      "\</h2\>" \+

      '\<div class="ny-academy-intro-copy"\>' \+  
        "This is not about watching five videos and learning another AI tool. " \+  
        "It is about experiencing what happens when AI becomes more personal, " \+  
        "more consistent, more memorable, more capable and more useful over time." \+  
      "\</div\>" \+

    "\</div\>" \+

    '\<div class="ny-academy-lessons"\>\</div\>';

  const lessonStack \=  
    academy.querySelector(  
      ".ny-academy-lessons"  
    );

  /\* \==========================================================  
     BUILD FIVE LESSONS  
     \========================================================== \*/

  LESSONS.forEach(function (lesson, lessonIndex) {

    const article \=  
      document.createElement("article");

    article.className \=  
      "ny-academy-lesson";

    const pointsHTML \=  
      lesson.points  
        .map(function (point) {

          return (

            '\<div class="ny-jewel-point"\>' \+

              '\<div class="ny-jewel-icon" aria-hidden="true"\>' \+  
                '\<span\>' \+  
                  point\[0\] \+  
                '\</span\>' \+  
              "\</div\>" \+

              '\<div class="ny-jewel-point-title"\>' \+  
                point\[1\] \+  
              "\</div\>" \+

              '\<div class="ny-jewel-point-text"\>' \+  
                point\[2\] \+  
              "\</div\>" \+

            "\</div\>"

          );

        })  
        .join("");

    article.innerHTML \=

      '\<div class="ny-academy-lesson-header"\>' \+

        '\<div class="ny-academy-day"\>' \+  
          lesson.day \+  
        "\</div\>" \+

        '\<h3 class="ny-academy-lesson-title"\>' \+  
          lesson.title \+  
        "\</h3\>" \+

      "\</div\>" \+

      '\<div class="ny-academy-video-shell"\>' \+

        '\<div class="ny-academy-video"\>' \+

          '\<iframe ' \+  
            'src="https\://www\.youtube-nocookie.com/embed/' \+  
              lesson.video \+  
              '?rel=0\&modestbranding=1\&playsinline=1\&vq=hd1080" ' \+  
            'title="' \+  
              lesson.day \+  
              " — " \+  
              lesson.title \+  
            '" ' \+  
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" ' \+  
            'allowfullscreen ' \+  
            'loading="' \+  
              (lessonIndex \=== 0 ? "eager" : "lazy") \+  
            '" ' \+  
            'referrerpolicy="strict-origin-when-cross-origin"\>' \+  
          "\</iframe\>" \+

        "\</div\>" \+

      "\</div\>" \+

      '\<div class="ny-jewel-panel" data-day="' \+  
        lesson.dayNumber \+  
      '"\>' \+

        '\<div class="ny-jewel-kicker"\>' \+  
          "IN A NUTSHELL" \+  
        "\</div\>" \+

        '\<div class="ny-jewel-title"\>' \+  
          lesson.title \+  
        "\</div\>" \+

        '\<div class="ny-jewel-summary"\>' \+  
          lesson.summary \+  
        "\</div\>" \+

        '\<div class="ny-jewel-points"\>' \+  
          pointsHTML \+  
        "\</div\>" \+

        '\<div class="ny-nutshell-line"\>' \+

          '\<div class="ny-nutshell-line-label"\>' \+  
            "THE BIG IDEA" \+  
          "\</div\>" \+

          '\<div class="ny-nutshell-line-text"\>' \+  
            lesson.nutshell \+  
          "\</div\>" \+

        "\</div\>" \+

      "\</div\>" \+

      '\<a class="ny-academy-cta" ' \+  
        'href="' \+ CHECKOUT\_URL \+ '" ' \+  
        'aria-label="Start ' \+  
          lesson.day \+  
          ' — ' \+  
          lesson.title \+  
        '"\>' \+

        '\<span class="ny-academy-cta-content"\>' \+

          '\<span class="ny-academy-cta-icon" aria-hidden="true"\>' \+  
            "★" \+  
          "\</span\>" \+

          '\<span class="ny-academy-cta-copy"\>' \+

            '\<span class="ny-academy-cta-title"\>' \+  
              "Start " \+  
              lesson.day \+  
              " — " \+  
              lesson.title \+  
            "\</span\>" \+

            '\<span class="ny-academy-cta-sub"\>' \+  
              "Experience Naya Power — Five Days. Zero Risk." \+  
            "\</span\>" \+

          "\</span\>" \+

        "\</span\>" \+

      "\</a\>";

    lessonStack.appendChild(article);

  });

  /\* \==========================================================  
     FINAL FEEDBACK EXPERIENCE  
     \========================================================== \*/

  const feedback \=  
    document.createElement("section");

  feedback.className \=  
    "ny-feel-power";

  feedback.setAttribute(  
    "aria-label",  
    "Which day did you feel Naya Power?"  
  );

  feedback.innerHTML \=

    '\<div class="ny-feel-eyebrow"\>' \+  
      "ONE LAST FAVOR" \+  
    "\</div\>" \+

    '\<h2 class="ny-feel-title"\>' \+  
      "Which Day Did You Feel Naya Power?" \+  
    "\</h2\>" \+

    '\<div class="ny-feel-subtitle"\>' \+  
      "Was there a moment when it just clicked?" \+  
    "\</div\>" \+

    '\<div class="ny-feel-copy"\>' \+  
      "Maybe it was the first conversation. Maybe it was the moment " \+  
      "Naya remembered something that mattered. Maybe it was your " \+  
      "Daily Intelligence Briefing — or the realization that you could " \+  
      "learn, create and improve with her beside you." \+  
    "\</div\>" \+

    '\<div class="ny-feel-question"\>' \+  
      "Tell us where you felt the power." \+  
    "\</div\>" \+

    '\<div class="ny-feel-days"\>' \+

      \[1,2,3,4,5\]  
        .map(function (day) {

          return (

            '\<a class="ny-feel-day" ' \+  
              'href="' \+ CHECKOUT\_URL \+ '" ' \+  
              'aria-label="I felt Naya Power on Day ' \+  
                day \+  
              '"\>' \+

              '\<span class="ny-feel-day-number"\>' \+  
                "DAY " \+  
                day \+  
              "\</span\>" \+

              '\<span class="ny-feel-day-question"\>' \+  
                "I felt it here." \+  
              "\</span\>" \+

            "\</a\>"

          );

        })  
        .join("") \+

    "\</div\>" \+

    '\<div class="ny-feel-footer"\>' \+  
      "Your answer helps us understand where the experience becomes real." \+  
    "\</div\>";

  academy.appendChild(feedback);

  /\* \==========================================================  
     INSERT — NEVER REPLACE THE EXISTING PAGE  
     \========================================================== \*/

  const existingPage \=  
    document.querySelector(  
      ".ny-page-inner"  
    );

  if (existingPage) {

    existingPage.appendChild(  
      academy  
    );

  } else {

    document.body.appendChild(  
      academy  
    );

  }

  /\* \==========================================================  
     CTA ENFORCEMENT  
     \========================================================== \*/

  academy  
    .querySelectorAll(  
      ".ny-academy-cta, .ny-feel-day"  
    )  
    .forEach(function (link) {

      link.href \=  
        CHECKOUT\_URL;

    });

})();  
\</script\>  
\<\!-- \============================================================  
🔱 NAYAPOWER — FINAL CTA / NAVIGATION OVERRIDE  
\============================================================

SAFE PATCH ONLY.

DO NOT:  
• rebuild the page  
• replace the Academy  
• replace videos  
• replace jewel boards  
• modify layout  
• modify styling

THIS PATCH ONLY:  
• redirects selected existing buttons  
• changes Free Gifts → Start Here  
• sends selected Academy-entry buttons to the canonical checkout

CANONICAL FREE-TRIAL DESTINATION:  
Human Maximus Codex / Naya POWER Academy  
\============================================================ \--\>

\<script\>  
(function () {

  "use strict";

  /\* \==========================================================  
     CANONICAL FREE-TRIAL / ACADEMY CHECKOUT  
     \========================================================== \*/

  const NAYA\_POWER\_CHECKOUT \=  
    "https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab";

  /\* \==========================================================  
     TEXT NORMALIZATION  
     \========================================================== \*/

  function normalize(text) {

    return (text \|\| "")  
      .replace(/\\s+/g, " ")  
      .trim()  
      .toLowerCase();

  }

  /\* \==========================================================  
     GET ALL LINKS  
     \========================================================== \*/

  const links \=  
    Array.from(  
      document.querySelectorAll("a")  
    );

  /\* \==========================================================  
     MATCH A LINK BY ITS VISIBLE TEXT  
     \========================================================== \*/

  function findLinkByText(matchers) {

    return links.find(function (link) {

      const text \=  
        normalize(link.textContent);

      return matchers.some(function (matcher) {

        return text \=== normalize(matcher) \|\|  
               text.includes(normalize(matcher));

      });

    });

  }

  /\* \==========================================================  
     APPLY CHECKOUT DESTINATION  
     \========================================================== \*/

  function sendToCheckout(link, newLabel) {

    if (\!link) {  
      return;  
    }

    link.href \=  
      NAYA\_POWER\_CHECKOUT;

    link.setAttribute(  
      "target",  
      "\_self"  
    );

    link.removeAttribute(  
      "target"  
    );

    link.setAttribute(  
      "aria-label",  
      newLabel \+ " — Start Naya Power Free Trial"  
    );

    if (newLabel) {

      /\*  
       \* Only change the visible text when the link is the  
       \* known navigation/portal button.  
       \*  
       \* Preserve nested visual elements when possible.  
       \*/

      const title \=  
        link.querySelector(  
          ".ny-title"  
        );

      if (title) {

        title.textContent \=  
          newLabel;

      } else {

        /\*  
         \* If there is no known title element, preserve  
         \* the existing internal structure whenever possible.  
         \*/

        const textNodes \= \[\];

        const walker \=  
          document.createTreeWalker(  
            link,  
            NodeFilter.SHOW\_TEXT  
          );

        let node;

        while (  
          (node \= walker.nextNode())  
        ) {

          if (  
            node.nodeValue &&  
            node.nodeValue.trim()  
          ) {  
            textNodes.push(node);  
          }

        }

        /\*  
         \* Replace the first meaningful text node only.  
         \* This avoids destroying icons or other markup.  
         \*/

        if (textNodes.length) {

          textNodes\[0\].nodeValue \=  
            newLabel;

        }

      }

    }

  }

  /\* \==========================================================  
     01 — FREE GIFTS  
       
     The old "Free Gifts" portal becomes:  
     START HERE  
     \========================================================== \*/

  const freeGifts \=  
    findLinkByText(\[  
      "Free Gifts",  
      "Free Gifts →",  
      "Free Gifts ›"  
    \]);

  sendToCheckout(  
    freeGifts,  
    "Start Here"  
  );

  /\* \==========================================================  
     02 — TAKE YOUR POWER BACK  
     \========================================================== \*/

  const takeYourPowerBack \=  
    findLinkByText(\[  
      "Take Your Power Back",  
      "Take Your Power Back →",  
      "Take Your Power Back ›"  
    \]);

  sendToCheckout(  
    takeYourPowerBack,  
    "Take Your Power Back"  
  );

  /\* \==========================================================  
     03 — AI MASTERCLASS  
       
     IMPORTANT:  
     The AI Masterclass button remains named AI Masterclass.  
     Only its destination changes.  
     \========================================================== \*/

  const aiMasterclass \=  
    findLinkByText(\[  
      "AI Masterclass",  
      "AI Masterclass →",  
      "AI Masterclass ›"  
    \]);

  sendToCheckout(  
    aiMasterclass,  
    "AI Masterclass"  
  );

  /\* \==========================================================  
     04 — PRO MAX PLAYER  
     \========================================================== \*/

  const proMaxPlayer \=  
    findLinkByText(\[  
      "ProMax Player",  
      "Pro Max Player",  
      "ProMAX Player",  
      "ProMax Player →",  
      "Pro Max Player →"  
    \]);

  sendToCheckout(  
    proMaxPlayer,  
    "ProMax Player"  
  );

  /\* \==========================================================  
     05 — EXISTING START / FREE TRIAL CTA  
       
     Catch common labels that may currently point to Services.  
     \========================================================== \*/

  const startCandidates \=  
    links.filter(function (link) {

      const text \=  
        normalize(link.textContent);

      return (  
        text.includes("free trial") \|\|  
        text \=== "start here" \|\|  
        text.includes("start your free") \|\|  
        text.includes("experience naya power")  
      );

    });

  startCandidates.forEach(function (link) {

    /\*  
     \* Do not touch the lesson CTAs or feedback buttons.  
     \* Those already use the correct checkout through the  
     \* Academy layer.  
     \*/

    if (  
      link.classList.contains("ny-academy-cta") \|\|  
      link.classList.contains("ny-feel-day")  
    ) {  
      return;  
    }

    link.href \=  
      NAYA\_POWER\_CHECKOUT;

    link.setAttribute(  
      "target",  
      "\_self"  
    );

    link.removeAttribute(  
      "target"  
    );

  });

  /\* \==========================================================  
     06 — EXISTING SECONDARY GRID SAFETY NET  
       
     If the portal system uses the known Naya secondary  
     classes, explicitly enforce the first four destinations.

     This is deliberately narrow.  
     \========================================================== \*/

  const secondaryButtons \=  
    Array.from(  
      document.querySelectorAll(  
        ".ny-secondary-grid .ny-secondary"  
      )  
    );

  if (secondaryButtons.length) {

    secondaryButtons.forEach(function (button) {

      const text \=  
        normalize(button.textContent);

      /\* Free Gifts → Start Here \*/

      if (  
        text.includes("free gifts")  
      ) {

        button.href \=  
          NAYA\_POWER\_CHECKOUT;

        const title \=  
          button.querySelector(".ny-title");

        if (title) {  
          title.textContent \=  
            "Start Here";  
        }

        button.setAttribute(  
          "aria-label",  
          "Start Here — Experience Naya Power Free Trial"  
        );

      }

      /\* Take Your Power Back \*/

      else if (  
        text.includes("take your power back")  
      ) {

        button.href \=  
          NAYA\_POWER\_CHECKOUT;

      }

      /\* AI Masterclass \*/

      else if (  
        text.includes("ai masterclass")  
      ) {

        button.href \=  
          NAYA\_POWER\_CHECKOUT;

      }

      /\* ProMax Player \*/

      else if (  
        text.includes("promax player") \|\|  
        text.includes("pro max player")  
      ) {

        button.href \=  
          NAYA\_POWER\_CHECKOUT;

      }

    });

  }

  /\* \==========================================================  
     07 — FINAL CANONICALITY PASS  
       
     Prevent accidental Services-page routing on the known  
     Academy-entry buttons.  
     \========================================================== \*/

  \[  
    freeGifts,  
    takeYourPowerBack,  
    aiMasterclass,  
    proMaxPlayer  
  \].forEach(function (link) {

    if (\!link) {  
      return;  
    }

    link.href \=  
      NAYA\_POWER\_CHECKOUT;

    link.setAttribute(  
      "target",  
      "\_self"  
    );

    link.removeAttribute(  
      "target"  
    );

  });

\<\!doctype html\>

\<html lang="en"\>  
\<head\>  
\<meta charset="utf-8"\>  
\<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"\>  
\<meta name="theme-color" content="\#000000"\>  
\<meta name="color-scheme" content="dark"\>  
\<meta name="maxess-artifact" content="E05-SECTION-05-WORKING"\>  
\<title\>MAXESS — Section 05 · Does Any of This Sound Familiar?\</title\>  
\<style\>  
\#e05{--bg:\#000;--white:\#fff;--soft:rgba(255,255,255,.68);--purple:\#9b62ff;position:relative;width:100%;background:\#000;color:\#fff;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden;isolation:isolate}  
\#e05,\#e05 \*{box-sizing:border-box}  
\#e05 .e05-glow{position:absolute;left:50%;top:0;width:900px;height:700px;transform:translateX(-50%);background:radial-gradient(circle,rgba(155,98,255,.12),transparent 66%);filter:blur(44px);pointer-events:none}  
\#e05 .e05-wrap{position:relative;z-index:2;width:min(1160px,100%);margin:auto;padding:78px 30px 90px}  
\#e05 .e05-head{text-align:center;max-width:820px;margin:0 auto 66px}  
\#e05 .e05-kicker{margin:0 0 17px;font-size:9px;font-weight:900;letter-spacing:.34em;text-transform:uppercase;color:rgba(255,255,255,.58)}  
\#e05 h1{margin:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(42px,6vw,72px);line-height:1;letter-spacing:-.05em}  
\#e05 .e05-intro{max-width:660px;margin:23px auto 0;color:rgba(255,255,255,.7);font-size:15px;line-height:1.72}  
\#e05 .e05-rule{width:90px;height:1px;margin:27px auto 0;background:linear-gradient(90deg,transparent,var(--purple),transparent);box-shadow:0 0 20px rgba(155,98,255,.55)}  
\#e05 .e05-item{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:54px;align-items:center;width:min(1060px,100%);margin:0 auto 86px}  
\#e05 .e05-item.reverse{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}  
\#e05 .e05-item.reverse .e05-visual{order:2}  
\#e05 .e05-item.reverse .e05-copy{order:1}  
\#e05 .e05-visual{position:relative;aspect-ratio:16/9;border:1px solid rgba(255,255,255,.12);border-radius:26px;overflow:hidden;background:\#050505;box-shadow:0 24px 70px rgba(0,0,0,.55),0 0 60px rgba(155,98,255,.08)}  
\#e05 .e05-visual img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.8) contrast(1.06);transition:transform .7s ease}  
\#e05 .e05-item:hover .e05-visual img{transform:scale(1.025)}  
\#e05 .e05-visual::after{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,0,0,.16),rgba(10,0,20,.42)),radial-gradient(circle at 72% 28%,rgba(155,98,255,.24),transparent 40%);pointer-events:none}  
\#e05 .e05-orbit{position:absolute;right:19px;bottom:18px;width:66px;height:66px;border:1px solid rgba(255,255,255,.22);border-radius:50%;box-shadow:0 0 26px rgba(155,98,255,.22);z-index:2}  
\#e05 .e05-orbit:before{content:"";position:absolute;inset:11px;border:1px solid rgba(255,255,255,.15);border-radius:50%}  
\#e05 .e05-orbit:after{content:"";position:absolute;top:0;left:50%;width:6px;height:6px;border-radius:50%;background:\#fff;box-shadow:0 0 12px 4px rgba(155,98,255,.8);transform:translateX(-50%)}  
\#e05 .e05-copy{padding:8px 4px}  
\#e05 .e05-meta{display:flex;align-items:center;gap:12px;margin-bottom:23px}  
\#e05 .e05-face{width:43px;height:43px;border-radius:50%;object-fit:cover;border:1px solid rgba(255,255,255,.28);box-shadow:0 0 22px rgba(155,98,255,.2)}  
\#e05 .e05-naya{font-size:9px;font-weight:900;letter-spacing:.25em;text-transform:uppercase}  
\#e05 .e05-mark{margin-left:auto;width:29px;height:29px;object-fit:contain;opacity:.82}  
\#e05 .e05-index{margin:0 0 9px;color:rgba(255,255,255,.38);font-size:9px;font-weight:900;letter-spacing:.28em;text-transform:uppercase}  
\#e05 .e05-title{margin:0;color:\#fff;font-family:Georgia,"Times New Roman",serif;font-size:clamp(27px,3.2vw,40px);line-height:1.1;letter-spacing:-.035em}  
\#e05 .e05-quote-mark{margin:22px 0 \-7px;color:var(--purple);font-family:Georgia,serif;font-size:70px;line-height:.65;text-shadow:0 0 24px rgba(155,98,255,.35)}  
\#e05 blockquote{margin:0;color:\#fff;font-family:Georgia,"Times New Roman",serif;font-size:clamp(20px,2.25vw,29px);line-height:1.32;letter-spacing:-.02em}  
\#e05 .e05-caption{margin:20px 0 0;padding-left:16px;border-left:1px solid rgba(155,98,255,.78);color:rgba(255,255,255,.66);font-size:12px;line-height:1.72}  
\#e05 .e05-footer{width:min(800px,100%);margin:6px auto 0;padding:38px 0 0;border-top:1px solid rgba(255,255,255,.1);text-align:center}  
\#e05 .e05-footer p{margin:0;color:\#fff;font-family:Georgia,"Times New Roman",serif;font-size:clamp(21px,2.5vw,28px);line-height:1.5;letter-spacing:-.015em}  
\#e05 .e05-footer small{display:block;margin-top:16px;color:rgba(255,255,255,.45);font-size:9px;font-weight:800;letter-spacing:.25em;text-transform:uppercase}  
@media(max-width:760px){\#e05 .e05-wrap{padding:54px 18px 66px}\#e05 .e05-head{margin-bottom:46px}\#e05 .e05-intro{font-size:14px}\#e05 .e05-item,\#e05 .e05-item.reverse{grid-template-columns:1fr;gap:28px;margin-bottom:66px}\#e05 .e05-item.reverse .e05-visual,\#e05 .e05-item.reverse .e05-copy{order:initial}\#e05 .e05-visual{border-radius:21px}\#e05 .e05-copy{padding:0 4px}\#e05 .e05-title{font-size:31px}\#e05 blockquote{font-size:25px}\#e05 .e05-footer p{font-size:21px}}  
@media print{\#e05{background:\#fff\!important;color:\#111\!important;overflow:visible}\#e05 .e05-glow{display:none}\#e05 .e05-wrap{padding:14mm 12mm;background:\#fff\!important}\#e05 .e05-item{break-inside:avoid;page-break-inside:avoid;margin-bottom:18mm}\#e05 h1,\#e05 .e05-title,\#e05 blockquote,\#e05 .e05-footer p{color:\#111}\#e05 .e05-kicker,\#e05 .e05-index,\#e05 .e05-caption,\#e05 .e05-intro,\#e05 .e05-footer small{color:\#444}\#e05 .e05-visual{box-shadow:none;border-color:\#ddd}\#e05 .e05-visual:after{display:none}\#e05 .e05-naya{color:\#111}\#e05 .e05-mark{filter:invert(1)}}  
@media(prefers-reduced-motion:reduce){\#e05 \*{transition:none\!important}}  
\</style\>  
\</head\>  
\<body\>  
\<section id="e05" aria-labelledby="e05-title"\>  
\<div class="e05-glow" aria-hidden="true"\>\</div\>\<div class="e05-wrap"\>  
\<header class="e05-head"\>\<p class="e05-kicker"\>MAXESS · THE AI FRICTION\</p\>\<h1 id="e05-title"\>Does any of this sound familiar?\</h1\>\<p class="e05-intro"\>If you've ever felt that AI should be giving you better results than it is, you're not alone. Here are seven of the most common moments that get in the way.\</p\>\<div class="e05-rule" aria-hidden="true"\>\</div\>\</header\>

\<article class="e05-item"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-black.jpg" alt="Naya" loading="eager"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>01 · The Direction Problem\</p\>\<h2 class="e05-title"\>"It doesn't understand what I mean."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>You know what you want. You explain it to AI… and somehow the answer still isn't what you had in your head.\</blockquote\>\<p class="e05-caption"\>The intelligence is there. The frustration often comes from not yet having a reliable way to translate your intention into direction AI can act on.\</p\>\</div\>\</article\>

\<article class="e05-item reverse"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-2.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>02 · The Consistency Problem\</p\>\<h2 class="e05-title"\>"Sometimes it's amazing. Sometimes it's… not."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>You get one incredible result, and then you try again and wonder why you can't get AI to do it that way consistently.\</blockquote\>\<p class="e05-caption"\>Great results are exciting. Repeatable great results are a system. That's the difference between discovering a trick and developing a method.\</p\>\</div\>\</article\>

\<article class="e05-item"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-4.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>03 · The Overwhelm Problem\</p\>\<h2 class="e05-title"\>"I know AI can do more. I just don't know where to start."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>There are prompts, models, tools, updates, agents, workflows… and suddenly using AI feels like another thing you have to learn.\</blockquote\>\<p class="e05-caption"\>You don't need more noise. You need a clear path that turns a huge possibility into a practical next move.\</p\>\</div\>\</article\>

\<article class="e05-item reverse"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-3.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>04 · The Context Problem\</p\>\<h2 class="e05-title"\>"Why does it keep forgetting?"\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>You already explained all of this. You had the conversation. And somehow you're back at the beginning again.\</blockquote\>\<p class="e05-caption"\>Losing context forces you to repeat yourself and breaks momentum. Better systems preserve what matters so your thinking can keep moving forward.\</p\>\</div\>\</article\>

\<article class="e05-item"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-5.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>05 · The Quality Problem\</p\>\<h2 class="e05-title"\>"It's good… but I know it could be better."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>The answer technically works. The design is almost there. The writing is okay. But something is missing—and you're not quite sure how to get it across the finish line.\</blockquote\>\<p class="e05-caption"\>Exceptional work rarely appears on the first attempt. The missing skill is often knowing how to evaluate, refine, and raise the standard deliberately.\</p\>\</div\>\</article\>

\<article class="e05-item reverse"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-7.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>06 · The "Start Over" Problem\</p\>\<h2 class="e05-title"\>"I keep having to start over."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>You spend time getting somewhere useful, then the thread changes, the context disappears, or the next session doesn't know what happened before.\</blockquote\>\<p class="e05-caption"\>Starting over costs more than time. It breaks continuity. A better AI workflow lets your work accumulate instead of constantly resetting.\</p\>\</div\>\</article\>

\<article class="e05-item"\>\<div class="e05-visual"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-6.jpg" alt="Naya" loading="lazy"\>\<div class="e05-orbit" aria-hidden="true"\>\</div\>\</div\>\<div class="e05-copy"\>\<div class="e05-meta"\>\<img class="e05-face" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-profile-black-face-zoom.jpg" alt="Naya"\>\<span class="e05-naya"\>Naya\</span\>\<img class="e05-mark" src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/icon-logo.png" alt="MAXESS"\>\</div\>\<p class="e05-index"\>07 · The "I Know There's More" Problem\</p\>\<h2 class="e05-title"\>"I know I'm only scratching the surface."\</h2\>\<div class="e05-quote-mark" aria-hidden="true"\>"\</div\>\<blockquote\>You can feel that AI is capable of something much bigger—but you haven't yet found the method that lets you consistently unlock it.\</blockquote\>\<p class="e05-caption"\>That feeling isn't a limitation. It's recognition that there's another level available—and that the right system can help you reach it.\</p\>\</div\>\</article\>

\<footer class="e05-footer"\>\<p\>If you recognized yourself in these moments, you've discovered a pattern — not a limitation.\</p\>\<small\>There is another way to work with AI.\</small\>\</footer\>  
\</div\>\</section\>  
\</body\>  
\</html\>

\<\!doctype html\>  
\<html lang="en"\>  
\<head\>  
\<meta charset="utf-8"\>  
\<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"\>  
\<meta name="theme-color" content="\#000000"\>  
\<meta name="color-scheme" content="dark"\>  
\<meta name="maxess-artifact" content="E06-SECTION-06-WORKING"\>  
\<meta name="maxis-source" content="MAXESS AAA dimensional depth / Naya Supercharger"\>  
\<title\>MAXESS — E06 · Naya Supercharger\</title\>  
\<style\>  
:root{--bg:\#020104;--ink:\#f8f6ff;--muted:\#aaa5b7;--purple:\#8a5cff;--violet:\#b895ff;--magenta:\#ed42c4;--blue:\#3ca8ff;--green:\#35e39b;--yellow:\#ffd34d;--ease:cubic-bezier(.2,.8,.2,1);--light:145deg}  
\*{box-sizing:border-box}html{background:\#000;scroll-behavior:smooth}body{margin:0;background:\#000;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}img{max-width:100%}button{font:inherit}\#e06{min-height:100svh;overflow:hidden;background:radial-gradient(circle at 50% \-5%,rgba(138,92,255,.12),transparent 34%),\#000}.shell{position:relative;width:min(1280px,100%);margin:auto;padding:24px clamp(14px,3.5vw,52px) 130px}.shell:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.035;background-image:radial-gradient(rgba(255,255,255,.8) .45px,transparent .55px);background-size:7px 7px;z-index:0}.hero,.super,.orbit,.proof,.boards,.custom,.closing{position:relative;z-index:1}.hero{text-align:center;max-width:1000px;margin:auto;padding:clamp(28px,6vw,72px) 0 0}.eyebrow{font-size:11px;font-weight:950;letter-spacing:.32em;text-transform:uppercase}.hero .eyebrow{display:inline-block;color:rgba(255,255,255,.58);padding:8px 14px;border:1px solid rgba(184,149,255,.22);border-radius:999px;background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.015));box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 12px 30px rgba(0,0,0,.45),0 0 35px rgba(138,92,255,.08)}.hero h1{margin:22px 0 0;font-family:Georgia,"Times New Roman",serif;font-size:clamp(50px,8vw,104px);font-weight:400;letter-spacing:-.065em;line-height:.9;text-shadow:0 3px 0 rgba(0,0,0,.9),0 8px 34px rgba(0,0,0,.8),0 0 55px rgba(138,92,255,.12)}.hero h1 em,.boards-intro h2 em,.custom h2 em,.closing h3 em{font-style:normal;color:var(--violet);text-shadow:0 0 28px rgba(184,149,255,.35)}.hero p{max-width:720px;margin:24px auto 0;color:rgba(255,255,255,.78);font-size:clamp(15px,1.6vw,18px);line-height:1.7;text-shadow:0 2px 18px \#000}.super{text-align:center;margin:28px auto \-8px}.super strong{display:inline-block;font-size:clamp(16px,1.8vw,23px);font-weight:950;letter-spacing:.28em;text-transform:uppercase;color:\#fff;text-shadow:0 2px 0 \#000,0 0 32px rgba(138,92,255,.55)}.super span{display:block;margin-top:8px;color:rgba(255,255,255,.48);font-size:10px;font-weight:900;letter-spacing:.28em;text-transform:uppercase}  
.orbit{--orbit-size:min(920px,76vw);--center-size:min(350px,30vw);--avatar-size:clamp(116px,14vw,164px);--orbit-radius:calc(var(--orbit-size)/2 \- var(--avatar-size)/2 \- 8px);position:relative;width:min(1160px,100%);height:calc(var(--orbit-size) \+ 145px);margin:0 auto}.orbit:before{content:"";position:absolute;left:50%;top:50%;width:calc(var(--orbit-size) \+ 150px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(138,92,255,.2),rgba(138,92,255,.05) 42%,transparent 69%);filter:blur(35px)}.orbit:after{content:"";position:absolute;left:50%;top:50%;width:calc(var(--orbit-size) \- 80px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;box-shadow:inset 0 0 80px rgba(138,92,255,.05),0 0 90px rgba(138,92,255,.06);pointer-events:none}.orbit-ring{position:absolute;left:50%;top:50%;width:var(--orbit-size);aspect-ratio:1;transform:translate(-50%,-50%);border:1px solid rgba(255,255,255,.2);border-radius:50%;box-shadow:0 0 70px rgba(138,92,255,.1),inset 0 0 70px rgba(138,92,255,.06)}.orbit-ring:before{content:"";position:absolute;inset:7%;border:1px solid rgba(138,92,255,.2);border-radius:50%}.orbit-ring:after{content:"";position:absolute;inset:16%;border:1px dashed rgba(255,255,255,.11);border-radius:50%}.center{position:absolute;left:50%;top:50%;width:var(--center-size);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.3),transparent 12%),radial-gradient(circle at 38% 30%,rgba(138,92,255,.4),transparent 39%),radial-gradient(circle at 58% 62%,rgba(237,66,196,.12),transparent 55%),radial-gradient(circle at 50% 48%,\#211b2b 0 30%,\#100c18 58%,\#050308 80%,\#000 100%);border:1px solid rgba(255,255,255,.42);box-shadow:inset 18px 15px 44px rgba(255,255,255,.1),inset \-42px \-45px 82px rgba(0,0,0,.94),inset 0 0 110px rgba(138,92,255,.23),0 55px 110px rgba(0,0,0,.95),0 0 130px rgba(138,92,255,.25);z-index:5}.center:before{content:"";position:absolute;inset:2.5%;border-radius:50%;border:1px solid rgba(255,255,255,.2);box-shadow:inset 0 0 24px rgba(255,255,255,.06)}.center:after{content:"";position:absolute;inset:-6%;border-radius:50%;border:1px solid rgba(184,149,255,.28);box-shadow:0 0 45px rgba(138,92,255,.2),0 0 90px rgba(138,92,255,.08)}.center img{position:absolute;inset:16px;width:calc(100% \- 32px);height:calc(100% \- 32px);border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.95);box-shadow:0 0 0 8px rgba(138,92,255,.13),0 0 55px rgba(138,92,255,.32),0 28px 65px rgba(0,0,0,.8);filter:contrast(1.05) saturate(.95)}.center-label{position:absolute;bottom:24px;z-index:6;text-align:center}.center-label b{display:block;font-family:Georgia,serif;font-size:clamp(30px,3vw,44px);font-weight:400;letter-spacing:-.055em;text-shadow:0 3px 22px \#000,0 0 30px rgba(138,92,255,.3)}.node{position:absolute;left:50%;top:50%;width:200px;text-align:center;z-index:8}.node .line{position:absolute;left:50%;top:50%;width:2px;height:var(--orbit-radius);background:linear-gradient(to top,rgba(255,255,255,.02),var(--accent));opacity:.42;transform:translate(-50%,-100%);transform-origin:bottom;box-shadow:0 0 10px color-mix(in srgb,var(--accent) 45%,transparent)}.node .dot{position:absolute;left:50%;top:50%;width:10px;height:10px;border-radius:50%;background:radial-gradient(circle at 30% 25%,\#fff,var(--accent) 42%,\#000 100%);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 12%,transparent),0 0 24px var(--accent);transform:translate(-50%,-50%) translateY(var(--orbit-radius))}.avatar{position:relative;width:var(--avatar-size);height:var(--avatar-size);margin:auto;padding:5px;border-radius:50%;border:1px solid rgba(255,255,255,.52);background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.2),transparent 20%),radial-gradient(circle,var(--accent),transparent 70%);box-shadow:inset 4px 4px 12px rgba(255,255,255,.12),inset \-12px \-15px 22px rgba(0,0,0,.55),0 0 0 9px rgba(255,255,255,.02),0 0 44px color-mix(in srgb,var(--accent) 28%,transparent),0 24px 48px rgba(0,0,0,.8);transition:transform .25s var(--ease),box-shadow .25s ease}.node:hover .avatar{transform:translateY(-5px) scale(1.04);box-shadow:inset 4px 4px 12px rgba(255,255,255,.16),inset \-12px \-15px 22px rgba(0,0,0,.55),0 0 0 9px rgba(255,255,255,.025),0 0 54px color-mix(in srgb,var(--accent) 38%,transparent),0 32px 58px rgba(0,0,0,.85)}.avatar img{width:100%;height:100%;display:block;border-radius:50%;object-fit:cover;border:1px solid rgba(255,255,255,.82)}.node-name{display:block;margin:13px auto 0;width:max-content;max-width:200px;padding:9px 13px;border:1px solid color-mix(in srgb,var(--accent) 45%,rgba(255,255,255,.18));border-radius:999px;background:linear-gradient(180deg,rgba(18,15,23,.96),\#030303);color:\#fff;font-size:11px;font-weight:950;letter-spacing:.075em;text-transform:uppercase;line-height:1.1;box-shadow:inset 0 1px 0 rgba(255,255,255,.12),inset 0 \-7px 14px rgba(0,0,0,.55),0 12px 26px rgba(0,0,0,.68),0 0 24px color-mix(in srgb,var(--accent) 9%,transparent);text-shadow:0 1px 8px \#000}.node-1{--accent:var(--magenta);transform:translate(-50%,-50%) rotate(-90deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(90deg)}.node-2{--accent:var(--purple);transform:translate(-50%,-50%) rotate(-50deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(50deg)}.node-3{--accent:var(--blue);transform:translate(-50%,-50%) rotate(-10deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(10deg)}.node-4{--accent:var(--green);transform:translate(-50%,-50%) rotate(30deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-30deg)}.node-5{--accent:var(--yellow);transform:translate(-50%,-50%) rotate(70deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-70deg)}.node-6{--accent:var(--magenta);transform:translate(-50%,-50%) rotate(110deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-110deg)}.node-7{--accent:var(--purple);transform:translate(-50%,-50%) rotate(150deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-150deg)}.node-8{--accent:var(--blue);transform:translate(-50%,-50%) rotate(190deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-190deg)}.node-9{--accent:var(--green);transform:translate(-50%,-50%) rotate(230deg) translateY(calc(-1 \* var(--orbit-radius))) rotate(-230deg)}  
.proof{max-width:840px;margin:0 auto 76px;text-align:center}.proof p{margin:0;color:rgba(255,255,255,.76);font-size:15px;line-height:1.75}.proof strong{color:\#fff;text-shadow:0 0 20px rgba(138,92,255,.22)}.boards{width:min(1160px,100%);margin:auto}.boards-intro{text-align:center;max-width:900px;margin:0 auto 42px}.boards-intro .eyebrow{color:rgba(255,255,255,.55)}.boards-intro h2{margin:14px 0 0;font-family:Georgia,serif;font-size:clamp(44px,6vw,78px);font-weight:400;letter-spacing:-.065em;line-height:.94;text-shadow:0 4px 28px rgba(0,0,0,.85)}.board-grid{display:grid;grid-template-columns:1fr;gap:30px}.board{--accent:var(--purple);position:relative;display:grid;grid-template-columns:minmax(300px,35%) minmax(0,1fr);border:1px solid color-mix(in srgb,var(--accent) 34%,rgba(255,255,255,.14));border-radius:32px;background:linear-gradient(145deg,rgba(25,19,34,.96),rgba(2,2,4,.99) 52%,\#000);box-shadow:0 38px 90px rgba(0,0,0,.9),inset 0 1px 0 rgba(255,255,255,.09),inset 0 \-30px 70px rgba(0,0,0,.55),0 0 80px color-mix(in srgb,var(--accent) 6%,transparent);overflow:hidden;isolation:isolate}.board:nth-child(1){--accent:var(--magenta)}.board:nth-child(2){--accent:var(--purple)}.board:nth-child(3){--accent:var(--blue)}.board:nth-child(4){--accent:var(--green)}.board:nth-child(5){--accent:var(--yellow)}.board:nth-child(6){--accent:var(--magenta)}.board:nth-child(7){--accent:var(--purple)}.board:nth-child(8){--accent:var(--blue)}.board:nth-child(9){--accent:var(--green)}.board:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 15% 0,color-mix(in srgb,var(--accent) 14%,transparent),transparent 38%),linear-gradient(110deg,transparent 25%,rgba(255,255,255,.018) 50%,transparent 75%);z-index:-1}.board:after{content:"";position:absolute;left:6%;right:6%;top:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent),\#fff,var(--accent),transparent);box-shadow:0 0 32px color-mix(in srgb,var(--accent) 60%,transparent);z-index:3}.board-media-column{position:relative;padding:28px 0 28px 28px;z-index:2}.board-media-column:after{content:"";position:absolute;left:14px;top:20px;bottom:20px;width:2px;background:linear-gradient(180deg,transparent,var(--accent),transparent);box-shadow:0 0 18px color-mix(in srgb,var(--accent) 45%,transparent)}.board-media{position:relative;width:100%;aspect-ratio:16/10;overflow:hidden;border-radius:24px;border:1px solid color-mix(in srgb,var(--accent) 54%,rgba(255,255,255,.24));background:\#030303;box-shadow:inset 0 1px 0 rgba(255,255,255,.15),inset 0 \-20px 35px rgba(0,0,0,.65),0 28px 55px rgba(0,0,0,.82),0 0 44px color-mix(in srgb,var(--accent) 12%,transparent);transform:translateZ(0)}.board-media:before{content:"";position:absolute;inset:0;background:linear-gradient(145deg,rgba(255,255,255,.14),transparent 23%,transparent 68%,rgba(0,0,0,.45));z-index:2;pointer-events:none}.board-media:after{content:"";position:absolute;inset:5px;border-radius:20px;border:1px solid rgba(255,255,255,.08);z-index:3;pointer-events:none}.board-media img{width:100%;height:100%;display:block;object-fit:cover}.board-brand{display:flex;align-items:center;justify-content:center;padding:16px 12px 0;opacity:.92}.board-brand img{display:block;width:min(320px,100%);filter:drop-shadow(0 10px 22px rgba(0,0,0,.88))}.board-content{position:relative;z-index:2;padding:34px 34px 34px 30px;min-width:0}.board-index{display:inline-flex;align-items:center;gap:10px;color:color-mix(in srgb,var(--accent) 76%,white 20%);font-size:11px;font-weight:950;letter-spacing:.23em;text-shadow:0 0 18px color-mix(in srgb,var(--accent) 30%,transparent)}.board-index:before{content:"";width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 30% 25%,\#fff,var(--accent) 42%,\#000 100%);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 10%,transparent),0 0 16px var(--accent)}.board h3{margin:11px 0 10px;font-family:Georgia,serif;font-size:clamp(34px,4vw,52px);font-weight:400;letter-spacing:-.055em;line-height:.96;text-shadow:0 3px 0 \#000,0 10px 30px rgba(0,0,0,.82),0 0 28px color-mix(in srgb,var(--accent) 14%,transparent)}.board-lead{margin:0 0 23px;color:\#fff;font-size:clamp(15px,1.45vw,18px);line-height:1.55;max-width:720px}.answers{width:100%;display:grid;gap:11px}.answer{--accent:var(--purple);position:relative;width:100%;min-height:78px;display:grid;grid-template-columns:58px minmax(0,1fr) 32px;align-items:center;gap:13px;padding:10px 10px 10px 8px;border:1px solid rgba(255,255,255,.12);border-radius:18px;background:linear-gradient(145deg,rgba(24,21,31,.98),rgba(4,4,6,.99));box-shadow:inset 0 1px 0 rgba(255,255,255,.1),inset 0 \-12px 22px rgba(0,0,0,.5),0 12px 28px rgba(0,0,0,.42);transition:transform .22s var(--ease),border-color .22s ease,box-shadow .22s ease}.answers .answer:nth-child(1){--accent:var(--magenta)}.answers .answer:nth-child(2){--accent:var(--purple)}.answers .answer:nth-child(3){--accent:var(--blue)}.answers .answer:nth-child(4){--accent:var(--green)}.answers .answer:nth-child(5){--accent:var(--yellow)}.answer:before{content:"";position:absolute;left:8px;right:8px;top:1px;height:1px;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 70%,white 20%),transparent);opacity:.75}.answer:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--accent) 62%,rgba(255,255,255,.22));box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 \-12px 22px rgba(0,0,0,.5),0 20px 36px rgba(0,0,0,.55),0 0 35px color-mix(in srgb,var(--accent) 12%,transparent)}.jewel{position:relative;width:50px;height:50px;display:grid;place-items:center;border-radius:15px;border:1px solid color-mix(in srgb,var(--accent) 78%,rgba(255,255,255,.22));background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.22),transparent 17%),linear-gradient(145deg,\#15111b,\#030303);box-shadow:inset 5px 5px 12px rgba(255,255,255,.07),inset \-10px \-13px 20px rgba(0,0,0,.72),0 0 0 4px color-mix(in srgb,var(--accent) 8%,transparent),0 0 30px color-mix(in srgb,var(--accent) 17%,transparent),0 10px 22px rgba(0,0,0,.7);overflow:hidden}.jewel:after{content:"";position:absolute;left:12%;top:7%;width:52%;height:25%;border-radius:50%;background:rgba(255,255,255,.22);filter:blur(4px);transform:rotate(-18deg)}.glyph{position:relative;z-index:1;font-size:18px;line-height:1;color:var(--accent);text-shadow:0 0 16px color-mix(in srgb,var(--accent) 55%,transparent),0 2px 0 \#000}.answer-copy{min-width:0;padding:4px 0}.answer-title{display:block;font-size:14px;line-height:1.25;font-weight:950;color:\#fff;text-shadow:0 1px 10px \#000}.answer-sub{display:block;margin-top:5px;font-size:13px;line-height:1.48;color:rgba(255,255,255,.76);font-style:italic}.answer-sub:before{content:"“";color:var(--accent);font-family:Georgia,serif;font-size:1.35em;font-style:normal;font-weight:700;line-height:0;vertical-align:-.08em;margin-right:2px}.answer-sub:after{content:"”";color:var(--accent);font-family:Georgia,serif;font-size:1.35em;font-style:normal;font-weight:700;line-height:0;vertical-align:-.08em;margin-left:2px}.chevron{width:28px;height:28px;display:grid;place-items:center;border-radius:50%;border:1px solid color-mix(in srgb,var(--accent) 30%,rgba(255,255,255,.12));background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(0,0,0,.45));color:\#817b8f;font-size:19px;box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 6px 14px rgba(0,0,0,.45);transition:all .22s var(--ease)}.answer:hover .chevron{color:\#fff;border-color:var(--accent);transform:translateX(3px);box-shadow:0 0 20px color-mix(in srgb,var(--accent) 24%,transparent)}  
.custom{position:relative;margin:105px auto 0;max-width:1120px;text-align:center;padding:clamp(54px,7vw,90px) clamp(20px,5vw,70px);border:1px solid rgba(184,149,255,.5);border-radius:42px;background:radial-gradient(circle at 50% 0,rgba(138,92,255,.34),transparent 42%),linear-gradient(180deg,\#14091f 0%,\#08030f 52%,\#000 100%);box-shadow:0 65px 160px rgba(0,0,0,.95),inset 0 1px 0 rgba(255,255,255,.13),inset 0 \-40px 80px rgba(0,0,0,.55),0 0 130px rgba(138,92,255,.14);overflow:hidden}.custom:before{content:"";position:absolute;left:6%;right:6%;top:0;height:3px;background:linear-gradient(90deg,transparent,var(--magenta),var(--purple),var(--blue),var(--green),var(--yellow),transparent);box-shadow:0 0 42px rgba(184,149,255,.7)}.custom:after{content:"";position:absolute;left:50%;top:0;width:65%;height:60%;transform:translateX(-50%);background:radial-gradient(circle,rgba(255,255,255,.07),transparent 66%);filter:blur(22px);pointer-events:none}.custom .eyebrow{color:var(--violet);text-shadow:0 0 18px rgba(184,149,255,.3)}.custom h2{position:relative;z-index:1;margin:15px 0 0;font-family:Georgia,serif;font-size:clamp(48px,7vw,88px);font-weight:400;letter-spacing:-.07em;line-height:.91;text-shadow:0 4px 30px rgba(0,0,0,.9)}.power-intro{position:relative;z-index:1;max-width:900px;margin:30px auto 0;color:\#fff;font-size:clamp(17px,1.8vw,22px);line-height:1.62}.power-intro strong{color:\#fff}.os-wrap{position:relative;z-index:1;margin:52px auto 0}.os-kicker{display:inline-block;margin-bottom:14px;color:var(--violet);font-size:11px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}.operating-system{display:grid;grid-template-columns:1fr 1fr;border:1px solid rgba(184,149,255,.48);border-radius:34px;overflow:hidden;background:\#000;box-shadow:0 42px 100px rgba(0,0,0,.82),inset 0 1px 0 rgba(255,255,255,.1)}.os-panel{position:relative;padding:clamp(34px,4.5vw,52px);text-align:left;color:\#fff}.os-panel:first-child{background:linear-gradient(145deg,\#180b2a,\#07030f);box-shadow:inset \-20px 0 40px rgba(0,0,0,.25)}.os-panel:last-child{background:radial-gradient(circle at 50% 0,rgba(138,92,255,.4),transparent 62%),linear-gradient(145deg,\#24103e,\#07030f);box-shadow:inset 20px 0 40px rgba(0,0,0,.2)}.os-panel:first-child:after{content:"";position:absolute;right:0;top:13%;bottom:13%;width:1px;background:linear-gradient(180deg,transparent,rgba(184,149,255,.5),transparent)}.os-label{display:block;color:var(--violet);font-size:11px;font-weight:950;letter-spacing:.25em;text-transform:uppercase}.os-panel h3{margin:13px 0 13px;font-family:Georgia,serif;font-size:clamp(34px,4.3vw,56px);font-weight:400;letter-spacing:-.05em;line-height:.98;color:\#fff;text-shadow:0 3px 0 \#000,0 10px 30px rgba(0,0,0,.65)}.os-panel p{margin:0;font-size:clamp(15px,1.55vw,18px);line-height:1.65;color:\#fff}.power-banner{position:relative;margin:20px auto 0;padding:clamp(30px,4vw,52px);border:1px solid rgba(255,255,255,.16);border-radius:30px;background:\#020202;overflow:hidden;box-shadow:0 34px 88px rgba(0,0,0,.8),inset 0 1px 0 rgba(255,255,255,.08)}.power-banner:before{content:"";position:absolute;inset:0;background:linear-gradient(110deg,rgba(237,66,196,.13),rgba(138,92,255,.12),rgba(60,168,255,.12),rgba(53,227,155,.12),rgba(255,211,77,.12))}.power-banner:after{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,transparent,\#fff,var(--purple),transparent);box-shadow:0 0 28px rgba(184,149,255,.45)}.power-banner\>\*{position:relative;z-index:1}.power-banner .banner-kicker{display:block;color:var(--violet);font-size:10px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}.power-banner h3{margin:11px 0 12px;font-family:Georgia,serif;font-size:clamp(38px,5.5vw,68px);font-weight:400;line-height:.94;letter-spacing:-.06em;text-shadow:0 3px 0 \#000,0 12px 30px rgba(0,0,0,.75)}.power-banner h3 em{font-style:normal;color:\#fff}.power-banner p{max-width:850px;margin:0 auto;color:\#fff;font-size:clamp(15px,1.6vw,19px);line-height:1.65}.power-benefits{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:22px auto 0;max-width:960px}.power-benefit{position:relative;padding:28px 23px 27px;border:1px solid rgba(184,149,255,.36);border-radius:24px;background:linear-gradient(145deg,rgba(27,19,40,.94),rgba(3,3,5,.98));text-align:left;box-shadow:inset 0 1px 0 rgba(255,255,255,.09),inset 0 \-16px 28px rgba(0,0,0,.45),0 20px 42px rgba(0,0,0,.5)}.power-benefit:before{content:"";position:absolute;left:16px;right:16px;top:0;height:1px;background:linear-gradient(90deg,transparent,var(--violet),transparent);box-shadow:0 0 15px rgba(184,149,255,.3)}.benefit-number{display:block;color:var(--violet);font-size:10px;font-weight:950;letter-spacing:.2em}.power-benefit h4{margin:11px 0 8px;font-family:Georgia,serif;font-size:clamp(25px,2.5vw,34px);font-weight:400;color:\#fff;letter-spacing:-.04em;text-shadow:0 2px 16px rgba(0,0,0,.8)}.power-benefit p{margin:0;color:rgba(255,255,255,.8);font-size:14px;line-height:1.58}.offer{position:relative;margin:40px auto 0;padding:42px clamp(22px,4vw,56px);border:1px solid rgba(184,149,255,.78);border-radius:32px;background:radial-gradient(circle at 50% 0,rgba(184,149,255,.28),transparent 55%),linear-gradient(145deg,\#1c0b33,\#07030e 66%,\#000);box-shadow:inset 0 1px 0 rgba(255,255,255,.16),inset 0 \-25px 50px rgba(0,0,0,.55),0 34px 100px rgba(0,0,0,.82),0 0 85px rgba(138,92,255,.17)}.offer:before{content:"";position:absolute;left:8%;right:8%;top:0;height:2px;background:linear-gradient(90deg,transparent,\#fff,var(--violet),\#fff,transparent);box-shadow:0 0 30px rgba(184,149,255,.6)}.offer-label{position:relative;z-index:1;color:var(--violet);font-size:12px;font-weight:950;letter-spacing:.28em;text-transform:uppercase}.offer h3{position:relative;z-index:1;margin:13px 0 12px;font-family:Georgia,serif;font-size:clamp(40px,5.5vw,68px);font-weight:400;letter-spacing:-.06em;line-height:.94;color:\#fff;text-shadow:0 3px 0 \#000,0 12px 30px rgba(0,0,0,.7)}.offer h3 em{font-style:normal;color:var(--violet)}.offer p{position:relative;z-index:1;max-width:820px;margin:0 auto;color:\#fff;font-size:clamp(15px,1.55vw,18px);line-height:1.65}.offer-value{position:relative;z-index:1;display:flex;align-items:center;justify-content:center;gap:18px;margin-top:26px}.offer-line{width:min(100px,15vw);height:1px;background:linear-gradient(90deg,transparent,rgba(184,149,255,.8))}.offer-price{font-family:Georgia,serif;font-size:clamp(36px,4.4vw,56px);color:\#fff;text-shadow:0 3px 0 \#000,0 0 28px rgba(184,149,255,.24)}.offer-price small{display:block;margin-top:5px;font-family:Inter,ui-sans-serif,system-ui,sans-serif;font-size:10px;font-weight:950;letter-spacing:.18em;color:var(--violet);text-transform:uppercase}.closing{max-width:1120px;margin:86px auto 0;text-align:center}.closing-card{position:relative;padding:clamp(48px,7vw,82px) clamp(22px,5vw,64px);border:1px solid rgba(255,255,255,.18);border-radius:42px;background:linear-gradient(180deg,\#0d0715,\#020202);box-shadow:0 55px 135px rgba(0,0,0,.95),inset 0 1px 0 rgba(255,255,255,.1),inset 0 \-35px 70px rgba(0,0,0,.6);overflow:hidden}.closing-card:before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--magenta),var(--purple),var(--blue),var(--green),var(--yellow));box-shadow:0 0 40px rgba(184,149,255,.55)}.closing-card:after{content:"";position:absolute;left:50%;top:0;width:70%;height:55%;transform:translateX(-50%);background:radial-gradient(circle,rgba(138,92,255,.16),transparent 68%);filter:blur(20px);pointer-events:none}.closing .closing-kicker{position:relative;z-index:1;color:var(--violet);font-size:11px;font-weight:950;letter-spacing:.32em;text-transform:uppercase}.closing h3{position:relative;z-index:1;margin:15px 0 15px;font-family:Georgia,serif;font-size:clamp(52px,7vw,92px);font-weight:400;letter-spacing:-.07em;line-height:.9;color:\#fff;text-shadow:0 4px 0 \#000,0 14px 35px rgba(0,0,0,.85)}.closing-lead{position:relative;z-index:1;max-width:850px;margin:0 auto;color:\#fff;font-size:clamp(17px,1.8vw,22px);line-height:1.6}.closing-grid{position:relative;z-index:1;display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:38px auto 0;max-width:900px;text-align:left}.closing-panel{padding:26px;border:1px solid rgba(255,255,255,.13);border-radius:24px;background:linear-gradient(145deg,rgba(22,18,28,.92),rgba(2,2,4,.98));box-shadow:inset 0 1px 0 rgba(255,255,255,.08),inset 0 \-14px 25px rgba(0,0,0,.45),0 18px 35px rgba(0,0,0,.5)}.closing-panel .label{display:block;color:var(--violet);font-size:10px;font-weight:950;letter-spacing:.2em;text-transform:uppercase}.closing-panel h4{margin:10px 0 8px;font-family:Georgia,serif;font-size:clamp(27px,3vw,39px);font-weight:400;letter-spacing:-.04em}.closing-panel p{margin:0;color:rgba(255,255,255,.78);font-size:14px;line-height:1.55}.closing-statement{position:relative;z-index:1;margin:38px auto 0;max-width:850px;font-size:clamp(20px,2vw,26px);line-height:1.5}.closing-mark{position:relative;z-index:1;display:grid;place-items:center;width:76px;height:76px;margin:32px auto 0;border:1px solid rgba(184,149,255,.62);border-radius:24px;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.14),transparent 18%),radial-gradient(circle,rgba(138,92,255,.38),transparent 68%),\#08050c;color:var(--violet);font-family:Georgia,serif;font-size:34px;box-shadow:inset 5px 5px 14px rgba(255,255,255,.07),inset \-12px \-15px 25px rgba(0,0,0,.65),0 0 0 6px rgba(138,92,255,.06),0 0 55px rgba(138,92,255,.24),0 18px 38px rgba(0,0,0,.7)}  
@media(max-width:900px){.orbit{--orbit-size:min(700px,82vw);--center-size:min(280px,34vw);--avatar-size:clamp(98px,15vw,136px);--orbit-radius:calc(var(--orbit-size)/2 \- var(--avatar-size)/2 \- 7px);height:calc(var(--orbit-size) \+ 110px)}.node{width:175px}.node-name{font-size:10px;max-width:175px}.board{grid-template-columns:240px minmax(0,1fr)}.board-media-column{padding:22px 0 22px 22px}.board-content{padding:25px 22px}.board h3{font-size:33px}.board-lead{font-size:14px}.answer{grid-template-columns:48px minmax(0,1fr) 28px;min-height:70px}.jewel{width:44px;height:44px}.answer-title{font-size:13px}.answer-sub{font-size:12.5px}.power-benefits{grid-template-columns:1fr 1fr}.power-benefit:last-child{grid-column:1/-1}.closing-grid{gap:12px}}  
@media(max-width:680px){.shell{padding-left:10px;padding-right:10px}.hero{padding-top:20px}.hero h1{font-size:clamp(45px,13vw,68px)}.hero p{font-size:14px}.orbit{--orbit-size:min(430px,92vw);--center-size:min(190px,40vw);--avatar-size:clamp(72px,18vw,94px);--orbit-radius:calc(var(--orbit-size)/2 \- var(--avatar-size)/2 \- 4px);height:calc(var(--orbit-size) \+ 64px);margin-top:6px}.center img{inset:11px;width:calc(100% \- 22px);height:calc(100% \- 22px)}.center-label{bottom:13px}.center-label b{font-size:25px}.node{width:112px}.node-name{margin-top:8px;padding:7px 8px;font-size:8px;letter-spacing:.045em;max-width:112px}.node .line{opacity:.26}.node .dot{width:7px;height:7px}.boards-intro h2{font-size:clamp(40px,11vw,58px)}.board{display:block;border-radius:26px}.board-media-column{padding:15px 15px 0}.board-media-column:after{display:none}.board-media{border-radius:19px;aspect-ratio:16/10}.board-brand{padding:11px 0 0}.board-content{padding:21px 15px 18px}.board h3{font-size:30px}.board-lead{font-size:13.5px;margin-bottom:16px}.answer{grid-template-columns:43px minmax(0,1fr) 24px;gap:9px;min-height:65px;border-radius:16px}.jewel{width:40px;height:40px;border-radius:13px}.glyph{font-size:16px}.answer-title{font-size:12px}.answer-sub{font-size:11px;line-height:1.5}.chevron{width:24px;height:24px;font-size:17px}.custom{margin-top:60px;border-radius:28px}.custom h2{font-size:clamp(44px,12vw,64px)}.power-intro{font-size:15px}.operating-system{grid-template-columns:1fr;border-radius:25px}.os-panel{padding:29px 20px}.os-panel:first-child:after{left:10%;right:10%;top:auto;bottom:0;width:auto;height:1px;background:linear-gradient(90deg,transparent,rgba(184,149,255,.5),transparent)}.power-benefits{grid-template-columns:1fr;gap:11px}.power-benefit:last-child{grid-column:auto}.power-banner{border-radius:23px;padding:29px 18px}.offer{padding:30px 18px;border-radius:25px}.offer p{font-size:14px}.closing{margin-top:58px}.closing-card{border-radius:28px;padding:42px 17px}.closing h3{font-size:clamp(45px,13vw,64px)}.closing-grid{grid-template-columns:1fr;margin-top:28px}.closing-panel{padding:21px}.closing-statement{font-size:18px}}  
@media(max-width:390px){.orbit{--orbit-size:320px;--center-size:138px;--avatar-size:62px;--orbit-radius:calc(var(--orbit-size)/2 \- var(--avatar-size)/2 \- 3px);height:365px}.node{width:82px}.node-name{font-size:6.8px;max-width:82px;padding:5px}.center-label{bottom:9px}.center-label b{font-size:20px}.board-content{padding:17px 11px}.answer{grid-template-columns:37px minmax(0,1fr) 20px;gap:7px}.jewel{width:37px;height:37px}.answer-title{font-size:11px}.answer-sub{font-size:10px}.offer h3{font-size:31px}.offer-price{font-size:29px}.closing h3{font-size:42px}}  
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.avatar,.answer,.chevron{transition:none}.node:hover .avatar{transform:none}}  
\</style\>  
\</head\>  
\<body\>  
\<main id="e06" aria-labelledby="e06-title"\>\<div class="shell"\>  
\<section class="hero"\>\<p class="eyebrow"\>MAXESS · NAYA ACTIVATION\</p\>\<h1 id="e06-title"\>Meet the \<em\>Naya Supercharger.\</em\>\</h1\>\<p\>One intelligence. Nine activated systems. A tuned way of working with AI that can keep getting more personal, capable and effective with you.\</p\>\</section\>  
\<div class="super" aria-label="Naya Supercharger, Mastery Activation Protocol"\>\<strong\>NAYA SUPERCHARGER\</strong\>\<span\>Mastery Activation Protocol\</span\>\</div\>  
\<section class="orbit" aria-label="Naya and the nine activated systems"\>\<div class="orbit-ring" aria-hidden="true"\>\</div\>\<div class="center"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-black.jpg" alt="Naya"\>\<div class="center-label"\>\<b\>Naya\</b\>\</div\>\</div\>  
\<div class="node node-1"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-2.jpg" alt="Naya Personality"\>\</div\>\<span class="node-name"\>Naya Personality\</span\>\</div\>  
\<div class="node node-2"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-3.jpg" alt="Naya Brain"\>\</div\>\<span class="node-name"\>Naya Brain\</span\>\</div\>  
\<div class="node node-3"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-4.jpg" alt="Naya Notes"\>\</div\>\<span class="node-name"\>Naya Notes\</span\>\</div\>  
\<div class="node node-4"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-5.jpg" alt="Naya Lead Mode"\>\</div\>\<span class="node-name"\>Naya Lead Mode\</span\>\</div\>  
\<div class="node node-5"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-6.jpg" alt="Naya Law"\>\</div\>\<span class="node-name"\>Naya Law\</span\>\</div\>  
\<div class="node node-6"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-7.jpg" alt="Naya Scorecarding"\>\</div\>\<span class="node-name"\>Naya Scorecarding\</span\>\</div\>  
\<div class="node node-7"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-8.jpg" alt="Naya Language"\>\</div\>\<span class="node-name"\>Naya Language\</span\>\</div\>  
\<div class="node node-8"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-10.jpg" alt="Naya Design"\>\</div\>\<span class="node-name"\>Naya Design\</span\>\</div\>  
\<div class="node node-9"\>\<span class="line"\>\</span\>\<span class="dot"\>\</span\>\<div class="avatar"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-9.jpg" alt="Naya Coder"\>\</div\>\<span class="node-name"\>Naya Coder\</span\>\</div\>\</section\>  
\<section class="proof"\>\<p\>\<strong\>Nine manifestations. One Naya.\</strong\> Scroll when you are ready to see what each activated system actually changes for you.\</p\>\</section\>  
\<section class="boards" aria-labelledby="systems-title"\>\<div class="boards-intro"\>\<span class="eyebrow"\>9 ACTIVATED SYSTEMS\</span\>\<h2 id="systems-title"\>What each system \<em\>changes for you.\</em\>\</h2\>\</div\>\<div class="board-grid"\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-2.jpg" alt="Naya Personality" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>01 · PERSONALITY\</span\>\<h3\>Naya Personality\</h3\>\<p class="board-lead"\>Work with an AI personality tuned to how you want the relationship to feel.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>You feel understood faster.\</span\>\<span class="answer-sub"\>Naya can reflect the tone, warmth and style you actually want.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Less explaining who you are.\</span\>\<span class="answer-sub"\>Your preferred way of working becomes part of the relationship.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>More consistency.\</span\>\<span class="answer-sub"\>Naya can show up with a recognizable personality across tasks.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>A better human–AI relationship.\</span\>\<span class="answer-sub"\>The experience feels more like working with an intelligent partner.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>You can tune it further.\</span\>\<span class="answer-sub"\>Tell Naya what to change as your preferences evolve.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-3.jpg" alt="Naya Brain" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>02 · INTELLIGENCE\</span\>\<h3\>Naya Brain\</h3\>\<p class="board-lead"\>Give AI a richer foundation so it can reason from more than the latest sentence.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Stop starting from zero.\</span\>\<span class="answer-sub"\>Important context and working knowledge can stay available.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Better decisions from better context.\</span\>\<span class="answer-sub"\>Naya has more of the information needed to reason well.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Less repetitive prompting.\</span\>\<span class="answer-sub"\>You spend less time rebuilding the same foundation.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>More continuity across work.\</span\>\<span class="answer-sub"\>Ideas and context can connect instead of living in isolated chats.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>A stronger starting point for every task.\</span\>\<span class="answer-sub"\>The system is designed to begin further ahead.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-4.jpg" alt="Naya Notes" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>03 · MEMORY\</span\>\<h3\>Naya Notes\</h3\>\<p class="board-lead"\>Keep the ideas, decisions and context that should not disappear when the conversation ends.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Your good ideas do not disappear.\</span\>\<span class="answer-sub"\>Important thoughts can become reusable knowledge.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Decisions stay connected to the work.\</span\>\<span class="answer-sub"\>Naya can keep track of what you decided and why.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Capture progress instead of recreating it.\</span\>\<span class="answer-sub"\>Useful discoveries can become part of your ongoing system.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Build on yesterday.\</span\>\<span class="answer-sub"\>Your work can accumulate instead of resetting.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make your knowledge more useful.\</span\>\<span class="answer-sub"\>Notes become inputs to better future work.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-5.jpg" alt="Naya Lead Mode" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>04 · LEADERSHIP\</span\>\<h3\>Naya Lead Mode\</h3\>\<p class="board-lead"\>Stop making yourself the project manager of your AI. Tell Naya the destination and let her help drive the work.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Stop managing every step.\</span\>\<span class="answer-sub"\>Naya can identify obvious next actions and move the work forward.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Get more initiative from AI.\</span\>\<span class="answer-sub"\>The system is designed to take the lead instead of waiting for every instruction.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Spend more time deciding, less time directing.\</span\>\<span class="answer-sub"\>You stay in control without micromanaging execution.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Keep momentum.\</span\>\<span class="answer-sub"\>Naya can surface the next useful move instead of stopping at an answer.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make AI feel like a capable partner.\</span\>\<span class="answer-sub"\>The relationship changes from answering to helping accomplish.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-6.jpg" alt="Naya Law" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>05 · STANDARD\</span\>\<h3\>Naya Law\</h3\>\<p class="board-lead"\>Set the standards Naya must protect instead of hoping she guesses what “good” means to you.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Your standards become explicit.\</span\>\<span class="answer-sub"\>Important expectations can be defined instead of assumed.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>More consistent results.\</span\>\<span class="answer-sub"\>Naya can check work against the standards you establish.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Fewer preventable mistakes.\</span\>\<span class="answer-sub"\>Rules can catch recurring problems before they become habits.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>You can update the law.\</span\>\<span class="answer-sub"\>Tell Naya when a standard should change for the way you work now.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make excellence repeatable.\</span\>\<span class="answer-sub"\>Your definition of excellent becomes part of the operating system.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-7.jpg" alt="Naya Scorecarding" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>06 · QUALITY\</span\>\<h3\>Naya Scorecarding\</h3\>\<p class="board-lead"\>Stop accepting “looks good.” Build a habit of knowing what strong work actually is.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Know why something is good.\</span\>\<span class="answer-sub"\>A score becomes useful when the reasons behind it are visible.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Spot weaknesses before shipping.\</span\>\<span class="answer-sub"\>Naya can actively look for what is missing or underperforming.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Turn “not a 10” into useful direction.\</span\>\<span class="answer-sub"\>Critique becomes a roadmap for the next version.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Improve instead of guessing.\</span\>\<span class="answer-sub"\>Evaluate quality against clear criteria rather than vibes alone.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Build a repeatable path to excellence.\</span\>\<span class="answer-sub"\>The system can learn what “excellent” means for your work.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-8.jpg" alt="Naya Language" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>07 · MEANING\</span\>\<h3\>Naya Language\</h3\>\<p class="board-lead"\>Define the words that matter so AI understands what you actually mean instead of choosing its own interpretation.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Less ambiguity.\</span\>\<span class="answer-sub"\>Important terms can have an explicit meaning inside your system.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Stop redefining the same words.\</span\>\<span class="answer-sub"\>A shared reference can reduce repeated explanations and corrections.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make your terminology portable.\</span\>\<span class="answer-sub"\>A defined directory can help other AI systems understand the same meanings.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>You can update the language.\</span\>\<span class="answer-sub"\>Tell Naya when a word, definition or meaning needs to change.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Communicate more precisely.\</span\>\<span class="answer-sub"\>The goal is shared meaning, so Naya spends less effort guessing what you mean.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-10.jpg" alt="Naya Design" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>08 · DESIGN\</span\>\<h3\>Naya Design\</h3\>\<p class="board-lead"\>Give Naya a master designer's eye so the work is not merely functional — it is clear, beautiful, intentional and easy to use.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make information easier to understand.\</span\>\<span class="answer-sub"\>Hierarchy, spacing, contrast and visual structure help people see what matters first.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Turn good ideas into beautiful experiences.\</span\>\<span class="answer-sub"\>Naya can design for clarity, usefulness, emotion and polish — not decoration alone.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Reduce cognitive overload.\</span\>\<span class="answer-sub"\>Dense information can be broken into a visual story people can skim, understand and remember.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Build a recognizable quality standard.\</span\>\<span class="answer-sub"\>Naya can apply your design laws consistently instead of reinventing the visual rules every time.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make the final result feel premium.\</span\>\<span class="answer-sub"\>The last layer is treated as part of the product — because presentation changes perceived value.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\<article class="board"\>\<div class="board-media-column"\>\<div class="board-media"\>\<img src="https\://pub-af3e2a956e4f427ba454a9daea600cf2.r2.dev/naya-profile-9.jpg" alt="Naya Coder" loading="lazy"\>\</div\>\<div class="board-brand"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/maximus-2.png" alt="Human Maximus Codex"\>\</div\>\</div\>\<div class="board-content"\>\<span class="board-index"\>09 · ENGINEERING\</span\>\<h3\>Naya Coder\</h3\>\<p class="board-lead"\>Give Naya a master coder's standard so the code is built to be correct, maintainable, resilient, accessible and ready for real users.\</p\>\<div class="answers"\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>◆\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Build for correctness first.\</span\>\<span class="answer-sub"\>Naya treats requirements, edge cases, state and failure handling as part of the code — not afterthoughts.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Make code easier to maintain.\</span\>\<span class="answer-sub"\>Clear structure, purposeful components and disciplined naming make future changes safer and faster.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>△\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Protect the user experience.\</span\>\<span class="answer-sub"\>Performance, responsiveness, accessibility and graceful failure are treated as engineering requirements.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✧\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Verify instead of assuming.\</span\>\<span class="answer-sub"\>Naya checks the actual behavior and looks for regressions rather than declaring success because code exists.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>  
\<div class="answer"\>\<span class="jewel"\>\<span class="glyph"\>✦\</span\>\</span\>\<span class="answer-copy"\>\<span class="answer-title"\>Ship code that can earn an AAA standard.\</span\>\<span class="answer-sub"\>The goal is not merely working code — it is thoughtful engineering that survives real use and future iteration.\</span\>\</span\>\<span class="chevron"\>›\</span\>\</div\>\</div\>\</div\>\</article\>  
\</div\>\</section\>  
\<section class="custom" aria-labelledby="custom-title"\>\<span class="eyebrow"\>NAYA POWER\</span\>\<h2 id="custom-title"\>Pre-tuned for maximum results.\<br\>\<em\>Customized for maximum personal fit.\</em\>\</h2\>\<p class="power-intro"\>\<strong\>You do not have to spend the next year figuring out how to make AI work this way.\</strong\> Naya Power gives you a ready-to-use operating foundation designed to make your AI more personal, more capable, more proactive and more consistent — without making you build the system yourself.\</p\>  
\<div class="os-wrap"\>\<span class="os-kicker"\>THE DIFFERENCE IS THE OPERATING SYSTEM\</span\>\<div class="operating-system"\>\<div class="os-panel"\>\<span class="os-label"\>AI MASTERY\</span\>\<h3\>Learn how to use AI.\</h3\>\<p\>You learn the skills, thinking patterns and methods that help \<strong\>you\</strong\> get better results from AI.\</p\>\</div\>\<div class="os-panel"\>\<span class="os-label"\>NAYA POWER\</span\>\<h3\>Activate AI to work with you.\</h3\>\<p\>Naya brings the operating foundation to the relationship — so your AI can \<strong\>understand you, remember what matters, take initiative, protect your standards, improve quality, design better and code at a higher standard.\</strong\>\</p\>\</div\>\</div\>\</div\>  
\<div class="power-banner"\>\<span class="banner-kicker"\>WHY THIS MATTERS\</span\>\<h3\>Stop learning the pieces separately.\<br\>\<em\>Activate the pieces together.\</em\>\</h3\>\<p\>Naya Power turns the nine systems into one coordinated way of working — so personality, intelligence, memory, initiative, standards, quality, language, design and engineering reinforce one another instead of living as isolated tricks.\</p\>\</div\>  
\<div class="power-benefits"\>\<div class="power-benefit"\>\<span class="benefit-number"\>01 · WHAT CHANGES\</span\>\<h4\>Less explaining.\</h4\>\<p\>Your preferences, communication style and way of working become part of the relationship, so you can spend more time creating and less time re-explaining yourself.\</p\>\</div\>\<div class="power-benefit"\>\<span class="benefit-number"\>02 · WHAT CHANGES\</span\>\<h4\>More continuity.\</h4\>\<p\>Important context, notes, language and decisions can carry forward, so your work can build instead of constantly restarting.\</p\>\</div\>\<div class="power-benefit"\>\<span class="benefit-number"\>03 · WHAT CHANGES\</span\>\<h4\>Higher standards.\</h4\>\<p\>Lead Mode, Law, Scorecarding, Design and Coder standards give the work stronger direction, quality control and finish.\</p\>\</div\>\</div\>  
\<div class="offer" aria-label="Naya Power exclusive Key 4 offer"\>\<span class="offer-label"\>KEY 4 · NAYA POWER INCLUDED\</span\>\<h3\>The Naya Supercharger.\<br\>\<em\>Skip the struggle. Start further ahead.\</em\>\</h3\>\<p\>Instead of spending months or years discovering these methods one problem at a time, you begin with a tuned foundation designed to help your AI understand you, work with you and improve with you. \<strong\>The hard-won operating system is already there.\</strong\>\</p\>\<div class="offer-value"\>\<span class="offer-line"\>\</span\>\<div class="offer-price"\>\$300+\<small\>Included value with Key 4\</small\>\</div\>\<span class="offer-line"\>\</span\>\</div\>\</div\>  
\</section\>  
\<section class="closing" aria-labelledby="closing-title"\>\<div class="closing-card"\>\<span class="closing-kicker"\>THE PAYOFF\</span\>\<h3 id="closing-title"\>Same AI.\<br\>\<em\>Different operating system.\</em\>\</h3\>\<p class="closing-lead"\>The difference is not another list of prompts. It is the way the intelligence is configured to work with you.\</p\>\<div class="closing-grid"\>\<div class="closing-panel"\>\<span class="label"\>AI MASTERY\</span\>\<h4\>You become better at using AI.\</h4\>\<p\>You learn the methods, thinking and craftsmanship that produce stronger results.\</p\>\</div\>\<div class="closing-panel"\>\<span class="label"\>NAYA POWER\</span\>\<h4\>Your AI becomes better equipped to work with you.\</h4\>\<p\>The operating foundation brings the nine systems together around your relationship with the intelligence.\</p\>\</div\>\</div\>\<p class="closing-statement"\>\<strong\>One intelligence. Nine activated systems.\</strong\>\<br\>More personal. More capable. More proactive. More aligned with the way you want to work.\</p\>\<div class="closing-mark" aria-hidden="true"\>N\</div\>\</div\>\</section\>  
\</div\>\</main\>  
\<script\>(function(){'use strict';const nodes=document.querySelectorAll('.node'),boards=document.querySelectorAll('.board'),answers=document.querySelectorAll('.answer');document.documentElement.dataset.e06Orbit=nodes.length===9?'nine':'invalid';document.documentElement.dataset.e06Boards=boards.length===9?'nine':'invalid';document.documentElement.dataset.e06Answers=answers.length===45?'45':'invalid';if(nodes.length\!==9\|\|boards.length\!==9\|\|answers.length\!==45)console.warn('E06 integrity failure',{nodes:nodes.length,boards:boards.length,answers:answers.length});})();\</script\>  
\</body\>  
\</html\>

\<\!doctype html\>  
\<html lang="en"\>  
\<head\>  
\<meta charset="utf-8"\>  
\<meta name="viewport" content="width=device-width,initial-scale=1"\>  
\<title\>MAXESS E08 — Human Maximus Codex Ecosystem\</title\>  
\<meta name="description" content="The Human Maximus Codex ecosystem — four learning experiences plus Naya Power AI Supercharger."\>  
\<style\>  
.maxess-e08{--bg:\#020204;--white:\#fff;--gold:\#f5c84b;--green:\#58d88d;--blue:\#62a9ff;--purple:\#aa7dff;--magenta:\#ef55c7;box-sizing:border-box;width:100%;margin:0 auto;padding:clamp(28px,5vw,68px) clamp(16px,3vw,34px) clamp(56px,7vw,96px);background:radial-gradient(circle at 50% 18%,rgba(170,125,255,.11),transparent 30%),radial-gradient(circle at 50% 70%,rgba(255,255,255,.025),transparent 46%),var(--bg);color:var(--white);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden;isolation:isolate}.maxess-e08 \*,.maxess-e08 \*::before,.maxess-e08 \*::after{box-sizing:border-box}.maxess-e08 a{color:inherit;text-decoration:none}.maxess-e08 .e8-shell{width:min(100%,1120px);margin:0 auto}.maxess-e08 .e8-kicker{text-align:center;font-size:10px;font-weight:900;letter-spacing:.3em;text-transform:uppercase;opacity:.7}.maxess-e08 .e8-title{text-align:center;margin:12px auto 10px;max-width:900px;font-size:clamp(34px,5vw,66px);line-height:.94;letter-spacing:-.055em;font-weight:950}.maxess-e08 .e8-lead{text-align:center;max-width:760px;margin:0 auto;color:\#fff;font-size:clamp(15px,1.5vw,19px);line-height:1.5;font-weight:600}  
.maxess-e08 .e8-hero{position:relative;width:min(100%,920px);height:clamp(560px,72vw,760px);margin:clamp(26px,4vw,46px) auto 0}.maxess-e08 .e8-orbit{position:absolute;left:50%;top:50%;width:min(70vw,650px);height:min(70vw,650px);transform:translate(-50%,-50%);border:1px solid rgba(255,255,255,.1);border-radius:50%;box-shadow:0 0 100px rgba(170,125,255,.08),inset 0 0 90px rgba(170,125,255,.025)}.maxess-e08 .e8-orbit::before{content:"";position:absolute;inset:9%;border:1px solid rgba(255,255,255,.035);border-radius:50%}.maxess-e08 .e8-orbit::after{content:"";position:absolute;inset:20%;border:1px dashed rgba(255,255,255,.025);border-radius:50%}  
.maxess-e08 .e8-hub{position:absolute;left:50%;top:50%;width:clamp(180px,23vw,255px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;overflow:hidden;display:grid;place-items:center;background:\#000;border:1px solid rgba(255,255,255,.38);box-shadow:0 0 0 8px rgba(255,255,255,.018),0 0 80px rgba(170,125,255,.25),0 0 150px rgba(170,125,255,.08);z-index:5}.maxess-e08 .e8-hub::before{content:"";position:absolute;inset:6px;border:1px solid rgba(255,255,255,.09);border-radius:50%;z-index:2;pointer-events:none}.maxess-e08 .e8-hub img{display:block;position:relative;width:74%;height:74%;object-fit:contain;z-index:1;filter:drop-shadow(0 12px 28px rgba(0,0,0,.95))}  
.maxess-e08 .e8-node{position:absolute;left:50%;top:50%;width:clamp(118px,14vw,176px);aspect-ratio:1;z-index:7}.maxess-e08 .e8-node--1{transform:translate(-50%,-50%) translateY(calc(min(35vw,320px) \* \-1))}.maxess-e08 .e8-node--2{transform:translate(-50%,-50%) rotate(72deg) translateY(calc(min(35vw,320px) \* \-1)) rotate(-72deg)}.maxess-e08 .e8-node--3{transform:translate(-50%,-50%) rotate(144deg) translateY(calc(min(35vw,320px) \* \-1)) rotate(-144deg)}.maxess-e08 .e8-node--4{transform:translate(-50%,-50%) rotate(216deg) translateY(calc(min(35vw,320px) \* \-1)) rotate(-216deg)}.maxess-e08 .e8-node--5{transform:translate(-50%,-50%) rotate(288deg) translateY(calc(min(35vw,320px) \* \-1)) rotate(-288deg)}  
.maxess-e08 .e8-node-link{display:block;width:100%;height:100%;padding:6px;border-radius:50%;background:var(--accent);border:2px solid rgba(255,255,255,.88);box-shadow:0 0 0 6px rgba(255,255,255,.028),0 0 46px var(--glow),0 18px 42px rgba(0,0,0,.65),inset 0 0 26px rgba(255,255,255,.2);transition:transform .22s ease,box-shadow .22s ease}.maxess-e08 .e8-node-link:hover,.maxess-e08 .e8-node-link:focus-visible{transform:scale(1.06);box-shadow:0 0 0 8px rgba(255,255,255,.05),0 0 68px var(--glow),0 22px 52px rgba(0,0,0,.7),inset 0 0 30px rgba(255,255,255,.24);outline:none}.maxess-e08 .e8-node-link img{display:block;width:100%;height:100%;object-fit:cover;border-radius:50%}.maxess-e08 .e8-node--1{--accent:var(--magenta);--glow:rgba(239,85,199,.7)}.maxess-e08 .e8-node--2{--accent:var(--gold);--glow:rgba(245,200,75,.58)}.maxess-e08 .e8-node--3{--accent:var(--green);--glow:rgba(88,216,141,.58)}.maxess-e08 .e8-node--4{--accent:var(--blue);--glow:rgba(98,169,255,.58)}.maxess-e08 .e8-node--5{--accent:var(--purple);--glow:rgba(170,125,255,.68)}  
.maxess-e08 .e8-stack{max-width:980px;margin:clamp(0px,1vw,12px) auto 0}.maxess-e08 .e8-stack-heading{text-align:center;margin:0 auto clamp(22px,3vw,34px);max-width:900px}.maxess-e08 .e8-stack-heading h2{margin:0 0 9px;font-size:clamp(27px,3.8vw,46px);line-height:1;letter-spacing:-.045em;font-weight:950}.maxess-e08 .e8-stack-heading p{margin:0;color:\#fff;font-size:clamp(15px,1.5vw,18px);line-height:1.45;font-weight:600}.maxess-e08 .e8-card{display:grid;grid-template-columns:190px 1fr;gap:26px;align-items:center;margin:0 0 14px;padding:16px;border:1px solid rgba(255,255,255,.13);border-radius:24px;background:linear-gradient(100deg,rgba(255,255,255,.065),rgba(255,255,255,.025) 48%,rgba(255,255,255,.04));box-shadow:0 18px 48px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.055);transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}.maxess-e08 .e8-card:hover,.maxess-e08 .e8-card:focus-visible{transform:translateY(-2px);box-shadow:0 24px 58px rgba(0,0,0,.4),0 0 28px rgba(170,125,255,.08);border-color:rgba(255,255,255,.28);outline:none}.maxess-e08 .e8-card-media{width:190px;aspect-ratio:16/9;border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.2);box-shadow:0 10px 28px rgba(0,0,0,.45)}.maxess-e08 .e8-card-media img{display:block;width:100%;height:100%;object-fit:cover}.maxess-e08 .e8-card-body{min-width:0;padding:4px 8px 5px 0}.maxess-e08 .e8-card-title{margin:0 0 8px;font-size:clamp(22px,2.8vw,36px);line-height:1.02;font-weight:950;letter-spacing:-.035em}.maxess-e08 .e8-card-kicker{display:block;margin-bottom:12px;font-size:clamp(11px,1.2vw,14px);font-weight:950;letter-spacing:.16em;text-transform:uppercase;color:\#fff}.maxess-e08 .e8-offer-note{display:inline-flex;align-items:center;gap:8px;margin:0 0 14px;padding:7px 12px;border:1px solid rgba(239,85,199,.65);border-radius:999px;background:linear-gradient(90deg,rgba(239,85,199,.18),rgba(255,255,255,.06));color:\#fff;font-size:11px;font-weight:950;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 0 22px rgba(239,85,199,.14)}.maxess-e08 .e8-offer-note::before{content:"✦";color:\#ef55c7}.maxess-e08 .e8-points{display:flex;flex-wrap:wrap;gap:7px 16px;margin:0 0 11px;padding:0;list-style:none}.maxess-e08 .e8-points li{font-size:12px;line-height:1.35;font-weight:800;color:\#fff}.maxess-e08 .e8-points li::before{content:"✦";margin-right:6px;color:var(--accent);font-size:10px}.maxess-e08 .e8-essence{margin:0;color:\#fff;font-size:13px;line-height:1.48;font-weight:600;max-width:760px}.maxess-e08 .e8-essence strong{color:\#fff;font-weight:950}.maxess-e08 .e8-card--1{--accent:var(--magenta);border-color:rgba(239,85,199,.25)}.maxess-e08 .e8-card--2{--accent:var(--gold);border-color:rgba(245,200,75,.22)}.maxess-e08 .e8-card--3{--accent:var(--green);border-color:rgba(88,216,141,.22)}.maxess-e08 .e8-card--4{--accent:var(--blue);border-color:rgba(98,169,255,.22)}.maxess-e08 .e8-card--5{--accent:var(--purple);border-color:rgba(170,125,255,.24)}  
.maxess-e08 .e8-final{text-align:center;max-width:900px;margin:clamp(34px,5vw,62px) auto 0}.maxess-e08 .e8-final h2{margin:0 0 10px;font-size:clamp(28px,4vw,50px);line-height:1;letter-spacing:-.045em;font-weight:950}.maxess-e08 .e8-final p{margin:0;color:\#fff;font-size:clamp(16px,1.7vw,20px);line-height:1.5;font-weight:650}.maxess-e08 .e8-actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:24px}.maxess-e08 .e8-btn{position:relative;isolation:isolate;display:flex;align-items:center;justify-content:center;width:min(700px,95vw);min-height:clamp(78px,7.3vw,112px);padding:2px;border-radius:clamp(18px,1.55vw,25px);border:0;background:linear-gradient(135deg,\#fff6ff 0%,\#e5baff 9%,\#b565ff 23%,\#7a32e5 42%,\#42118d 63%,\#8f42ee 82%,\#e8c0ff 100%);color:\#fff;font-size:clamp(18px,1.55vw,25px);font-weight:900;letter-spacing:-.02em;text-align:center;box-shadow:0 0 0 1px rgba(255,255,255,.28),0 8px 22px rgba(55,14,119,.52),0 20px 55px rgba(74,20,157,.30),0 0 65px rgba(150,69,255,.28),inset 0 1px 1px rgba(255,255,255,.82);transition:transform .22s cubic-bezier(.2,.8,.2,1),filter .22s ease,box-shadow .22s ease}.maxess-e08 .e8-btn::before{content:"";position:absolute;inset:2px;border-radius:clamp(16px,1.4vw,23px);z-index:-2;background:linear-gradient(145deg,\#29222d 0%,\#151117 27%,\#09080b 58%,\#030305 100%);box-shadow:inset 0 1px 2px rgba(255,255,255,.20),inset 0 \-18px 30px rgba(0,0,0,.60)}.maxess-e08 .e8-btn::after{content:"";position:absolute;top:3px;left:12%;width:76%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.78),transparent);opacity:.78;pointer-events:none}.maxess-e08 .e8-btn .e8-btn-copy{display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;z-index:2;text-shadow:0 2px 9px rgba(0,0,0,.95)}.maxess-e08 .e8-btn .e8-btn-title{display:block;font-size:clamp(17px,1.5vw,24px);line-height:1.08;font-weight:850}.maxess-e08 .e8-btn .e8-btn-sub{display:block;margin-top:6px;color:rgba(255,255,255,.78);font-size:clamp(11px,.9vw,14px);line-height:1.15;font-weight:600;letter-spacing:.025em}.maxess-e08 .e8-btn:hover,.maxess-e08 .e8-btn:focus-visible{transform:translateY(-4px);filter:brightness(1.07);box-shadow:0 0 0 1px rgba(255,255,255,.32),0 12px 30px rgba(55,14,119,.60),0 25px 65px rgba(74,20,157,.38),0 0 78px rgba(150,69,255,.34),inset 0 1px 1px rgba(255,255,255,.86);outline:none}.maxess-e08 .e8-btn:active{transform:translateY(1px) scale(.995)}  
@media(max-width:760px){.maxess-e08 .e8-hero{height:520px;margin-top:20px}.maxess-e08 .e8-orbit{width:390px;height:390px}.maxess-e08 .e8-hub{width:170px}.maxess-e08 .e8-node{width:100px}.maxess-e08 .e8-node--1{transform:translate(-50%,-50%) translateY(-190px)}.maxess-e08 .e8-node--2{transform:translate(-50%,-50%) rotate(72deg) translateY(-190px) rotate(-72deg)}.maxess-e08 .e8-node--3{transform:translate(-50%,-50%) rotate(144deg) translateY(-190px) rotate(-144deg)}.maxess-e08 .e8-node--4{transform:translate(-50%,-50%) rotate(216deg) translateY(-190px) rotate(-216deg)}.maxess-e08 .e8-node--5{transform:translate(-50%,-50%) rotate(288deg) translateY(-190px) rotate(-288deg)}.maxess-e08 .e8-card{grid-template-columns:1fr;gap:14px;padding:14px}.maxess-e08 .e8-card-media{width:100%;max-width:none}.maxess-e08 .e8-card-body{padding:0 3px 4px}.maxess-e08 .e8-points{display:block}.maxess-e08 .e8-points li{margin-bottom:5px}.maxess-e08 .e8-title{font-size:clamp(32px,10vw,48px)}.maxess-e08 .e8-card-title{font-size:clamp(24px,8vw,34px)}.maxess-e08 .e8-card-kicker{font-size:12px}.maxess-e08 .e8-offer-note{font-size:10px}.maxess-e08 .e8-btn{width:100%;min-height:88px}.maxess-e08 .e8-btn .e8-btn-title{font-size:19px}.maxess-e08 .e8-btn .e8-btn-sub{font-size:11px}}  
@media(prefers-reduced-motion:reduce){.maxess-e08 .e8-node-link,.maxess-e08 .e8-card,.maxess-e08 .e8-btn{transition:none}}  
\</style\>  
\</head\>  
\<body\>  
\<section class="maxess-e08" aria-label="Human Maximus Codex ecosystem"\>  
\<div class="e8-shell"\>  
\<div class="e8-kicker"\>THE HUMAN MAXIMUS ECOSYSTEM\</div\>  
\<h1 class="e8-title"\>One ecosystem. Five ways to activate your MAX.\</h1\>  
\<p class="e8-lead"\>Master AI. Be Your MAX. Take your power back. Everything connects—and every piece has a purpose.\</p\>  
\<div class="e8-hero" aria-label="Five-part Human Maximus ecosystem"\>  
\<div class="e8-orbit" aria-hidden="true"\>\</div\>  
\<div class="e8-hub"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/human-maximus-codex.png" alt="Human Maximus Codex"\>\</div\>  
\<a class="e8-node e8-node--1" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Naya Power AI Supercharger"\>\<span class="e8-node-link"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-power.jpg" alt="Naya Power"\>\</span\>\</a\>  
\<a class="e8-node e8-node--2" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Human Maximus Pro Max Player"\>\<span class="e8-node-link"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/pro-max-player.jpg" alt="Human Maximus Pro Max Player"\>\</span\>\</a\>  
\<a class="e8-node e8-node--3" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Human Maximus Complete Series"\>\<span class="e8-node-link"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/human-maximus-codex-series.jpg" alt="Human Maximus Complete Series"\>\</span\>\</a\>  
\<a class="e8-node e8-node--4" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Human Maximus AI Masterclass"\>\<span class="e8-node-link"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/ai-masterclass.jpg" alt="Human Maximus AI Masterclass"\>\</span\>\</a\>  
\<a class="e8-node e8-node--5" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Human Maximus Power Seven Days a Week"\>\<span class="e8-node-link"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/power-7-days-a-week.jpg" alt="Human Maximus Power Seven Days a Week"\>\</span\>\</a\>  
\</div\>  
\<div class="e8-stack"\>  
\<div class="e8-stack-heading"\>\<h2\>What’s inside the ecosystem\</h2\>\<p\>Five distinct experiences. One connected mission: help you become the MAX you can be—and make AI work at its MAX for you.\</p\>\</div\>  
\<a class="e8-card e8-card--1" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Open AI Supercharger checkout"\>\<div class="e8-card-media"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/naya-power.jpg" alt="Naya Power"\>\</div\>\<div class="e8-card-body"\>\<h3 class="e8-card-title"\>AI Supercharger\</h3\>\<span class="e8-card-kicker"\>Activate AI to work with you\</span\>\<span class="e8-offer-note"\>✦ Limited · Exclusive with Key 4 ✦\</span\>\<ul class="e8-points"\>\<li\>Pre-tuned for maximum results\</li\>\<li\>Customized for maximum personal fit\</li\>\<li\>Designed to make AI work with you by default\</li\>\</ul\>\<p class="e8-essence"\>\<strong\>In a nutshell:\</strong\> Naya Power turns AI from something you operate into an intelligent partner you can activate, direct and build with—so the power of AI starts working around your goals, your systems and your way of thinking.\</p\>\</div\>\</a\>  
\<a class="e8-card e8-card--2" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Open Pro Max Player checkout"\>\<div class="e8-card-media"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/pro-max-player.jpg" alt="Human Maximus Pro Max Player"\>\</div\>\<div class="e8-card-body"\>\<h3 class="e8-card-title"\>Worldwide Listening \&amp; Learning Center\</h3\>\<span class="e8-card-kicker"\>Human Maximus Pro Max Player\</span\>\<ul class="e8-points"\>\<li\>Explore the Human Maximus library\</li\>\<li\>Listen, learn and experience the chemistry\</li\>\<li\>Take the journey with you anywhere\</li\>\</ul\>\<p class="e8-essence"\>\<strong\>In a nutshell:\</strong\> Some things can be explained. Some things must be experienced. Pro Max Player is the worldwide listening and learning center where the Human Maximus ecosystem becomes something you can hear, explore, feel and live.\</p\>\</div\>\</a\>  
\<a class="e8-card e8-card--3" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Open Human Maximus Codex Library checkout"\>\<div class="e8-card-media"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/human-maximus-codex-series.jpg" alt="Human Maximus Complete Series"\>\</div\>\<div class="e8-card-body"\>\<h3 class="e8-card-title"\>Human Maximus Codex Library\</h3\>\<span class="e8-card-kicker"\>Take Your Power Back\</span\>\<ul class="e8-points"\>\<li\>Discover your power\</li\>\<li\>Activate what is already in you\</li\>\<li\>Be your MAX\</li\>\</ul\>\<p class="e8-essence"\>\<strong\>In a nutshell:\</strong\> The complete Human Maximus journey gives you the perspectives, tools and deeper framework to recognize your power, activate it and become the MAX you can be.\</p\>\</div\>\</a\>  
\<a class="e8-card e8-card--4" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Open AI Masterclass checkout"\>\<div class="e8-card-media"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/ai-masterclass.jpg" alt="Human Maximus AI Masterclass"\>\</div\>\<div class="e8-card-body"\>\<h3 class="e8-card-title"\>AI Masterclass\</h3\>\<span class="e8-card-kicker"\>Learn to Work \&amp; Master AI\</span\>\<ul class="e8-points"\>\<li\>Think with AI\</li\>\<li\>Create and build with AI\</li\>\<li\>Turn AI into real leverage\</li\>\</ul\>\<p class="e8-essence"\>\<strong\>In a nutshell:\</strong\> Learn to work with and master AI—not just prompts. Build the judgment, creativity and practical skill to make intelligent, powerful AI use part of how you think, work and create.\</p\>\</div\>\</a\>  
\<a class="e8-card e8-card--5" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Open Power Seven Days a Week checkout"\>\<div class="e8-card-media"\>\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/power-7-days-a-week.jpg" alt="Human Maximus Power Seven Days a Week"\>\</div\>\<div class="e8-card-body"\>\<h3 class="e8-card-title"\>Power Seven Days a Week\</h3\>\<span class="e8-card-kicker"\>Make Your Power Practical\</span\>\<ul class="e8-points"\>\<li\>Turn insight into action\</li\>\<li\>Build practices that actually stick\</li\>\<li\>Live your power every day\</li\>\</ul\>\<p class="e8-essence"\>\<strong\>In a nutshell:\</strong\> Knowing is not enough. Power Seven Days a Week helps you take what you discover and put it into motion—so growth becomes something you practice, not something you postpone.\</p\>\</div\>\</a\>  
\</div\>  
\<div class="e8-final"\>\<h2\>Master AI. Be Your MAX. Get Paid.\</h2\>\<p\>One connected ecosystem for maximizing the human and the AI—so you can learn, experience, activate and create results.\</p\>\<div class="e8-actions"\>\<a class="e8-btn" href="https\://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab" aria-label="Start your free trial — zero cost to start"\>\<span class="e8-btn-copy"\>\<span class="e8-btn-title"\>START YOUR FREE TRIAL\</span\>\<span class="e8-btn-sub"\>ZERO COST TO START\</span\>\</span\>\</a\>\</div\>\</div\>  
\</div\>  
\</section\>  
\</body\>  
\</html\>

\<\!doctype html\>  
\<html lang="en"\>  
\<head\>  
\<meta charset="utf-8"\>  
\<meta name="viewport" content="width=device-width,initial-scale=1"\>  
\<title\>MAXESS E09 — Member Preview\</title\>  
\<meta name="description" content="A look inside the Human Maximus member experience."\>  
\<style\>  
.maxess-e09{box-sizing:border-box;width:100%;margin:0;padding:clamp(24px,4vw,48px) clamp(14px,3vw,34px) clamp(42px,6vw,72px);background:\#030305;color:\#fff;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden;isolation:isolate}.maxess-e09 \*,.maxess-e09 \*::before,.maxess-e09 \*::after{box-sizing:border-box}.e9-shell{width:min(100%,1180px);margin:0 auto}.e9-kicker{text-align:center;color:\#f4c95d;font-size:10px;font-weight:900;letter-spacing:.3em;text-transform:uppercase;margin:0 0 8px}.e9-title{text-align:center;margin:0 auto 8px;font-size:clamp(28px,4vw,48px);line-height:1;letter-spacing:-.045em;font-weight:950}.e9-sub{text-align:center;margin:0 auto clamp(24px,4vw,42px);max-width:620px;color:rgba(255,255,255,.72);font-size:clamp(14px,1.4vw,17px);line-height:1.45;font-weight:600}.e9-gallery{display:flex;flex-direction:column;align-items:center;gap:clamp(18px,3vw,34px)}.e9-shot{display:block;width:100%;overflow:hidden;border:1px solid rgba(255,255,255,.14);border-radius:20px;background:\#08080b;box-shadow:0 18px 55px rgba(0,0,0,.42);transition:border-color .2s ease,box-shadow .2s ease,transform .2s ease}.e9-shot:hover,.e9-shot:focus-visible{border-color:rgba(173,130,255,.55);box-shadow:0 24px 70px rgba(0,0,0,.5),0 0 34px rgba(173,130,255,.09);transform:translateY(-2px);outline:none}.e9-shot img{display:block;width:100%;height:auto;max-width:100%;margin:0;background:\#08080b}.e9-shot:focus-visible{outline:2px solid \#ad82ff;outline-offset:3px}.e9-login{width:min(100%,980px)}.e9-courses{width:min(100%,1120px)}.e9-nav{width:min(100%,980px)}.e9-final{text-align:center;margin:clamp(28px,5vw,54px) auto 0}.e9-btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 28px;border-radius:999px;background:\#fff;color:\#050507;text-decoration:none;font-size:13px;font-weight:950;letter-spacing:.02em;box-shadow:0 12px 32px rgba(255,255,255,.08);transition:transform .2s ease,box-shadow .2s ease}.e9-btn:hover,.e9-btn:focus-visible{transform:translateY(-2px);box-shadow:0 16px 40px rgba(255,255,255,.14);outline:none}.e9-btn:focus-visible{outline:2px solid \#ad82ff;outline-offset:4px}  
@media(max-width:620px){.maxess-e09{padding:20px 12px 42px}.e9-sub{margin-bottom:24px}.e9-gallery{gap:14px}.e9-shot{border-radius:15px}.e9-btn{width:100%;max-width:360px}}  
@media(prefers-reduced-motion:reduce){.e9-shot,.e9-btn{transition:none}}  
\</style\>  
\</head\>  
\<body\>  
\<section class="maxess-e09" aria-label="Member preview"\>  
\<div class="e9-shell"\>  
\<div class="e9-kicker"\>MEMBER\</div\>  
\<h1 class="e9-title"\>A Look Inside\</h1\>  
\<p class="e9-sub"\>A snapshot of what’s waiting for you inside.\</p\>  
\<div class="e9-gallery"\>  
\<a class="e9-shot e9-login" href="https\://hmclibrary.groovemember.net/home" aria-label="Open Human Maximus member login"\>  
\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/membership-login-preview.png" alt="Human Maximus Codex member login and library" loading="eager"\>  
\</a\>  
\<a class="e9-shot e9-courses" href="https\://hmclibrary.groovemember.net/home" aria-label="Open member courses preview"\>  
\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/membership-courses-preview.png" alt="Member courses and learning area" loading="lazy"\>  
\</a\>  
\<a class="e9-shot e9-nav" href="https\://hmclibrary.groovemember.net/home" aria-label="Open member navigation preview"\>  
\<img src="https\://pub-e1d4c1dd548847f5858993b820f00700.r2.dev/membership-nav-preview.png" alt="Member navigation and Human Maximus ecosystem" loading="lazy"\>  
\</a\>  
\</div\>  
\<div class="e9-final"\>  
\<a class="e9-btn" href="https\://hmclibrary.groovemember.net/home"\>START YOUR FREE TRIAL — ZERO COST\</a\>  
\</div\>  
\</div\>  
\</section\>  
\</body\>  
\</html\>

