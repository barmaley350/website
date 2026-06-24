from app.apps.main.routers import router as main
from app.apps.object.routers import router as flats
from app.apps.stat.routers import router as stat

__all__ = ["flats", "main", "stat"]
