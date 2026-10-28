'use strict';
/*
 * activation-v1.js — Smart Search ACTIVATION fix (TEAM BUILD, 2026-10-28).
 * Workspace harness only, NOT live.
 *
 * The known live-baseline failure: Q1–Q3 return the right block at #1, but
 * Open fails — the live chassis navigates to /hub/feed and scroll-jumps to
 * a feed card, or does nothing visible. The mechanism, proven from the
 * harness itself: the panel card's "Open the block" link points at
 * /s/<sn> (see rank-v3.js renderResultCard), and live /s/<sn> paths
 * redirect to the Hub feed — there is no standalone article/block view
 * on live for ANY note. So even a correct #1 with a correct block fails
 * at the Open step: the open TARGET does not serve the block.
 *
 * The fix, at the activation layer (this file): activation resolves a
 * ranked result to the block ITSELF as a standalone view — the block's
 * own rendered content, with NO navigation of any kind. The standalone
 * view is the panel card HTML with its navigation anchor stripped, so
 * the activated view carries no href, no /hub/feed target, no /s/
 * redirect to follow. Activation never falls back to the feed: a result
 * without a block is UNAVAILABLE, stated plainly, never a scroll jump.
 *
 * What this does NOT claim: the live route. Live still needs the Hub
 * lane to serve a standalone block view (either /s/<sn> serving the
 * block itself, or the live panel opening the block view in place the
 * way this activation does). Until that landing exists, this activation
 * is proven in the harness only — the live Open failure is NOT claimed
 * fixed. The remaining live work is named in the report, not hidden.
 *
 * This file changes NO ranking (rank-v3.js untouched) and NO panel
 * shape (integration-v3.js untouched). The five open ranks (exact-
 * phrase spec decision) are untouched and remain owed.
 */
const RANK = require('./rank-v3.js');

function stripAnchors(html) {
  return String(html).replace(/<a\b[^>]*>.*?<\/a\s*>/gi, '');
}

function activateResult(item) {
  const base = { feedScroll: false, feedNavigation: null, openTarget: 'block-itself' };
  if (!item || typeof item !== 'object') {
    return Object.assign({ action: 'unavailable', reason: 'no result to open' }, base);
  }
  const block = item.block;
  if (!block || !block.title) {
    return Object.assign({ action: 'unavailable', reason: 'result carries no block', noteId: item.id || null }, base);
  }
  const cardHtml = RANK.renderResultCard(item);
  const standaloneHtml = stripAnchors(cardHtml);
  return Object.assign({
    action: 'open-block-standalone',
    noteId: item.id,
    title: block.title,
    block: block,
    standaloneHtml: standaloneHtml,
    panelCardHtml: cardHtml,
    matchedTier: item.matchedTier || null,
  }, base);
}

module.exports = { activateResult, stripAnchors };
