import json

FIXTURE = {"INV-2041": {"total": 1840.00, "currency": "USD"}}
RATES = {("USD", "EUR"): 0.92}


def get_invoice(invoice_id: str) -> str:
    return json.dumps(FIXTURE[invoice_id])


def convert(amount: float, from_currency: str, to_currency: str) -> str:
    rate = RATES[from_currency + to_currency]
    return json.dumps({"amount": round(amount * rate, 2), "currency": to_currency})


TOOLS = {"get_invoice": get_invoice, "convert": convert}


def call_tool(name: str, args_json: str) -> str:
    return TOOLS[name](**json.loads(args_json))
