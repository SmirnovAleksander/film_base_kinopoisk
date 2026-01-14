from fastapi.middleware.cors import CORSMiddleware

from core.config import settings


def setup_cors(app):
    """Настройки CORS"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allowed_origins if hasattr(settings, 'cors') else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )