---
layout: cover
title: Formal Guarantees Meet Practical Constraints
---

---
layout: bars
title: Running Example
section: Introduction
message: "Input: income, debt and the requested amount. Output: the approved amount."
clicks: 2
---

<div class="cols">
<div class="col">
  <div class="card">
    <div class="card-head"><span class="keep">v2</span>, after the cleanup</div>
    <LoanCode name="v2" :marked="false" :focus="$clicks === 1 ? [6, 7] : $clicks >= 2 ? [9, 10, 11] : []" />
  </div>
</div>
<div class="col grow">
  <div v-click="1" class="card"><ScorePlot :width="756" /></div>
  <div v-click="2" class="card"><LoanLanes view="single" :width="756" :tests="false" /></div>
</div>
</div>

---
layout: bars
title: Regression Detection
shot: regression-detection
section: Introduction
message: The three tests do not detect that the limit for full approvals dropped from 60 to 50.
messageAt: 3
clicks: 3
---

<div class="cols">
<div class="col">
  <div class="card">
    <div class="card-head"><span class="keep">v2</span>, after the cleanup</div>
    <LoanCode name="v2body" :marked="$clicks >= 3" />
  </div>
  <div v-click="2" class="card">
    <div class="card-head"><span class="keep">v1</span>, before the cleanup</div>
    <LoanCode name="v1body" :marked="$clicks >= 3" />
  </div>
</div>
<div class="col grow">
  <div class="card">
    <LoanLanes :view="$clicks >= 3 ? 'both' : 'question'" :width="756" :tests="$clicks >= 1" :missed="$clicks >= 3" />
  </div>
  <div v-click="1" class="card">
    <table class="io">
      <thead><tr><th></th><th>call</th><th>v1</th><th>v2</th></tr></thead>
      <tbody>
        <tr><td><span class="dot" /></td><td>approvedAmount(300, 10, 20)</td><td>20<span class="ok">&#10003;</span></td><td>20<span class="ok">&#10003;</span></td></tr>
        <tr><td><span class="dot" /></td><td>approvedAmount(60, 10, 8)</td><td>5<span class="ok">&#10003;</span></td><td>5<span class="ok">&#10003;</span></td></tr>
        <tr><td><span class="dot" /></td><td>approvedAmount(10, 30, 1)</td><td>0<span class="ok">&#10003;</span></td><td>0<span class="ok">&#10003;</span></td></tr>
        <tr v-click="3" class="hit"><td><span class="box" /></td><td>approvedAmount(200, 10, 55)</td><td>55</td><td>50</td></tr>
      </tbody>
    </table>
    <div class="key"><span class="dot" /> developer test <span v-click="3">&nbsp; <span class="box" /> no test</span></div>
  </div>
</div>
</div>

---
layout: bars
title: Formal Guarantees Meet Practical Constraints
section: Background
message: For this method, the comparison of v1 and v2 ends in UNKNOWN.
messageAt: 2
clicks: 2
sources: "Symbolic analysis: King 1976, Person et al. 2008. Limitations: Cadar and Sen 2013, Baldoni et al. 2018, Matiyasevich 1970."
---

<!-- Solver limitations: tried on 2026-11-14 (evidence/solver-check). Z3 with PASDA's encoding returns unknown at once for each of the three path conditions, cvc5 times out after 30 s, and dReal answers delta-sat. -->

<div class="limits">
  <div class="card compact analysis">
    <div class="card-head">Method summaries of <span class="keep">v1</span> and <span class="keep">v2</span>, from symbolic analysis</div>
    <LoanLanes :view="$clicks === 0 ? 'blank' : 'program'" :verdict="$clicks === 1 ? 'NEQ' : 'UNKNOWN'" :witness="$clicks === 1" :lane-label="['', 'in theory', 'in practice'][$clicks]" :width="1120" :tests="false" summary />
  </div>
  <div class="solver">
    <div v-click="1" class="card compact fact"><div class="card-head">In theory</div>A solver compares the summaries of v1 and v2 for all inputs.<div class="key"><span class="chip medium eq">EQ</span> proven equal &nbsp; <span class="chip medium neq">NEQ</span> proven different</div></div>
    <div v-click="2" class="card compact fact"><div class="card-head">In practice</div>The solver cannot decide whether inputs satisfy the <span class="ringed">path conditions</span>.<div class="verdict"><span class="chip medium unk">UNKNOWN</span> for v1 against v2 as a whole</div></div>
  </div>
  <div v-click="2" class="card compact fact"><div class="card-head">Path explosion</div><JavaCode code="while (debt &gt; 0) debt -= rate;" bare />One path per number of iterations, with no bound on debt.</div>
  <div v-click="2" class="card compact fact"><div class="card-head">Unmodeled behavior</div><JavaCode code="score = Math.log10(income);" bare />A native method that<br>the analysis has no model for.</div>
  <div v-click="2" class="card compact fact"><div class="card-head">Solver limitations</div><JavaCode code="p = 1 / (1 + Math.exp(risk));" bare />Z3 returns unknown for a condition on p, and cvc5 times out.</div>
