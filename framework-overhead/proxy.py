import time, httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()
openai_api = httpx.AsyncClient(base_url="https://api.openai.com/v1", timeout=120)
totals = {"api_ms": 0.0, "tokens": 0}


@app.post("/reset")
async def reset():
    snapshot = dict(totals)
    totals.update(api_ms=0.0, tokens=0)
    return snapshot


@app.post("/{arm}/v1/{path:path}")
async def relay(arm: str, path: str, request: Request):
    body = await request.body()
    start = time.perf_counter()
    resp = await openai_api.post(
        path,
        content=body,
        headers={
            "Authorization": request.headers["authorization"],
            "Content-Type": "application/json",
        },
    )
    totals["api_ms"] += (time.perf_counter() - start) * 1000
    totals["tokens"] += resp.json().get("usage", {}).get("prompt_tokens", 0)
    with open(f"payloads_{arm}.jsonl", "a", encoding="utf-8") as f:
        f.write(body.decode() + "\n")
    return Response(resp.content, resp.status_code, media_type="application/json")
