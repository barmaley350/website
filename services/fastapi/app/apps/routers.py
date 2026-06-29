from app.apps.main.routers import router as main
from app.apps.projects.routers import router as project
from app.apps.stats.routers import router as stat

__all__ = ["main", "project", "stat"]