</div>

<style>
.limits { width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px 24px; }
.limits .analysis { grid-column: span 2; }
.limits .solver { display: flex; flex-direction: column; gap: 20px; }
.limits .solver > .card { flex: none; }
.limits .solver > .card:last-child { flex: 1; }
.limits .verdict { margin-top: 10px; display: flex; align-items: center; gap: 12px; font-size: var(--fs-note); color: var(--muted); }
.limits .ringed { margin-right: -8px; padding: 0 8px; border-radius: 8px; background: var(--spec-in); }
.limits .key { margin-top: 12px; }
.limits .java { margin-bottom: 8px; font-size: var(--fs-note); line-height: 1.3; }
</style>

---
layout: bars
title: Overview
section: Background
message: ""
clicks: 1
---

<!-- The overview returns before the Teralizer part and before the conclusion, with the part that starts marked. -->

<Overview :active="$clicks" />

---
layout: bars
title: Equivalence Checking
section: PASDA
message: Checking each path on its own narrows UNKNOWN from the whole method to full approvals above 50.
messageAt: 1
clicks: 1
sources: "PRV: Böhme et al. 2013. ARDiff: Badihi et al. 2020. DSE: Person et al. 2008."
---

<div class="levels">
  <div class="card compact">
    <div class="card-head cited">Program level: one verdict for the method<span class="cite">existing</span></div>
    <LoanLanes view="program" :width="820" :tests="false" lane-label="ARDiff, DSE" undecided />
  </div>
  <div v-click="1" class="card compact">
    <div class="card-head cited">Partition level: one verdict per path<span class="cite">existing</span></div>
    <LoanLanes view="noproof" :width="820" :tests="false" lane-label="PRV" undecided />
  </div>
  <div class="card compact reasons">
    <div class="reason"><span class="chip unk">UNKNOWN</span><span>the solver cannot decide the conditions on <code>p</code></span></div>
  </div>
  <div v-click="1" class="card compact reasons">
    <div class="reason"><span class="chip eq">EQ</span><span>same output in v1 and v2, whatever <code>p</code> is</span></div>
    <div class="reason"><span class="chip unk">UNKNOWN</span><span>different outputs, but <code>p >= 0.8</code> is undecided</span></div>
  </div>
</div>

<style>
.levels { width: 100%; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 24px; align-items: start; }
.levels .reasons { display: flex; flex-direction: column; gap: 12px; }
.levels .reason { display: grid; grid-template-columns: 150px minmax(0, 1fr); align-items: center; column-gap: 18px; font-size: var(--fs-note); line-height: 1.3; }
.levels .reason .chip { padding: 4px 0; font-size: var(--fs-label); text-align: center; }
.levels .reason code { font-size: 0.92em; }
</style>

---
layout: bars
title: Best-Effort Classification
shot: best-effort-classification
section: PASDA
message: PASDA reports MAYBE_NEQ for full approvals above 50 and EQ for all other inputs.
messageAt: 2
clicks: 2
sources: "PASDA: Glock, Pichler and Pinzger 2024."
---

<div class="cols">
<div class="col">
  <div class="card"><LoanLanes view="pasda" :width="990" :tests="false" prior questions :answers="$clicks >= 1" :result="$clicks >= 2" /></div>
</div>
<div class="col grow">
  <div class="card">
    <div class="card-head">Verdict for <span class="keep">v1</span> against <span class="keep">v2</span></div>
    <table class="verdicts">
      <tbody>
        <tr><td>ARDiff</td><td><span class="chip unk">UNKNOWN</span></td></tr>
        <tr><td>DSE</td><td><span class="chip unk">UNKNOWN</span></td></tr>
        <tr v-click="2" class="main"><td>PASDA</td><td><span class="chip mneq">MAYBE_NEQ</span></td></tr>
      </tbody>
    </table>
    <p v-click="2" class="why">Above 50 the outputs provably differ. The solver cannot decide whether any input reaches that path.</p>
    <div v-click="2" class="key other"><span class="chip medium meq">MAYBE_EQ</span> when no path shows a difference<br>but not all paths are proven equal</div>
  </div>
</div>
</div>

<style>
.key.other { margin-top: 18px; padding-top: 18px; border-top: 2px solid var(--rule); }
.key.other .chip { margin-right: 10px; }
</style>

---
layout: bars
title: Classification Results
section: PASDA
message: PASDA proves 104 of the 141 pairs, 9 more than PRV, the next best tool.
sources: "PRV: Böhme et al. 2013. ARDiff and benchmark: Badihi et al. 2020. DSE: Person et al. 2008."
---

