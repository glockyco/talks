# Can a solver decide the example's path condition?

Run on 2026-11-14. The condition is `p >= 0.8` with `p = 1 / (1 + exp((3.0 * debt - income) / 100.0))` and both inputs from -100 to 100. It is satisfiable: `income = 100, debt = -13` gives `p = 0.8006`.

| Solver | Query | Answer | Time |
| --- | --- | --- | --- |
| Z3 5.4.1 (pip `z3-solver`), PASDA's encoding of `exp` as `2.718281828459045 ^ x` (`ModelToZ3Transformer`, case `EXP`) | `p >= 0.8`, integer inputs | unknown: "smt tactic failed to show goal to be sat/unsat (incomplete (theory arithmetic))" | at once |
| Z3, `exp` as an uninterpreted function | the same | sat, which holds for some function and says nothing about `exp` | at once |
| Z3, the condition rewritten without `exp` (`risk <= -1.3863`) | the same | sat, with `income = 1, debt = -46` | at once |
| cvc5 1.4.2, logic QF_NIRAT, `exp` as its transcendental function | `p >= 0.8`, integer inputs | unknown (timeout) | 30 s |
| cvc5, logic QF_NRAT | `p >= 0.8`, real inputs | unknown (timeout) | 30 s |
| cvc5 | `p > 1`, which no input satisfies | unsat | at once |
| dReal 4 (Docker image `dreal/dreal4`, on the MacBook) | `p >= 0.8`, real inputs | delta-sat with delta = 0.001, `income` near -25, `debt` near -86.55 | under 1 s |
| dReal 4 | `p > 1`, `risk` from -4 to 4 | unsat | under 1 s |
| Python, all 201 x 201 integer inputs | `p >= 0.8` | 10,921 inputs satisfy it | 9 ms |

The Z3 here is the current release from pip, not the build that the PASDA replication bundles. The scripts are `check.py`, `exp.smt2` and `unsat.smt2` in this folder.

The floating-point theory of SMT-LIB has addition, subtraction, multiplication, division, fused multiply-add, square root, remainder, rounding, minimum and maximum, and no `exp` (https://smt-lib.org/theories-FloatingPoint.shtml). Java does not define `Math.exp` bit for bit: the methods of `Math` "are not defined to return the bit-for-bit same results" (https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html).

Symbolic PathFinder, in the version PASDA bundles (`projects/pasda-impl/Implementation/jpf-git/jpf-symbc`), has symbolic models for `sqrt`, `exp`, `asin`, `acos`, `atan`, `atan2`, `log`, `tan`, `sin`, `cos` and `pow` (`MathFunction.java`). For `Math.log10` with a symbolic argument its peer throws "symbolic log10 not implemented" (`JPF_java_lang_Math.java`).

Z3 with PASDA's encoding also returns unknown for the other two path conditions, `0.5 <= p < 0.8` and `p < 0.5` (`check-paths.py`). By enumeration, 10,921, 9,313 and 20,167 of the 40,401 inputs take the three paths.
