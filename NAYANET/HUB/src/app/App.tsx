import { IdentityProvider } from '../identity/session';
import { HubBaselineApp } from '../baseline/HubBaselineApp';

export default function App() {
  return <IdentityProvider><HubBaselineApp /></IdentityProvider>;
}

