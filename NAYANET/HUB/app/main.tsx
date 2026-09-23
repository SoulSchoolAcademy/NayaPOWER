import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import '../styles/canonical.css';

const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-REACT-CANONICAL';

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