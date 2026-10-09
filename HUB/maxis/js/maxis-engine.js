

/* =========================================================
   MAXESS — CONFIGURATION
========================================================= */

/* Bank is loaded as data: window.MAXIS_BANK (see banks/*.bank.js) */
const MAXESS_ASSESSMENT = window.MAXIS_BANK;

/* Interest areas come from the bank. */
const AI_AREAS = (window.MAXIS_BANK.interestAreas || []);



/* =========================================================
   STATE
========================================================= */

const state = {

  currentQuestionIndex:0,

  selectedAnswerId:null,

  responses:[],

  status:"in_progress",

  startedAt:new Date().toISOString(),

  completedAt:null,

  transitioning:false,

  nayaPlaying:false,

  teachingOpen:false,

  interestBoard:0,

  selectedInterests:new Set(),

  results:null

};


/* =========================================================
   DOM
========================================================= */

const DOM = {

  assessmentStage:
    document.getElementById("assessmentStage"),

  questionArea:
    document.getElementById("questionArea"),

  questionLabel:
    document.getElementById("questionLabel"),

  questionTitle:
    document.getElementById("questionTitle"),

  answers:
    document.getElementById("answers"),

  continueButton:
    document.getElementById("continueButton"),

  continueText:
    document.getElementById("continueText"),

  progressLabel:
    document.getElementById("progressLabel"),

  progressFill:
    document.getElementById("progressFill"),

  progressPercent:
    document.getElementById("progressPercent"),

  nayaButton:
    document.getElementById("nayaButton"),

  nayaPrimary:
    document.getElementById("nayaPrimary"),

  nayaSecondary:
    document.getElementById("nayaSecondary"),

  interstitial:
    document.getElementById("teachingInterstitial"),

  cloudEyebrow:
    document.getElementById("cloudEyebrow"),

  cloudTitle:
    document.getElementById("cloudTitle"),

  cloudBody:
    document.getElementById("cloudBody"),

  cloudContinue:
    document.getElementById("cloudContinue"),

  interestsView:
    document.getElementById("interestsView"),

  interestContinue:
    document.getElementById("interestContinue"),

  interestSkip:
    document.getElementById("interestSkip"),

  resultsView:
    document.getElementById("resultsView"),

  overallScore:
    document.getElementById("overallScore"),

  scoreStage:
    document.getElementById("scoreStage"),

  resultLevel:
    document.getElementById("resultLevel"),

  resultLevelText:
    document.getElementById("resultLevelText"),

  resultSubtitle:
    document.getElementById("resultSubtitle"),

  dimensionConstellation:
    document.getElementById("dimensionConstellation"),

  strongestName:
    document.getElementById("strongestName"),

  strongestScore:
    document.getElementById("strongestScore"),

  strongestText:
    document.getElementById("strongestText"),

  opportunityName:
    document.getElementById("opportunityName"),

  opportunityScore:
    document.getElementById("opportunityScore"),

  opportunityText:
    document.getElementById("opportunityText"),

  analysisCloud:
    document.getElementById("analysisCloud"),

  nextPath:
    document.getElementById("nextPath"),

  selectedInterests:
    document.getElementById("selectedInterests"),

  interestReportIntro:
    document.getElementById("interestReportIntro"),

  interestReportSection:
    document.getElementById("interestReportSection"),

  enterNayaButton:
    document.getElementById("enterNayaButton"),

  freeTrialButton:
    document.getElementById("freeTrialButton"),

  pdfButton:
    document.getElementById("pdfButton"),

  restartButton:
    document.getElementById("restartButton")

};


/* =========================================================
   HELPERS
========================================================= */

function questions(){

  return [...MAXESS_ASSESSMENT.questions]
    .sort((a,b)=>a.order-b.order);

}


function currentQuestion(){

  return questions()[state.currentQuestionIndex];

}


function answerObjects(question){

  return question.answers.map(item=>({

    id:item[0],
    title:item[1],
    description:item[2],
    score:item[3],
    accent:item[4],
    glyph:item[5]

  }));

}


