(function () {

  "use strict";

  /* ==========================================================
     CANONICAL FREE-TRIAL / ACADEMY CHECKOUT
     ========================================================== */

  const NAYA_POWER_CHECKOUT =
    "https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab";


  /* ==========================================================
     TEXT NORMALIZATION
     ========================================================== */

  function normalize(text) {

    return (text || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();

  }


  /* ==========================================================
     GET ALL LINKS
     ========================================================== */

  const links =
    Array.from(
      document.querySelectorAll("a")
    );


  /* ==========================================================
     MATCH A LINK BY ITS VISIBLE TEXT
     ========================================================== */

  function findLinkByText(matchers) {

    return links.find(function (link) {

      const text =
        normalize(link.textContent);

      return matchers.some(function (matcher) {

        return text === normalize(matcher) ||
               text.includes(normalize(matcher));

      });

    });

  }


  /* ==========================================================
     APPLY CHECKOUT DESTINATION
     ========================================================== */

  function sendToCheckout(link, newLabel) {

    if (!link) {
      return;
    }

    link.href =
      NAYA_POWER_CHECKOUT;

    link.setAttribute(
      "target",
      "_self"
    );

    link.removeAttribute(
      "target"
    );

    link.setAttribute(
      "aria-label",
      newLabel + " — Start Naya Power Free Trial"
    );

    if (newLabel) {

      /*
       * Only change the visible text when the link is the
       * known navigation/portal button.
       *
       * Preserve nested visual elements when possible.
       */

      const title =
        link.querySelector(
          ".ny-title"
        );

      if (title) {

        title.textContent =
          newLabel;

      } else {

        /*
         * If there is no known title element, preserve
         * the existing internal structure whenever possible.
         */

        const textNodes = [];

        const walker =
          document.createTreeWalker(
            link,
            NodeFilter.SHOW_TEXT
          );

        let node;

        while (
          (node = walker.nextNode())
        ) {

          if (
            node.nodeValue &&
            node.nodeValue.trim()
          ) {
            textNodes.push(node);
          }

        }

        /*
         * Replace the first meaningful text node only.
         * This avoids destroying icons or other markup.
         */

        if (textNodes.length) {

          textNodes[0].nodeValue =
            newLabel;

        }

      }

    }

  }


  /* ==========================================================
     01 — FREE GIFTS
     
     The old "Free Gifts" portal becomes:
     START HERE
     ========================================================== */

  const freeGifts =
    findLinkByText([
      "Free Gifts",
      "Free Gifts →",
      "Free Gifts ›"
    ]);

  sendToCheckout(
    freeGifts,
    "Start Here"
  );


  /* ==========================================================
     02 — TAKE YOUR POWER BACK
     ========================================================== */

  const takeYourPowerBack =
    findLinkByText([
      "Take Your Power Back",
      "Take Your Power Back →",
      "Take Your Power Back ›"
    ]);

  sendToCheckout(
    takeYourPowerBack,
    "Take Your Power Back"
  );


  /* ==========================================================
     03 — AI MASTERCLASS
     
     IMPORTANT:
     The AI Masterclass button remains named AI Masterclass.
     Only its destination changes.
     ========================================================== */

  const aiMasterclass =
    findLinkByText([
      "AI Masterclass",
      "AI Masterclass →",
      "AI Masterclass ›"
    ]);

  sendToCheckout(
    aiMasterclass,
    "AI Masterclass"
  );


  /* ==========================================================
     04 — PRO MAX PLAYER
     ========================================================== */

  const proMaxPlayer =
    findLinkByText([
      "ProMax Player",
      "Pro Max Player",
      "ProMAX Player",
      "ProMax Player →",
      "Pro Max Player →"
    ]);

  sendToCheckout(
    proMaxPlayer,
    "ProMax Player"
  );


  /* ==========================================================
     05 — EXISTING START / FREE TRIAL CTA
     
     Catch common labels that may currently point to Services.
     ========================================================== */

  const startCandidates =
    links.filter(function (link) {

      const text =
        normalize(link.textContent);

      return (
        text.includes("free trial") ||
        text === "start here" ||
        text.includes("start your free") ||
        text.includes("experience naya power")
      );

    });


  startCandidates.forEach(function (link) {

    /*
     * Do not touch the lesson CTAs or feedback buttons.
     * Those already use the correct checkout through the
     * Academy layer.
     */

    if (
      link.classList.contains("ny-academy-cta") ||
      link.classList.contains("ny-feel-day")
    ) {
      return;
    }

    link.href =
      NAYA_POWER_CHECKOUT;

    link.setAttribute(
      "target",
      "_self"
    );

    link.removeAttribute(
      "target"
    );

  });


  /* ==========================================================
     06 — EXISTING SECONDARY GRID SAFETY NET
     
     If the portal system uses the known Naya secondary
     classes, explicitly enforce the first four destinations.

     This is deliberately narrow.
     ========================================================== */

  const secondaryButtons =
    Array.from(
      document.querySelectorAll(
        ".ny-secondary-grid .ny-secondary"
      )
    );


  if (secondaryButtons.length) {

    secondaryButtons.forEach(function (button) {

      const text =
        normalize(button.textContent);


      /* Free Gifts → Start Here */

      if (
        text.includes("free gifts")
      ) {

        button.href =
          NAYA_POWER_CHECKOUT;

        const title =
          button.querySelector(".ny-title");

        if (title) {
          title.textContent =
            "Start Here";
        }

        button.setAttribute(
          "aria-label",
          "Start Here — Experience Naya Power Free Trial"
        );

      }


      /* Take Your Power Back */

      else if (
        text.includes("take your power back")
      ) {

        button.href =
          NAYA_POWER_CHECKOUT;

      }


      /* AI Masterclass */

      else if (
        text.includes("ai masterclass")
      ) {

        button.href =
          NAYA_POWER_CHECKOUT;

      }


      /* ProMax Player */

      else if (
        text.includes("promax player") ||
        text.includes("pro max player")
      ) {

        button.href =
          NAYA_POWER_CHECKOUT;

      }

    });

  }


  /* ==========================================================
     07 — FINAL CANONICALITY PASS
     
     Prevent accidental Services-page routing on the known
     Academy-entry buttons.
     ========================================================== */

  [
    freeGifts,
    takeYourPowerBack,
    aiMasterclass,
    proMaxPlayer
  ].forEach(function (link) {

    if (!link) {
      return;
    }

    link.href =
      NAYA_POWER_CHECKOUT;

    link.setAttribute(
      "target",
      "_self"
    );

    link.removeAttribute(
      "target"
    );

  });


