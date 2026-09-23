/* NayaNET name-first identity adapter.
 * One adapter only: Welcome/Identity -> existing Supabase Auth -> members -> nayanet_profiles.
 * The NayaNET alias is an application namespace, not an email address.
 * Canonical browser session: Supabase Auth persistence is the session authority.
 * Runtime verification is intentionally performed against the live Supabase Auth boundary.
 */
(function (global) {
  const SUPABASE_URL = 'https://dahisasgpfvziswqvmvm.supabase.co';
  const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue';

  let clientPromise;

  function loadSupabase() {
    if (global.supabase?.createClient) return Promise.resolve(global.supabase);
    if (clientPromise) return clientPromise;
    clientPromise = new Promise((resolve, reject) => {
      const existing = document.querySelector('script[data-nayanet-supabase]');
      if (existing) {
        existing.addEventListener('load', () => resolve(global.supabase), { once: true });
        existing.addEventListener('error', reject, { once: true });
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
      script.async = true;
      script.dataset.nayanetSupabase = 'true';
      script.onload = () => global.supabase ? resolve(global.supabase) : reject(new Error('Supabase client failed to load'));
      script.onerror = () => reject(new Error('Unable to load Supabase client'));
      document.head.appendChild(script);
    });
    return clientPromise;
  }

  async function getClient() {
    const sdk = await loadSupabase();
    if (!sdk?.createClient) throw new Error('Supabase client unavailable');
    if (!global.__NayaNETSupabaseClient) {
      global.__NayaNETSupabaseClient = sdk.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
        auth: {
          persistSession: true,
          autoRefreshToken: true,
          detectSessionInUrl: true,
          storage: global.localStorage,
          storageKey: 'nayanet.supabase.auth'
        }
      });
    }
    return global.__NayaNETSupabaseClient;
  }

  function cleanName(value) {
    return String(value || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  }

  function cleanAlias(value) {
    return String(value || '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 48);
  }

  async function provision(client, user, smartName, smartAlias) {
    const { error: metadataError } = await client.auth.updateUser({
      data: {
        display_name: smartName,
        full_name: smartName,
        smart_name: smartName,
        smart_alias: smartAlias,
        nayanet_identity_version: 'name-first-v1'
      }
    });
    if (metadataError) throw metadataError;

    const { error: memberError } = await client
      .from('members')
      .upsert({ id: user.id, display_name: smartName }, { onConflict: 'id' });
    if (memberError) throw memberError;

    const smartId = smartAlias || ('member-' + user.id.replace(/-/g, '').slice(0, 16));

    // The profile has two uniqueness boundaries: member_id and smart_id.
    // Upserting on member_id alone turns an alias collision into an opaque
    // database error. Resolve the alias boundary explicitly so the human
    // gets a truthful, actionable result and repeated identity establishment
    // remains idempotent for the same member.
    const { data: existingByAlias, error: aliasLookupError } = await client
      .from('nayanet_profiles')
      .select('member_id,smart_id,public_alias')
      .eq('smart_id', smartId)
      .maybeSingle();
    if (aliasLookupError) throw aliasLookupError;
    if (existingByAlias && existingByAlias.member_id !== user.id) {
      throw new Error('NAYANET_ADDRESS_TAKEN');
    }

    const { error: profileError } = await client
      .from('nayanet_profiles')
      .upsert({
        member_id: user.id,
        smart_id: smartId,
        public_alias: smartAlias || null,
        recovery_ready: false
      }, { onConflict: 'member_id' });
    if (profileError) throw profileError;

    return { userId: user.id, smartName, smartAlias, smartId };
  }

  async function establish({ name, alias } = {}) {
    const smartName = cleanName(name);
    const smartAlias = cleanAlias(alias || smartName);
    if (!smartName) throw new Error('NAME_REQUIRED');
    if (!smartAlias) throw new Error('ALIAS_REQUIRED');

    const client = await getClient();
    let sessionResult = await client.auth.getSession();
    let session = sessionResult.data?.session || null;

    if (!session) {
      const result = await client.auth.signInAnonymously({
        options: {
          data: {
            display_name: smartName,
            full_name: smartName,
            smart_name: smartName,
            smart_alias: smartAlias,
            nayanet_identity_version: 'name-first-v1'
          }
        }
      });
      if (result.error) {
        if (result.error.message === 'Anonymous sign-ins are disabled' || result.error.code === 'anonymous_provider_disabled') {
          throw new Error('ANONYMOUS_AUTH_DISABLED');
        }
        throw result.error;
      }
      session = result.data?.session || null;
    }

    if (!session?.user?.id) throw new Error('AUTH_SESSION_NOT_ESTABLISHED');
    const identity = await provision(client, session.user, smartName, smartAlias);

    localStorage.setItem('nayanet_smart_name', smartName);
    localStorage.setItem('nayanet_smart_alias', smartAlias);
    sessionStorage.setItem('nayanet_user_name', smartName);

    return {
      ...identity,
      sessionId: session.user.id,
      isAnonymous: !!session.user.is_anonymous,
      authenticated: true
    };
  }

  async function current() {
    const client = await getClient();
    const { data, error } = await client.auth.getSession();
    if (error) throw error;
    const session = data.session;
    if (!session?.user?.id) return null;
    return {
      access_token: session.access_token,
      userId: session.user.id,
      isAnonymous: !!session.user.is_anonymous,
      authenticated: true,
      smartName: session.user.user_metadata?.smart_name || session.user.user_metadata?.display_name || '',
      smartAlias: session.user.user_metadata?.smart_alias || ''
    };
  }

  global.NayaNETNameFirstAuth = Object.freeze({ establish, current });
})(window);
