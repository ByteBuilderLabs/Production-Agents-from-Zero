from openai import OpenAI
from contract import MODEL, TEMPERATURE, SYSTEM_PROMPT, TOOL_SCHEMAS
from tools import call_tool

client = OpenAI()
def run(task: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    while True:
        msg = (
            client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                messages=messages,
                tools=TOOL_SCHEMAS,)
            .choices[0]
            .message)
        if not msg.tool_calls:
            return msg.content
        messages.append(
            {
                "role": "assistant",
                "tool_calls": [c.model_dump() for c in msg.tool_calls],
            })
        for c in msg.tool_calls:
            result = call_tool(c.function.name, c.function.arguments)
            messages.append({"role": "tool", "tool_call_id": c.id, "content": result})
