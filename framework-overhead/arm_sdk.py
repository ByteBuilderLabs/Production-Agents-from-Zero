from agents import (Agent,FunctionTool,ModelSettings,Runner,set_default_openai_api,set_tracing_disabled)
from contract import MODEL, TEMPERATURE, SYSTEM_PROMPT, TOOL_SCHEMAS
from tools import call_tool

set_default_openai_api("chat_completions")
set_tracing_disabled(True)
def as_tool(f):
    async def invoke(ctx, args):
        return call_tool(f["name"], args)

    return FunctionTool(
        name=f["name"],
        description=f["description"],
        params_json_schema=f["parameters"],
        on_invoke_tool=invoke,
    )

agent = Agent(
    name="invoices",
    instructions=SYSTEM_PROMPT,
    model=MODEL,
    model_settings=ModelSettings(temperature=TEMPERATURE),
    tools=[as_tool(s["function"]) for s in TOOL_SCHEMAS],
)

def run(task: str) -> str:
    return Runner.run_sync(agent, task).final_output
