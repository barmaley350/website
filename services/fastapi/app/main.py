from fastapi import FastAPI

from .routers.main import router as main_router
from .routers.post import router as post_router

app = FastAPI(title="TestAPI", version="1.0.0", root_path="/backend")


app.include_router(main_router)
app.include_router(post_router)
