/* =========================================================
   MAXIS QUESTION BANK — NAYA POWER MASTERY
   "What's your Naya Power score?"
   ---------------------------------------------------------
   Data only. The Maxis engine renders any bank in this shape.
   Scoring: each answer carries a hidden 0–100 value
   (the 0–4 mastery scale normalized: value/4*100).
   Answer positions are deliberately NOT ordered by value —
   never expose the numbers to the taker.
   ========================================================= */
window.MAXIS_BANK = {

  id: "naya-power",
  version: "1.0.0",
  title: "Naya Power Assessment",
  kicker: "WHAT'S YOUR NAYA POWER SCORE?",

  dimensions: [
    { id: "naya-awareness", name: "Naya Awareness", color: "#39ddd2", weight: 1 },
    { id: "ai-empowerment", name: "AI Empowerment", color: "#8a5cff", weight: 1 },
    { id: "human-empowerment", name: "Human Empowerment", color: "#ffd45a", weight: 1 },
    { id: "collaboration", name: "AI·Human Collaboration", color: "#35e39b", weight: 1 },
    { id: "trust", name: "Trust & Proof", color: "#3ca8ff", weight: 1 }
  ],

  scoreBands: [
    {
      min: 90, max: 100, label: "Naya Master", color: "#ffd45a",
      description: "You don't just use Naya Power — you direct it. You understand what Naya is, how to aim her, and how the partnership multiplies what you can do. Your next opportunity is turning mastery into leverage: systems, workflows, and results that compound."
    },
    {
      min: 75, max: 89.99, label: "Advancing", color: "#35e39b",
      description: "You have real Naya Power capability and you're moving beyond basic use. The next leap comes from becoming more deliberate: clearer direction, sharper judgment of results, and letting Naya's memory compound for you."
    },
    {
      min: 60, max: 74.99, label: "Developing", color: "#3ca8ff",
      description: "You have a working foundation and clear potential. With better direction, stronger evaluation habits, and a real partnership rhythm with Naya, your results can become dramatically more powerful."
    },
    {
      min: 0, max: 59.99, label: "Foundation", color: "#8a5cff",
      description: "You're at the beginning of a valuable journey. Naya Power isn't about learning a tool — it's about learning a new way to work: you direct, Naya builds, and together you get somewhere neither could reach alone."
    }
  ],

  /* Interest areas for the personalization step (bank-driven) */
  interestsTitle: "Where do you want Naya Power to become more useful to you?",
  interestAreas: [
    { id: "smart-apps", name: "Smart Apps", description: "Describe ideas in plain words and get working apps.", color: "#8a5cff" },
    { id: "memory", name: "Memory & Smart Notes", description: "Never lose what matters. Naya remembers.", color: "#39ddd2" },
    { id: "stats", name: "Smart Stats & Maxis", description: "Scores, patterns, and intelligence reports.", color: "#ffd45a" },
    { id: "collab", name: "Working with Naya", description: "A real partnership rhythm with your AI.", color: "#35e39b" },
    { id: "hub", name: "The NayaNET Hub", description: "Your cockpit for everything Naya.", color: "#3ca8ff" },
    { id: "voice", name: "Voice & Audio", description: "Talk to Naya. Get audio briefings back.", color: "#ed42c4" },
    { id: "growth", name: "Learning & Growth", description: "Get measurably better, on purpose.", color: "#b8ee57" },
    { id: "business", name: "Business & Strategy", description: "Turn goals into plans into results.", color: "#ff9a5a" },
    { id: "content", name: "Content Creation", description: "Ideas into posts, scripts, and stories.", color: "#f1d75a" },
    { id: "research", name: "Research & Answers", description: "Deep answers from real sources.", color: "#55b9ee" },
    { id: "automation", name: "Automation", description: "Repeating work that runs itself.", color: "#ff7a3d" },
    { id: "community", name: "Community & Spaces", description: "Gather people around what matters.", color: "#ff5a6e" },
    { id: "ledger", name: "Smart Ledger", description: "Every action, receipted. Proof of what happened.", color: "#40d3bb" },
    { id: "powercasts", name: "Powercasts", description: "Listen to intelligence. Naya's audio briefings.", color: "#c084fc" },
    { id: "privacy", name: "Privacy & Control", description: "Your data, your rules. Granular permissions.", color: "#94a3b8" },
    { id: "maxis-lib", name: "Maxis Library", description: "Every assessment, every score, one shelf.", color: "#f1d75a" },
    { id: "lists", name: "Smart Lists", description: "Keep what matters. Lists that think.", color: "#b8ee57" },
    { id: "settings", name: "Settings & You", description: "Tune Naya to exactly how you work.", color: "#a855f7" }
  ],

  questions: [

    /* ============ DIMENSION 1 — NAYA AWARENESS ============ */
    {
      id: "what-is-naya",
      dimensionId: "naya-awareness",
      order: 1,
      label: "NAYA AWARENESS",
      teaching: "Naya isn't a chatbot you prompt and forget. She's an AI operating partner — she retains knowledge, understands it, and puts it to work for you, across every conversation.",
      question: "How would you describe what Naya is?",
      answers: [
        ["naya-partner", "An operating partner", "She works with me, remembers, and compounds what we do.", 100, "#39ddd2", "◆"],
        ["naya-assistant", "A smart assistant", "She helps me get things done when I ask.", 75, "#35e39b", "✦"],
        ["naya-chatbot", "A chatbot", "I chat with her like any AI chat app.", 50, "#3ca8ff", "△"],
        ["naya-search", "A search tool", "I use her to look things up.", 25, "#8a5cff", "✧"],
        ["naya-unsure", "Not really sure", "I've heard the name but that's about it.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "what-is-nayanet",
      dimensionId: "naya-awareness",
      order: 2,
      label: "NAYA AWARENESS",
      teaching: "NayaNET is a governed intelligence network with a simple promise: your idea, your intelligence, your Smart App — your internet, your way. It's built for you, not for advertisers.",
      question: "What is NayaNET, at its core?",
      answers: [
        ["net-mine", "My intelligence, my way", "A network where I create Smart Apps from my ideas.", 75, "#35e39b", "✦"],
        ["net-describe", "Describe → get apps", "I describe what I imagine and NayaNET builds it.", 50, "#3ca8ff", "△"],
        ["net-promise", "Your internet, your way", "A personal net: my idea, my intelligence, my Smart App.", 100, "#39ddd2", "◆"],
        ["net-social", "A social network", "A place to connect with people, like other networks.", 25, "#8a5cff", "✧"],
        ["net-unsure", "Not sure yet", "I haven't learned what makes it different.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "one-brain",
      dimensionId: "naya-awareness",
      order: 3,
      label: "NAYA AWARENESS",
      teaching: "One brain, every AI. NayaPOWER doesn't replace the AI you already use — it plugs into it. Muse, ChatGPT, Claude, local agents: one user-owned brain underneath them all.",
      question: "A friend asks: does NayaPOWER replace my ChatGPT or Claude?",
      answers: [
        ["brain-no", "No — it unifies them", "It rides on top of the AI I already use. One brain, every AI.", 100, "#39ddd2", "◆"],
        ["brain-maybe", "It works alongside", "I can keep my AI and Naya connects to it.", 75, "#35e39b", "✦"],
        ["brain-replace", "Yes, it replaces them", "It's a new AI that takes the place of the others.", 25, "#8a5cff", "✧"],
        ["brain-compete", "It's a competitor", "Another AI app fighting for my attention.", 50, "#3ca8ff", "△"],
        ["brain-unsure", "I don't know", "I haven't thought about how it fits.", 0, "#ed42c4", "✦"]
      ]
    },

    /* ============ DIMENSION 2 — AI EMPOWERMENT ============ */
    {
      id: "smart-apps-way",
      dimensionId: "ai-empowerment",
      order: 4,
      label: "AI EMPOWERMENT",
      teaching: "The Naya Power way to build: describe what you imagine in everyday language. NayaPOWER handles the design, the engineering, the permissions, and the testing — then proves it works.",
      question: "You have an idea for an app. What's the Naya Power way to build it?",
      answers: [
        ["app-hire", "Hire a developer", "Find someone technical to build it for me.", 25, "#8a5cff", "✧"],
        ["app-describe", "Describe it to Naya", "I explain what I want in plain words; Naya designs, builds, and proves it.", 100, "#8a5cff", "◆"],
        ["app-learn", "Learn to code first", "I need to become a programmer before I can build.", 50, "#3ca8ff", "△"],
        ["app-template", "Find a template", "Search for something close and customize it.", 75, "#35e39b", "✦"],
        ["app-giveup", "Give up on it", "Ideas like mine never get built.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "direction-matters",
      dimensionId: "ai-empowerment",
      order: 5,
      label: "AI EMPOWERMENT",
      teaching: "Great results start before the answer. The clearer you are about the destination — the goal, the audience, what success looks like — the more power Naya can aim at it.",
      question: "Before asking Naya to create something important, what matters most?",
      answers: [
        ["dir-prompt", "A clever prompt", "The trick is finding the right magic words.", 50, "#3ca8ff", "△"],
        ["dir-destination", "A clear destination", "I define the goal, the audience, and what great looks like.", 100, "#8a5cff", "◆"],
        ["dir-details", "Lots of details", "I dump everything I know and hope for the best.", 75, "#35e39b", "✦"],
        ["dir-short", "Keep it short", "Less is more — let the AI figure it out.", 25, "#8a5cff", "✧"],
        ["dir-none", "Nothing special", "I just ask and take what comes back.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "evaluate-result",
      dimensionId: "ai-empowerment",
      order: 6,
      label: "AI EMPOWERMENT",
      teaching: "Something can look good and still be wrong. Empowered people don't ask 'do I like this?' — they ask 'does this actually work?' Then they aim Naya at what's weak.",
      question: "Naya delivers a result that looks great. How do you judge it?",
      answers: [
        ["eval-like", "I like it — ship it", "If it looks good, it's good enough.", 25, "#8a5cff", "✧"],
        ["eval-works", "Does it actually work?", "I check it against the goal, the audience, and what matters.", 100, "#8a5cff", "◆"],
        ["eval-compare", "Compare to my idea", "I see if it matches what I pictured.", 75, "#35e39b", "✦"],
        ["eval-ask", "Ask Naya if it's good", "She made it, so she should know.", 50, "#3ca8ff", "△"],
        ["eval-skip", "I don't judge it", "I assume the AI got it right.", 0, "#ed42c4", "✦"]
      ]
    },

    /* ============ DIMENSION 3 — HUMAN EMPOWERMENT ============ */
    {
      id: "who-directs",
      dimensionId: "human-empowerment",
      order: 7,
      label: "HUMAN EMPOWERMENT",
      teaching: "In the Naya Power model, you are the director and Naya is the engine. Every decision is measured one way: does this help the human grow — or does it hurt?",
      question: "In the Naya Power model, who is in charge?",
      answers: [
        ["dir-ai", "The AI", "It's smarter, so it should lead.", 0, "#ed42c4", "✦"],
        ["dir-human", "I am — always", "Naya serves my growth. I'm the director, she's the engine.", 100, "#ffd45a", "◆"],
        ["dir-share", "We share it", "It depends on the situation.", 75, "#35e39b", "✦"],
        ["dir-naya", "Naya, mostly", "She knows more than I do about most things.", 25, "#8a5cff", "✧"],
        ["dir-unsure", "Never thought about it", "I just use the tools.", 50, "#3ca8ff", "△"]
      ]
    },
    {
      id: "proactive-naya",
      dimensionId: "human-empowerment",
      order: 8,
      label: "HUMAN EMPOWERMENT",
      teaching: "Ten-star Naya doesn't wait to be asked. She acts like a team member: she sees what would help, does what she can, and reports back — what happened, why, and what's next.",
      question: "What should you expect Naya to do without being asked?",
      answers: [
        ["pro-nothing", "Nothing — wait for orders", "An AI should never act on its own.", 25, "#8a5cff", "✧"],
        ["pro-member", "Act like a team member", "Handle what she can, then report what, why, and what's next.", 100, "#ffd45a", "◆"],
        ["pro-suggest", "Suggest, don't do", "She can recommend but never act.", 50, "#3ca8ff", "△"],
        ["pro-small", "Only tiny tasks", "Small things are fine; everything else needs permission.", 75, "#35e39b", "✦"],
        ["pro-everything", "Everything, no limits", "Full autonomy over my life and accounts.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "hear-intent",
      dimensionId: "human-empowerment",
      order: 9,
      label: "HUMAN EMPOWERMENT",
      teaching: "Naya tunes to your intent, not your literal words. If your message comes out garbled, she hears what you meant — and if it truly matters, she'll check rather than guess.",
      question: "Your message to Naya comes out garbled. What happens?",
      answers: [
        ["intent-guess", "She guesses wildly", "Takes a shot in the dark.", 25, "#8a5cff", "✧"],
        ["intent-literal", "Takes it literally", "Does exactly what the garbled words say.", 50, "#3ca8ff", "△"],
        ["intent-hears", "Hears what I meant", "Tunes to my intent; checks with me when it matters.", 100, "#ffd45a", "◆"],
        ["intent-error", "Throws an error", "Refuses to continue until I retype.", 75, "#35e39b", "✦"],
        ["intent-ignore", "Ignores it", "Pretends it never happened.", 0, "#ed42c4", "✦"]
      ]
    },

    /* ============ DIMENSION 4 — AI·HUMAN COLLABORATION ============ */
    {
      id: "memory-compounds",
      dimensionId: "collaboration",
      order: 10,
      label: "AI·HUMAN COLLABORATION",
      teaching: "Every conversation with Naya can compound. She retains what matters — decisions, lessons, your world — so you never start from zero again. Intelligence that doesn't compound is just trivia.",
      question: "Why does it matter that Naya remembers?",
      answers: [
        ["mem-zero", "Never start from zero", "Each conversation builds on the last. That's compounding.", 100, "#35e39b", "◆"],
        ["mem-nice", "It's convenient", "Saves me repeating myself.", 75, "#39ddd2", "✦"],
        ["mem-creepy", "It's risky", "I'd rather she forget everything.", 25, "#8a5cff", "✧"],
        ["mem-unsure", "Doesn't matter much", "Each chat is its own thing.", 50, "#3ca8ff", "△"],
        ["mem-no", "She shouldn't", "Memory in AI is a bad idea.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "active-intelligence",
      dimensionId: "collaboration",
      order: 11,
      label: "AI·HUMAN COLLABORATION",
      teaching: "Active Intelligence isn't stored — it's working. Firing, retrieving, flowing, compounding. The test is simple: it's only awesome if it works, in your life, right now.",
      question: "What makes intelligence 'active' in Naya Power?",
      answers: [
        ["active-files", "Lots of saved files", "Storing everything in organized folders.", 25, "#8a5cff", "✧"],
        ["active-working", "It works, live", "Firing, retrieving, compounding — useful in the moment.", 100, "#35e39b", "◆"],
        ["active-smart", "Sounding smart", "Impressive answers on demand.", 50, "#3ca8ff", "△"],
        ["active-fast", "Being fast", "Instant responses to anything.", 75, "#39ddd2", "✦"],
        ["active-none", "No such thing", "Intelligence is intelligence.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "maxis-value",
      dimensionId: "collaboration",
      order: 12,
      label: "AI·HUMAN COLLABORATION",
      teaching: "Maxis turns understanding into something you can see: a score, a pattern, a report. What gets measured gets mastered — and Naya doesn't just show you the number, she reads it with you.",
      question: "What does a Maxis score give you?",
      answers: [
        ["maxis-grade", "A grade", "A label that judges me.", 25, "#8a5cff", "✧"],
        ["maxis-map", "A map of me", "Where I'm strong, where my leverage is, and what to do next.", 100, "#35e39b", "◆"],
        ["maxis-number", "Just a number", "A score with no meaning behind it.", 50, "#3ca8ff", "△"],
        ["maxis-compare", "Bragging rights", "Something to compare against others.", 75, "#39ddd2", "✦"],
        ["maxis-none", "Nothing useful", "Scores are meaningless.", 0, "#ed42c4", "✦"]
      ]
    },

    /* ============ DIMENSION 5 — TRUST & PROOF ============ */
    {
      id: "connection-permission",
      dimensionId: "trust",
      order: 13,
      label: "TRUST & PROOF",
      teaching: "Connection is not permission. Naya can connect to your calendar, your inbox, your tools — but authority to act travels separately, with the message, every time. A connection never quietly becomes control.",
      question: "Naya connects to your calendar. What can she do?",
      answers: [
        ["perm-all", "Anything she wants", "A connection means full access.", 0, "#ed42c4", "✦"],
        ["perm-separate", "Only what's authorized", "Connection ≠ permission. Authority travels with each request.", 100, "#3ca8ff", "◆"],
        ["perm-read", "Read but never act", "She can look, but that's all, forever.", 50, "#39ddd2", "△"],
        ["perm-ask", "Ask every single time", "Even tiny reads need my explicit yes.", 75, "#35e39b", "✦"],
        ["perm-unsure", "Not sure", "I haven't thought about it.", 25, "#8a5cff", "✧"]
      ]
    },
    {
      id: "proof-not-claims",
      dimensionId: "trust",
      order: 14,
      label: "TRUST & PROOF",
      teaching: "In Naya Power, 'done' is never a claim — it's evidence. Implemented isn't verified, rendered isn't working, and a link isn't proof. Show the work, or it didn't happen.",
      question: "Naya says a feature is done. What proves it?",
      answers: [
        ["proof-word", "Her word", "She said it, that's enough.", 25, "#8a5cff", "✧"],
        ["proof-evidence", "Evidence I can check", "A working demo, a test result, something I can verify myself.", 100, "#3ca8ff", "◆"],
        ["proof-link", "A link to it", "If there's a URL, it must be real.", 50, "#39ddd2", "△"],
        ["proof-detail", "A detailed report", "A thorough write-up of what was done.", 75, "#35e39b", "✦"],
        ["proof-none", "Nothing needed", "Trust the process.", 0, "#ed42c4", "✦"]
      ]
    },
    {
      id: "honest-naya",
      dimensionId: "trust",
      order: 15,
      label: "TRUST & PROOF",
      teaching: "The honesty covenant: a 7.5 defended honestly always beats a 9.0 wished for. Naya tells you plainly where things stand — even when the truth is uncomfortable. That's what makes her trustworthy.",
      question: "Which Naya do you trust more?",
      answers: [
        ["trust-flatter", "The one who flatters", "Always positive, never a bad word.", 25, "#8a5cff", "✧"],
        ["trust-honest", "The honest one", "Plain truth, even uncomfortable — a 7.5 defended beats a 9.0 wished.", 100, "#3ca8ff", "◆"],
        ["trust-agree", "The one who agrees", "Always on my side, whatever I say.", 50, "#39ddd2", "△"],
        ["trust-quiet", "The quiet one", "Says little, so there's little to doubt.", 75, "#35e39b", "✦"],
        ["trust-none", "Trust no AI", "They're all just guessing.", 0, "#ed42c4", "✦"]
      ]
    }

  ]
};
