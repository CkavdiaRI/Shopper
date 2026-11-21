import asyncio
import random

from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

friends = {
    "auth": {"delay": 0, "fail": 0, "code": 503},   # how slow (ms), how often it fails (%), which code it fails with
    "groq": {"delay": 0, "fail": 0, "code": 503},
}

calls = {"auth": 0, "groq": 0}                       # how many calls each friend got


@app.get("/set")
async def set_friend(who: str | None = None, delay: int | None = None, fail: int | None = None, code: int | None = None):
    """Set the behavior of a friend service. Delay in ms, fail in % and code is the HTTP error code."""
    if who in friends:
        if delay is not None:
            friends[who]["delay"] = delay
        if fail is not None:
            friends[who]["fail"] = fail
        if code is not None:
            friends[who]["code"] = code
    return friends

@app.get("/calls")
async def get_calls(reset: bool = False):
    """Get the number of calls each friend service got."""
    if reset:
        for who in calls:
            calls[who] = 0
    return calls


@app.get("/groq")
async def groq():
    calls["groq"] += 1
    settings = friends["groq"]
    await asyncio.sleep(settings["delay"] / 1000)