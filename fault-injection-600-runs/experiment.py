import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from faults import MODES
from agent import EXPECTED

BUCKETS = {
    "ok": "#3a3f47",
    "crash": "#007BFF",
    "visible": "#9aa0a6",
    "silent_wrong": "#e5484d",
}
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 100
TIMEOUT = 20


def one(mode):
    cmd = [sys.executable, "run_once.py", mode]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "crash"
    if p.returncode != 0 or not p.stdout.strip():
        return "crash"
    answer = json.loads(p.stdout.strip().splitlines()[-1])["answer"]
    if "TASK_FAILED" in answer:
        return "visible"
    return "ok" if EXPECTED in answer else "silent_wrong"


def column(mode):
    with ThreadPoolExecutor(max_workers=8) as pool:
        runs = list(pool.map(one, [mode] * RUNS))
    counts = {k: runs.count(k) for k in BUCKETS}
    print(mode, counts, flush=True)
    return counts


results = {m: column(m) for m in MODES}
json.dump(results, open("results.json", "w"), indent=2)

plt.style.use("dark_background")
plt.figure(figsize=(11, 5))
bottom = [0] * len(MODES)
for label, color in BUCKETS.items():
    vals = [results[m][label] for m in MODES]
    plt.bar(MODES, vals, bottom=bottom, label=label, color=color, width=0.6)
    bottom = [b + v for b, v in zip(bottom, vals)]
plt.ylabel("runs out of %d" % RUNS)
plt.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.22))
plt.savefig("results.png", dpi=160, bbox_inches="tight")
