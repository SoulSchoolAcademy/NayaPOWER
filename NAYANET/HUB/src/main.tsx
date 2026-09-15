import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import './styles/hub-509-baseline.css';
import './styles/hub-509-fullscreen.css';
import './styles/hub-live-surgical.css';
import './styles/hub-feed-extraordinary.css';
import './styles/hub-509-nine-board.css';

const releaseCommit = import.meta.env.VITE_RELEASE_COMMIT || 'development';
document.documentElement.dataset.nayanetRelease = releaseCommit;
document.documentElement.dataset.nayanetCanonical = 'NAYANET-HUB-REACT-CANONICAL';

document.documentElement.dataset.nayanetPresentation = 'NAYA-509-NINE-BOARD';
createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
