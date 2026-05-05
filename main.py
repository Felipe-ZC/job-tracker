from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import get_settings
from db import DbClient
from routes import companies


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.db = DbClient(settings.db_conn_str)
    await app.state.db.connect()
    yield
    await app.state.db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(companies.router)
