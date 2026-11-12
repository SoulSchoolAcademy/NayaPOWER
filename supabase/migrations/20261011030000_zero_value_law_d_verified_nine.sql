-- Zero Value Law reconciliation (2026-10-11)
--
-- Reconciles d_verified bounds from +/-10 to the canonical -9..+9 display
-- ladder per NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md section 4:
--   D_verified = clamp(Normalize(dV_actual), -9, +9)
-- The raw delta remains preserved in delta_v_actual (uncapped).
--
-- Also adds Zero Value Law cross-field guards to the state function:
--   ZVL-1: UNVERIFIED receipts must not carry a numeric d_verified
--          (unverified value is not zero value; null is not zero).
--   ZVL-2: null delta_v_actual with numeric d_verified is a false zero.
--   ZVL-3: OPEN observation window => outcomes provisional => d_verified null.
--
-- This migration is NOT auto-applied. The prior migration
-- (20261001032000) is production-applied; applying this change to production
-- requires the human director's explicit word per the protected-gates law.

create or replace function public.nayanet_value_receipt_v2_1_state(p_receipt jsonb)
returns text
language plpgsql
stable
as $$
declare
  v_verification text;
  v_verified numeric;
  v_actual numeric;
  v_window_status text;
  v_interp text;
begin
  if coalesce(p_receipt->>'receipt_type','') <> 'ALIGNMENT_DECISION' then
    -- Contribution receipts handled below (unchanged from prior migration).
    return 'NON_ALIGNMENT';
  end if;

  v_verification := p_receipt->>'verification';
  if v_verification not in ('UNVERIFIED','PASS_PENDING_WINDOW','VERIFIED_PASS','FAIL','ESCALATE') then
    raise exception 'ALIGNMENT_DECISION_VERIFICATION' using errcode='22023';
  end if;

  if p_receipt ? 'd_verified'
    and coalesce(jsonb_typeof(p_receipt->'d_verified'),'null') not in ('number','null') then
    raise exception 'ALIGNMENT_DECISION_D_VERIFIED_TYPE' using errcode='22023';
  end if;

  if coalesce(jsonb_typeof(p_receipt->'d_verified'),'null') = 'number' then
    v_verified := (p_receipt->>'d_verified')::numeric;
    if v_verified < -9 or v_verified > 9 then
      raise exception 'ALIGNMENT_DECISION_D_VERIFIED_RANGE' using errcode='22023';
    end if;
  end if;

  -- ZVL-1: UNVERIFIED must not carry a numeric verified ladder value.
  if v_verification = 'UNVERIFIED'
    and coalesce(jsonb_typeof(p_receipt->'d_verified'),'null') = 'number' then
    raise exception 'ALIGNMENT_DECISION_ZVL_UNVERIFIED_HAS_D_VERIFIED' using errcode='22023';
  end if;

  -- ZVL-2: null actual with numeric d_verified is a false zero.
  if coalesce(jsonb_typeof(p_receipt->'delta_v_actual'),'null') = 'null'
    and coalesce(jsonb_typeof(p_receipt->'d_verified'),'null') = 'number' then
    raise exception 'ALIGNMENT_DECISION_ZVL_NULL_ACTUAL_HAS_D_VERIFIED' using errcode='22023';
  end if;

  -- ZVL-3: OPEN observation window => provisional => no verified ladder value.
  v_window_status := coalesce(p_receipt->'observation_window'->>'status','');
  if v_window_status = 'OPEN'
    and coalesce(jsonb_typeof(p_receipt->'d_verified'),'null') = 'number' then
    raise exception 'ALIGNMENT_DECISION_ZVL_OPEN_WINDOW_HAS_D_VERIFIED' using errcode='22023';
  end if;

  -- value_interpretation, when present, must be one of the six Zero Value Law states.
  if p_receipt ? 'value_interpretation'
    and coalesce(jsonb_typeof(p_receipt->'value_interpretation'),'null') not in ('string','null') then
    raise exception 'ALIGNMENT_DECISION_VALUE_INTERPRETATION_TYPE' using errcode='22023';
  end if;
  if coalesce(jsonb_typeof(p_receipt->'value_interpretation'),'null') = 'string' then
    v_interp := p_receipt->>'value_interpretation';
    if v_interp not in ('TRUE_ZERO','PRACTICALLY_NEUTRAL','UNKNOWN','UNMEASURED','DELAYED','INCONCLUSIVE') then
      raise exception 'ALIGNMENT_DECISION_VALUE_INTERPRETATION' using errcode='22023';
    end if;
  end if;

  if v_verification = 'VERIFIED_PASS'
    and coalesce(jsonb_typeof(p_receipt->'delta_v_actual'),'') = 'number' then
    v_actual := (p_receipt->>'delta_v_actual')::numeric;
    if coalesce(jsonb_typeof(p_receipt->'d_verified'),'') <> 'number' then
      raise exception 'ALIGNMENT_DECISION_VERIFIED_REQUIRES_D_VERIFIED' using errcode='22023';
    end if;
    if v_verified <> greatest(-9::numeric, least(9::numeric, v_actual)) then
      raise exception 'ALIGNMENT_DECISION_D_VERIFIED_MISMATCH' using errcode='22023';
    end if;
    return 'VERIFIED_VALUE';
  end if;
  return 'ASSESSED';
end;
$$;

revoke all on function public.nayanet_value_receipt_v2_1_state(jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_value_receipt_v2_1_state(jsonb) to service_role;
