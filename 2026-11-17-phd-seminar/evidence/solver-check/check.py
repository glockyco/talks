# Can a solver decide whether the full-approval path of the loan example is reachable?
#   risk = (3.0 * debt - income) / 100.0, p = 1 / (1 + exp(risk)), path condition p >= 0.8
# with income and debt as integers from -100 to 100, as in the recorded PASDA runs.
# A witness exists: income = 100, debt = -13 gives p = 0.8006.
import math, time
import z3

def z3_query(encode_exp, timeout_ms=30000):
    income, debt = z3.Ints('income debt')
    risk = (3.0 * z3.ToReal(debt) - z3.ToReal(income)) / 100.0
    p = 1 / (1 + encode_exp(risk))
    s = z3.Solver(); s.set('timeout', timeout_ms)
    s.add(income >= -100, income <= 100, debt >= -100, debt <= 100, p >= 0.8)
    t = time.time(); r = s.check()
    return str(r), round(time.time() - t, 2), (s.reason_unknown() if r == z3.unknown else '')

# 1. PASDA's encoding (ModelToZ3Transformer, case EXP): e as a decimal constant to the power x.
print('z3, PASDA encoding (2.718281828459045 ^ risk):', z3_query(lambda x: z3.RealVal('2.718281828459045') ** x))
# 2. exp as an uninterpreted function, as for sin, cos, tan and log in the same transformer.
f = z3.Function('exp', z3.RealSort(), z3.RealSort())
print('z3, exp as an uninterpreted function:', z3_query(lambda x: f(x)))
# 3. The same condition without exp, for comparison: risk <= -1.3863 (which is ln 0.25).
income, debt = z3.Ints('income debt')
s = z3.Solver(); s.add(income >= -100, income <= 100, debt >= -100, debt <= 100, (3.0 * z3.ToReal(debt) - z3.ToReal(income)) / 100.0 <= -1.3863)
print('z3, linear condition without exp:', s.check(), s.model())

# 4. cvc5, which has a theory of transcendental functions.
import cvc5
from cvc5 import Kind
def cvc5_query(sign):
    tm = cvc5.TermManager() if hasattr(cvc5, 'TermManager') else None
    slv = cvc5.Solver(tm) if tm else cvc5.Solver()
    mk = tm if tm else slv
    slv.setLogic('QF_NIRAT'); slv.setOption('produce-models', 'true'); slv.setOption('tlimit-per', '30000')
    I, R = mk.getIntegerSort(), mk.getRealSort()
    income, debt = mk.mkConst(I, 'income'), mk.mkConst(I, 'debt')
    real = lambda t: mk.mkTerm(Kind.TO_REAL, t)
    num = lambda v: mk.mkReal(str(v))
    risk = mk.mkTerm(Kind.DIVISION, mk.mkTerm(Kind.SUB, mk.mkTerm(Kind.MULT, num(3), real(debt)), real(income)), num(100))
    p = mk.mkTerm(Kind.DIVISION, num(1), mk.mkTerm(Kind.ADD, num(1), mk.mkTerm(Kind.EXPONENTIAL, risk)))
    for v in (income, debt):
        slv.assertFormula(mk.mkTerm(Kind.GEQ, v, mk.mkInteger(-100))); slv.assertFormula(mk.mkTerm(Kind.LEQ, v, mk.mkInteger(100)))
    slv.assertFormula(mk.mkTerm(sign, p, mk.mkReal('4/5')))
    t = time.time(); r = slv.checkSat()
    return str(r), round(time.time() - t, 2)
print('cvc5, p >= 0.8 (reachable in fact):', cvc5_query(Kind.GEQ))
# A condition that no input satisfies, to see whether cvc5 can refute: p > 1.
def cvc5_unsat():
    tm = cvc5.TermManager(); slv = cvc5.Solver(tm); slv.setLogic('QF_NIRAT'); slv.setOption('tlimit-per', '30000')
    x = tm.mkConst(tm.getRealSort(), 'risk')
    p = tm.mkTerm(Kind.DIVISION, tm.mkReal('1'), tm.mkTerm(Kind.ADD, tm.mkReal('1'), tm.mkTerm(Kind.EXPONENTIAL, x)))
    slv.assertFormula(tm.mkTerm(Kind.GT, p, tm.mkReal('1')))
    t = time.time(); r = slv.checkSat(); return str(r), round(time.time() - t, 2)
print('cvc5, p > 1 (unreachable in fact):', cvc5_unsat())

# 5. Trying all inputs, which the bounded range allows.
t = time.time()
hits = [(i, d) for i in range(-100, 101) for d in range(-100, 101) if 1 / (1 + math.exp((3.0 * d - i) / 100.0)) >= 0.8]
print('enumeration of 201 x 201 inputs:', len(hits), 'satisfy p >= 0.8, first', hits[0], 'in', round(time.time() - t, 3), 's')
