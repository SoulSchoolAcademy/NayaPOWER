import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import './styles/hub-509-baseline.css';
import './styles/hub-509-fullscreen.css';

const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-509-CANONICAL';

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
