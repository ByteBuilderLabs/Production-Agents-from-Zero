import sqlite3, sys
from agent import DB

prefix = sys.argv[1]
con = sqlite3.connect(DB)
done = {
    r[0]
    for r in con.execute(
        "SELECT run_id FROM final_state WHERE run_id LIKE ? AND value='approved'",
        (prefix + "-%",),
    )
}
dirty = {
    r[0]
    for r in con.execute(
        "SELECT run_id FROM field_writes WHERE run_id LIKE ? "
        "GROUP BY run_id HAVING COUNT(*) > 1",
        (prefix + "-%",),
    )
}
print(f"{prefix}: finished {len(done)}")
print(f"{prefix}: duplicated {len(done & dirty)}")
