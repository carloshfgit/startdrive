# HTTP API Interface
# Routers FastAPI e controllers.

from . import deps
from .v1 import router as v1_router

__all__ = ["deps", "v1_router"]
