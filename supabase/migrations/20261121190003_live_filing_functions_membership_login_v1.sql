-- Live filing: membership login RPCs — 10 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Login throttle, OTP/code flow, sessions, invites.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- login_throttled(p_alias text)
--   live: public.login_throttled — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Is this alias throttled from logging in? (Membership login)
--   captured: pg_get_functiondef(login_throttled) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.login_throttled(p_alias text)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COUNT(*) >= 5 FROM public.login_attempts
  WHERE alias = p_alias AND ok = false AND attempted_at > now() - interval '15 minutes'
$function$;

-- ---------------------------------------------------------------------------
-- record_login_attempt(p_alias text, p_ok boolean)
--   live: public.record_login_attempt — SECURITY DEFINER, language sql, kind f, volatile v
--   purpose (DATABASE.md): Record a login attempt (feeds the throttle). (Membership login)
--   captured: pg_get_functiondef(record_login_attempt) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.record_login_attempt(p_alias text, p_ok boolean)
 RETURNS void
 LANGUAGE sql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  INSERT INTO public.login_attempts (alias, ok) VALUES (p_alias, p_ok)
$function$;

-- ---------------------------------------------------------------------------
-- mship_request_code(p_membership_id uuid, p_alias text)
--   live: public.mship_request_code — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Member requests a login code (email). (Membership login)
--   captured: pg_get_functiondef(mship_request_code) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_request_code(p_membership_id uuid, p_alias text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_code text;
  v_live integer;
  v_member boolean;
  v_mname text;
  v_thread uuid;
  v_pref_email text;
  v_pref_wants boolean;
  v_body text;
BEGIN
  IF p_alias IS NULL OR p_alias = '' THEN RAISE EXCEPTION 'alias required'; END IF;
  -- Throttle: at most 5 live codes per alias per 15 minutes.
  SELECT COUNT(*) INTO v_live FROM public.member_otp_codes
  WHERE membership_id = p_membership_id AND member_alias = p_alias
    AND consumed_at IS NULL AND expires_at > now()
    AND created_at > now() - interval '15 minutes';
  IF v_live >= 5 THEN RAISE EXCEPTION 'too many codes requested'; END IF;
  -- Target check: only real, active, unexpired members get codes.
  SELECT EXISTS (
    SELECT 1 FROM public.membership_members
    WHERE membership_id = p_membership_id AND member_alias = p_alias
      AND status = 'active' AND (expires_at IS NULL OR expires_at > now())
  ) INTO v_member;
  IF NOT v_member THEN RAISE EXCEPTION 'code not sent'; END IF;  -- generic: no oracle
  -- Membership name for the message body.
  SELECT m.name INTO v_mname FROM public.memberships m WHERE m.id = p_membership_id;
  -- 6-digit code (harvested from 003; hash + 10-min expiry + 5-live
  -- throttle bound the brute-force window).
  v_code := lpad((floor(random() * 1000000))::int::text, 6, '0');
  INSERT INTO public.member_otp_codes (membership_id, member_alias, code_hash, expires_at)
  VALUES (p_membership_id, p_alias, public._mship_hash(v_code), now() + interval '10 minutes');
  -- SMART MAIL DELIVERY: the code, plaintext, in the member's own inbox.
  -- This is the ONLY plaintext exposure of the code (the hash is stored).
  v_body := 'Your login code for ' || COALESCE(v_mname, 'the membership') || ' is ' || v_code
    || '. It expires in 10 minutes and works once. Never share it — Naya will never ask for it.';
  INSERT INTO public.smart_mail_threads (subject, from_alias, to_alias, preview)
  VALUES ('Your login code', 'naya', p_alias,
          'Your 6-digit login code — it expires in 10 minutes.')
  RETURNING id INTO v_thread;
  INSERT INTO public.smart_mail_messages (thread_id, from_alias, body)
  VALUES (v_thread, 'naya', v_body);
  -- EMAIL OPT-IN: if the member opted in, ALSO queue an SMTP send.
  SELECT p.email, p.wants_email_codes INTO v_pref_email, v_pref_wants
  FROM public.membership_code_prefs p
  WHERE p.membership_id = p_membership_id AND p.member_alias = p_alias;
  IF FOUND AND COALESCE(v_pref_wants, false)
     AND v_pref_email IS NOT NULL AND v_pref_email <> '' THEN
    INSERT INTO public.pending_email_sends (to_email, subject, body)
    VALUES (v_pref_email,
            'Your ' || COALESCE(v_mname, 'membership') || ' login code',
            'Your login code is ' || v_code
            || '. It expires in 10 minutes and works once.'
            || ' Tip: you can also read it any time in your Smart Mail inbox.');
  END IF;
  RETURN 'sent';
END $function$;

-- ---------------------------------------------------------------------------
-- mship_request_otp(p_membership_id uuid, p_alias text, p_email text)
--   live: public.mship_request_otp — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Member requests a one-time code. (Membership login)
--   captured: pg_get_functiondef(mship_request_otp) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_request_otp(p_membership_id uuid, p_alias text, p_email text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_code text;
  v_live integer;
  v_member boolean;
BEGIN
  IF p_alias IS NULL OR p_alias = '' THEN RAISE EXCEPTION 'alias required'; END IF;
  IF p_email IS NULL OR p_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' THEN
    RAISE EXCEPTION 'valid email required';
  END IF;
  -- Throttle: at most 5 live codes per alias per 15 minutes.
  SELECT COUNT(*) INTO v_live FROM public.member_otp_codes
  WHERE membership_id = p_membership_id AND member_alias = p_alias
    AND consumed_at IS NULL AND expires_at > now()
    AND created_at > now() - interval '15 minutes';
  IF v_live >= 5 THEN RAISE EXCEPTION 'too many codes requested'; END IF;
  -- Target check: only real, active, unexpired members get codes.
  SELECT EXISTS (
    SELECT 1 FROM public.membership_members
    WHERE membership_id = p_membership_id AND member_alias = p_alias
      AND status = 'active' AND (expires_at IS NULL OR expires_at > now())
  ) INTO v_member;
  IF NOT v_member THEN RAISE EXCEPTION 'code not sent'; END IF;  -- generic: no oracle
  -- 6-digit CSPRNG code.
  v_code := lpad((floor(random() * 1000000))::int::text, 6, '0');
  -- NOTE: random() is not CSPRNG-grade; the hash + 10-min expiry + 5-attempt
  -- throttle bound the brute-force window. The mail-worker path (pattern a)
  -- should pass a CSPRNG code via p_code_override when it exists.
  INSERT INTO public.member_otp_codes (membership_id, member_alias, code_hash, expires_at)
  VALUES (p_membership_id, p_alias, public._mship_hash(v_code), now() + interval '10 minutes');
  -- Bind the email hash (verified on successful verify).
  INSERT INTO public.membership_member_emails (membership_id, member_alias, email_hash)
  VALUES (p_membership_id, p_alias, public._mship_hash(lower(p_email)))
  ON CONFLICT (membership_id, member_alias) DO UPDATE
    SET email_hash = EXCLUDED.email_hash;
  RETURN 'sent';
END $function$;

-- ---------------------------------------------------------------------------
-- mship_verify_otp(p_membership_id uuid, p_alias text, p_code text)
--   live: public.mship_verify_otp — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Verify a one-time code (login). (Membership login)
--   captured: pg_get_functiondef(mship_verify_otp) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_verify_otp(p_membership_id uuid, p_alias text, p_code text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_row public.member_otp_codes%ROWTYPE;
  v_token text;
  v_ok boolean := false;
BEGIN
  IF p_alias IS NULL OR p_alias = '' OR p_code IS NULL OR p_code = '' THEN
    RAISE EXCEPTION 'code not accepted';
  END IF;
  IF public.login_throttled(p_alias) THEN
    PERFORM public.record_login_attempt(p_alias, false);
    RAISE EXCEPTION 'too many attempts';
  END IF;
  SELECT * INTO v_row FROM public.member_otp_codes
  WHERE membership_id = p_membership_id AND member_alias = p_alias
    AND consumed_at IS NULL AND expires_at > now()
  ORDER BY created_at DESC LIMIT 1;
  -- Constant-time-ish compare on hashes; generic failure either way.
  IF FOUND AND v_row.code_hash = public._mship_hash(p_code) THEN
    v_ok := true;
  END IF;
  PERFORM public.record_login_attempt(p_alias, v_ok);
  IF NOT v_ok THEN RAISE EXCEPTION 'code not accepted'; END IF;
  -- Single use.
  UPDATE public.member_otp_codes SET consumed_at = now() WHERE id = v_row.id;
  -- Member must STILL be active at verify time (status could have changed).
  IF NOT EXISTS (
    SELECT 1 FROM public.membership_members
    WHERE membership_id = p_membership_id AND member_alias = p_alias
      AND status = 'active' AND (expires_at IS NULL OR expires_at > now())
  ) THEN RAISE EXCEPTION 'code not accepted'; END IF;
  -- Mark the email verified.
  UPDATE public.membership_member_emails SET verified_at = now()
  WHERE membership_id = p_membership_id AND member_alias = p_alias;
  -- Mint: 256-bit CSPRNG, hex. Store ONLY the hash.
  v_token := encode(extensions.gen_random_bytes(32), 'hex');  -- §7 fix
  INSERT INTO public.member_sessions (kind, alias, membership_id, token_hash, expires_at)
  VALUES ('member', p_alias, p_membership_id,
          public._mship_hash(v_token), now() + interval '30 days');
  RETURN v_token;  -- plaintext leaves the DB exactly once, right here
END $function$;

-- ---------------------------------------------------------------------------
-- mship_revoke_session(p_token text)
--   live: public.mship_revoke_session — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Revoke a member session. (Membership login)
--   captured: pg_get_functiondef(mship_revoke_session) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_revoke_session(p_token text)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  UPDATE public.member_sessions
  SET revoked_at = now()
  WHERE token_hash = public._mship_hash(p_token) AND revoked_at IS NULL;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_set_code_pref(p_membership_id uuid, p_alias text, p_email text, p_wants_email boolean)
--   live: public.mship_set_code_pref — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Member sets email-code preference. (Membership login)
--   captured: pg_get_functiondef(mship_set_code_pref) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_set_code_pref(p_membership_id uuid, p_alias text, p_email text, p_wants_email boolean)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_member boolean;
  v_email text := NULLIF(lower(trim(COALESCE(p_email, ''))), '');
  v_email_hash text;
  v_onfile text;
BEGIN
  IF p_alias IS NULL OR p_alias = '' THEN RAISE EXCEPTION 'alias required'; END IF;
  -- Target check: only active members set prefs (generic failure).
  SELECT EXISTS (
    SELECT 1 FROM public.membership_members
    WHERE membership_id = p_membership_id AND member_alias = p_alias
      AND status = 'active' AND (expires_at IS NULL OR expires_at > now())
  ) INTO v_member;
  IF NOT v_member THEN RAISE EXCEPTION 'pref not saved'; END IF;
  IF COALESCE(p_wants_email, false) THEN
    IF v_email IS NULL OR v_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' THEN
      RAISE EXCEPTION 'valid email required';
    END IF;
    v_email_hash := public._mship_hash(v_email);
    SELECT e.email_hash INTO v_onfile FROM public.membership_member_emails e
    WHERE e.membership_id = p_membership_id AND e.member_alias = p_alias;
    IF v_onfile IS NULL THEN
      -- First bind: the member claims this email for the alias.
      INSERT INTO public.membership_member_emails (membership_id, member_alias, email_hash)
      VALUES (p_membership_id, p_alias, v_email_hash);
    ELSIF v_onfile <> v_email_hash THEN
      -- No silent override: the join-bound email wins. Changes are
      -- session-gated (post-login), never pre-login.
      RAISE EXCEPTION 'pref not saved';
    END IF;
    INSERT INTO public.membership_code_prefs (membership_id, member_alias, email, wants_email_codes)
    VALUES (p_membership_id, p_alias, v_email, true)
    ON CONFLICT (membership_id, member_alias) DO UPDATE
      SET email = EXCLUDED.email, wants_email_codes = true, updated_at = now();
    RETURN 'email on';
  ELSE
    INSERT INTO public.membership_code_prefs (membership_id, member_alias, wants_email_codes)
    VALUES (p_membership_id, p_alias, false)
    ON CONFLICT (membership_id, member_alias) DO UPDATE
      SET wants_email_codes = false, updated_at = now();
    RETURN 'smart mail only';
  END IF;
END $function$;

-- ---------------------------------------------------------------------------
-- gen_invite_code()
--   live: public.gen_invite_code — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Mint a new invite code. (Inviter)
--   captured: pg_get_functiondef(gen_invite_code) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.gen_invite_code()
 RETURNS text
 LANGUAGE plpgsql
AS $function$
declare
  alphabet constant text := '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  code text := '';
  i int;
begin
  for i in 1..8 loop
    code := code || substr(alphabet, (floor(random()*32))::int + 1, 1);
  end loop;
  return code;
end $function$;

-- ---------------------------------------------------------------------------
-- redeem_invite(p_membership_id uuid, p_alias text, p_code text, p_email_hash text)
--   live: public.redeem_invite — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Redeem an invite code on joining. (Inviter)
--   captured: pg_get_functiondef(redeem_invite) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.redeem_invite(p_membership_id uuid, p_alias text, p_code text, p_email_hash text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_inv public.membership_invites%ROWTYPE;
BEGIN
  IF p_alias IS NULL OR p_alias = '' OR p_code IS NULL OR p_code = '' THEN
    RAISE EXCEPTION 'alias and code required';
  END IF;
  SELECT * INTO v_inv FROM public.membership_invites
  WHERE membership_id = p_membership_id
    AND code_hash = public._mship_hash(p_code)
  LIMIT 1;
  -- Generic failure: never reveal whether the code was wrong, expired, or used up.
  IF NOT FOUND OR (v_inv.expires_at IS NOT NULL AND v_inv.expires_at <= now())
     OR v_inv.uses >= v_inv.max_uses THEN
    RAISE EXCEPTION 'invite not accepted';
  END IF;
  UPDATE public.membership_invites SET uses = uses + 1 WHERE id = v_inv.id;
  INSERT INTO public.membership_members (membership_id, member_alias, status)
  VALUES (p_membership_id, p_alias, 'pending')
  ON CONFLICT (membership_id, member_alias) DO NOTHING;
  IF p_email_hash IS NOT NULL AND p_email_hash <> '' THEN
    INSERT INTO public.membership_member_emails (membership_id, member_alias, email_hash)
    VALUES (p_membership_id, p_alias, p_email_hash)
    ON CONFLICT (membership_id, member_alias) DO UPDATE SET email_hash = EXCLUDED.email_hash;
  END IF;
  RETURN 'pending';
END $function$;

-- ---------------------------------------------------------------------------
-- owner_alias_for(p_token text)
--   live: public.owner_alias_for — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Resolve the owner alias for a token/session. (Identity)
--   captured: pg_get_functiondef(owner_alias_for) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.owner_alias_for(p_token text)
 RETURNS text
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COALESCE((
    SELECT s.alias FROM public.member_sessions s
    WHERE s.kind = 'owner'
      AND s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL
      AND s.expires_at > now()
    LIMIT 1
  ), '')
$function$;
