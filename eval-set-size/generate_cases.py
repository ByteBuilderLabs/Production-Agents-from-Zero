import json, random
from tools import PRICES, TAX
from oracle import expected

TEMPLATE = (
    "A customer in {city} orders {qty} units of {product}. Look up the unit price "
    "and the tax rate, then compute the total in EUR including tax. "
    "End with one line: ANSWER: <total as a plain number like 1234.56>"
)
rng = random.Random(42)  # fixed seed: same 400 cases on every machine

with open("cases.jsonl", "w") as f:
    for i in range(400):
        case = {
            "id": i,
            "product": rng.choice(list(PRICES)),
            "city": rng.choice(list(TAX)),
            "qty": rng.randint(12, 480),
        }
        case["question"] = TEMPLATE.format(**case)
        case["expected"] = expected(case["product"], case["city"], case["qty"])
        f.write(json.dumps(case) + "\n")
