__all__ = ("templates",)

from fastapi.templating import Jinja2Templates
from core.config import BASE_DIR, ApiPrefix

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)