import re
from tools import PRICES, TAX


def expected(product: str, city: str, qty: int) -> float:
    return round(qty * PRICES[product] * (1 + TAX[city] / 100), 2)


def grade(case: dict, answer: str) -> bool:
    numbers = re.findall(r"ANSWER:\D*([\d,]*\.?\d+)", answer)
    if not numbers:
        return False
    got = float(numbers[-1].replace(",", ""))
    return round(abs(got - case["expected"]), 2) <= 0.01
