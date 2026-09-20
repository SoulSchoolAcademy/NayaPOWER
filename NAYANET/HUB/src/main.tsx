import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import './styles/tokens.css';
import './styles/feature-surfaces.css';
import './styles/globals.css';
import './styles/responsive.css';
import './styles/smart-feed-board.css';
import './styles/smart-board-apply-use.css';
import './styles/nayanet-v3.css';
import './styles/nayanet-elite-feed.css';
import './styles/hub-reconstruction-v1.css';
import './styles/hub-intelligence-v10.css';
import './styles/hub-intelligence-v11.css';
import './styles/hub-intelligence-v12.css';
import './styles/feed-edge-to-edge.css';
import './styles/hub-intelligent-block-v1.css';
import './styles/intelligent-hub-command-center-v1.css';
import './styles/hub-restored-primo-v1.css';
import './styles/hub-right-rail.css';
import './styles/smart-feed-surgical-elevation.css';
import './styles/smart-board-complete-edge.css';
import './styles/sparkling-shape-reactive.css';
import './styles/hub-aaa-elevation-v1.css';
const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-REACT-CANONICAL';
// Naya Power release-probe marker: this line is intentionally behavior-neutral.
// Its purpose is to force the canonical source → build → deploy → runtime proof chain.
// V2 promotion is the sole production release authority.
// Release-authority hardening verified: competing V1 path removed.
// Canonical React Build Handoff: immutable artifact identity is required before runtime promotion.
const hubIdentity = (window as Window & { NayaNETNameFirstAuth?: { establish(input:{name:string;alias:string}): Promise<{authenticated:boolean;userId:string;smartName:string;smartAlias:string}> } }).NayaNETNameFirstAuth;
async function bootstrapNameFirstHubSession() {
  const params = new URLSearchParams(window.location.search);
  const name = params.get('name')?.trim();
  const alias = params.get('alias')?.trim();
  if (!name || !alias || !hubIdentity) return;
  try {
    const identity = await hubIdentity.establish({ name, alias });
    if (identity?.authenticated && identity?.userId) {
      window.history.replaceState({}, document.title, window.location.pathname + window.location.hash);
    }
  } catch (error) {
    console.error('NAYANET_HUB_IDENTITY_BOOTSTRAP_FAILED', error);
  }
}
bootstrapNameFirstHubSession().finally(() => {
  createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
});
