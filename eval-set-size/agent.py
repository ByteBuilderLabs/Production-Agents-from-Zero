import anthropic
from tools import TOOLS, call_tool

client = anthropic.Anthropic(
    max_retries=5
)  # a 400-case run will hit a rate limit somewhere
MODEL = "claude-haiku-5-5"


def run_agent(question: str, max_turns: int = 5) -> str:
    messages = [{"role": "user", "content": question}]
    for _ in range(max_turns):
        reply = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": reply.content})
        if reply.stop_reason != "tool_use":
            return "".join(b.text for b in reply.content if b.type == "text")
        results = [call_tool(b) for b in reply.content if b.type == "tool_use"]
        messages.append({"role": "user", "content": results})
    return ""
