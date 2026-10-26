import asyncio, time, uuid
from cost import RequestCost, write_row
from llm import MODEL, MAX_STEPS, call_model, run_tools


async def agent_loop(question: str, rc: RequestCost) -> str | None:
    messages = [{"role": "user", "content": question}]
    for step in range(1, MAX_STEPS + 1):
        rc.steps = step
        resp = await call_model(messages, rc)  # sends the WHOLE history, bills the call
        if resp.stop_reason != "tool_use":
            rc.terminal_state = "completed"
            return "".join(b.text for b in resp.content if b.type == "text")
        messages += [
            {"role": "assistant", "content": resp.content},
            {"role": "user", "content": run_tools(resp)},
        ]  # history grows every step
    rc.terminal_state = "step_limit"  # ran out of steps, returns None


async def run_agent(question: str, timeout_s: float) -> dict:
    rc = RequestCost(request_id=uuid.uuid4().hex, model=MODEL)
    answer, start = None, time.perf_counter()
    try:
        async with asyncio.timeout(timeout_s):
            answer = await agent_loop(question, rc)
    except TimeoutError:
        rc.terminal_state = "timeout"
    finally:  # runs on success, timeout AND crash
        rc.wall_ms = int((time.perf_counter() - start) * 1000)
        try:
            await asyncio.to_thread(write_row, rc)  # sync driver, off the event loop
        except Exception as e:  # a lost row must never fail the request
            print("cost row lost:", rc.request_id, e)
    return {"request_id": rc.request_id, "answer": answer, "state": rc.terminal_state}
