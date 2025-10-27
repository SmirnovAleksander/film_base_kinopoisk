from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.config import settings
from api import router as api_router
from core.models import db_helper
from core.middleware.cors import setup_cors

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("🚀 Запуск FastAPI приложения...")
    try:
        await db_helper.init_db()
        logger.info("✅ База данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
    
    yield
    
    # shutdown
    logger.info("🛑 Остановка приложения...")
    print("Dispose engine")
    await db_helper.dispose()
    logger.info("✅ Движок БД освобожден")


# Обработчик глобальных ошибок
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Необработанная ошибка: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Внутренняя ошибка сервера", "detail": str(exc)}
    )


main_app = FastAPI(
    lifespan=lifespan,
    title="Film Base API",
    description="API для базы данных фильмов",
    version="1.0.0",
)

# Добавляем middleware
setup_cors(main_app)

# Глобальный обработчик исключений
main_app.add_exception_handler(Exception, global_exception_handler)

# Подключаем API роутер
main_app.include_router(
    api_router,
)

# Health check endpoint
@main_app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API работает корректно"}

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.debug
    )