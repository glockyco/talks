---
layout: bars
title: Symbolic Analysis
section: Backup
message: Each path of the method yields a path condition and a symbolic output.
sources: "Symbolic execution: King 1976. Symbolic PathFinder: Păsăreanu et al. 2013."
---

<!-- Backup: what symbolic analysis does, on v2 of the example, shown only if someone asks. The paths are those of the map on the main slides. Symbolic PathFinder splits a path further where Math.min decides: the path condition it records for the developer test of v1 ends in amount <= 60 (slide Test Generalization). -->

<div class="cols symb">
<div class="col">
  <div class="card">
    <div class="card-head"><span class="keep">v2</span> of the example</div>
    <LoanCode name="v2" />
  </div>
</div>
<div class="col grow">
  <div class="card">
    <div class="card-head">Assignments build formulas over the inputs</div>
    <div class="row"><code>risk</code><span>=</span><code>(3.0 * debt - income) / 100.0</code></div>
    <div class="row"><code>p</code><span>=</span><code>1 / (1 + exp((3.0 * debt - income) / 100.0))</code></div>
  </div>
  <div class="card">
    <div class="card-head">Each return ends a path</div>
    <div class="row"><i class="full" /><code class="in">p >= 0.8</code><Arrow /><code class="out">min(amount, 50)</code></div>
    <div class="row"><i class="partial" /><code class="in">0.5 &lt;= p &lt; 0.8</code><Arrow /><code class="out">min(amount, 5)</code></div>
    <div class="row"><i class="reject" /><code class="in">p &lt; 0.5</code><Arrow /><code class="out">0</code></div>
    <div class="key"><span class="swatch in" /> path condition &nbsp; <span class="swatch out" /> symbolic output</div>
  </div>
</div>
</div>

<style>
.symb .row { margin: 10px 0; display: flex; align-items: center; gap: 12px; }
.symb .row code { font-size: var(--fs-note); white-space: nowrap; }
.symb .row code.in, .symb .row code.out { padding: 4px 12px; }
.symb .row i { flex: none; width: 8px; height: 36px; border-radius: 4px; }
.symb .row i.full { background: var(--branch-full); }
.symb .row i.partial { background: var(--branch-partial); }
.symb .row i.reject { background: var(--branch-reject); }
.symb .key { margin-top: 14px; }
</style>

---
layout: bars
title: Why Reachability Is Hard
section: Backup
message: To prove that line 5 can be reached, a solver has to find the password.
---

<!-- Backup: why "can an input reach this path?" is the hard question, shown only if someone asks. MessageDigest and Arrays are from the Java standard library. Tried on 2026-11-15 with Z3 (.agent-build/phd-seminar/hash-check in the thesis repository): SHA-256 over bit vectors for a password of eight bytes. With the bytes fixed to the password, Z3 answers sat in 0.8 s. With the bytes unknown, it returns unknown (timeout) after 300 s. Loan example: .agent-build/phd-seminar/solver-check (Z3 returns unknown for each path condition, trying all 201 x 201 inputs takes 9 ms). -->

<div class="cols reach">
<div class="col">
  <div class="card">
    <div class="card-head">A password check</div>
    <JavaCode code="boolean login(String password) throws Exception {&#10;  MessageDigest sha = MessageDigest.getInstance(&quot;SHA-256&quot;);&#10;  byte[] hash = sha.digest(password.getBytes());&#10;&#10;  if (Arrays.equals(hash, STORED)) return true;&#10;  return false;&#10;}" :tints="{ 5: 'in' }" />
    <div class="card-head">Path condition of line 5</div>
    <code class="in">SHA-256(password) == STORED</code>
  </div>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">Can an input reach line 5?</div>Only a valid password does. To find one, a solver has to invert SHA&#8209;256, which the function is built to prevent.</div>
  <div class="card fact"><div class="card-head">Tried with <span class="keep">Z3</span></div>Given the password, Z3 confirms the path in 1&nbsp;s. Without it, Z3 has no answer after 300&nbsp;s.</div>
  <div class="card fact"><div class="card-head">The loan example</div>Its path conditions contain <code>Math.exp</code>, and Z3 has no answer either. Running the method with inputs reaches every path in milliseconds.</div>
</div>
</div>

<style>
.reach .card > code.in { display: inline-block; padding: 4px 12px; font-size: var(--fs-note); }
</style>

---
layout: bars
title: How PASDA Works
section: Backup
message: PASDA combines three existing approaches and adds best-effort verdicts on top.
sources: "DSE: Person et al. 2008. ARDiff: Badihi et al. 2020. PRV: Böhme et al. 2013. PASDA: Glock, Pichler and Pinzger 2024."
---

