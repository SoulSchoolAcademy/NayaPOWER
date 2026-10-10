/**
 * MOCK brain documents — clearly labeled, never mistaken for the real brain.
 * Every surface that serves these must carry backend:"MOCK" and brainSha:"MOCK".
 */
export const MOCK_MANIFEST = {
  brainSha: 'MOCK',
  indexVersion: 'scaffold-mock-0.1.0',
  builtAt: 'scaffold-build-time',
  docCount: 3,
};

export const MOCK_DOCS = [
  {
    id: 'judgment-rule',
    path: 'BRAIN/01-GOVERNANCE/the-judgment-rule.md',
    title: 'The Judgment Rule',
    grammar: 'definition',
    color: 'cyan',
    status: 'CANDIDATE',
    claims: [
      'Obedience without judgment is not service; it is abdication.',
      'If an instruction is wrong — factually, logically, or it would make the system worse — stop, explain why with evidence, and propose the right path.',
      'Hard stops (harm, illegal acts, destroying evidence, breaking trust) are never executed, regardless of who asks.',
    ],
    text: 'The Judgment Rule (Shawn, 2026-09-30, DIRECTOR-STATED, Prime 1). Obedience without judgment is not service; it is abdication.',
  },
  {
    id: 'nine-nodes',
    path: 'BRAIN/03-KERNEL/NODES/README.md',
    title: 'The Nine NayaPOWER Nodes',
    grammar: 'principles',
    color: 'gold',
    status: 'CANDIDATE',
    chips: [
      { n: '1', name: 'SELF', c: 'cyan' },
      { n: '2', name: 'LAW', c: 'cyan' },
      { n: '3', name: 'ACT', c: 'lime' },
      { n: '4', name: 'KNOW', c: 'lime' },
      { n: '5', name: 'PROVE', c: 'gold' },
      { n: '6', name: 'CONNECT', c: 'gold' },
      { n: '7', name: 'VERIFY', c: 'magenta' },
      { n: '8', name: 'LEARN', c: 'magenta' },
      { n: '9', name: 'EVOLVE', c: 'purple' },
    ],
    claims: [
      'The nine NayaPOWER nodes: SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE.',
      'One governed mind, nine functions — each node owns a slice of the organism.',
    ],
    text: 'NayaPOWER runs on nine nodes: SELF LAW ACT KNOW PROVE CONNECT VERIFY LEARN EVOLVE.',
  },
  {
    id: 'awesome-rule',
    path: 'BRAIN/11-KNOWLEDGE/awesome-code.md',
    title: 'The Awesome Rule',
    grammar: 'principles',
    color: 'lime',
    status: 'CANDIDATE',
    claims: [
      "It's only a problem when you're not awesome.",
      'Keep looking for anything that is not good / not awesome — identify it, fix it, don\'t wait to be asked.',
    ],
    text: 'The Awesome Rule (Shawn, 2026-09-30): utter awesomeness is the goal — produce it, be it, share it.',
    // Demonstrates the supersession → correction path end to end in mock.
    supersededBy: {
      claimId: 'awesome-rule-v2',
      retractText: 'An earlier telling reduced the Awesome Rule to "do good work".',
      retractCite: 'MOCK · earlier telling',
      newText: 'Correction — the Awesome Rule is not "do good work". It is: it\'s only a problem when you\'re not awesome. Active, not decorative.',
      newCite: 'MOCK · awesome-rule-v2',
      speakText: 'Actually — let me correct that. The Awesome Rule is not "do good work". It\'s only a problem when you\'re not awesome.',
    },
  },
];
