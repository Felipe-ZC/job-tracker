from fastapi import Request


# Get a db connection form the pool when a request starts and release it when it ends
async def get_db_conn(request: Request):
    async with request.app.state.db.get_db_conn() as conn:
        yield conn
