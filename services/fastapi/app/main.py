from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.apps import routers

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     await db.db_engine.dispose()  # закрыть пул соединений


# app = FastAPI(title="TestAPI", version="1.0.0", root_path="/backend", lifespan=lifespan)
app = FastAPI(title="TestAPI", version="1.0.0", root_path="/backend")


@app.exception_handler(NoResultFound)
async def handle_no_result(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Requested resource not found."},
    )


@app.exception_handler(MultipleResultsFound)
async def handle_multiple_results(request: Request, exc: MultipleResultsFound):
    # Это обычно означает логическую ошибку в запросе или данных
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,  # или 500, или 400
        content={"detail": "Multiple records found where only one was expected."},
    )


app.include_router(routers.project)
app.include_router(routers.main)
app.include_router(routers.stat)
