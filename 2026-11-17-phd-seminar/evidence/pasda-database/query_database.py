"""Read-only queries for the PASDA backup-slide evidence report."""
import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent
connection = sqlite3.connect((ROOT / 'results.db').as_uri() + '?mode=ro', uri=True)
connection.row_factory = sqlite3.Row
queries = {}
results = {}


def query(name, sql):
    queries[name] = sql
    rows = [dict(row) for row in connection.execute(sql)]
    results[name] = rows
    print(name, json.dumps(rows, ensure_ascii=True), flush=True)


query('tables', "SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")
for table in ('partition', 'settings', '_run_', 'iteration', 'instruction', 'partition_instruction'):
    query('schema_' + table, f'PRAGMA table_info("{table}")')
query('configurations', '''SELECT s.tool, s.run_timeout, s.iteration_timeout,
 s.solver_timeout, s.depth_limit, count(*) AS runs,
 count(DISTINCT r.benchmark) AS benchmarks
 FROM _run_ r JOIN settings s ON s.run_id=r.run_id
 GROUP BY s.tool,s.run_timeout,s.iteration_timeout,s.solver_timeout,s.depth_limit''')

BASE = '''WITH ranked AS (
 SELECT r.*, row_number() OVER (
 PARTITION BY benchmark,run_timeout,depth_limit ORDER BY run_id) AS ordinal
 FROM _run_ r WHERE tool='PASDA-diff'
), selected AS (SELECT * FROM ranked WHERE ordinal=1),
 data AS (SELECT r.benchmark,r.run_timeout,r.run_id,r.result AS program_result,
 i.iteration,p.* FROM selected r
 JOIN iteration i ON i.run_id=r.run_id AND i.iteration=r.result_iteration
 JOIN partition p ON p.iteration_id=i.id WHERE p.result IS NOT NULL)
'''
query('final_partition_classes_by_timeout', BASE + '''SELECT run_timeout,result,count(*) AS n
 FROM data GROUP BY run_timeout,result ORDER BY run_timeout,result''')
query('final_cross_300', BASE + '''SELECT has_uif,neq_status,eq_status,count(*) AS n
 FROM data WHERE run_timeout=300 GROUP BY has_uif,neq_status,eq_status
 ORDER BY has_uif,neq_status,eq_status''')
query('final_cross_3600', BASE + '''SELECT has_uif,neq_status,eq_status,count(*) AS n
 FROM data WHERE run_timeout=3600 GROUP BY has_uif,neq_status,eq_status
 ORDER BY has_uif,neq_status,eq_status''')
query('final_maybe_eq_cases', BASE + '''SELECT benchmark,run_timeout,run_id,iteration,id AS partition_id,
 partition,result,has_uif,pc_status,neq_status,eq_status,neq_reason_unknown,
 eq_result_v1,eq_result_v2,eq_model FROM data WHERE result='MAYBE_EQ'
 ORDER BY run_timeout,length(benchmark),benchmark,partition''')
query('final_one_unknown_cases_300', BASE + '''SELECT benchmark,run_timeout,run_id,iteration,
 id AS partition_id,partition,result,has_uif,has_uif_pc,has_uif_v1,has_uif_v2,
 pc_status,neq_status,eq_status,neq_reason_unknown,eq_reason_unknown,
 pc_model,neq_model,eq_model,neq_result_v1,neq_result_v2,eq_result_v1,eq_result_v2
 FROM data WHERE run_timeout=300 AND
 ((neq_status=0 AND eq_status IN (-1,1)) OR (eq_status=0 AND neq_status IN (-1,1)))
 ORDER BY CASE WHEN neq_status=0 AND eq_status=-1 THEN 0
 WHEN neq_status=0 AND eq_status=1 THEN 1 ELSE 2 END,length(benchmark),benchmark,partition
 LIMIT 50''')
query('all_iterations_classes_by_timeout', '''WITH ranked AS (
 SELECT r.*,row_number() OVER (PARTITION BY benchmark,run_timeout,depth_limit ORDER BY run_id) AS ordinal
 FROM _run_ r WHERE tool='PASDA-diff')
 SELECT r.run_timeout,p.result,count(*) AS n FROM ranked r
 JOIN iteration i ON i.run_id=r.run_id JOIN partition p ON p.iteration_id=i.id
 WHERE r.ordinal=1 GROUP BY r.run_timeout,p.result ORDER BY r.run_timeout,p.result''')
query('all_runs_all_iterations_maybe_eq', '''SELECT r.benchmark,r.run_timeout,r.run_id,
 i.iteration,p.id AS partition_id,p.partition,p.result,p.has_uif,
 p.pc_status,p.neq_status,p.eq_status,p.neq_reason_unknown,
 p.eq_result_v1,p.eq_result_v2,p.eq_model
 FROM _run_ r JOIN iteration i ON i.run_id=r.run_id
 JOIN partition p ON p.iteration_id=i.id
 WHERE r.tool='PASDA-diff' AND p.result='MAYBE_EQ'
 ORDER BY length(r.benchmark),r.benchmark,r.run_timeout,r.run_id,i.iteration,p.partition''')
query('all_iterations_cross_300', '''WITH ranked AS (
 SELECT r.*,row_number() OVER (PARTITION BY benchmark,run_timeout,depth_limit ORDER BY run_id) AS ordinal
 FROM _run_ r WHERE tool='PASDA-diff')
 SELECT p.has_uif,p.neq_status,p.eq_status,count(*) AS n FROM ranked r
 JOIN iteration i ON i.run_id=r.run_id JOIN partition p ON p.iteration_id=i.id
 WHERE r.ordinal=1 AND r.run_timeout=300 AND p.result IS NOT NULL
 GROUP BY p.has_uif,p.neq_status,p.eq_status
 ORDER BY p.has_uif,p.neq_status,p.eq_status''')
(ROOT / 'queries.json').write_text(json.dumps(queries, indent=2), encoding='utf-8')
(ROOT / 'query-results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
