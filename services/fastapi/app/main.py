from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.db import async_engine
from .routers.main import router as main_router
from .routers.object import router as object_router
from .routers.post import router as post_router
from .routers.stat import router as stat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()  # закрыть пул соединений


app = FastAPI(title="TestAPI", version="1.0.0", root_path="/backend", lifespan=lifespan)


app.include_router(main_router)
# app.include_router(post_router)
app.include_router(object_router)
app.include_router(stat_router)
