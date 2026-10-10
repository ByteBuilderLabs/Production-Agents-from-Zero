PRICES = {"widget": 18.45, "bolt": 0.73, "gear": 12.90, "valve": 47.60, "sensor": 129.99}
TAX = {"Sofia": 20, "Berlin": 19, "Lisbon": 23, "Prague": 21, "Vienna": 20}
FUNCS = {"get_unit_price": lambda product: PRICES.get(product, "unknown product"),
         "get_tax_rate": lambda city: TAX.get(city, "unknown city")}

def schema(name, desc, arg):
    return {"name": name, "description": desc, "input_schema": {
        "type": "object", "properties": {arg: {"type": "string"}}, "required": [arg]}}

TOOLS = [schema("get_unit_price", "Unit price in EUR for one unit of a product.", "product"),
         schema("get_tax_rate", "Sales tax rate in percent for a city.", "city")]

def call_tool(block):
    result = FUNCS[block.name](**block.input)
    return {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}