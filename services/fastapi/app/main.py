from fastapi import FastAPI

from .routers.main import router as main_router

app = FastAPI(title="FastAPI", version="1.0.0", root_path="/backend")


app.include_router(main_router)
