# Import all model modules here so tools (Alembic) can find them when importing `app.models`
from .user import User
from .instructor import InstructorProfile
# Adições da Fase 2:
from .availability import Availability
from .ride import Ride