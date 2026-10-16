# Uvicorn -> Server program -> listens for requests on a port
# FastAPI -> The backend FRAMEWORK -- routes, check input, build the response

# python -m venv .venv

# Virtual Environment -> Isolated Python environment for your project

Blocking IO pattern -> While waiting on something slow (network, disk, another service), 
                        the server does zero useful work and cannot serve anyone else.

Event Loop (non-blocking) -> one worker that never sits idle. The moment something starts waiting, 
                            it moves on to other work, and returns the instant the wait is over.


product_id: int -> TYPE Hint . FastAPi reads it and converts the url text into a integer for us

http://127.0.0.1:8000/docs -> Swagger UI for testing the apis

async def -> gives the function permission to pause. 
await -> It is the actual handoff

Just using async def will not solve the blocking IO. You will have to use await also