function escapeHtml(value){

  return String(value)
    .replace(/&/g,"&amp;")
    .replace(/</g,"&lt;")
    .replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;")
    .replace(/'/g,"&#039;");

}


/* =========================================================
   VALIDATION
========================================================= */

function validate(){

  if(!MAXESS_ASSESSMENT.id){
    throw new Error("Assessment ID missing.");
  }

  if(!MAXESS_ASSESSMENT.version){
    throw new Error("Assessment version missing.");
  }

  if(
    !Array.isArray(MAXESS_ASSESSMENT.questions) ||
    MAXESS_ASSESSMENT.questions.length !== 15
  ){
    throw new Error("MAXESS requires exactly 15 questions.");
  }

  const ids=new Set();

  MAXESS_ASSESSMENT.questions.forEach(question=>{

    if(ids.has(question.id)){
      throw new Error(
        `Duplicate question ID: ${question.id}`
      );
    }

    ids.add(question.id);

    if(!question.dimensionId){
      throw new Error(
        `Question ${question.id} has no dimension.`
      );
    }

    if(!Array.isArray(question.answers)){
      throw new Error(
        `Question ${question.id} has no answers.`
      );
    }

    if(question.answers.length!==5){
      throw new Error(
        `Question ${question.id} must contain five answers.`
      );
    }

  });

  if(AI_AREAS.length!==18){
    throw new Error(
      "MAXESS requires exactly 18 AI areas."
    );
  }

}


/* =========================================================
   PROGRESS
========================================================= */

function updateProgress(){

  const total=questions().length;

  const current=
    state.currentQuestionIndex+1;

  const percentage=
    Math.round(
      (current/total)*100
    );

  DOM.progressLabel.textContent=
    `QUESTION ${current} OF ${total}`;

  DOM.progressFill.style.width=
    `${percentage}%`;

  DOM.progressPercent.textContent=
    `${percentage}%`;

}


/* =========================================================
   CONTINUE BUTTON
========================================================= */

function updateContinue(){

  const enabled=
    !!state.selectedAnswerId &&
    !state.transitioning;

  DOM.continueButton.disabled=
    !enabled;

  DOM.continueButton.setAttribute(
    "aria-disabled",
    String(!enabled)
  );

  const final=
    state.currentQuestionIndex===
    questions().length-1;

  DOM.continueText.textContent=
    final
      ? "Continue"
      : "Continue";

}


/* =========================================================
   RENDER QUESTION
========================================================= */

function renderQuestion(){

  const question=currentQuestion();

  if(!question){
    return;
  }

  state.selectedAnswerId=null;
  state.transitioning=false;

  DOM.questionLabel.textContent=
    question.label;

  DOM.questionTitle.textContent=
    question.question;

  DOM.answers.innerHTML="";

  answerObjects(question)
    .forEach(answer=>{

      const button=
        document.createElement("button");

      button.type="button";

      button.className="answer";

      button.dataset.answerId=
        answer.id;

      button.style.setProperty(
        "--accent",
        answer.accent
      );

      button.setAttribute(
        "aria-pressed",
        "false"
      );

      button.innerHTML=`

        <span
          class="jewel"
          aria-hidden="true"
        >
          <span class="glyph">
            ${escapeHtml(answer.glyph)}
          </span>
        </span>

        <span class="answer-copy">

          <span class="answer-title">
            ${escapeHtml(answer.title)}
          </span>

          <span class="answer-sub">
            ${escapeHtml(answer.description)}
          </span>

        </span>

        <span
          class="chevron"
          aria-hidden="true"
        >
          ›
        </span>

      `;

      button.addEventListener(
        "click",
        ()=>selectAnswer(
          answer.id,
          button
        )
      );

      DOM.answers.appendChild(button);

    });

  updateProgress();

  updateContinue();

}


/* =========================================================
   SELECT ANSWER
========================================================= */

function selectAnswer(
  answerId,
  button
){

  if(state.transitioning){
    return;
  }

  state.selectedAnswerId=
    answerId;

  DOM.answers
    .querySelectorAll(".answer")
    .forEach(item=>{

      const selected=
        item===button;

      item.classList.toggle(
        "selected",
        selected
      );

      item.setAttribute(
        "aria-pressed",
        String(selected)
      );

    });

  updateContinue();

}


/* =========================================================
   SAVE RESPONSE
========================================================= */

function saveResponse(){

  const question=currentQuestion();

  const answer=
    answerObjects(question)
      .find(
        item=>item.id===state.selectedAnswerId
      );

  if(!answer){
    return false;
  }

  const response={

    assessmentId:
      MAXESS_ASSESSMENT.id,

    assessmentVersion:
      MAXESS_ASSESSMENT.version,

    questionId:
      question.id,

    questionOrder:
      question.order,

    dimensionId:
      question.dimensionId,

    answerId:
      answer.id,

    score:
      answer.score,

    answeredAt:
      new Date().toISOString()

  };

  const index=
    state.responses.findIndex(
      item=>
        item.questionId===
        question.id
    );

  if(index>=0){
    state.responses[index]=response;
  }else{
    state.responses.push(response);
  }

  return true;

}


/* =========================================================
   TEACHING CLOUD
========================================================= */

function showTeachingCloud(){

  const question=currentQuestion();

  if(!question){
    return;
  }

  DOM.cloudEyebrow.textContent=
    `${question.label} · QUESTION ${question.order}`;

  DOM.cloudTitle.textContent=
    "Before you answer, here's what we're really looking at.";

  DOM.cloudBody.innerHTML=
    `<strong>${escapeHtml(question.teaching)}</strong>`;

  DOM.interstitial.classList.add(
    "visible"
  );

  state.teachingOpen=true;

  DOM.cloudContinue.focus();

}


function closeTeachingCloud(){

  DOM.interstitial.classList.remove(
    "visible"
  );

  state.teachingOpen=false;

  requestAnimationFrame(()=>{

    const first=
      DOM.answers.querySelector(".answer");

    if(first){
      first.focus();
    }

  });

}


/* =========================================================
   CONTINUE ASSESSMENT
========================================================= */

function continueAssessment(){

  if(
    !state.selectedAnswerId ||
    state.transitioning
  ){
    return;
  }

  state.transitioning=true;

  saveResponse();

  const final=
    state.currentQuestionIndex===
    questions().length-1;

  if(final){

    state.status="interest_selection";

    state.transitioning=false;

    showInterestSelection();

    return;

  }

  state.currentQuestionIndex++;

  transitionQuestion();

}


function transitionQuestion(){

  stopNaya();

  const reduced=
    window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

  if(reduced){

    renderQuestion();

    showTeachingCloud();

    return;

  }

  DOM.questionArea.animate(
    [
      {
        opacity:1,
        transform:"translateY(0)"
      },
      {
        opacity:0,
        transform:"translateY(-8px)"
      }
    ],
    {
      duration:150,
      easing:"ease-in"
    }
  ).finished
  .then(()=>{

    renderQuestion();

    DOM.questionArea.animate(
      [
        {
          opacity:0,
          transform:"translateY(10px)"
        },
        {
          opacity:1,
          transform:"translateY(0)"
        }
      ],
      {
        duration:280,
        easing:"cubic-bezier(.2,.8,.2,1)"
      }
    );

    setTimeout(
      showTeachingCloud,
      120
    );

  })
  .catch(()=>{

    renderQuestion();
    showTeachingCloud();

  });

}


/* =========================================================
   INTEREST BOARDS
========================================================= */

function buildInterestBoards(){

  const boards=
    document.querySelectorAll(
      ".interest-board"
    );

  boards.forEach(board=>{
    board.innerHTML="";
  });

  AI_AREAS.forEach(
    (area,index)=>{

      const boardIndex=
        Math.floor(index/6);

      const board=
        boards[boardIndex];

      const button=
        document.createElement("button");

      button.type="button";

      button.className=
        "interest-area";

      button.style.setProperty(
        "--interest",
        area.color
      );

      button.dataset.areaId=
        area.id;

      button.setAttribute(
        "aria-pressed",
        "false"
      );

      button.innerHTML=`

        <span
          class="interest-orb"
          aria-hidden="true"
        >
          <span class="interest-check">
            ✓
          </span>
        </span>

        <span class="interest-name">
          ${escapeHtml(area.name)}
        </span>

        <span class="interest-description">
          ${escapeHtml(area.description)}
        </span>

      `;

      button.addEventListener(
        "click",
        ()=>toggleInterest(
          area.id,
          button
        )
      );

      board.appendChild(button);

    }
  );

}


function toggleInterest(
  id,
  button
){

  if(state.selectedInterests.has(id)){

    state.selectedInterests.delete(id);

    button.classList.remove(
      "selected"
    );

    button.setAttribute(
      "aria-pressed",
      "false"
    );

  }else{

    state.selectedInterests.add(id);

    button.classList.add(
      "selected"
    );

    button.setAttribute(
      "aria-pressed",
      "true"
    );

  }

}


function showInterestSelection(){
    stopNaya();
    DOM.assessmentStage.style.display=
    "none";

  DOM.nayaButton.style.display=
    "none";

  DOM.continueButton.style.display=
    "none";

  DOM.interestsView.classList.add(
    "visible"
  );

  state.interestBoard=0;

  updateInterestBoard();

}


function updateInterestBoard(){

  const boards=
    document.querySelectorAll(
      ".interest-board"
    );

  const dots=
    document.querySelectorAll(
      ".board-dot"
    );

  boards.forEach(
    (board,index)=>
      board.classList.toggle(
        "active",
        index===state.interestBoard
      )
  );

  dots.forEach(
    (dot,index)=>
      dot.classList.toggle(
        "active",
        index===state.interestBoard
      )
  );

}


/* =========================================================
   RESULTS
========================================================= */

function calculateResults(){

  const dimensions=
    MAXESS_ASSESSMENT.dimensions
      .map(dimension=>{

        const relevant=
          state.responses.filter(
            response=>
              response.dimensionId===
              dimension.id
          );

        const score=
          relevant.length
            ? relevant.reduce(
                (sum,response)=>
                  sum+response.score,
                0
              )/relevant.length
            : 0;

        return {

          id:dimension.id,

          name:dimension.name,

          color:dimension.color,

          weight:dimension.weight,

          score:
            Math.round(
              score*10
            )/10

        };

      });


  const overall=
    dimensions.length
      ? dimensions.reduce(
          (sum,dimension)=>
            sum+
            dimension.score*
            dimension.weight,
          0
        ) /
        dimensions.reduce(
          (sum,dimension)=>
            sum+dimension.weight,
          0
        )
      : 0;


  const rounded=
    Math.round(overall*10)/10;

  const band=
    MAXESS_ASSESSMENT.scoreBands.find(
      item=>
        rounded>=item.min &&
        rounded<=item.max
    );


  return {

    overall:rounded,

    band,

    dimensions

  };

}


/* =========================================================
   PERSONALIZED LANGUAGE
========================================================= */

function strongestMessage(
  dimension,
  score
){

  const messages={

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

  return messages[dimension.id];

}


function opportunityMessage(
  dimension,
  score
){

  const messages={

    direction:
      "Your biggest opportunity is becoming even more deliberate about the destination before you begin. A clearer target can dramatically reduce wasted iterations.",

    communication:
      "Your biggest opportunity is giving AI richer context and more precise direction. The clearer the conversation, the less work you have to spend correcting it later.",

    evaluation:
      "Your biggest opportunity is strengthening your quality filter. Make “Why is this not a 10?” a normal part of your workflow.",

    iteration:
      "Your biggest opportunity is turning revision into a deliberate craft. Diagnose the weakness, preserve what works, improve what does not, and repeat.",

    systems:
      "Your biggest opportunity is capturing what works. A successful workflow should become an asset you can reuse rather than a trick you have to rediscover."

  };

  return messages[dimension.id];

}


function buildAnalysis(
  results,
  strongest,
  opportunity
){

  const band=results.band;

  const opening=

    results.overall>=90

      ? "Your score shows highly developed AI craftsmanship. You are not starting from zero — you are at the point where refinement, leverage, and system-building become increasingly valuable."

      : results.overall>=75

      ? "Your score shows meaningful AI capability. You are already beyond basic experimentation, and your next gains are likely to come from becoming more deliberate and repeatable."

      : results.overall>=60

      ? "Your score shows a useful foundation with significant room to grow. The encouraging part is that the biggest gains are often created by changing the way you work with AI, not by learning hundreds of new tools."

      : "Your score shows that there is a large opportunity ahead. That is not a negative verdict — it is a map. A few foundational habits can change the amount of value you get from AI very quickly.";


  const strongestLine=
    `Your strongest dimension is ${strongest.name} at ${Math.round(strongest.score)}/100. ${strongestMessage(strongest,strongest.score)}`;


  const opportunityLine=
    `Your biggest leverage opportunity is ${opportunity.name} at ${Math.round(opportunity.score)}/100. ${opportunityMessage(opportunity,opportunity.score)}`;


  const philosophy=
    "The central lesson behind your assessment is simple: AI is the engine, but you are the director. Your advantage grows when you know what you want, communicate it clearly, judge the result honestly, improve it deliberately, and turn successful work into something reusable.";


  return [

    `<p>${escapeHtml(opening)}</p>`,

    `<p>${escapeHtml(strongestLine)}</p>`,

    `<p>${escapeHtml(opportunityLine)}</p>`,

    `<p>${escapeHtml(philosophy)}</p>`

  ].join("");

}


/* =========================================================
   NEXT PATH
========================================================= */

function buildPath(
  strongest,
  opportunity,
  overall
){

  const path=[];


  path.push({

    title:
      `Strengthen ${opportunity.name}`,

    body:
      opportunityMessage(
        opportunity,
        opportunity.score
      )

  });


  path.push({

    title:
      "Use the 10-point test",

    body:
      "Before accepting an important AI result, ask: What is working? What is missing? What is unclear? What could be better? Then tell AI exactly what to improve."

  });


  path.push({

    title:
      "Turn wins into systems",

    body:
      "Whenever you discover a workflow that works, save the method. Your future self should start from the successful version, not from a blank page."

  });


  return path;

}


/* =========================================================
   COLOR FOR SCORE
========================================================= */

function scoreColor(score){

  if(score>=90){
    return "#ffd45a";
  }

  if(score>=75){
    return "#35e39b";
  }

  if(score>=60){
    return "#3ca8ff";
  }

  return "#765cff";

}


/* =========================================================
   RENDER DIMENSIONS
========================================================= */

function renderDimensions(
  results
){

  DOM.dimensionConstellation.innerHTML="";

  results.dimensions.forEach(
    dimension=>{

      const card=
        document.createElement("div");

      card.className=
        "dimension-orb";

      card.style.setProperty(
        "--dimensionColor",
        dimension.color
      );

      card.innerHTML=`

        <div
          class="dimension-ring"
          style="
            --dimDeg:${dimension.score*3.6}deg
          "
        >

          <span class="dimension-score">
            ${Math.round(dimension.score)}
          </span>

        </div>

        <div class="dimension-name">
          ${escapeHtml(dimension.name)}
        </div>

        <div class="dimension-status">
          ${escapeHtml(
            dimensionLevel(
              dimension.score
            )
          )}
        </div>

      `;

      DOM.dimensionConstellation
        .appendChild(card);

    }
  );

}


function dimensionLevel(score){

  if(score>=90) return "Master";
  if(score>=75) return "Advancing";
  if(score>=60) return "Developing";
  return "Foundation";

}


/* =========================================================
   RENDER INTERESTS
========================================================= */

function renderInterests(){

  DOM.selectedInterests.innerHTML="";

  const selected=
    AI_AREAS.filter(
      area=>
        state.selectedInterests.has(
          area.id
        )
    );


  if(!selected.length){

    DOM.interestReportIntro.textContent=
      "You chose to keep this part open. Your report below is based entirely on your assessment.";

    DOM.selectedInterests.innerHTML=
      `<span class="interest-pill">
        No areas selected
      </span>`;

    return;

  }


  DOM.interestReportIntro.textContent=
    "You told us where you would like AI to become more useful. These areas can help shape what you explore next.";

  selected.forEach(
    area=>{

      const pill=
        document.createElement("span");

      pill.className=
        "interest-pill";

      pill.textContent=
        area.name;

      DOM.selectedInterests
        .appendChild(pill);

    }
  );

}


/* =========================================================
   RENDER RESULTS
========================================================= */

function renderResults(){

  const results=
    calculateResults();

  state.results=
    results;

  state.status=
    "completed";

  state.completedAt=
    new Date().toISOString();


  const strongest=
    [...results.dimensions]
      .sort(
        (a,b)=>b.score-a.score
      )[0];


  const opportunity=
    [...results.dimensions]
      .sort(
        (a,b)=>a.score-b.score
      )[0];


  const color=
    results.band.color;


  DOM.resultsView.classList.add(
    "visible"
  );


  document.body.classList.add(
    "showing-results"
  );


  DOM.overallScore.textContent=
    Math.round(results.overall);


  DOM.scoreStage.style.setProperty(
    "--scoreColor",
    color
  );

  DOM.scoreStage.style.setProperty(
    "--scoreDeg",
    `${results.overall*3.6}deg`
  );


  DOM.resultLevel.style.setProperty(
    "--scoreColor",
    color
  );


  DOM.resultLevelText.textContent=
    `${results.band.label} · ${Math.round(results.overall)}/100`;


  DOM.resultSubtitle.textContent=
    results.band.description;


  renderDimensions(results);


  DOM.strongestName.textContent=
    strongest.name;

  DOM.strongestScore.textContent=
    Math.round(strongest.score);

  DOM.strongestText.textContent=
    strongestMessage(
      strongest,
      strongest.score
    );


  DOM.opportunityName.textContent=
    opportunity.name;

  DOM.opportunityScore.textContent=
    Math.round(opportunity.score);

  DOM.opportunityText.textContent=
    opportunityMessage(
      opportunity,
      opportunity.score
    );


  DOM.analysisCloud.innerHTML=
    buildAnalysis(
      results,
      strongest,
      opportunity
    );


  const path=
    buildPath(
      strongest,
      opportunity,
      results.overall
    );


  DOM.nextPath.innerHTML="";

  path.forEach(
    (step,index)=>{

      const card=
        document.createElement("article");

      card.className=
        "path-step";

      card.innerHTML=`

        <div class="path-number">
          ${index+1}
        </div>

        <h4>
          ${escapeHtml(step.title)}
        </h4>

        <p>
          ${escapeHtml(step.body)}
        </p>

      `;

      DOM.nextPath.appendChild(card);

    }
  );


  renderInterests();


  if(results.overall>=90){

    document.getElementById(
      "ctaTitle"
    ).textContent=
      "You are ready to turn AI capability into leverage.";

    document.getElementById(
      "ctaBody"
    ).textContent=
      "You have already developed a strong level of AI craftsmanship. The next opportunity is learning how to turn that capability into repeatable workflows, stronger outputs, and a larger personal advantage.";

  }else if(results.overall>=75){

    document.getElementById(
      "ctaTitle"
    ).textContent=
      "You are closer to the next level than you may think.";

    document.getElementById(
      "ctaBody"
    ).textContent=
      "You already have meaningful capability. The next step is not trying everything. It is strengthening the few habits that will multiply what you can already do.";

  }else{

    document.getElementById(
      "ctaTitle"
    ).textContent=
      "You now know exactly where to begin.";

    document.getElementById(
      "ctaBody"
    ).textContent=
      "Your score is not a judgment of your potential. It is a starting map. The right AI habits can turn the technology from something you occasionally use into something that consistently works for you.";

  }


  window.scrollTo({
    top:0,
    behavior:"smooth"
  });

}


/* =========================================================
   SHOW RESULTS AFTER INTERESTS
========================================================= */

function finishInterestSelection(){

  DOM.interestsView.classList.remove(
    "visible"
  );

  renderResults();

}


/* =========================================================
   NAYA
========================================================= */

/* =========================================================
   NAYA VOICE — canonical interface only.
   naya-voice.js (NayaVoice.speak / NayaVoice.stop) is the
   ONLY voice interface. Never raw speechSynthesis here.
   The label is shown honestly (SN-0502): Tier 1 reads
   "SYNTHESIZED VOICE" until her true voice lands.
========================================================= */
function nayaVoiceAvailable(){
  return typeof window.NayaVoice !== "undefined" &&
         typeof window.NayaVoice.speak === "function";
}

function refreshVoiceLabel(){
  const el=document.getElementById("voiceLabel");
  if(!el) return;
  if(nayaVoiceAvailable()){
    el.textContent=window.NayaVoice.voiceLabel;
    el.style.display="";
  }else{
    el.textContent="";
    el.style.display="none";
  }
}

function setNayaButtonUI(playing){
  state.nayaPlaying=playing;
  DOM.nayaButton.classList.toggle("playing", playing);
  DOM.nayaButton.setAttribute("aria-pressed", String(playing));
  DOM.nayaPrimary.textContent=playing ? "Pause Naya" : "Press Play";
  DOM.nayaSecondary.textContent=playing ? "Naya is speaking" : "Listen to Naya";
}

function playNaya(){
  if(!nayaVoiceAvailable()){
    return;
  }
  refreshVoiceLabel();
  const question=currentQuestion();
  if(!question){
    return;
  }
  /* One control per question: speak THIS question's text.
     NayaVoice.speak cancels in-flight speech — no overlap. */
  window.NayaVoice.speak(question.question, {
    onstart:()=>setNayaButtonUI(true),
    onend:()=>setNayaButtonUI(false),
    onerror:()=>setNayaButtonUI(false)
  });
}

function stopNaya(){
  /* Navigating away stops audio — never bleed across questions. */
  if(nayaVoiceAvailable()){
    window.NayaVoice.stop();
  }
  setNayaButtonUI(false);
}

/* =========================================================
   PDF / PRINT
========================================================= */

function downloadReport(){

  if(!state.results){
    return;
  }

  window.print();

}


/* =========================================================
   RESET
========================================================= */

function resetAssessment(){

  stopNaya();

  state.currentQuestionIndex=0;

  state.selectedAnswerId=null;

  state.responses=[];

  state.status="in_progress";

  state.startedAt=
    new Date().toISOString();

  state.completedAt=null;

  state.transitioning=false;

  state.teachingOpen=false;

  state.interestBoard=0;

  state.selectedInterests=
    new Set();

  state.results=null;


  DOM.resultsView.classList.remove(
    "visible"
  );


  document.body.classList.remove(
    "showing-results"
  );

  DOM.interestsView.classList.remove(
    "visible"
  );

  DOM.assessmentStage.style.display=
    "";

  DOM.nayaButton.style.display=
    "";

  DOM.continueButton.style.display=
    "";

  renderQuestion();

  setTimeout(
    showTeachingCloud,
    100
  );

}


/* =========================================================
   NAVIGATION
========================================================= */

function openNayaNET(){

  /*
    Destination is configurable via window.MAXIS_CONFIG.
    Falls back to the NayaNET home.
  */

  const url =
    (window.MAXIS_CONFIG || {}).enterNayanetUrl ||
    "https://nayanet.xyz/";

  if (/^https?:\/\//.test(url)) {
    window.open(url, "_blank", "noopener,noreferrer");
  } else {
    window.location.href = url;
  }

}


function openFreeTrial(){

  /*
    "Order Naya Power" destination — configurable via
    window.MAXIS_CONFIG.orderUrl. No URL configured means
    no checkout exists yet: the button shows "Coming soon"
    (see maxis-app.js) and this is a deliberate no-op.
    Never invent a fake checkout here.
  */

  const url = (window.MAXIS_CONFIG || {}).orderUrl;
  if (!url) return;
  window.open(url, "_blank", "noopener,noreferrer");

}


/* =========================================================
   EVENTS
========================================================= */

DOM.continueButton.addEventListener(
  "click",
  continueAssessment
);


DOM.cloudContinue.addEventListener(
  "click",
  closeTeachingCloud
);


DOM.interestContinue.addEventListener(
  "click",
  finishInterestSelection
);


DOM.interestSkip.addEventListener(
  "click",
  finishInterestSelection
);


DOM.nayaButton.addEventListener(
  "click",
  ()=>{

    if(state.nayaPlaying){
      stopNaya();
    }else{
      playNaya();
    }

  }
);


DOM.pdfButton.addEventListener(
  "click",
  downloadReport
);


DOM.restartButton.addEventListener(
  "click",
  resetAssessment
);


DOM.enterNayaButton.addEventListener(
  "click",
  openNayaNET
);


DOM.freeTrialButton.addEventListener(
  "click",
  openFreeTrial
);


document.addEventListener(
  "keydown",
  event=>{

    if(
      event.key==="Escape" &&
      state.teachingOpen
    ){

      closeTeachingCloud();

      return;

    }

    if(
      event.key==="Escape" &&
      state.nayaPlaying
    ){

      stopNaya();

    }

  }
);


/* =========================================================
   INITIALIZATION
========================================================= */

try{

  validate();

  buildInterestBoards();

  refreshVoiceLabel();
  if(!nayaVoiceAvailable() && DOM.nayaButton){
    /* No canonical voice interface: no dead control. */
    DOM.nayaButton.style.display="none";
  }

  renderQuestion();

  /*
    The first teaching cloud introduces
    the assessment before the first answer.
  */

  setTimeout(
    showTeachingCloud,
    160
  );

}catch(error){

  console.error(
    "MAXESS initialization error:",
    error
  );

  DOM.questionLabel.textContent=
    "ASSESSMENT ERROR";

  DOM.questionTitle.textContent=
    "MAXESS is temporarily unavailable.";

  DOM.answers.innerHTML="";

  DOM.continueButton.disabled=true;

}

