"""Docstring для services.fastapi.app.routers.main."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


# http://localhost:1338/fastapi/api/v1/projects
@router.get("/")
def get_routes() -> dict:
    """_summary_.

    :return: _description_
    :rtype: dict
    """
    return {"message": "Check http://localhost:1338/fastapi/docs for mode details"}