<div class="cols">
<div class="col">
  <div class="card">
    <div class="card-head">Timeout of <span class="keep">1&nbsp;h</span> per pair</div>
    <UndecidedZoom :timeout="3600" style="width: 1130px" />
  </div>
</div>
<div class="col grow">
<div class="card fact"><div class="card-head">Setup</div>141 program pairs (73 EQ, 68 NEQ) against PRV, ARDiff and DSE.</div>
<div class="card fact"><div class="card-head">Result</div>With a 1&nbsp;h timeout, 32 of the 37 pairs not proven get a best&#8209;effort verdict. 23 are correct.</div>
<div class="card fact"><div class="card-head">Cost</div>6 to 17% slower than PRV. Against ARDiff 20 to 35% slower for EQ, 2 to 3 times faster for NEQ.</div>
</div>
</div>

---
layout: bars
title: Limitations of PASDA
section: PASDA
message: PASDA's best-effort verdicts come from the same paths and solver answers as its proofs.
messageAt: 1
clicks: 3
sources: "PASDA: Glock, Pichler and Pinzger 2024. Directions: Yang et al. 2014, Kuchta et al. 2018, Godefroid and Luchaup 2011, Sharma et al. 2020, Noller et al. 2020."
---

<!-- The process of the PASDA part with PASDA on the full approval of the example, then on clicks the three reasons of the Background slide at their stages and the two directions of thesis Section 4.7 drawn on it. -->

<Routes stage="directions" :step="$clicks" />

---
layout: bars
title: Overview
section: Teralizer
message: ""
---

<Overview :active="2" />

---
layout: bars
title: Test Generalization
shot: test-generalization
section: Teralizer
message: The generalized test detects the regression that the developer test misses.
messageAt: 2
clicks: 2
sources: "Teralizer: Glock, Bauer and Pinzger 2025. Test generalization: Fraser and Zeller 2011, Peleg et al. 2018. Property-based testing: Claessen and Hughes 2000, jqwik-team 2022."
---

<!-- From the developer test to its path, to the generalized test, to the inputs it samples. Left the two tests, right the path of the developer test through v1 and the sampled inputs on v1 and v2. The slide opens with the developer test and its path, the first click adds the generalized test, the second the sampled inputs and the message. Both maps share one width, so that the amounts line up. The recorded condition reads p > 0.8, and the slide writes >= as the code does. The sampled amounts are illustrative. -->

<div class="cols merged">
<div class="col grow">
  <div class="card compact fill">
    <div class="card-head">Developer test</div>
    <LoanCode name="test" />
  </div>
  <div v-click="1" class="card compact">
    <div class="card-head cited">Generalized test<span class="cite">simplified</span></div>
    <LoanCode name="property" />
    <div class="key"><span class="swatch in" /> from the path condition &nbsp; <span class="swatch out" /> from the symbolic output</div>
  </div>
</div>
<div class="col">
  <div class="card compact">
    <div class="card-head cited"><span>The path it follows through <span class="keep">v1</span></span><span class="cite">single-path symbolic analysis</span></div>
    <LoanLanes view="path" :width="850" :scale="0.9" summary axis-label="inline" />
    <div class="rec"><span>recorded without a solver</span><code class="in">p &gt;= 0.8 &amp;&amp; amount &lt;= 60</code><code class="out">amount</code></div>
  </div>
  <div v-click="2" class="card compact">
    <div class="card-head">Sampled inputs of this path</div>
    <LoanLanes view="teralizer" only="full" headless :axis-label="false" summary :width="850" :scale="0.9" />
  </div>
</div>
</div>

<style>
.merged { gap: 24px; }
.merged .rec { margin-top: 12px; display: flex; align-items: center; gap: 12px; font-size: var(--fs-note); color: var(--muted); white-space: nowrap; }
.merged .rec code { padding: 3px 12px; font-size: var(--fs-label); color: var(--ink); }
.merged .rec .in { margin-left: auto; }
</style>

---
layout: bars
title: Detection and Runtime
section: Teralizer
message: On both benchmarks, the generalized tests detect more mutants than the tests they come from.
sources: "EvoSuite: Fraser and Arcuri 2011. EqBench: Badihi et al. 2021. Mutation testing with PIT: Coles et al. 2016."
---

<!-- The plots show the configurations on the Pareto frontier (tab:pareto-eqbench and tab:pareto-commons) and EvoSuite with 60 s on EqBench. Each EvoSuite budget was generalized with two strategies and 10, 50 and 200 tries, so some of its six generalized configurations are not on the frontier and not shown. -->

