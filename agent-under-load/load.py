import sys, time, httpx
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

TASK = {"task": "Order A101 arrived 4 days late. Look it up and calculate the refund."}


def ask():
    try:
        r = httpx.post("http://localhost:8000/run", json=TASK, timeout=30)
    except httpx.TimeoutException:
        return "lost", 0
    return r.status_code, r.elapsed.total_seconds()


rate = int(sys.argv[1])  # requests per second, whether or not earlier ones finished
with ThreadPoolExecutor(500) as pool:
    futures = []
    for _ in range(rate * 60):  # one minute of traffic
        futures.append(pool.submit(ask))
        time.sleep(1 / rate)
    results = [f.result() for f in futures]
ok = sorted(t for code, t in results if code == 200)
print(
    f"{rate} req/s: p50 {ok[len(ok) // 2]:.1f}s, "
    f"p95 {ok[int(len(ok) * 0.95)]:.1f}s, {dict(Counter(c for c, _ in results))}"
)
