from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.db import async_engine
from app.endpoints import main, stat
from app.endpoints import object as flats


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()  # закрыть пул соединений


app = FastAPI(title="TestAPI", version="1.0.0", root_path="/backend", lifespan=lifespan)

app.include_router(flats.router)
app.include_router(main.router)
app.include_router(stat.router)
