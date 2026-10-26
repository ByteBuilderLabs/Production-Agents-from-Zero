from anthropic import AsyncAnthropic

client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY
MODEL, MAX_STEPS = "claude-sonnet-5-5", 25  # the model you're measuring [VERIFY]
TOOLS = [{
        "name": "multiply",
        "description": "Multiply two integers. Use it for every multiplication.",
        "input_schema": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},},}]

async def call_model(messages, rc):  # the one place that talks to the model...
    resp = await client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=TOOLS,
        messages=messages,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    )
    rc.input_tokens += resp.usage.input_tokens  # ...so it's the one place that bills
    rc.output_tokens += resp.usage.output_tokens
    return resp

def run_tools(resp):  # do the multiplication, return the result
    return [{
            "type": "tool_result",
            "tool_use_id": b.id,
            "content": str(b.input["a"] * b.input["b"]),}
        for b in resp.content
        if b.type == "tool_use"]
