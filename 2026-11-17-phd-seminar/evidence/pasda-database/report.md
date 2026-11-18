# PASDA backup-slide evidence

Paths below are relative to the thesis repository. `I/` abbreviates `projects/pasda-impl/Implementation/`. `T` abbreviates `chapters/04-pasda/03-approach.tex`. Status names render the thesis's LaTeX macros as their printed classification names. Logical explanations below are deductions from the quoted assertions, not measurements.

## Q1

NEQ-Query asks whether some assignment in this partition makes the outputs different. EQ-Query asks whether some assignment makes them equal.
Both queries include the same path condition. SAT of EQ-Query is an equality witness, not a proof of equivalence over the partition.
In the selected 300 s data, one query is UNKNOWN and the other is answered in 400 of 4917 paired records (8.14%). The queries are existential questions, not the same proof attempted twice.

### Exact queries and meanings

Let `P` be the product-program path condition and `o1`, `o2` the two symbolic return expressions. The assertions are exactly:

- NEQ-Query: `P AND NOT(o1 = o2)`.
- EQ-Query: `P AND (o1 = o2)`.

All free symbolic constants are existentially assigned by satisfiability checking. These include shared input symbols and auxiliary symbols in the path condition or outputs. Where UIFs occur, the solver also chooses their interpretations, subject to their sorts and the constraints. There is no explicit universal quantifier and no fresh return variable in these partition queries. Integer and real symbolic variables become `mkIntConst(variable.name)` and `mkRealConst(variable.name)`. UIF applications use named function declarations. Evidence: `I/src/main/java/differencing/transformer/ModelToZ3Transformer.java:143-181`. A missing path-condition model becomes `true`, so the path condition is then vacuous, not deliberately omitted. Evidence: the same file, lines 31-39.

The caller extracts the current product-program path condition and both symbolic values, converts them to models, and calls both queries unconditionally. Evidence: `I/src/main/java/differencing/DifferencingListener.java:207-248`.

The complete builders, quoted from `I/src/main/java/differencing/SatisfiabilityChecker.java:36-62`:

```java
public EquivalenceCheckResult checkNeq(Model pcModel, Model v1Model, Model v2Model) {
    ModelToZ3Transformer modelToZ3 = new ModelToZ3Transformer(this.context);
    Expr<BoolSort> pcExpr = (Expr<BoolSort>) modelToZ3.transform(pcModel);
    Expr<?> v1Expr = modelToZ3.transform(v1Model);
    Expr<?> v2Expr = modelToZ3.transform(v2Model);

    Solver solver = this.context.mkSolver();
    solver.add(pcExpr);
    solver.add(this.context.mkNot(this.context.mkEq(v1Expr, v2Expr)));
    solver = this.removeFuncDeclsForBuiltIns(solver);

    return this.createEqualityResult(solver, solver.check(), v1Expr, v2Expr);
}

public EquivalenceCheckResult checkEq(Model pcModel, Model v1Model, Model v2Model) {
    ModelToZ3Transformer modelToZ3 = new ModelToZ3Transformer(this.context);
    Expr<BoolSort> pcExpr = (Expr<BoolSort>) modelToZ3.transform(pcModel);
    Expr<?> v1Expr = modelToZ3.transform(v1Model);
    Expr<?> v2Expr = modelToZ3.transform(v2Model);

    Solver solver = this.context.mkSolver();
    solver.add(pcExpr);
    solver.add(this.context.mkEq(v1Expr, v2Expr));
    solver = this.removeFuncDeclsForBuiltIns(solver);

    return this.createEqualityResult(solver, solver.check(), v1Expr, v2Expr);
}
```

The postprocessing removes declarations that would shadow built-in trigonometric functions and reparses the assertions. It does not remove the path condition. A code comment explicitly says that `log` remains uninterpreted for comparability with ARDiff. Evidence: `I/src/main/java/differencing/SatisfiabilityChecker.java:131-165`.

| Query | SAT means | UNSAT means |
|---|---|---|
| NEQ | A model satisfies the partition's path condition and makes the outputs different. With UIFs this witness may be spurious for the original programs. | No model in the partition makes outputs different. The outputs are equal throughout the modeled partition, including its overapproximation. |
| EQ | A model satisfies the path condition and makes outputs equal. This does not exclude other models with different outputs. | No model in the partition makes outputs equal. If the partition is reachable, its outputs are necessarily different. |

