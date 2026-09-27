MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
SYSTEM_PROMPT = "Answer invoice questions using the tools. Reply with the number only, two decimals."
TASK = "Invoice INV-2041 is billed in USD. What is its total in EUR?"
EXPECTED = "1692.80"
STR, NUM = {"type": "string"}, {"type": "number"}
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_invoice",
            "description": "Look up an invoice by ID.",
            "parameters": {
                "type": "object",
                "required": ["invoice_id"],
                "properties": {"invoice_id": STR},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert",
            "description": "Convert an amount between currencies.",
            "parameters": {
                "type": "object",
                "required": ["amount", "from_currency", "to_currency"],
                "properties": {"amount": NUM, "from_currency": STR, "to_currency": STR},
            },
        },
    },
]
