import json, sys
import agent, faults

mode = sys.argv[1]
if mode == "poisoned":
    agent.FIXTURE["EUR"] = 0.50

agent.call_tool = faults.wrap(agent.call_tool, mode)
answer = agent.run(agent.QUESTION, faults.MAX_TOKENS.get(mode, 1024))
print(json.dumps({"answer": answer}))