These meanings follow directly from the quoted assertions. Reachability still matters. The thesis downgrades output NEQ to overall MAYBE_NEQ when the partition is only MAYBE_REACHABLE (`T:175-178`). UNKNOWN means neither satisfiability nor unsatisfiability was established. The implementation stores `solver.getReasonUnknown()` for that result (`I/src/main/java/differencing/SatisfiabilityChecker.java:118-124`).

### Why the answers are not determined together

The following are logical deductions from the builders:

- Both SAT: there is an equality witness and a disequality witness. Without UIFs these can be different inputs in the same partition. For example, with `P = true`, `o1 = x`, `o2 = -x`, equality holds at `x = 0` and disequality at `x = 1`. With UIFs the models can also choose different UIF interpretations, so do not automatically describe two concrete original-program inputs.
- NEQ UNSAT: equality holds everywhere in the modeled partition. If `P` is satisfiable, EQ is mathematically SAT, but a resource-limited solver can still answer UNKNOWN on that second query.
- EQ UNSAT: equality holds nowhere in the modeled partition. If `P` is satisfiable, NEQ is mathematically SAT, but its solver call can still return UNKNOWN.
- Both UNSAT: possible only when `P` itself is unsatisfiable. Such paths are skipped during symbolic execution according to `T:115-116`.
- NEQ UNKNOWN and EQ SAT: at least one equality witness exists, but absence of a disequality witness has not been proved. This is the partition-output MAYBE_EQ rule (`T:159-162,170-172`).
- NEQ UNKNOWN and EQ UNSAT: there is no equality witness. This supports output NEQ even when the disequality call was inconclusive (`T:161`).
- NEQ SAT and EQ UNKNOWN: disequality has a witness, but the equality question remains unanswered. This gives output NEQ without UIFs and MAYBE_NEQ with UIFs (`T:163-166`).

The second query is particularly useful when the first returns UNKNOWN, and when a SAT disequality witness involves UIF overapproximations. The thesis states the heuristic explicitly at `T:172`: MAYBE_NEQ reflects a non-equivalence indication that UIFs prevent from being proved, whereas MAYBE_EQ reflects no disequality indication and at least one equality witness.

### Evaluation data, cohort, and reproducible queries

