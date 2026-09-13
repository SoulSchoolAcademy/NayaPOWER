import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import { CANONICAL_EXPERIENCE_MARKERS } from './config/canonical-experience-markers';
import './styles/hub-509-baseline.css';

const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-REACT-CANONICAL';
if (CANONICAL_EXPERIENCE_MARKERS.length === 0) console.warn('Canonical experience markers unavailable');

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
