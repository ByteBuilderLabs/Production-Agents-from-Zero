import asyncio
from fastapi import FastAPI, HTTPException
from agent import run_agent

MAX_CONCURRENT = 8  # agent runs in flight at once
TIMEOUT_S = 60  # wall-clock cap per request
app = FastAPI()
slots = asyncio.Semaphore(MAX_CONCURRENT)


@app.post("/ask")
async def ask(body: dict):
    if slots.locked():  # every slot busy: say no instead of queueing
        raise HTTPException(429, "at capacity", headers={"Retry-After": "2"})
    async with slots:
        return await run_agent(body["q"], TIMEOUT_S)
