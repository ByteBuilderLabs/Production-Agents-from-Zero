from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from contract import MODEL, TEMPERATURE, SYSTEM_PROMPT, TOOL_SCHEMAS
from tools import TOOLS


def as_tool(f):
    return StructuredTool.from_function(
        TOOLS[f["name"]],
        name=f["name"],
        description=f["description"],
        args_schema=f["parameters"],
    )


llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE, use_responses_api=False)
agent = create_react_agent(
    llm, [as_tool(s["function"]) for s in TOOL_SCHEMAS], prompt=SYSTEM_PROMPT
)


def run(task: str) -> str:
    return agent.invoke({"messages": [("user", task)]})["messages"][-1].content
