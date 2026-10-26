import csv, math, random, httpx
from concurrent.futures import ThreadPoolExecutor


def ask(_):
    nums = [
        random.randint(2, 9) for _ in range(1 + min(int(random.paretovariate(1.2)), 20))
    ]
    q = f"Multiply {' by '.join(map(str, nums))}. Use one tool call per multiplication."
    r = httpx.post("http://127.0.0.1:8000/ask", json={"q": q}, timeout=120)
    if r.status_code != 200:
        return None  # 500 = crash, the server already wrote its row
    body = r.json()
    return body["request_id"], str(math.prod(nums)) in (body["answer"] or "").replace(
        ",", ""
    )


with ThreadPoolExecutor(6) as pool:  # 6 in flight, under the server's 8 slots
    rows = [row for row in pool.map(ask, range(200)) if row]
csv.writer(open("labels.csv", "w", newline="")).writerows(
    [("request_id", "correct"), *rows]
)
print(f"sent 200 requests, labelled {len(rows)} answers")
