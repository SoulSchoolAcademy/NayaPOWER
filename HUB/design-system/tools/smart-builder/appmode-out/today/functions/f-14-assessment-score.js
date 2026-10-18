/* NayaFunction: f-14-assessment-score v1.0.0
   What: Questions -> answers -> score -> explained report with bands (MAXESS engine, harvested verbatim)
   Activation: <div data-fn="f-14-assessment-score" data-fn-config='{...}'></div>
   Config: {
     assessment: { id*, version*, title, dimensions[{id*,name,color,weight}], scoreBands[{min,max,label,color,description}], questions[{id,dimensionId,order,label,teaching,question,answers:[[id,title,description,score,accent,glyph]]}] } — replaces the built-in MAXESS dataset
     title: header title (default: assessment title)
     intro: intro line under the header
     restartLabel: retake button label (default "Retake assessment")
     accent: unit accent token (default #a06bff)
     storeKey: localStorage key to persist the last completed result (optional)
   }
   Ready behavior: full assessment runs client-side — start, answer, continue, explained results report with band, dimension rings, analysis, next path, retake. Zero backend.
   Connected behavior: none
   Backend twin: none
*/
(function(){
'use strict';
var NF_F14_DEFAULT_ASSESSMENT = {

  id:"ai-mastery",

  version:"2.0.0",

  title:"AI Mastery Assessment",

  dimensions:[

    {
      id:"direction",
      name:"Direction",
      color:"#ffd45a",
      weight:1
    },

    {
      id:"communication",
      name:"Communication",
      color:"#35e39b",
      weight:1
    },

    {
      id:"evaluation",
      name:"Evaluation",
      color:"#3ca8ff",
      weight:1
    },

    {
      id:"iteration",
      name:"Iteration",
      color:"#765cff",
      weight:1
    },

    {
      id:"systems",
      name:"Systems Thinking",
      color:"#ed42c4",
      weight:1
    }

  ],


  scoreBands:[

    {
      min:90,
      max:100,
      label:"Master",
      color:"#ffd45a",
      description:
        "You are operating at a highly developed level. Your greatest opportunity is no longer simply learning how to use AI — it is learning how to multiply what you can already do."
    },

    {
      min:75,
      max:89.99,
      label:"Advancing",
      color:"#35e39b",
      description:
        "You have meaningful AI capability and are moving beyond basic usage. The next leap comes from becoming more deliberate, consistent, and systematic."
    },

    {
      min:60,
      max:74.99,
      label:"Developing",
      color:"#3ca8ff",
      description:
        "You have a useful foundation and clear potential. With better direction, evaluation, and repetition, AI can become dramatically more powerful for you."
    },

    {
      min:0,
      max:59.99,
      label:"Foundation",
      color:"#765cff",
      description:
        "You are at the beginning of a valuable journey. The opportunity is not a lack of intelligence — it is learning a better way to direct, judge, improve, and reuse AI."
    }

  ],


  questions:[

    {
      id:"destination-definition",
      dimensionId:"direction",
      order:1,
      label:"AI DIRECTION",
      teaching:
        "Great AI work starts before the answer. This question is really asking whether you know what you want the finished result to accomplish — not just what words you want AI to produce.",
      question:
        "When you ask AI to create something important, how clearly do you define the destination?",
      answers:[
        ["extremely-clearly","Extremely clearly","I define the destination precisely.",100,"#ffd45a","◆"],
        ["very-clearly","Very clearly","I usually know what great looks like.",85,"#35e39b","✦"],
        ["fairly-clearly","Fairly clearly","I give AI a clear direction, then refine it.",70,"#3ca8ff","△"],
        ["somewhat-clearly","Somewhat clearly","I have the destination, but it evolves.",55,"#765cff","✧"],
        ["figure-it-out","I figure it out as I go","The first result often helps me discover what I want.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"communication",
      dimensionId:"communication",
      order:2,
      label:"AI COMMUNICATION",
      teaching:
        "AI cannot reliably read your mind. The better you can explain the outcome, context, audience, constraints, and details, the less time you spend correcting misunderstandings.",
      question:
        "How clearly do you communicate what you want AI to understand, create, or change?",
      answers:[
        ["communication-100","Extremely clearly","I communicate the outcome, context, constraints, and important details.",100,"#ffd45a","◆"],
        ["communication-85","Very clearly","AI usually understands exactly what I mean.",85,"#35e39b","✦"],
        ["communication-70","Fairly clearly","I communicate the main idea and refine details later.",70,"#3ca8ff","△"],
        ["communication-55","Somewhat clearly","Sometimes AI understands me, sometimes I need to clarify.",55,"#765cff","✧"],
        ["communication-35","I explain it as I go","I discover what I mean through the conversation.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"evaluation",
      dimensionId:"evaluation",
      order:3,
      label:"AI EVALUATION",
      teaching:
        "One of the biggest differences between casual AI use and AI craftsmanship is judgment. Getting an answer is easy. Knowing whether the answer is actually good is the higher-value skill.",
      question:
        "When AI gives you an answer, how deliberately do you judge whether it is actually good enough?",
      answers:[
        ["evaluation-100","Very deliberately","I use clear standards and actively look for weaknesses.",100,"#ffd45a","◆"],
        ["evaluation-85","Usually deliberately","I regularly inspect quality before accepting the result.",85,"#35e39b","✦"],
        ["evaluation-70","Sometimes","I evaluate important outputs but not everything.",70,"#3ca8ff","△"],
        ["evaluation-55","Occasionally","I usually know when something feels wrong.",55,"#765cff","✧"],
        ["evaluation-35","Rarely","If the answer looks useful, I usually move on.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"iteration",
      dimensionId:"iteration",
      order:4,
      label:"AI ITERATION",
      teaching:
        "The first answer is rarely the best answer. Excellence usually comes from seeing what works, identifying what does not, and directing the next version without throwing away the good parts.",
      question:
        "When the first AI result is not a 10, what do you normally do?",
      answers:[
        ["iteration-100","Diagnose and improve it","I identify exactly why it is not a 10 and direct AI to improve it.",100,"#ffd45a","◆"],
        ["iteration-85","Refine it","I give feedback and continue improving the result.",85,"#35e39b","✦"],
        ["iteration-70","Try another version","I ask AI to make another attempt.",70,"#3ca8ff","△"],
        ["iteration-55","Make a few changes","I fix obvious issues and move forward.",55,"#765cff","✧"],
        ["iteration-35","Usually accept it","I normally use the first useful result.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"systems",
      dimensionId:"systems",
      order:5,
      label:"SYSTEMS THINKING",
      teaching:
        "A powerful AI user does not just get one good answer. They notice what worked, preserve it, and turn it into something reusable so tomorrow's work starts further ahead.",
      question:
        "How often do you turn successful AI workflows into reusable systems instead of starting from scratch?",
      answers:[
        ["systems-100","Almost always","I capture successful methods and turn them into reusable systems.",100,"#ffd45a","◆"],
        ["systems-85","Very often","I reuse strong workflows whenever possible.",85,"#35e39b","✦"],
        ["systems-70","Sometimes","I reuse some workflows but still start fresh often.",70,"#3ca8ff","△"],
        ["systems-55","Occasionally","I reuse things only when it is convenient.",55,"#765cff","✧"],
        ["systems-35","Rarely","I usually begin again with each new task.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"context",
      dimensionId:"direction",
      order:6,
      label:"DIRECTION",
      teaching:
        "Context is the invisible fuel behind a good AI result. The more relevant information AI has about the situation, the better it can reason about the situation instead of guessing.",
      question:
        "How consistently do you give AI the context it needs before asking it to solve an important problem?",
      answers:[
        ["context-100","Almost always","I make sure AI understands the situation first.",100,"#ffd45a","◆"],
        ["context-85","Very often","I provide context whenever the task matters.",85,"#35e39b","✦"],
        ["context-70","Often","I usually give useful background information.",70,"#3ca8ff","△"],
        ["context-55","Sometimes","I add context when AI gets confused.",55,"#765cff","✧"],
        ["context-35","Rarely","I usually get straight to the request.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"audience",
      dimensionId:"communication",
      order:7,
      label:"COMMUNICATION",
      teaching:
        "The same answer can be brilliant for one person and useless for another. Knowing who the work is for changes the language, depth, examples, tone, and even the structure.",
      question:
        "How effectively do you explain your intended audience, purpose, and desired outcome to AI?",
      answers:[
        ["audience-100","Extremely effectively","Audience and purpose are always part of my direction.",100,"#ffd45a","◆"],
        ["audience-85","Very effectively","I usually make the audience clear.",85,"#35e39b","✦"],
        ["audience-70","Fairly effectively","I explain it when it is important.",70,"#3ca8ff","△"],
        ["audience-55","Sometimes","I think about the audience after the first result.",55,"#765cff","✧"],
        ["audience-35","Rarely","I mostly let AI decide how to present it.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"verification",
      dimensionId:"evaluation",
      order:8,
      label:"EVALUATION",
      teaching:
        "AI can sound confident and still be wrong. Verification is the difference between using AI as a source of possibilities and trusting it blindly.",
      question:
        "How consistently do you verify important AI-generated information before relying on it?",
      answers:[
        ["verification-100","Almost always","I verify important claims before relying on them.",100,"#ffd45a","◆"],
        ["verification-85","Very often","I verify information when accuracy matters.",85,"#35e39b","✦"],
        ["verification-70","Often","I check important information most of the time.",70,"#3ca8ff","△"],
        ["verification-55","Sometimes","I verify things when something feels questionable.",55,"#765cff","✧"],
        ["verification-35","Rarely","I generally trust useful-looking answers.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"feedback",
      dimensionId:"iteration",
      order:9,
      label:"ITERATION",
      teaching:
        "Feedback becomes powerful when it changes the next result. The question is not whether you revise — it is whether each revision teaches the process something useful.",
      question:
        "How effectively do you use feedback from one AI result to produce a better next result?",
      answers:[
        ["feedback-100","Extremely effectively","Every revision gives AI specific information about what to improve.",100,"#ffd45a","◆"],
        ["feedback-85","Very effectively","I usually give useful feedback and get better results.",85,"#35e39b","✦"],
        ["feedback-70","Fairly effectively","I make useful corrections as I go.",70,"#3ca8ff","△"],
        ["feedback-55","Sometimes","My feedback is often fairly general.",55,"#765cff","✧"],
        ["feedback-35","Not very effectively","I often start over instead of diagnosing the issue.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"workflow",
      dimensionId:"systems",
      order:10,
      label:"SYSTEMS THINKING",
      teaching:
        "A workflow is simply a repeatable way of getting something done. Once you discover one that works, you should not have to rediscover it every time.",
      question:
        "How often do you design repeatable AI workflows instead of treating every task as a one-off?",
      answers:[
        ["workflow-100","Almost always","I deliberately build repeatable workflows.",100,"#ffd45a","◆"],
        ["workflow-85","Very often","I turn repeated tasks into workflows.",85,"#35e39b","✦"],
        ["workflow-70","Sometimes","I build workflows for tasks I do frequently.",70,"#3ca8ff","△"],
        ["workflow-55","Occasionally","I reuse processes informally.",55,"#765cff","✧"],
        ["workflow-35","Rarely","Most AI work begins from scratch.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"excellence",
      dimensionId:"direction",
      order:11,
      label:"DIRECTION",
      teaching:
        "Useful and excellent are not the same thing. Excellence requires a standard — a mental picture of what would make the result truly worth using, sharing, or shipping.",
      question:
        "How clearly can you recognize the difference between an AI output that is useful and one that is truly excellent?",
      answers:[
        ["excellence-100","Very clearly","I can articulate what separates good from exceptional.",100,"#ffd45a","◆"],
        ["excellence-85","Clearly","I usually know when something needs another level of refinement.",85,"#35e39b","✦"],
        ["excellence-70","Fairly clearly","I can recognize obvious quality differences.",70,"#3ca8ff","△"],
        ["excellence-55","Somewhat","I mostly judge quality by instinct.",55,"#765cff","✧"],
        ["excellence-35","Not very clearly","If it works, I usually consider it good enough.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"correction",
      dimensionId:"communication",
      order:12,
      label:"COMMUNICATION",
      teaching:
        "Being misunderstood by AI is not failure. The real skill is recognizing the misunderstanding quickly and communicating the correction clearly enough to get the conversation back on track.",
      question:
        "How effectively do you correct AI when it misunderstands what you want?",
      answers:[
        ["correction-100","Extremely effectively","I diagnose the misunderstanding and redirect precisely.",100,"#ffd45a","◆"],
        ["correction-85","Very effectively","I usually correct AI quickly.",85,"#35e39b","✦"],
        ["correction-70","Fairly effectively","I can usually get things back on track.",70,"#3ca8ff","△"],
        ["correction-55","Sometimes","I often need several attempts.",55,"#765cff","✧"],
        ["correction-35","Not very effectively","I often abandon the direction and start again.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"red-team",
      dimensionId:"evaluation",
      order:13,
      label:"EVALUATION",
      teaching:
        "Strong AI users do not only ask, “What is good here?” They also ask, “What could be wrong?” That second question is where much of the real quality control happens.",
      question:
        "How often do you deliberately look for what could be wrong with an AI-generated result?",
      answers:[
        ["redteam-100","Almost always","I actively challenge important outputs.",100,"#ffd45a","◆"],
        ["redteam-85","Very often","I deliberately look for weaknesses.",85,"#35e39b","✦"],
        ["redteam-70","Often","I check important results for obvious problems.",70,"#3ca8ff","△"],
        ["redteam-55","Sometimes","I inspect results when something feels off.",55,"#765cff","✧"],
        ["redteam-35","Rarely","I usually focus on what is useful.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"preservation",
      dimensionId:"iteration",
      order:14,
      label:"ITERATION",
      teaching:
        "Improvement should not destroy the parts that already work. One of the most important habits in high-level AI craftsmanship is preserving strengths while deliberately fixing weaknesses.",
      question:
        "How intentionally do you preserve what is already working while improving what is not?",
      answers:[
        ["preservation-100","Extremely intentionally","I protect what works while targeting specific weaknesses.",100,"#ffd45a","◆"],
        ["preservation-85","Very intentionally","I usually preserve strong elements during revisions.",85,"#35e39b","✦"],
        ["preservation-70","Fairly intentionally","I try not to lose good parts.",70,"#3ca8ff","△"],
        ["preservation-55","Sometimes","Improvement sometimes changes more than necessary.",55,"#765cff","✧"],
        ["preservation-35","Rarely","I often replace the whole thing when revising.",35,"#ed42c4","✦"]
      ]
    },


    {
      id:"capability",
      dimensionId:"systems",
      order:15,
      label:"SYSTEMS THINKING",
      teaching:
        "The highest level is not having one clever AI trick. It is building capability — a repeatable combination of knowledge, workflows, tools, standards, and habits that gets stronger over time.",
      question:
        "How effectively do you turn individual AI successes into a larger repeatable capability?",
      answers:[
        ["capability-100","Extremely effectively","I turn successful experiments into durable capability.",100,"#ffd45a","◆"],
        ["capability-85","Very effectively","I regularly capture and reuse what works.",85,"#35e39b","✦"],
        ["capability-70","Fairly effectively","I reuse some successful approaches.",70,"#3ca8ff","△"],
        ["capability-55","Sometimes","I remember useful methods but don't formalize them.",55,"#765cff","✧"],
        ["capability-35","Rarely","Most successes stay as one-off experiences.",35,"#ed42c4","✦"]
      ]
    }

  ]

};

/* ------------------------------------------------------------------
   Engine — harvested from MAXESS (Maxis_App_Design.html), adapted to
   the NayaFunction unit contract. Questions/scoring come from `A`
   (config.assessment or the verbatim default above).
------------------------------------------------------------------- */

function nf14esc(v){
  return String(v)
    .replace(/&/g,"&amp;")
    .replace(/</g,"&lt;")
    .replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;")
    .replace(/'/g,"&#039;");
}

function nf14AnswerObjects(question){
  return question.answers.map(function(item){
    return {
      id:item[0],
      title:item[1],
      description:item[2],
      score:item[3],
      accent:item[4],
      glyph:item[5]
    };
  });
}

/* Harvested: dimension averages -> weighted overall -> band lookup */
function nf14CalculateResults(A, responses){
  var dimensions = A.dimensions.map(function(dimension){
    var relevant = responses.filter(function(r){ return r.dimensionId === dimension.id; });
    var score = relevant.length
      ? relevant.reduce(function(s,r){ return s + r.score; }, 0) / relevant.length
      : 0;
    return {
      id: dimension.id,
      name: dimension.name,
      color: dimension.color,
      weight: dimension.weight,
      score: Math.round(score*10)/10
    };
  });

  var overall = dimensions.length
    ? dimensions.reduce(function(s,d){ return s + d.score*d.weight; }, 0) /
      dimensions.reduce(function(s,d){ return s + d.weight; }, 0)
    : 0;

  var rounded = Math.round(overall*10)/10;

  var band = null;
  for (var i=0;i<A.scoreBands.length;i++){
    var b = A.scoreBands[i];
    if (rounded >= b.min && rounded <= b.max){ band = b; break; }
  }
  if (!band){ band = A.scoreBands[A.scoreBands.length-1]; }

  return { overall: rounded, band: band, dimensions: dimensions };
}

/* Harvested verbatim — personalized language for the MAXESS dimensions */
function nf14StrongestMessage(dimension, score){
  var messages={
    direction:
      "You have a strong instinct for giving AI a destination. That means you are already thinking beyond the prompt itself and toward the result you actually want.",
    communication:
      "You have a strong ability to translate your intent into language AI can work with. That is one of the highest-leverage human skills in an AI workflow.",
    evaluation:
      "You have a strong quality-control instinct. You are less likely to simply accept an impressive-looking answer and more likely to ask whether it deserves to be trusted.",
    iteration:
      "You understand that good work is built through refinement. That gives you a major advantage because AI becomes dramatically more useful when you direct the next version intelligently.",
    systems:
      "You are beginning to think beyond individual outputs and toward reusable capability. That is the bridge from using AI to building with AI."
  };
  if (messages[dimension.id]) return messages[dimension.id];
  return "Your strongest showing is in " + dimension.name + " — this is the capability to lean on and multiply first.";
}

/* Harvested verbatim */
function nf14OpportunityMessage(dimension, score){
  var messages={
    direction:
      "Your biggest opportunity is becoming even more deliberate about the destination before you begin. A clearer target can dramatically reduce wasted iterations.",
    communication:
      "Your biggest opportunity is giving AI richer context and more precise direction. The clearer the conversation, the less work you have to spend correcting it later.",
    evaluation:
      "Your biggest opportunity is strengthening your quality filter. Make \u201cWhy is this not a 10?\u201d a normal part of your workflow.",
    iteration:
      "Your biggest opportunity is turning revision into a deliberate craft. Diagnose the weakness, preserve what works, improve what does not, and repeat.",
    systems:
      "Your biggest opportunity is capturing what works. A successful workflow should become an asset you can reuse rather than a trick you have to rediscover."
  };
  if (messages[dimension.id]) return messages[dimension.id];
  return "Your biggest leverage opportunity is in " + dimension.name + " — deliberate practice here moves the whole score fastest.";
}

/* Harvested verbatim */
function nf14BuildAnalysis(results, strongest, opportunity){
  var opening =
    results.overall>=90
      ? "Your score shows highly developed AI craftsmanship. You are not starting from zero — you are at the point where refinement, leverage, and system-building become increasingly valuable."
      : results.overall>=75
      ? "Your score shows meaningful AI capability. You are already beyond basic experimentation, and your next gains are likely to come from becoming more deliberate and repeatable."
      : results.overall>=60
      ? "Your score shows a useful foundation with significant room to grow. The encouraging part is that the biggest gains are often created by changing the way you work with AI, not by learning hundreds of new tools."
      : "Your score shows that there is a large opportunity ahead. That is not a negative verdict — it is a map. A few foundational habits can change the amount of value you get from AI very quickly.";

  var strongestLine =
    "Your strongest dimension is " + strongest.name + " at " + Math.round(strongest.score) + "/100. " + nf14StrongestMessage(strongest, strongest.score);

  var opportunityLine =
    "Your biggest leverage opportunity is " + opportunity.name + " at " + Math.round(opportunity.score) + "/100. " + nf14OpportunityMessage(opportunity, opportunity.score);

  var philosophy =
    "The central lesson behind your assessment is simple: AI is the engine, but you are the director. Your advantage grows when you know what you want, communicate it clearly, judge the result honestly, improve it deliberately, and turn successful work into something reusable.";

  return "<p>"+nf14esc(opening)+"</p>" +
         "<p>"+nf14esc(strongestLine)+"</p>" +
         "<p>"+nf14esc(opportunityLine)+"</p>" +
         "<p>"+nf14esc(philosophy)+"</p>";
}

/* Harvested verbatim */
function nf14BuildPath(strongest, opportunity, overall){
  var path=[];
  path.push({
    title: "Strengthen " + opportunity.name,
    body: nf14OpportunityMessage(opportunity, opportunity.score)
  });
  path.push({
    title: "Use the 10-point test",
    body: "Before accepting an important AI result, ask: What is working? What is missing? What is unclear? What could be better? Then tell AI exactly what to improve."
  });
  path.push({
    title: "Turn wins into systems",
    body: "Whenever you discover a workflow that works, save the method. Your future self should start from the successful version, not from a blank page."
  });
  return path;
}

/* Harvested verbatim */
function nf14DimensionLevel(score){
  if(score>=90) return "Master";
  if(score>=75) return "Advancing";
  if(score>=60) return "Developing";
  return "Foundation";
}

(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var F14_CSS = "\n.f14-wrap{max-width:640px;margin:0 auto;padding:22px 18px 30px;color:#fff;background:#0b0b10;border:1px solid rgba(255,255,255,.14);border-radius:18px;position:relative}\n.f14-rail{position:absolute;top:0;left:24px;right:24px;height:3px;border-radius:2px;opacity:.9}\n.f14-title{color:#fff;font-size:26px;margin:10px 0 6px;letter-spacing:.01em}\n.f14-sub{color:#c9c9d4;font-size:15px;margin:0 0 4px}\n.f14-note{color:#8a8a99;font-size:13px;margin:8px 0}\n.f14-note strong{color:#fff}\n.f14-btn{display:inline-block;background:transparent;border:1.5px solid #fff;color:#fff;border-radius:999px;padding:11px 26px;font-size:15px;font-weight:600;cursor:pointer;transition:all .18s ease}\n.f14-btn:hover{border-color:#a06bff;box-shadow:0 0 18px rgba(160,107,255,.55);transform:translateY(-1px)}\n.f14-btn.off{opacity:.35;cursor:not-allowed}\n.f14-progress{height:8px;border-radius:5px;background:rgba(255,255,255,.1);overflow:hidden;margin:6px 0 12px}\n.f14-bar{height:100%;border-radius:5px;transition:width .25s ease}\n.f14-count{color:#8a8a99;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 6px}\n.f14-label{color:#fff;font-size:12px;letter-spacing:.16em;margin:0 0 8px;opacity:.85}\n.f14-q{color:#fff;font-size:21px;line-height:1.35;margin:0 0 10px}\n.f14-teach{margin:0 0 14px;border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:9px 14px}\n.f14-teach summary{color:#fff;cursor:pointer;font-size:14px;font-weight:600}\n.f14-teach p{color:#c9c9d4;font-size:14px;line-height:1.5;margin:8px 0 4px}\n.f14-answers{display:flex;flex-direction:column;gap:10px;margin:0 0 18px}\n.f14-answer{display:flex;gap:12px;align-items:flex-start;text-align:left;background:rgba(255,255,255,.03);border:1.5px solid #fff;color:#fff;border-radius:14px;padding:13px 15px;cursor:pointer;transition:all .18s ease;width:100%}\n.f14-answer:hover{border-color:var(--a)}\n.f14-answer.sel{border-color:var(--a);background:rgba(255,255,255,.07);box-shadow:0 0 18px rgba(255,255,255,.08)}\n.f14-glyph{color:var(--a);font-size:18px;line-height:1.4;flex:0 0 auto}\n.f14-at{display:flex;flex-direction:column;gap:3px}\n.f14-atitle{color:#fff;font-weight:650;font-size:15px}\n.f14-adesc{color:#c9c9d4;font-size:13.5px;line-height:1.45}\n.f14-nav{display:flex;justify-content:space-between;align-items:center}\n.f14-scorewrap{text-align:center;margin:8px 0 18px}\n.f14-ring{width:120px;height:120px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;position:relative}\n.f14-ring::after{content:\"\";position:absolute;inset:9px;border-radius:50%;background:#0b0b10}\n.f14-rnum{color:#fff;font-size:26px;font-weight:750;position:relative;z-index:1}\n.f14-bigring{width:170px;height:170px}\n.f14-bignum{font-size:44px}\n.f14-rof{color:#c9c9d4;font-size:14px;position:relative;z-index:1;margin-top:22px;margin-left:2px}\n.f14-band{color:#fff;font-size:24px;margin:12px 0 6px}\n.f14-banddesc{color:#c9c9d4;font-size:15px;line-height:1.55;max-width:520px;margin:0 auto}\n.f14-dims{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin:22px 0}\n.f14-dim{width:104px;text-align:center}\n.f14-dname{color:#fff;font-size:13px;font-weight:650;margin:8px 0 2px}\n.f14-dlevel{color:#8a8a99;font-size:12px;margin:0}\n.f14-analysis{border-top:1px solid rgba(255,255,255,.12);margin-top:6px;padding-top:16px}\n.f14-analysis p{color:#c9c9d4;font-size:15px;line-height:1.6;margin:0 0 12px}\n.f14-pathhead{color:#fff;font-size:18px;margin:18px 0 10px}\n.f14-path{display:flex;flex-direction:column;gap:10px;margin-bottom:20px}\n.f14-step{display:flex;gap:12px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:13px 15px}\n.f14-snum{flex:0 0 auto;width:30px;height:30px;border-radius:50%;border:1.5px solid #fff;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}\n.f14-stitle{color:#fff;font-weight:650;font-size:15px;margin:2px 0 4px}\n.f14-sbody{color:#c9c9d4;font-size:13.5px;line-height:1.5;margin:0}\n";

NF.register('f-14-assessment-score', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.fnBound){ return { destroy: function(){} }; }
    root.dataset.fnBound = '1';

    var A = (config.assessment && Array.isArray(config.assessment.questions) && config.assessment.questions.length)
      ? config.assessment
      : NF_F14_DEFAULT_ASSESSMENT;

    /* fail soft: the dataset must carry dimensions + bands too */
    if (!A.dimensions || !A.dimensions.length || !A.scoreBands || !A.scoreBands.length){
      A = NF_F14_DEFAULT_ASSESSMENT;
    }

    var accent = config.accent || '#a06bff';
    var title = config.title || A.title || 'Assessment';
    var intro = config.intro || 'Answer each question honestly. Your score, explained.';
    var restartLabel = config.restartLabel || 'Retake assessment';

    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-f14','1');
    styleEl.textContent = F14_CSS;
    root.appendChild(styleEl);

    var questions = A.questions.slice().sort(function(a,b){ return (a.order||0)-(b.order||0); });
    var st = { i: 0, responses: [], selected: null };

    function lastScore(){
      if (!config.storeKey) return null;
      try {
        var raw = localStorage.getItem(config.storeKey);
        if (!raw) return null;
        var d = JSON.parse(raw);
        return (typeof d.overall === 'number') ? d : null;
      } catch(e){ return null; }
    }

    function renderIntro(){
      var prev = lastScore();
      var prevLine = prev
        ? '<p class="f14-note">Last completed score: <strong>' + Math.round(prev.overall) + '/100</strong>' +
          (prev.bandLabel ? ' &middot; ' + nf14esc(prev.bandLabel) : '') + '</p>'
        : '';
      clearViews();
      root.insertAdjacentHTML('beforeend',
        '<div class="f14-wrap" data-f14-view="intro">' +
          '<div class="f14-rail" style="background:' + accent + '"></div>' +
          '<h3 class="f14-title">' + nf14esc(title) + '</h3>' +
          '<p class="f14-sub">' + nf14esc(intro) + '</p>' +
          '<p class="f14-note">' + questions.length + ' questions &middot; about a minute &middot; scored instantly</p>' +
          prevLine +
          '<button class="f14-btn f14-start" type="button">Start assessment</button>' +
        '</div>');
    }

    function clearViews(){
      var views = root.querySelectorAll('[data-f14-view]');
      for (var i=0;i<views.length;i++){ views[i].remove(); }
    }

    function renderQuestion(){
      var q = questions[st.i];
      var answers = nf14AnswerObjects(q);
      var pct = Math.round((st.i / questions.length) * 100);
      var ansHtml = answers.map(function(a){
        var sel = (st.selected === a.id);
        return '<button type="button" class="f14-answer' + (sel ? ' sel' : '') + '" data-aid="' + nf14esc(a.id) + '"' +
               ' style="--a:' + nf14esc(a.accent || accent) + '"' +
               ' aria-pressed="' + (sel ? 'true' : 'false') + '">' +
          '<span class="f14-glyph" aria-hidden="true">' + nf14esc(a.glyph || '\u25c6') + '</span>' +
          '<span class="f14-at"><span class="f14-atitle">' + nf14esc(a.title) + '</span>' +
          '<span class="f14-adesc">' + nf14esc(a.description) + '</span></span>' +
        '</button>';
      }).join('');
      var teach = q.teaching
        ? '<details class="f14-teach"><summary>Why this question matters</summary><p>' + nf14esc(q.teaching) + '</p></details>'
        : '';
      clearViews();
      root.insertAdjacentHTML('beforeend',
        '<div class="f14-wrap" data-f14-view="q">' +
          '<div class="f14-progress"><div class="f14-bar" style="width:' + pct + '%;background:' + accent + '"></div></div>' +
          '<p class="f14-count">Question ' + (st.i+1) + ' of ' + questions.length + '</p>' +
          (q.label ? '<p class="f14-label">' + nf14esc(q.label) + '</p>' : '') +
          '<h3 class="f14-q">' + nf14esc(q.question) + '</h3>' +
          teach +
          '<div class="f14-answers">' + ansHtml + '</div>' +
          '<div class="f14-nav">' +
            (st.i > 0 ? '<button type="button" class="f14-btn f14-back">&larr; Back</button>' : '<span></span>') +
            '<button type="button" class="f14-btn f14-continue' + (st.selected ? '' : ' off') + '"' +
              (st.selected ? '' : ' aria-disabled="true"') + '>Continue &rarr;</button>' +
          '</div>' +
        '</div>');
    }

    function selectAnswer(answerId){
      st.selected = answerId;
      var btns = root.querySelectorAll('.f14-answer');
      for (var i=0;i<btns.length;i++){
        var sel = btns[i].getAttribute('data-aid') === answerId;
        btns[i].classList.toggle('sel', sel);
        btns[i].setAttribute('aria-pressed', String(sel));
      }
      var c = root.querySelector('.f14-continue');
      if (c){ c.classList.remove('off'); c.removeAttribute('aria-disabled'); }
    }

    /* Harvested saveResponse logic */
    function saveResponse(){
      var q = questions[st.i];
      var ans = nf14AnswerObjects(q).filter(function(a){ return a.id === st.selected; })[0];
      if (!ans) return false;
      var resp = {
        assessmentId: A.id,
        assessmentVersion: A.version,
        questionId: q.id,
        questionOrder: q.order,
        dimensionId: q.dimensionId,
        answerId: ans.id,
        score: ans.score,
        answeredAt: new Date().toISOString()
      };
      var idx = -1;
      for (var i=0;i<st.responses.length;i++){
        if (st.responses[i].questionId === q.id){ idx = i; break; }
      }
      if (idx >= 0) st.responses[idx] = resp; else st.responses.push(resp);
      return true;
    }

    /* Harvested renderResults logic */
    function renderResults(){
      var results = nf14CalculateResults(A, st.responses);
      var dims = results.dimensions.slice();
      var strongest = dims.slice().sort(function(a,b){ return b.score-a.score; })[0] || dims[0];
      var opportunity = dims.slice().sort(function(a,b){ return a.score-b.score; })[0] || dims[0];
      var band = results.band;
      var deg = Math.max(0, Math.min(100, results.overall)) * 3.6;

      if (config.storeKey){
        try {
          localStorage.setItem(config.storeKey, JSON.stringify({
            overall: results.overall,
            bandLabel: band.label,
            at: new Date().toISOString()
          }));
        } catch(e){}
      }

      var dimHtml = results.dimensions.map(function(d){
        return '<div class="f14-dim">' +
          '<div class="f14-ring" style="background:conic-gradient(' + nf14esc(d.color || accent) + ' ' + (d.score*3.6) + 'deg, rgba(255,255,255,.12) 0deg)">' +
            '<span class="f14-rnum">' + Math.round(d.score) + '</span>' +
          '</div>' +
          '<p class="f14-dname">' + nf14esc(d.name) + '</p>' +
          '<p class="f14-dlevel">' + nf14esc(nf14DimensionLevel(d.score)) + '</p>' +
        '</div>';
      }).join('');

      var pathHtml = nf14BuildPath(strongest, opportunity, results.overall).map(function(p, i){
        return '<div class="f14-step"><span class="f14-snum">' + (i+1) + '</span>' +
               '<div><p class="f14-stitle">' + nf14esc(p.title) + '</p>' +
               '<p class="f14-sbody">' + nf14esc(p.body) + '</p></div></div>';
      }).join('');

      clearViews();
      root.insertAdjacentHTML('beforeend',
        '<div class="f14-wrap" data-f14-view="results">' +
          '<div class="f14-progress"><div class="f14-bar" style="width:100%;background:' + accent + '"></div></div>' +
          '<p class="f14-count">Results &middot; ' + nf14esc(A.title || title) + '</p>' +
          '<div class="f14-scorewrap">' +
            '<div class="f14-ring f14-bigring" style="background:conic-gradient(' + nf14esc(band.color || accent) + ' ' + deg + 'deg, rgba(255,255,255,.12) 0deg)">' +
              '<span class="f14-rnum f14-bignum">' + Math.round(results.overall) + '</span>' +
              '<span class="f14-rof">/ 100</span>' +
            '</div>' +
            '<h3 class="f14-band">' + nf14esc(band.label) + '</h3>' +
            '<p class="f14-banddesc">' + nf14esc(band.description || '') + '</p>' +
          '</div>' +
          '<div class="f14-dims">' + dimHtml + '</div>' +
          '<div class="f14-analysis">' + nf14BuildAnalysis(results, strongest, opportunity) + '</div>' +
          '<h4 class="f14-pathhead">Your next path</h4>' +
          '<div class="f14-path">' + pathHtml + '</div>' +
          '<button type="button" class="f14-btn f14-restart">' + nf14esc(restartLabel) + '</button>' +
        '</div>');
      var w = root.querySelector('[data-f14-view="results"]');
      if (w && w.scrollIntoView) w.scrollIntoView({block:'nearest'});
    }

    function onClick(e){
      var t = e.target.closest ? e.target.closest('button') : null;
      if (!t || !root.contains(t)) return;
      if (t.classList.contains('f14-start')){
        st.i = 0; st.responses = []; st.selected = null; renderQuestion();
      } else if (t.classList.contains('f14-answer')){
        selectAnswer(t.getAttribute('data-aid'));
      } else if (t.classList.contains('f14-back')){
        if (st.i > 0){
          st.i--;
          var prev = null;
          for (var i=0;i<st.responses.length;i++){
            if (st.responses[i].questionOrder === questions[st.i].order){ prev = st.responses[i]; break; }
          }
          st.selected = prev ? prev.answerId : null;
          renderQuestion();
        }
      } else if (t.classList.contains('f14-continue')){
        if (!st.selected) return; /* no staged continue */
        if (!saveResponse()) return;
        st.i++;
        st.selected = null;
        if (st.i >= questions.length){ renderResults(); }
        else { renderQuestion(); }
      } else if (t.classList.contains('f14-restart')){
        st.i = 0; st.responses = []; st.selected = null; renderIntro();
      }
    }

    root.addEventListener('click', onClick);
    renderIntro();

    return { destroy: function(){ root.removeEventListener('click', onClick); } };
  }
});
})();

})();
