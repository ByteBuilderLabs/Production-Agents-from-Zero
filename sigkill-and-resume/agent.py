import json, os, sqlite3, sys

DB = "runs.db"
RUN_ID, CKPT, PARK = None, None, None

PLAN = [
    ("get_record", "r-1"),
    ("validate_record", "r-1"),
    ("write_field", "status=approved"),
    ("finalize", "r-1"),
]


def get_record(arg):
    return "record:" + arg


def validate_record(arg):
    return "valid"


def ensure_tables():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS field_writes (run_id, field, value)")
    con.execute("CREATE TABLE IF NOT EXISTS final_state (run_id PRIMARY KEY, value)")
    con.commit()
    con.close()


def write_field(arg):
    field, value = arg.split("=")
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO field_writes VALUES (?,?,?)", (RUN_ID, field, value))
    con.commit()
    con.close()
    return "wrote " + field


def finalize(arg):
    con = sqlite3.connect(DB)
    con.execute("INSERT OR REPLACE INTO final_state VALUES (?,?)", (RUN_ID, "approved"))
    con.commit()
    con.close()
    return "done"


TOOLS = {
    "get_record": get_record,
    "validate_record": validate_record,
    "write_field": write_field,
    "finalize": finalize,
}


def load_state():
    if CKPT and os.path.exists(CKPT):
        with open(CKPT) as f:
            return json.load(f)
    return {"step": 0}


def save_state(state):
    if not CKPT:
        return
    with open(CKPT, "w") as f:
        json.dump(state, f)


def run():
    state = load_state()
    while state["step"] < len(PLAN):
        name, arg = PLAN[state["step"]]
        result = TOOLS[name](arg)
        print(f"TOOL_RESULT {state['step']} {name} {result}", flush=True)
        if PARK == state["step"]:
            print("WINDOW_OPEN", flush=True)
            sys.stdin.readline()
        state["step"] += 1
        save_state(state)


if __name__ == "__main__":
    RUN_ID = sys.argv[1]
    CKPT = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    PARK = int(sys.argv[3]) if len(sys.argv) > 3 else None
    ensure_tables()
    run()
