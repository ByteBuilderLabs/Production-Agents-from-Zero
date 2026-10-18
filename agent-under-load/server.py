import asyncio
import anthropic
from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool
from agent import run_agent
from server_naive import lifespan, provider_error  # same pool, same error handling

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(anthropic.APIError, provider_error)
client = anthropic.Anthropic(
    max_retries=0, timeout=3.0
)  # fix 1: was 10 minutes per call
runs = asyncio.Semaphore(16)  # fix 2: what the provider handled with zero 429s


admitted = asyncio.Semaphore(16 + 16)  # fix 3: 16 running + 16 waiting, nobody else


@app.post("/run")
async def run(body: dict):
    if admitted.locked():  # full: say no now, not in thirty seconds
        raise HTTPException(503, "queue full", headers={"Retry-After": "2"})
    async with admitted, runs:
        return {
            "answer": await run_in_threadpool(
                run_agent, body["task"], client, max_turns=4
            )
        }
