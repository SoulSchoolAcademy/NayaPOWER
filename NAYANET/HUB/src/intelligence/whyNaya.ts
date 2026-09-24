import type { IntelligentEvent } from './types';

export type WhyNayaItem = { label: string; text: string };

const text = (value: unknown, fallback: string) => typeof value === 'string' && value.trim() ? value.trim() : fallback;

export function buildWhyNaya(event: IntelligentEvent): WhyNayaItem[] {
  const block = event.intelligent_block;
  const context = event.context || {};
  const interpretation = event.naya_interpretation || {};
  const meaning = event.meaning || {};
  const action = event.action || {};
  const evidence = event.machine_evidence || {};
  const authority = block?.authority || {};
  return [
    { label: 'WHAT NAYA USED', text: `${text(event.source?.label, 'This intelligence')} · ${text(context.topic, 'the recorded context')} · ${Array.isArray(context.tags) && context.tags.length ? context.tags.slice(0, 3).join(', ') : 'no extra tags recorded'}` },
    { label: 'WHAT NAYA UNDERSTOOD', text: text(interpretation.interpretation, text(interpretation.observation, 'No interpretation has been recorded.')) },
    { label: 'WHY IT MATTERS', text: text(meaning.text, text(meaning.significance, 'No significance has been recorded.')) },
    { label: 'WHAT NAYA RECOMMENDS', text: text(action.text, text(interpretation.recommendation, 'No recommendation has been recorded.')) },
    { label: 'WHAT IS VERIFIED', text: `Trust: ${text(event.trust?.level, 'NOT STATED')} · Verification: ${text(evidence.verification_state, 'NOT STATED')} · Authority: ${text(authority.state, 'NOT STATED')}` },
    { label: 'WHAT REMAINS UNCERTAIN', text: text(interpretation.uncertainty, 'No uncertainty has been recorded.') }
  ];
}