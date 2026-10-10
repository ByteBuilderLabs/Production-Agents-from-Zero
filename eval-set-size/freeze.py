import json
from agent import run_agent
from oracle import grade

cases = [json.loads(line) for line in open("cases.jsonl")]
passed = 0
with open("results.jsonl", "w") as f:
    for case in cases:
        answer = run_agent(case["question"])
        ok = grade(case, answer)
        passed += ok
        f.write(json.dumps({"id": case["id"], "answer": answer, "correct": ok}) + "\n")
        print(f"case {case['id']:>3}: {'PASS' if ok else 'FAIL'}")
print(f"all {len(cases)} cases: {passed / len(cases):.1%}")
