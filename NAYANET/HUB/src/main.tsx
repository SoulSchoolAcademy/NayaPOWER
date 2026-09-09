import React from'react';import{createRoot}from'react-dom/client';import App from'./app/App';import'./styles/tokens.css';import'./styles/globals.css';import'./styles/responsive.css';import'./styles/smart-feed-board.css';
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
