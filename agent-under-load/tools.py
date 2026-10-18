ORDERS = {"A100": 120.0, "A101": 89.5, "A102": 240.0}  # the fixed fixture

def lookup_order(order_id: str) -> str:
    return f"Order {order_id} total: {ORDERS[order_id]} EUR"

def calculate_refund(total: float, days_late: int) -> str:
    return f"Refund: {round(total * min(0.05 * days_late, 0.5), 2)} EUR"

FUNCS = {"lookup_order": lookup_order, "calculate_refund": calculate_refund}
TOOLS = [
    {
        "name": "lookup_order",
        "description": "Get an order's total in EUR.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],},},
    {
        "name": "calculate_refund",
        "description": "Refund owed for a late order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "total": {"type": "number"},
                "days_late": {"type": "integer"},
            },
            "required": ["total", "days_late"],},},]
