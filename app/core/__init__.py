from app.core.config import get_settings
from app.core.logger import init_log_handlers

settings = get_settings()

init_log_handlers(settings)
