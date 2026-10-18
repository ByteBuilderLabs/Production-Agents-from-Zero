from contextlib import asynccontextmanager
import anthropic
from anyio import to_thread
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from agent import run_agent


@asynccontextmanager
async def lifespan(app):
    to_thread.current_default_thread_limiter().total_tokens = (
        16  # the fixed worker pool
    )
    yield


app = FastAPI(lifespan=lifespan)

client = anthropic.Anthropic(max_retries=0)  # no hidden retries: 429s stay visible


@app.exception_handler(anthropic.APIError)
async def provider_error(request, exc):  # 429 stays 429, timeouts become 504
    status = getattr(exc, "status_code", 504)
    return JSONResponse({"error": type(exc).__name__}, status_code=status)


@app.post("/run")
def run(body: dict):
    return {"answer": run_agent(body["task"], client)}
