from app.apps.main.routers import router as main
from app.apps.project.routers import router as project
from app.apps.stat.routers import router as stat

__all__ = ["main", "project", "stat"]