<div class="stack">
<div class="key plotkey"><span class="bdot b1" />1 s &nbsp; <span class="bdot b10" />10 s &nbsp; <span class="bdot b60" />60 s search budget &nbsp;&nbsp; <span class="bdot ring" />EvoSuite alone &nbsp; <span class="bdot plain" />then generalized with 10, 50 and 200 inputs per test</div>
<div class="cols">
  <div class="card"><div class="card-head"><span class="keep">EqBench</span></div><ParetoPlot :width="824" :height="240" /></div>
  <div class="card"><div class="card-head">Apache Commons</div><ParetoPlot dataset="commons" :width="824" :height="240" /></div>
</div>
<div class="facts"><div class="card fact"><div class="card-head">Setup</div>EvoSuite tests with 1&nbsp;s, 10&nbsp;s or 60&nbsp;s per class, generalized by Teralizer.</div><div class="card fact"><div class="card-head">Result</div>EqBench: +1.2 to 3.9 points. Apache Commons: +0.8 to 1.3 points.</div><div class="card fact"><div class="card-head">Limitations</div>Generalized suites take up to 27.5 times as long to run. Developer tests gain 0.05 to 0.07 points.</div></div>
</div>

---
layout: bars
title: Overview
section: Conclusion
message: ""
---

<Overview :active="3" />

---
layout: bars
title: Summary
shot: summary
section: Conclusion
message: "PASDA: a correct verdict for 23 of 37 pairs not proven. Teralizer: up to 3.9 points more mutants detected."
clicks: 1
sources: "PASDA: Glock, Pichler and Pinzger 2024. Teralizer: Glock, Bauer and Pinzger 2025."
---

<!-- The research question of the overview above the picture of Limitations of PASDA with both routes. The click adds what limits each stage. 23 of 37: tab:program-level-classifications-3 (1 h timeout). 3.9 points: sec:teralizer-rq1 (EqBench, 1.2 to 3.9). -->

<div class="summary">
  <Question compact />
  <Routes stage="summary" :step="$clicks" />
</div>

<style>
.summary { width: 100%; display: flex; flex-direction: column; gap: 40px; align-items: stretch; }
</style>

---
layout: bars
title: Questions
section: Conclusion
message: ""
---

<!-- The four key slides of the talk, as anchors for questions. The images are renders of this deck in public/shots/. Refresh them with `pnpm shots` after `pnpm png`. -->

<div class="shots four">
  <img src="/shots/regression-detection.png" alt="Regression Detection">
  <img src="/shots/best-effort-classification.png" alt="Best-Effort Classification">
  <img src="/shots/test-generalization.png" alt="Test Generalization">
  <img src="/shots/summary.png" alt="Summary">
</div>

<style>
.shots.four { width: 100%; display: grid; grid-template-columns: repeat(2, 704px); justify-content: center; gap: 20px 40px; }
.shots.four img { display: block; width: 704px; height: 396px; border: 2px solid var(--rule); border-radius: 8px; }
</style>

---
layout: bars
title: Papers
section: Backup
message: ""
---

<!-- Backup: the four papers behind the thesis, shown only if someone asks. The images are the first pages of the published PDFs on glockyco.com, rendered with `pdftoppm -r 150 -singlefile -png` and cropped to the text area with a margin of 24 px, 13 wide to 15 high from the top. The doctoral symposium PDF starts with a cover sheet of the ACM Digital Library, so its image is page 2. -->

<div class="papers">
  <figure class="card"><img src="/papers/pasda.png" alt="First page of the PASDA paper"><figcaption><div class="card-head">PASDA</div>Journal of Systems and Software, 2024<br><span class="id">doi:10.1016/<wbr>j.jss.2024.112037</span></figcaption></figure>
  <figure class="card"><img src="/papers/teralizer.png" alt="First page of the Teralizer paper"><figcaption><div class="card-head">Teralizer</div>Preprint, 2025<br><span class="id">arXiv:2512.14475</span></figcaption></figure>
  <figure class="card"><img src="/papers/teralizer-tool.png" alt="First page of the Teralizer tool paper"><figcaption><div class="card-head">Teralizer tool</div>Preprint, 2026<br><span class="id">arXiv:2611.19242</span></figcaption></figure>
  <figure class="card"><img src="/papers/docsym.png" alt="First page of the doctoral symposium paper"><figcaption><div class="card-head">Doctoral symposium</div>ICSE Companion, 2024<br><span class="id">doi:10.1145/<wbr>3639478.3639783</span></figcaption></figure>
</div>

<style>
.papers { width: 100%; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; font-size: var(--fs-small); line-height: 1.35; }
.papers figure { margin: 0; padding: 20px 20px 24px; }
/* The upper part of each first page, so that title, authors and abstract stay readable. */
.papers img { display: block; width: 100%; height: 410px; object-fit: cover; object-position: top; border: 2px solid var(--rule); border-radius: 6px; background: #fff; }
.papers figcaption { margin-top: 20px; }
.papers .id { font-family: var(--mono); font-size: var(--fs-note); color: var(--muted); }
</style>
