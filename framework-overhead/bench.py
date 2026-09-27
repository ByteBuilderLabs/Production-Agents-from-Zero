import os, sys, time, statistics, importlib, httpx

ARM = sys.argv[1]
os.environ["OPENAI_BASE_URL"] = f"http://127.0.0.1:8080/{ARM}/v1"
from contract import TASK, EXPECTED

run = importlib.import_module(f"arm_{ARM}").run
overhead, tokens, correct = [], [], 0
for _ in range(200):
    start = time.perf_counter()
    correct += EXPECTED in (run(TASK) or "")
    wall_ms = (time.perf_counter() - start) * 1000
    api = httpx.post("http://127.0.0.1:8080/reset").json()
    overhead.append(wall_ms - api["api_ms"])
    tokens.append(api["tokens"])
q = statistics.quantiles(overhead, n=100)
print(
    f"{ARM}: {statistics.mean(tokens):.2f} tokens/run, p50 {q[49]:.0f}ms, p95 {q[94]:.0f}ms, {correct}/200 correct"
)
