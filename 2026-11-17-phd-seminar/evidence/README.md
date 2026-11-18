# Evidence

The runs behind claims on the slides that the thesis does not state itself. Comments in the slides point here.

- `solver-check/`: whether Z3, cvc5 and dReal decide the path condition of the loan example (Formal Guarantees Meet Practical Constraints, Why Reachability Is Hard). `results.md` holds the answers, `check.py` and the `.smt2` files reproduce them.
- `hash-check/`: whether Z3 finds an input that passes a SHA-256 password check (Why Reachability Is Hard). Run `python check.py 300`.
- `pasda-database/`: queries on the results database of PASDA's replication package (Two Queries on the Outputs, MAYBE_EQ for a Partition). `acquire_database.py` downloads the database of about 28 GB from Zenodo, `query_database.py` runs `queries.json`, and `report.md` explains the results. Its file paths refer to the thesis repository, which is not public. The PASDA benchmarks are also in the [PASDA repository](https://github.com/glockyco/PASDA/tree/main/benchmarks).