<!-- Backup: PASDA's mechanism, shown only if someone asks. The figure is the process overview of the PASDA paper (projects/pasda-paper/process-overview.pdf in the thesis repository), rendered with `pdftoppm -r 300 -singlefile -png`. Combination: sec:pasda-background and sec:pasda-approach. Retrofit: sec:pasda-rq2 (tab:program-level-classifications-3) and sec:reflections-findings. -->

<div class="cols mech">
<div class="col">
  <figure class="card"><img src="/backup/pasda-process.png" alt="PASDA's process, from the PASDA paper"><figcaption>PASDA's process, from the paper. Gray: changed or new in PASDA.</figcaption></figure>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">Combines</div>Differential symbolic execution of both versions, ARDiff's abstraction and refinement, PRV's partitions.</div>
  <div class="card fact"><div class="card-head">Adds</div>MAYBE_EQ and MAYBE_NEQ for each partition and for the method, from the partial proofs.</div>
  <div class="card fact"><div class="card-head">Retrofitted</div>Added to ARDiff, DSE and PRV, the best&#8209;effort verdicts reach comparable accuracy.</div>
</div>
</div>

<style>
.mech figure { margin: 0; padding: 28px 28px 22px; }
.mech img { display: block; width: 980px; background: #fff; border-radius: 6px; }
.mech figcaption { margin-top: 14px; font-size: var(--fs-note); color: var(--muted); }
</style>

---
layout: bars
title: Classification Rules
section: Backup
message: Each partition gets its verdict from three questions to the solver.
sources: "PASDA: Glock, Pichler and Pinzger 2024."
---

<!-- Backup: how PASDA classifies, in words, shown only if someone asks. The rows summarize tab:partition-reachability and tab:partition-output-classification of the thesis and the rule of sec:pasda-classification that combines them. Two Queries on the Outputs shows the rule for the outputs as a matrix of the two queries. The method's verdict is the aggregation of sec:pasda-program-classification. The three questions are the PC-Query, the NEQ-Query and the EQ-Query. Two of them are the lanes "path reachable?" and "outputs differ?" on Best-Effort Classification. -->

<div class="rules">
  <div class="card">
    <div class="card-head">Verdict for a partition</div>
    <table class="by">
      <tbody>
        <tr><th rowspan="2">proof</th><td><span class="chip small eq">EQ</span></td><td>No input of the partition gives different outputs.</td><td class="how">outputs differ? no</td></tr>
        <tr><td><span class="chip small neq">NEQ</span></td><td>An input that reaches the partition gives different outputs.</td><td class="how">outputs differ? yes, or outputs equal? no<br>path reachable? yes</td></tr>
        <tr class="group"><th rowspan="2">best effort</th><td><span class="chip small meq">MAYBE_EQ</span></td><td>An input gives equal outputs, and the solver has no answer on a difference.</td><td class="how">outputs differ? no answer<br>outputs equal? yes</td></tr>
        <tr><td><span class="chip small mneq">MAYBE_NEQ</span></td><td>An input gives different outputs, but through an uninterpreted function or in a partition that may be unreachable.</td><td class="how">outputs differ? yes<br>with an uninterpreted function,<br>or path reachable? no answer</td></tr>
        <tr class="group"><th>no evidence</th><td><span class="chip small unk">UNKNOWN</span></td><td>The solver has no answer on a difference and none on equality.</td><td class="how">outputs differ? no answer<br>outputs equal? no answer</td></tr>
      </tbody>
    </table>
    <div class="key">Each question asks the solver for an input of the partition: one that reaches it, one with different outputs, one with equal outputs.</div>
  </div>
  <div class="side">
    <div class="card">
      <div class="card-head">Verdict for the method</div>
      <table class="agg">
        <tbody>
          <tr><td><span class="chip small eq">EQ</span></td><td>all partitions are EQ</td></tr>
          <tr><td><span class="chip small meq">MAYBE_EQ</span></td><td>some are EQ or MAYBE_EQ, none is NEQ or MAYBE_NEQ</td></tr>
          <tr><td>otherwise</td><td>the first that occurs of NEQ, MAYBE_NEQ, UNKNOWN, DEPTH_LIMITED</td></tr>
        </tbody>
      </table>
    </div>
    <div class="key">Uninterpreted function: stands for unchanged code, so its value is not tied to the real code.<br>DEPTH_LIMITED: the analysis stopped at its limit for loops.</div>
  </div>
</div>

<style>
.rules { width: 100%; display: grid; grid-template-columns: minmax(0, 1fr) 460px; gap: 24px; align-items: start; }
.rules table { width: 100%; border-collapse: collapse; font-size: var(--fs-detail); line-height: 1.3; }
.rules td, .rules th { padding: 10px 20px 10px 0; border-bottom: 1px solid var(--rule); vertical-align: top; text-align: left; }
.rules th { width: 110px; font-size: var(--fs-note); font-weight: 700; color: var(--muted); }
.rules tr.group td, .rules tr.group th { border-top: 2px solid var(--muted); }
.rules td:last-child { padding-right: 0; }
.rules .how { width: 430px; font-size: var(--fs-label); color: var(--muted); }
.rules .agg td:first-child { white-space: nowrap; color: var(--muted); }
.rules tbody tr:last-child td, .rules tbody tr:last-child th { border-bottom: none; }
.rules .chip { white-space: nowrap; }
.rules .key { margin-top: 14px; line-height: 1.3; }
.rules .side { display: flex; flex-direction: column; gap: 24px; }
.rules .side > .key { margin-top: 0; padding: 0 28px; }
</style>

---
layout: bars
title: Two Queries on the Outputs
section: Backup
message: For 61% of the partitions, the two queries get different answers.
sources: "PASDA: Glock, Pichler and Pinzger 2024."
---

<!-- Backup: the output classification of tab:partition-output-classification (Table 2 of the paper) as a matrix of the two queries, shown only if someone asks. The queries: NEQ-Query checks P and o1 != o2, EQ-Query checks P and o1 = o2, each for satisfiability (SatisfiabilityChecker.java in the implementation). Reachability: tab:partition-reachability. Counts: results database of the replication package (doi:10.5281/zenodo.10033132), PASDA at 300 s, first repetition of each pair, all iterations, 4,917 partition records with both results (.agent-build/phd-seminar/pasda-research/report.md in the thesis repository). The answers differ in 3,002 of them. Both UNSAT needs an unsatisfiable path condition, and such paths are skipped. -->

<div class="cols two">
<div class="col">
  <div class="card">
    <table class="mx">
      <thead>
        <tr><th></th><th colspan="3" class="axis">outputs equal? <span>EQ-Query</span></th></tr>
        <tr><th class="axis side">outputs differ? <span>NEQ-Query</span></th><th>yes</th><th>no</th><th>no answer</th></tr>
      </thead>
      <tbody>
        <tr><th>no</th><td><span class="chip small eq">EQ</span><i>1,916</i></td><td class="none">cannot occur<i>0</i></td><td><span class="chip small eq">EQ</span><i>350</i></td></tr>
        <tr><th>yes</th><td><span class="chip small neq">NEQ</span><i>54</i><br><span class="chip small mneq">MAYBE_NEQ</span><i>1,568</i></td><td><span class="chip small neq">NEQ</span><i>686</i></td><td><span class="chip small neq">NEQ</span><i>2</i><br><span class="chip small mneq">MAYBE_NEQ</span><i>0</i></td></tr>
        <tr><th>no answer</th><td><span class="chip small meq">MAYBE_EQ</span><i>13</i></td><td><span class="chip small neq">NEQ</span><i>35</i></td><td><span class="chip small unk">UNKNOWN</span><i>293</i></td></tr>
      </tbody>
    </table>
    <div class="key">Two verdicts in a cell: MAYBE_NEQ if an uninterpreted function is involved.<br>Numbers: partitions at a timeout of 300&nbsp;s, 4,917 with both answers.</div>
  </div>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">Each query asks for an input</div>One input of the partition with different outputs, and one with equal outputs. Both can exist.</div>
  <div class="card fact"><div class="card-head">With an uninterpreted function (UIF)</div>It stands for unchanged code, so a difference found through it may not exist in the real code.</div>
  <div class="card fact"><div class="card-head">Then: path reachable?</div>NEQ needs an input that reaches the partition, found without a UIF. Otherwise it becomes MAYBE_NEQ.</div>
</div>
</div>

<style>
.two .mx { border-collapse: separate; border-spacing: 8px; font-size: var(--fs-detail); }
.two .mx th { padding: 4px 10px; font-weight: 400; color: var(--muted); text-align: center; white-space: nowrap; }
.two .mx tbody th { text-align: right; }
.two .mx .axis { font-weight: 700; color: var(--ink); }
.two .mx .axis span { margin-left: 8px; font-size: var(--fs-note); font-weight: 400; color: var(--muted); }
.two .mx td { width: 224px; height: 112px; padding: 10px 14px; border-radius: 10px; background: #fff; box-shadow: inset 0 0 0 2px var(--rule); vertical-align: middle; line-height: 1.9; white-space: nowrap; }
.two .mx .side { text-align: right; vertical-align: bottom; }
.two .mx .side span { display: block; margin: 0; }
.two .mx td.none { background: none; box-shadow: inset 0 0 0 2px var(--rule); color: var(--muted); font-size: var(--fs-note); }
.two .mx i { margin-left: 10px; font-style: normal; font-size: var(--fs-note); color: var(--muted); font-variant-numeric: tabular-nums; }
.two .key { margin-top: 12px; line-height: 1.4; }
.two .col:first-child .card { width: min-content; }
</style>

---
layout: bars
title: MAYBE_EQ for a Partition
section: Backup
message: Partitions with MAYBE_EQ occur for 1 of the 141 pairs, where the solver has no answer to the NEQ-Query.
sources: "PASDA: Glock, Pichler and Pinzger 2024. Benchmark: Badihi et al. 2020."
---

<!-- Backup: when a partition gets MAYBE_EQ, shown only if someone asks. From the results database of PASDA's replication package (doi:10.5281/zenodo.10033132), queried on 2026-11-15 (.agent-build/phd-seminar/pasda-research/report.md in the thesis repository): over all repetitions, timeouts and iterations, only sine/mysin/Eq has such partitions (255 records, NEQ-Query UNKNOWN by solver timeout in 243 and by memory limit in 12). The record on the slide is partition 15 of iteration 10 of the first repetition at 300 s (partition.id 658810). The code is lines 55 of oldV.java and 15 and 56 of newV.java in projects/pasda-impl/benchmarks/sine/mysin/Eq. The package does not hold the partition's path condition and symbolic outputs. 0.1%: tab:partition-level-classifications, row 11. -->

<div class="onepart">
  <div class="card">
    <div class="card-head">The pair <span class="keep">sine/mysin/Eq</span>: one of its changes</div>
    <div class="ver">v1</div>
    <JavaCode code="return x*(1.0-x*x*1.0/6.0);" :numbers="[55]" :marks="['55:1.0/6.0']" />
    <div class="ver">v2</div>
    <JavaCode code="double sixth = 1.0/6.0;&#10;return x*(1.0-x*x*sixth);" :numbers="[15, 56]" :marks="['56:sixth']" />
    <div class="key">A sine function of about 150 lines with bit operations and floating-point arithmetic.</div>
  </div>
  <div class="card">
    <div class="card-head">One of its partitions, at a timeout of <span class="keep">300 s</span></div>
    <table>
      <tbody>
        <tr><td>PC-Query</td><td>SAT, with UIF: MAYBE_REACHABLE</td></tr>
        <tr><td>NEQ-Query</td><td>UNKNOWN, the solver timed out</td></tr>
        <tr><td>EQ-Query</td><td>SAT, an input with equal outputs</td></tr>
        <tr><td>verdict</td><td><span class="chip small meq">MAYBE_EQ</span></td></tr>
      </tbody>
    </table>
  </div>
  <div class="card fact"><div class="card-head">How often</div>0.1% of the partitions of a run, at a timeout of 300&nbsp;s. No other pair has such a partition at any timeout.</div>
  <div class="card fact"><div class="card-head">Why the NEQ-Query has no answer</div>Over all runs, 255 partitions of the pair get MAYBE_EQ: 243 after a timeout of the solver, 12 at its memory limit.</div>
</div>

<style>
.onepart { width: 100%; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; align-items: stretch; }
.onepart .ver { margin: 10px 0 4px; font-size: var(--fs-note); font-weight: 700; color: var(--muted); }
.onepart .key { margin-top: 16px; line-height: 1.3; }
.onepart table { width: 100%; border-collapse: collapse; font-size: var(--fs-note); }
.onepart td { padding: 12px 0; border-bottom: 1px solid var(--rule); }
.onepart td:first-child { width: 170px; color: var(--muted); white-space: nowrap; }
.onepart tr:last-child td { border-bottom: none; }
</style>

---
layout: bars
title: "Evaluation Setup: PASDA"
section: Backup
message: The evaluation covers 16,920 runs, from 141 pairs, four tools, six timeouts and five repetitions.
sources: "Benchmark and ARDiff: Badihi et al. 2020. DSE: Person et al. 2008. PRV: Böhme et al. 2013."
---

<!-- Backup: PASDA's evaluation setup, shown only if someone asks. sec:pasda-evaluated-tools, sec:pasda-benchmark and the setup paragraph of sec:pasda-rq1. -->

<div class="setup">
  <div class="card fact"><div class="card-head">Benchmark</div>141 pairs of Java programs with seeded changes: 73 equivalent, 68 not. 8 to 201 lines per program.</div>
  <div class="card fact"><div class="card-head">What the programs contain</div>Loops, method calls and non-linear arithmetic over integers and doubles. No recursion, no other data types.</div>
  <div class="card fact"><div class="card-head">Timeouts and runs</div>10&nbsp;s, 30&nbsp;s, 90&nbsp;s, 300&nbsp;s, 900&nbsp;s and 1&nbsp;h per pair, five runs each. The five reach the same verdict in 3,360 of 3,384 cases.</div>
  <div class="card fact"><div class="card-head"><span class="keep">ARDiff</span> and <span class="keep">DSE</span></div>The implementations of Badihi et al., with two bugs fixed that led to wrong NEQ verdicts.</div>
  <div class="card fact"><div class="card-head"><span class="keep">PRV</span></div>Not available. PASDA's first iteration without best&#8209;effort verdicts stands in for it.</div>
  <div class="card fact"><div class="card-head">Machine and limits</div>MacBook Air M2 with 24&nbsp;GB of memory. The analysis follows a loop for at most 10 iterations.</div>
</div>

---
layout: bars
title: Results at All Timeouts
section: Backup
message: PASDA proves more pairs than PRV, ARDiff and DSE at every timeout.
sources: "PRV: Böhme et al. 2013. ARDiff and benchmark: Badihi et al. 2020. DSE: Person et al. 2008."
---

<!-- Backup: the results over the six timeouts, shown only if someone asks. Proofs and best-effort verdicts per timeout: tab:program-level-classifications-1 and -3 (the numbers are in ProofsOverTime). Accuracy of the best-effort verdicts: sec:pasda-rq2. -->

<div class="cols">
<div class="col">
  <div class="card">
    <div class="card-head">Timeouts from <span class="keep">10&nbsp;s</span> to <span class="keep">1&nbsp;h</span> per pair</div>
    <ProofsOverTime :width="1130" />
  </div>
</div>
<div class="col grow">
<div class="card fact"><div class="card-head">Setup</div>141 program pairs (73 EQ, 68 NEQ) against PRV, ARDiff and DSE.</div>
<div class="card fact"><div class="card-head">Proofs</div>PASDA proves 86 pairs at 10&nbsp;s and 104 at 1&nbsp;h. PRV proves 82 and 95.</div>
<div class="card fact"><div class="card-head">Best-effort verdicts</div>MAYBE_EQ is correct for 70 to 75% of its pairs, MAYBE_NEQ for 55 to 85%.</div>
</div>
</div>

---
layout: bars
title: "Evaluation Setup: Teralizer"
section: Backup
message: Three sets of projects lead from a benchmark for symbolic analysis to unmodified open-source projects.
sources: "EqBench: Badihi et al. 2021. EvoSuite: Fraser and Arcuri 2011. RepoReapers: Munaiah et al. 2017. PIT: Coles et al. 2016."
---

<!-- Backup: Teralizer's evaluation setup, shown only if someone asks. sec:teralizer-framework and tab:dataset-statistics. The RepoReapers projects ran with one strategy, constraint-aware generation with 200 inputs per test. -->

<div class="setup">
  <div class="card fact"><div class="card-head"><span class="keep">EqBench</span></div>652 classes of numeric programs without tests. EvoSuite generates the tests, with 1&nbsp;s, 10&nbsp;s and 60&nbsp;s per class.</div>
  <div class="card fact"><div class="card-head">Apache Commons</div>247 utility classes from 17 projects, with EvoSuite tests as for EqBench and with the 725 tests of the developers.</div>
  <div class="card fact"><div class="card-head"><span class="keep">RepoReapers</span></div>584 open-source Java projects with 85,368 test methods, selected by size, build tool, Java and JUnit version.</div>
  <div class="card fact"><div class="card-head">Generalization</div>Inputs sampled at random or with constraint-aware generators, 10, 50 or 200 per test.</div>
  <div class="card fact"><div class="card-head">Measures</div>Mutation score with PIT's default operators, runtime per stage, and the reason for every test that is excluded.</div>
  <div class="card fact"><div class="card-head">Limits</div>10&nbsp;s of symbolic analysis per assertion, 1,800&nbsp;s per generalized test suite, 1&nbsp;h of mutation testing per suite.</div>
</div>

---
layout: bars
title: Mutation Testing
section: Backup
message: The mutation score is the share of small seeded faults that a test suite detects.
sources: "Mutation testing: Jia and Harman 2011, Papadakis et al. 2019. Real faults: Just et al. 2014, Papadakis et al. 2018. PIT: Coles et al. 2016."
---

<!-- Backup: the measure of the Teralizer evaluation, shown only if someone asks. sec:mutation-testing, sec:teralizer-background (why not coverage), tab:pit-mutators (the Math operator replaces an arithmetic operation), sec:teralizer-threats-to-validity. The mutant on the slide is the Math operator applied to line 6 of v2. With it, (300, 10, 20) and (60, 10, 8) return 0, so two of the three developer tests fail. -->

<div class="cols mut">
<div class="col">
  <div class="card">
    <div class="card-head">A mutant of the example</div>
    <div class="pair"><span class="ver">v2</span><JavaCode code="double risk = (3.0 * debt - income) / 100.0;" bare /></div>
    <div class="pair"><span class="ver">mutant</span><JavaCode code="double risk = (3.0 * debt + income) / 100.0;" bare :marks="['1:+']" /></div>
    <div class="out"><span class="tag hit">detected</span>two of the three developer tests fail</div>
    <div class="card-head">The example's regression, a fault of the same size</div>
    <div class="pair"><span class="ver">v1</span><JavaCode code="p >= 0.8 ? 60 : 5" bare :marks="['1:60']" /></div>
    <div class="pair"><span class="ver">v2</span><JavaCode code="final int FULL = 50;" bare :marks="['1:50']" /></div>
    <div class="out"><span class="tag miss">not detected</span>the three developer tests pass</div>
    <div class="out"><span class="tag hit">detected</span>the generalized test fails for 51 to 60</div>
  </div>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">Why not coverage?</div>A generalized test follows the path of its developer test, so the coverage stays the same.</div>
  <div class="card fact"><div class="card-head">Do mutants stand for real faults?</div>In two empirical studies, mutation scores correlate with the detection of real faults.</div>
  <div class="card fact"><div class="card-head">In the evaluation</div>PIT's default operators change arithmetic, return values and conditions, and remove calls. They are not regressions from a project's history.</div>
</div>
</div>

<style>
.mut .pair { margin: 4px 0; display: flex; align-items: baseline; gap: 14px; }
.mut .ver { flex: none; width: 84px; font-size: var(--fs-note); font-weight: 700; color: var(--muted); }
.mut .out { margin: 10px 0 0; display: flex; align-items: center; gap: 14px; font-size: var(--fs-detail); }
.mut .tag { flex: none; width: 170px; padding: 3px 0; border-radius: 6px; font-size: var(--fs-tiny); font-weight: 700; text-align: center; }
.mut .tag.hit { background: var(--ink); color: #fff; }
.mut .tag.miss { background: #fff; box-shadow: inset 0 0 0 2px var(--ink); color: var(--ink); }
</style>

---
layout: bars
title: Constraint-Aware Input Generation
section: Backup
message: The generalized test builds simple conditions into its input generator and filters on the rest.
sources: "Teralizer: Glock, Bauer and Pinzger 2025. jqwik: jqwik-team 2022."
---

<!-- Backup: how the generated test samples inputs, shown only if someone asks. sec:teralizer-three-variant-design, sec:teralizer-constraint-encoding and sec:teralizer-rq2. The code is the supplier of the example in the notation of lst:improved-supplier: the generated supplier draws income and debt from all integers, bounds amount at 60 and filters on the path condition (.agent-build/phd-seminar/15-frame-and-example.md in the thesis repository). -->

<div class="cols gen">
<div class="col">
  <div class="card">
    <div class="card-head cited">Input generator of the generalized test<span class="cite">simplified</span></div>
    <JavaCode code="class ImprovedSupplier {&#10;  Arbitrary get() {&#10;    return Arbitraries.integers().flatMap(&#10;      income -> Arbitraries.integers().flatMap(&#10;        debt -> Arbitraries.integers()&#10;          .between(Integer.MIN_VALUE, 60)&#10;          .map(amount -> new TestParams(&#10;            income, debt, amount))))&#10;      .filter(this::satisfiesInputSpec);&#10;  }&#10;}" :tints="{ 6: 'in', 9: 'in' }" />
    <div class="key">line 6: <code>amount &lt;= 60</code> is built into the generator<br>line 9: <code>p >= 0.8</code> is checked for every sample</div>
  </div>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">Why not only filter?</div>If too few random samples pass the filter, jqwik gives up and the test is lost. For <code>a == b &amp;&amp; b == c</code> almost none pass.</div>
  <div class="card fact"><div class="card-head">What is built in</div>Comparisons of an input with a constant or with another input, such as <code>x &lt; 10</code> or <code>y >= x</code>.</div>
  <div class="card fact"><div class="card-head">Effect</div>Random sampling fails 2 to 2.5 times as often with too many filter misses. It still detects more mutants on EqBench.</div>
</div>
</div>

<style>
.gen .key { margin-top: 14px; line-height: 1.4; }
</style>

---
layout: bars
title: Real-World Applicability
section: Backup
message: Of 180,548 assertions in 584 open-source projects, 6,905 pass all of Teralizer's filters.
sources: "Projects: Munaiah et al. 2017 (RepoReapers)."
---

<!-- Backup: where Teralizer loses tests on real projects, shown only if someone asks. Three losses as three equal panels. The fourth large one, assertions without an identified tested method (MissingValue, 39.1% of the assertions), is left out, because it takes long to explain. -->
<!-- 32.9% of tests: NoAssertions (24,266 of 73,662). 36.5% and 31.8% of assertions: ParameterType, ReturnType. All in chapters/05-teralizer/tables. -->

<div class="loss">
  <div class="group-head">Teralizer's analysis of the test</div>
  <div class="group-head two">The symbolic analysis, as for PASDA</div>
  <div class="card"><span class="part">assertions to generalize</span><div class="stat"><div class="big">32.9% <span>of the tests</span></div><div class="track"><i style="width: 32.9%" /></div><div class="lack">no assertion found<small>often one in a helper method</small></div><div class="fwd"><Arrow />follow calls into helpers</div></div></div>
  <div class="card"><span class="part in">inputs to sample</span><div class="stat"><div class="big in">36.5% <span>of the assertions</span></div><div class="track"><i class="in" style="width: 36.5%" /></div><div class="lack">no input that can be sampled<small>objects, collections, arrays</small></div><div class="fwd"><Arrow />generators of valid objects</div></div></div>
  <div class="card"><span class="part out">outputs to assert</span><div class="stat"><div class="big out">31.8% <span>of the assertions</span></div><div class="track"><i class="out" style="width: 31.8%" /></div><div class="lack">no output that can be asserted<small>void, List, Object</small></div><div class="fwd"><Arrow />side effects as outputs</div></div></div>
</div>

<style>
.loss { width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 24px; row-gap: 14px; font-size: var(--fs-small); line-height: 1.3; }
.loss .two { grid-column: span 2; }
.loss .card { display: flex; flex-direction: column; }
.loss .part { align-self: flex-start; display: inline-block; padding: 5px 14px; border-radius: 8px; background: #fff; box-shadow: inset 0 0 0 2px var(--rule); font-size: var(--fs-note); white-space: nowrap; }
.loss .part.in { background: var(--spec-in); box-shadow: none; }
.loss .part.out { background: var(--spec-out); box-shadow: none; }
.loss .stat { display: flex; flex-direction: column; flex: 1; }
.loss .big { margin: 16px 0 8px; font-size: 64px; line-height: 1; font-weight: 700; }
.loss .big span { font-size: var(--fs-note); font-weight: 400; color: var(--muted); }
.loss .track { height: 22px; border-radius: 6px; background: var(--rule); overflow: hidden; }
.loss .track i { display: block; height: 100%; background: var(--muted); }
.loss .track i.in { background: var(--spec-in-line); }
.loss .track i.out { background: var(--spec-out-line); }
.loss .lack { margin-top: 12px; }
.loss small { display: block; margin-top: 2px; font-size: var(--fs-note); color: var(--muted); }
.loss .fwd { margin-top: auto; padding-top: 14px; display: flex; align-items: center; gap: 12px; }
.loss .fwd svg { flex: none; }
</style>

---
layout: bars
title: Teralizer and JARVIS
section: Backup
message: On the 12 projects of JARVIS's evaluation, Teralizer generalizes tests for 337 methods in 9 projects.
sources: "JARVIS: Peleg et al. 2018. Teralizer: Glock, Bauer and Pinzger 2025."
---

<!-- Backup: the closest earlier approach, shown only if someone asks. Methods under test with generalized tests per project: tab:teralizer-rq0-breadth and chapters/05-teralizer/tables/macros.tex (TzRqzeroCensus...SoundMuts and ...JarvisMuts). JARVIS's numbers are those its paper reports. commons-email and commons-jexl were not reached, commons-pool failed before the generalization. Scenarios: sec:teralizer-rq0-table2. -->

<div class="cols jarvis">
<div class="col">
  <div class="card">
    <div class="card-head">Methods with generalized tests</div>
    <table>
      <thead><tr><th>Apache Commons</th><th>JARVIS</th><th>Teralizer</th></tr></thead>
      <tbody>
        <tr><td>lang</td><td>2</td><td>208</td></tr>
        <tr><td>math</td><td>7</td><td>90</td></tr>
        <tr><td>text</td><td>-</td><td>12</td></tr>
        <tr><td>configuration</td><td>-</td><td>9</td></tr>
        <tr><td>io</td><td>-</td><td>7</td></tr>
        <tr><td>codec</td><td>-</td><td>6</td></tr>
        <tr><td>cli</td><td>-</td><td>2</td></tr>
        <tr><td>collections</td><td>-</td><td>2</td></tr>
        <tr><td>csv</td><td>-</td><td>1</td></tr>
        <tr><td>email, jexl, pool</td><td>-</td><td>-</td></tr>
      </tbody>
    </table>
    <div class="key dash">- &nbsp;none reported by JARVIS, none created by Teralizer</div>
  </div>
</div>
<div class="col grow">
  <div class="card fact"><div class="card-head">JARVIS</div>Generalizes from the test code alone. Its numbers are those of its paper, because the tool is not available.</div>
  <div class="card fact"><div class="card-head">Teralizer</div>Generalizes from the execution of the test, by single-path symbolic analysis.</div>
  <div class="card fact"><div class="card-head">On JARVIS's 10 scenarios</div>Teralizer generalizes 7, with more distinct inputs than JARVIS in 4 and fewer in 3.</div>
</div>
</div>

<style>
.jarvis table { width: 760px; border-collapse: collapse; font-size: var(--fs-small); font-variant-numeric: tabular-nums; }
.jarvis th { padding: 0 0 10px 32px; border-bottom: 2px solid var(--ink); font-size: var(--fs-note); font-weight: 400; color: var(--muted); text-align: right; }
.jarvis td { padding: 7px 0 7px 32px; border-bottom: 1px solid var(--rule); text-align: right; }
.jarvis th:first-child, .jarvis td:first-child { padding-left: 0; text-align: left; }
.jarvis .dash { margin-top: 16px; color: var(--muted); }
</style>

---
layout: bars
title: Uses of the Results
section: Backup
message: The thesis proposes these uses and evaluates none of them.
sources: "Prioritization: Khatibsyarbini et al. 2018. Fault localization: Wong et al. 2016. Selection: Rothermel and Harrold 1997. Repair: Smith et al. 2015. Developers: Glock 2024."
---

<!-- Backup: what the two results can be input for, shown only if someone asks. PASDA: sec:pasda-use-cases (test case prioritization, fault localization) and sec:reflections-directions (regression test selection, presentation for developers, glock_2024_understanding). Teralizer: sec:reflections-directions (program repair and coding agents, reviewable generalized tests). -->

<div class="uses">
  <div></div>
  <div class="group-head">Input for tools</div>
  <div class="group-head">Input for developers</div>
  <div class="what">PASDA's verdicts</div>
  <div class="card">
    <div class="use">Run the tests of partitions with NEQ and MAYBE_NEQ first.</div>
    <div class="use">Skip a test only if all it reaches is proven EQ.</div>
    <div class="use">Rank lines by the verdicts of the partitions that cover them, to locate a fault.</div>
  </div>
  <div class="card">
    <div class="use">Show which inputs and which lines a verdict covers, with an input to try.</div>
    <div class="use">Decide which changes to inspect first.</div>
  </div>
  <div class="what">Generalized tests</div>
  <div class="card">
    <div class="use">A stronger test suite for program repair and coding agents: it can reject a patch that only fits the developer tests.</div>
  </div>
  <div class="card">
    <div class="use">A test that keeps the structure of the developer's test, with the path condition and the expected output to review.</div>
  </div>
</div>

<style>
.uses { width: 100%; display: grid; grid-template-columns: 250px minmax(0, 1fr) minmax(0, 1fr); gap: 20px 24px; align-items: stretch; }
.uses .what { align-self: center; font-size: var(--fs-small); font-weight: 700; line-height: 1.3; }
.uses .card { display: flex; flex-direction: column; justify-content: center; gap: 14px; font-size: var(--fs-small); line-height: 1.3; }
.uses .use { padding-left: 18px; border-left: 4px solid var(--rule); text-wrap: balance; }
</style>
