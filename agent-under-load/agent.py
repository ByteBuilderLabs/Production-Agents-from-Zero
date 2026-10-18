from tools import TOOLS, FUNCS


def run_agent(task: str, client, max_turns: int = 5) -> str:
    messages = [{"role": "user", "content": task}]
    for _ in range(max_turns):
        resp = client.messages.create(
            model="claude-haiku-5-5", max_tokens=512, tools=TOOLS, messages=messages
        )
        if resp.stop_reason != "tool_use":
            return resp.content[0].text
        messages.append({"role": "assistant", "content": resp.content})
        results = [
            {
                "type": "tool_result",
                "tool_use_id": b.id,
                "content": FUNCS[b.name](**b.input),
            }
            for b in resp.content
            if b.type == "tool_use"
        ]
        messages.append({"role": "user", "content": results})
    return "Stopped: hit max turns."
