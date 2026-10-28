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


-----------

IEEE 754 double-precision floating-point format
Some decimal numbers cannot be represented EXACTLY using this format. 
Hence we should use Decimal module from python for decimal calculations
Decimal keeps the digits exactly as we write them. Build it from a string, never from a float
Ex:
Decimal("0.1") + Decimal("0.2")
Decimal(0.1)

-----------

pip install pymysql cryptography

SQL Injection

query = f"SELECT * FROM demo_product WHERE name = '{name}'"
cur.execute(query)
name = "x' OR '1'='1"
The input can change the meaning of the SQL command. 
In this example, the condition '1'='1' is always true, potentially causing every row to be returned.

This vulnerability is called SQL injection.

use Paramteriezed query
cur.execute(
    "SELECT * FROM demo_product WHERE name = %s",
    (name,)
)

NEVER build SQL using f-strings

------------

ORM - Object Relational Mapper

pip install "sqlalchemy[asyncio]" asyncmy alembic

---------
Put this in youe env file 
DATABASE_URL=mysql+asyncmy://root:your_password@localhost:3306/shopnest


----------

AsyncContextManager
-- Prepares the application for startup and shutdown