# Can Z3 decide whether inputs reach each of the three paths of the loan example?
# Same setup as check.py: PASDA's encoding of exp, inputs from -100 to 100.
import math, z3
E = z3.RealVal('2.718281828459045')
def reach(cond):
    income, debt = z3.Ints('income debt')
    p = 1 / (1 + E ** ((3.0 * z3.ToReal(debt) - z3.ToReal(income)) / 100.0))
    s = z3.Solver(); s.set('timeout', 30000)
    s.add(income >= -100, income <= 100, debt >= -100, debt <= 100, cond(p))
    r = s.check(); return str(r) + (' (' + s.reason_unknown() + ')' if r == z3.unknown else '')
paths = {'full approval, p >= 0.8': lambda p: p >= 0.8,
         'partial approval, 0.5 <= p < 0.8': lambda p: z3.And(p >= 0.5, p < 0.8),
         'rejection, p < 0.5': lambda p: p < 0.5}
for name, cond in paths.items():
    print(name, '->', reach(cond))
P = lambda i, d: 1 / (1 + math.exp((3.0 * d - i) / 100.0))
grid = [(i, d) for i in range(-100, 101) for d in range(-100, 101)]
print('inputs per path by enumeration:', sum(P(*g) >= 0.8 for g in grid), sum(0.5 <= P(*g) < 0.8 for g in grid), sum(P(*g) < 0.5 for g in grid))
