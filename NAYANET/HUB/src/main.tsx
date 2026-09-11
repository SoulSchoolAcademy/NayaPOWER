import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import './styles/tokens.css';
import './styles/globals.css';
import './styles/responsive.css';
import './styles/smart-feed-board.css';
import './styles/nayanet-v3.css';
import './styles/nayanet-elite-feed.css';
import './styles/hub-reconstruction-v1.css';
import './styles/hub-intelligence-v10.css';
import './styles/hub-intelligence-v11.css';
import './styles/hub-intelligence-v12.css';
import './styles/feed-edge-to-edge.css';
const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-REACT-CANONICAL';
// Naya Power release-probe marker: this line is intentionally behavior-neutral.
// Its purpose is to force the canonical source → build → deploy → runtime proof chain.
// V2 promotion is the sole production release authority.
// Release-authority hardening verified: competing V1 path removed.
createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