The database was extracted from the [Zenodo replication package, version 10.5281/zenodo.10033132](https://doi.org/10.5281/zenodo.10033132), member `PASDA/Implementation/analysis/results/results.db`, into `.agent-build/phd-seminar/pasda-research/results.db`. The [record API](https://zenodo.org/api/records/10033132) identifies the package and its file. Acquisition details are in `archive-evidence.json` and `acquire_database.py` in the report directory. The GitHub checkout intentionally lacks the collected data (`projects/pasda-impl/README.md:3-14,23-49`).

The primary cohort is PASDA (`PASDA-diff`), run timeout 300 s, depth limit 10, and the first recorded repetition per benchmark, selected by ascending `run_id`. All iterations of those runs are included. This is 141 runs for 141 benchmarks, with 6644 classified partition records. They are per-iteration records, not 6644 distinct concrete-input partitions across refinement iterations. Three additional interrupted records have NULL classification and are excluded. There are 4917 records with both query results and 1727 depth-limited records with neither result. The stored solver-timeout setting is 45. Evidence: queries `configurations`, `all_iterations_classes_by_timeout`, and `all_iterations_cross_300` in `queries.json`, their results in `query-results.json`, and `selected_cohort_300` in `supplementary-queries.json`.

This is an explicitly selected repetition, not a majority classification over five runs and not the paper's average of per-run percentages. The paper-facing SQL selects each run's result-bearing iteration when producing its partition summaries (`I/analysis/create-materialized-views.sql:891-910`). Results for that narrower scope are given below too. PASDA-diff's mapping to PASDA is in `projects/pasda-impl/README.md:78-87`.

This is the exact primary cross-table query, also saved as `all_iterations_cross_300` in `queries.json`:

```sql
WITH ranked AS (
 SELECT r.*,row_number() OVER (
   PARTITION BY benchmark,run_timeout,depth_limit ORDER BY run_id) AS ordinal
 FROM _run_ r WHERE tool='PASDA-diff'
)
SELECT p.has_uif,p.neq_status,p.eq_status,count(*) AS n
FROM ranked r
JOIN iteration i ON i.run_id=r.run_id
JOIN partition p ON p.iteration_id=i.id
WHERE r.ordinal=1 AND r.run_timeout=300 AND p.result IS NOT NULL
GROUP BY p.has_uif,p.neq_status,p.eq_status
ORDER BY p.has_uif,p.neq_status,p.eq_status;
```

The stored status values are SAT = 1, UNSAT = -1, UNKNOWN = 0. Evidence: [Z3 4.11.2 Status.java, enum constants](https://github.com/Z3Prover/z3/blob/z3-4.11.2/src/api/java/Status.java#L24-L32). NULL means no recorded query result, not UNKNOWN.

| NEQ-Query | EQ-Query | UIF no | UIF yes | Total |
|---|---|---:|---:|---:|
| SAT | SAT | 54 | 1568 | 1622 |
| SAT | UNSAT | 233 | 453 | 686 |
| SAT | UNKNOWN | 2 | 0 | 2 |
| UNSAT | SAT | 716 | 1200 | 1916 |
| UNSAT | UNSAT | 0 | 0 | 0 |
| UNSAT | UNKNOWN | 257 | 93 | 350 |
| UNKNOWN | SAT | 0 | 13 | 13 |
| UNKNOWN | UNSAT | 35 | 0 | 35 |
| UNKNOWN | UNKNOWN | 137 | 156 | 293 |
| NULL | NULL | 457 | 1270 | 1727 |
| Total | | 1891 | 4753 | 6644 |

The two results differ in 3002 of 4917 paired records (61.05%). This includes 2602 SAT/UNSAT or UNSAT/SAT pairs and 400 pairs with exactly one UNKNOWN (8.14%). The latter split into 350 UNSAT/UNKNOWN, 35 UNKNOWN/UNSAT, 13 UNKNOWN/SAT, and 2 SAT/UNKNOWN. These are sums of the query result above, with unqueried records excluded from the denominator.

For comparison, restricting the same 300 s cohort to each run's result-bearing iteration gives 2309 classified records, 1826 paired results, and 483 unqueried depth-limited records. There are 1242 different result pairs (68.02%), including 278 pairs with exactly one UNKNOWN (15.22%). The cross table is:

| NEQ-Query | EQ-Query | UIF no | UIF yes |
|---|---|---:|---:|
| SAT | SAT | 54 | 420 |
| SAT | UNSAT | 233 | 43 |
| SAT | UNKNOWN | 2 | 0 |
| UNSAT | SAT | 523 | 165 |
| UNSAT | UNSAT | 0 | 0 |
| UNSAT | UNKNOWN | 220 | 19 |
| UNKNOWN | SAT | 0 | 4 |
| UNKNOWN | UNSAT | 33 | 0 |
| UNKNOWN | UNKNOWN | 89 | 21 |
| NULL | NULL | 245 | 238 |

Evidence: `final_cross_300` in `queries.json` and `query-results.json`. At 3600 s, the same first-repetition/result-bearing-iteration selection has 7970 classified records, of which 7014 have paired results. There are 5833 different pairs (83.16%) and 341 pairs with exactly one UNKNOWN (4.86%). Evidence: `final_cross_3600` in the same files. These supplemental figures use the narrower scope, not the primary all-iterations scope.

### Three concrete asymmetric records

All three belong to the selected 300 s repetition. Query:

```sql
SELECT id,iteration_id,partition,result,pc_status,
       has_uif,has_uif_pc,has_uif_v1,has_uif_v2,
       neq_status,eq_status,neq_reason_unknown,eq_reason_unknown,
       neq_result_v1,neq_result_v2,eq_result_v1,eq_result_v2,pc_model
FROM partition WHERE id IN (153200,658810,152310);
```

The full result and the joins identifying the benchmark and repetition are saved as `three_examples` and `selected_runs` in `supplementary-queries.json`.

| Benchmark | run_id | Iteration | Partition | partition.id | UIF | PC-Query | NEQ-Query | EQ-Query | Overall class |
|---|---:|---:|---:|---:|---|---|---|---|---|
| sine/mysin/Eq | 30384 | 10 | 15 | 658810 | yes | SAT | UNKNOWN | SAT | MAYBE_EQ |
| Ell/rf/NEq | 17472 | 1 | 3 | 153200 | no | UNKNOWN | UNKNOWN | UNSAT | MAYBE_NEQ |
| Ell/rc/Eq | 17432 | 1 | 2 | 152310 | no | UNKNOWN | UNSAT | UNKNOWN | EQ |

- For sine/mysin/Eq, `neq_reason_unknown` is exactly `timeout`. The EQ witness evaluates both returns to `33`. These are model-evaluated values, not the symbolic output expressions. Its stored EQ model includes input symbol `x_10_SYMREAL = 2.0` and UIF interpretations. This is an abstract equality witness, not necessarily a concrete execution of the unabstracted program.
- For Ell/rf/NEq, `neq_reason_unknown` is exactly `smt tactic failed to show goal to be sat/unsat (incomplete (theory arithmetic))`. All four stored output-value fields are NULL. EQ UNSAT gives output NEQ, but PC UNKNOWN downgrades the overall result to MAYBE_NEQ.
- For Ell/rc/Eq, `eq_reason_unknown` is exactly `incomplete`. All four output-value fields are NULL. NEQ UNSAT is sufficient for EQ even though the EQ call is inconclusive.

The exact path conditions and symbolic output expressions for these records were not found in the package. `pc_model` is a satisfying assignment, not a path condition. The distinction is explicit in `I/src/main/java/differencing/SatisfiabilityChecker.java:65-73,94-124`. The absence is documented under "What could not be found" below. Do not label the witness value `33` as a symbolic output formula.


## Q2

In the selected 300 s first repetitions, 13 of 6644 classified partition records are MAYBE_EQ (0.20%), across all iterations.
Only sine/mysin/Eq has such partitions. Its result-bearing iteration contains four, all caused by a recorded NEQ-query timeout with an EQ-query SAT witness.
The package lacks their path conditions and symbolic output expressions, so a complete source-to-query slide example is not available from the collected evidence.

Evidence: `T:159-162,175-185`. The implementation also gives timeout and depth-limit handling precedence over output classification. See `I/src/main/java/differencing/classification/PartitionClassifier.java:72-102,138-207`.

### Counts by class and timeout

These are raw classified partition-record counts across all iterations of the first repetition for each benchmark, using the same primary cohort rule as Q1. Query `all_iterations_classes_by_timeout` in `queries.json` gives:

| Timeout (s) | EQ | NEQ | MAYBE_EQ | MAYBE_NEQ | UNKNOWN | DEPTH_LIMITED | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 484 | 164 | 0 | 98 | 61 | 210 | 1017 |
| 30 | 854 | 228 | 4 | 349 | 113 | 495 | 2043 |
| 90 | 1410 | 264 | 15 | 758 | 191 | 1063 | 3701 |
| 300 | 2266 | 286 | 13 | 2059 | 293 | 1727 | 6644 |
| 900 | 3426 | 285 | 12 | 4655 | 325 | 3429 | 12132 |
| 3600 | 6820 | 288 | 9 | 13949 | 322 | 4700 | 26088 |

TIMEOUT, ERROR, UNREACHABLE, MISSING, and BASE_TOOL_MISSING each occur zero times among the classified records in this query. Additional NULL-result records, excluded from the table, number 3, 4, 1, 3, 0, and 1 respectively by ascending timeout. They are not UNKNOWN classifications.

For the paper-style result-bearing-iteration scope of the same first repetitions, query `final_partition_classes_by_timeout` gives:

| Timeout (s) | EQ | NEQ | MAYBE_EQ | MAYBE_NEQ | UNKNOWN | DEPTH_LIMITED | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 390 | 164 | 0 | 31 | 42 | 126 | 753 |
| 30 | 588 | 228 | 1 | 58 | 69 | 311 | 1255 |
| 90 | 798 | 264 | 6 | 239 | 106 | 391 | 1804 |
| 300 | 927 | 286 | 4 | 499 | 110 | 483 | 2309 |
| 900 | 965 | 285 | 5 | 402 | 103 | 476 | 2236 |
| 3600 | 3345 | 288 | 3 | 3281 | 97 | 956 | 7970 |

These raw counts are not the paper's average per-run percentages.

### Which benchmarks have MAYBE_EQ partitions?

Only `sine/mysin/Eq` was found, even when expanding the search to every PASDA repetition, every timeout, and every iteration. Query and result:

```sql
SELECT r.benchmark,count(*) AS n,
       group_concat(DISTINCT p.neq_reason_unknown) AS reasons
FROM _run_ r JOIN iteration i ON i.run_id=r.run_id
JOIN partition p ON p.iteration_id=i.id
WHERE r.tool='PASDA-diff' AND p.result='MAYBE_EQ'
GROUP BY r.benchmark;
```

| benchmark | n | reasons |
|---|---:|---|
| sine/mysin/Eq | 255 | timeout,max. memory exceeded |

Of these 255 records, 243 have reason `timeout` and 12 have `max. memory exceeded`. Evidence: `all_runs_all_iterations_maybe_eq` in `query-results.json`. Counts across all five repetitions, by timeout, are 0 at 10 s, 22 at 30 s, 66 at 90 s, 56 at 300 s, 60 at 900 s, and 51 at 3600 s. Evidence: `maybe_eq_by_timeout_all_iterations` in `supplementary-queries.json`.

The first repetition at 300 s has 13 such records across iterations. The four in its result-bearing iteration are:

| run_id | Iteration | Partition | partition.id | NEQ | EQ | NEQ unknown reason | EQ-witness outputs |
|---:|---:|---:|---:|---|---|---|---|
| 30384 | 10 | 15 | 658810 | UNKNOWN | SAT | timeout | 33, 33 |
| 30384 | 10 | 18 | 658813 | UNKNOWN | SAT | timeout | 33, 33 |
| 30384 | 10 | 21 | 658816 | UNKNOWN | SAT | timeout | 33, 33 |
| 30384 | 10 | 24 | 658819 | UNKNOWN | SAT | timeout | 33, 33 |

Evidence: `final_maybe_eq_cases` in `queries.json` and `query-results.json`. The program-level result of this run is MAYBE_NEQ, not MAYBE_EQ (`selected_runs` in `supplementary-queries.json`). Other partitions take precedence.

### Source excerpts and the limit on a worked slide

There is no shorter different benchmark among the observed MAYBE_EQ cases, because the exhaustive PASDA query above finds only `sine/mysin/Eq`. Its source versions are 151 and 152 lines long (`projects/pasda-impl/benchmarks/sine/mysin/Eq/oldV.java` and `newV.java`).

The following are short genuine source excerpts showing one changed expression. They are not complete programs and are not claimed to be the symbolic outputs of partition 15.

Old version, `projects/pasda-impl/benchmarks/sine/mysin/Eq/oldV.java:52-56`:

```java
else if( xexp <= (IEEE_BIAS - IEEE_MANT - 2) ){
  return x;
}else if( xexp <= (IEEE_BIAS - IEEE_MANT/4) ){
  return x*(1.0-x*x*1.0/6.0);
}
```

New version declares `double sixth = 1.0/6.0;//change` at `projects/pasda-impl/benchmarks/sine/mysin/Eq/newV.java:15`, and has this branch at lines 53-57:

```java
else if( xexp <= (IEEE_BIAS - IEEE_MANT - 2) ){
  return x;
}else if( xexp <= (IEEE_BIAS - IEEE_MANT/4) ){
  return x*(1.0-x*x*sixth);//change
}
```

A defensible compact evidence slide can show the record `sine/mysin/Eq`, run 30384, iteration 10, partition 15, NEQ UNKNOWN (`timeout`), EQ SAT, witness returns `33, 33`, and UIF present in the path condition and both output expressions. The precise reason is: "The NEQ solver call timed out, while the separate EQ call found an abstract equality witness." This comes directly from the stored fields, not an inferred diagnosis of nonlinear arithmetic. Its exact path condition and symbolic outputs are not found, so this is not the requested complete worked example.


### What the thesis and paper say about rarity

The thesis says, verbatim apart from rendering macros, at `chapters/04-pasda/04-evaluation.tex:198`:

> Because partition-level MAYBE_EQ requires NEQ-Query to return UNKNOWN and EQ-Query to return SAT on the same partition, it occurs rarely in Table [tab:partition-level-classifications] (0.0--1.9%). Program-level MAYBE_EQ (rows #2 and #7) instead arises primarily when most partitions are proven EQ and the remaining partitions are DEPTH_LIMITED or UNKNOWN.

These are average per-run percentages grouped by program-level result, not a cross-dataset partition count. The thesis table reports an overall average of 0.1% MAYBE_EQ partitions at 300 s, and 1.9% in the expected-EQ/actual-MAYBE_NEQ group. Evidence: `chapters/04-pasda/04-evaluation.tex:174-190`.

The paper has the same numbers in its table (`projects/pasda-paper/main.tex:1287-1311`). Its explanatory paragraph at line 1317 describes the aggregation heuristics, but does not contain the thesis's explicit sentence that partition-level MAYBE_EQ is rare.

## Q3

The thesis labels are `tab:partition-reachability` and `tab:partition-output-classification`. There is no active combined-classification table in the thesis.
MAYBE_REACHABLE downgrades output NEQ to overall MAYBE_NEQ. Other output classes stay unchanged, and depth-limited paths get DEPTH_LIMITED.
Program EQ requires all partitions proved EQ. Otherwise positive evidence can yield MAYBE_EQ, with NEQ and MAYBE_NEQ taking precedence.

### Partition reachability classification

Caption: "Partition reachability classification."

Label: `tab:partition-reachability`.

Source: `chapters/04-pasda/03-approach.tex:141-150`. Entries and column headings are transcribed verbatim, with LaTeX macros rendered as their classification names.

| UIF | PC-Query | Reachability Classification |
|---|---|---|
| no | SAT | REACHABLE |
| no | UNSAT | UNREACHABLE |
| no | UNKNOWN | MAYBE_REACHABLE |
| yes | SAT | MAYBE_REACHABLE |
| yes | UNSAT | UNREACHABLE |
| yes | UNKNOWN | MAYBE_REACHABLE |

### Partition output equivalence classification

Caption: "Partition output equivalence classification."

Label: `tab:partition-output-classification`.

Source: `chapters/04-pasda/03-approach.tex:155-166`. `*` is the table's wildcard.

| UIF | NEQ-Query | EQ-Query | Output Classification |
|---|---|---|---|
| * | UNSAT | * | EQ |
| * | UNKNOWN | SAT | MAYBE_EQ |
| * | UNKNOWN | UNSAT | NEQ |
| * | UNKNOWN | UNKNOWN | UNKNOWN |
| no | SAT | * | NEQ |
| yes | SAT | SAT | MAYBE_NEQ |
| yes | SAT | UNSAT | NEQ |
| yes | SAT | UNKNOWN | MAYBE_NEQ |

The reachability table's UIF flag refers only to the path condition (`T:134`). The output table's UIF flag covers the partition-effects pairs (`T:171`). In code the latter is the OR of UIF occurrence in the path condition and both output expressions, not just output-only UIF occurrence (`I/src/main/java/differencing/DifferencingListener.java:240-253`). The visitor recognizes names starting with `UF_`, not every mathematical function application (`I/src/main/java/differencing/HasUifVisitor.java:22-40`).

### Combining reachability and output classification

There is no active table or label for this in the thesis. Its rule is the following text at `chapters/04-pasda/03-approach.tex:176-178`, with macros rendered:

> The partition reachability classification and partition output classification are combined to produce the overall partition-level equivalence classification.
> Specifically, a reachability result of MAYBE_REACHABLE turns NEQ results into MAYBE_NEQ results (because in this case, it is not possible to prove that the non-equivalence can be observed in a concrete execution of the two original programs). For all other combinations, the overall classification is the same as the output classification.
> Thus, each partition is assigned to one of six equivalence classes: EQ, NEQ, MAYBE_EQ, MAYBE_NEQ or UNKNOWN if the partition is not depth-limited (as described in this section), or DEPTH_LIMITED otherwise (as described in the previous section).

The paper contains a commented-out table named `tab:partition-overall-classification`, but it is not active published table content. Evidence: `projects/pasda-paper/main.tex:936-949`. Its active text gives the same rule at lines 925-928.

### Aggregating partitions into a program classification

Quoted from `chapters/04-pasda/03-approach.tex:185`, with macros rendered:

> Once the symbolic execution concludes, the results of the partition-level equivalence classifications are aggregated to form the program-level equivalence classification of the current iteration. A program-level result of EQ is reported if all partitions could be identified, analyzed, and proven to be EQ within the given timeout. A result of MAYBE_EQ is reported if at least some partitions were identified and classified as EQ or MAYBE_EQ but none were classified as NEQ or MAYBE_NEQ. Otherwise, the program-level result is determined by the partition-level result with the highest priority, where priorities are as follows: NEQ > MAYBE_NEQ > UNKNOWN > DEPTH_LIMITED.

The exceptional cases, quoted from the end of `T:186`:

> If an error (e.g. OutOfMemoryError) occurs during PASDA's execution, a classification of ERROR is reported. If PASDA cannot analyze even a single partition within the given timeout, a classification of TIMEOUT is reported.

The paper has the same aggregation rule and exceptions at `projects/pasda-paper/main.tex:986-987`.

### Thesis versus paper

Both active classification tables have identical labels, captions, rows, and decisions. Evidence: thesis `T:141-166` versus paper `projects/pasda-paper/main.tex:953-979`.

The combination rule and program-aggregation rule are also unchanged. The thesis adds explicit explanations for MAYBE_REACHABLE (`T:135`), the output-class heuristics (`T:172`), and partition-level MAYBE_EQ rarity (`chapters/04-pasda/04-evaluation.tex:198`). The paper instead gives its reachability example as inability to prove whether `Math.tan(2 * x) < 0` holds "for all x" (`projects/pasda-paper/main.tex:912`). The thesis describes the relevant test correctly as satisfiability of the path condition and explains Z3's inconclusive handling of the transcendental terms (`T:134-136`). This is an explanatory wording difference, not a different classification table.

## What could not be found

- Exact path-condition formulas for the three concrete asymmetric records. `PRAGMA table_info('partition')`, saved in `query-results.json`, contains `pc_model` but no path-condition expression field. `pc_model` stores `solver.getModel().toString()`, not the asserted formula (`I/src/main/java/differencing/SatisfiabilityChecker.java:65-73`). A database search for table names containing `path`, `symbol`, `output`, or `effect` returns no rows. The exact SQL and empty result are saved as `other_tables` in `supplementary-queries.json`.
- The generated per-partition path-condition JSON files. The implementation writes them as `...-P<partition>-JSON-PC.json` (`I/src/main/java/differencing/PathConditionListener.java:92-107`), but the downloaded ZIP central directory contains zero `.json` members. Evidence: `archive-evidence.json`. The local benchmark checkout also has no matching generated JSON files.
- Symbolic return-expression formulas for the three records. The stored `neq_result_v1/v2` and `eq_result_v1/v2` fields are `model.eval(...)` values, not symbolic expressions (`I/src/main/java/differencing/SatisfiabilityChecker.java:94-124`). They are only populated for SAT results. The schema and `three_examples` query show the available fields and NULLs.
- A complete short worked MAYBE_EQ example containing both complete program versions, the actual abstract partition path condition, and both symbolic return expressions. Only the longer `sine/mysin/Eq` benchmark has observed PASDA MAYBE_EQ records. The report provides its source excerpts and actual solver outcomes, without inventing missing formulas or presenting witness values as expressions.
- A second distinct PASDA benchmark with partition-level MAYBE_EQ. The query over all PASDA repetitions, timeouts, and iterations returns only `sine/mysin/Eq`.
- An active thesis table combining reachability and output classes. The thesis gives prose rules instead. The paper's combined table exists only as commented-out source.

No PASDA analysis, build, test suite, or benchmark re-execution was run. The work read the implementation and manuscript sources, extracted the existing replication database, and executed read-only SQLite queries. All files written for this task are under `.agent-build/phd-seminar/pasda-research/`.
