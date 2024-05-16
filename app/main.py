# import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from redis import asyncio as aioredis

from app.config.app_settings import settings
# from app.lessons.math.equations.quadratic_equations import (
#     equation_router
# )
from app.auth import auth_router
from app.users import users_router
from app.files import files_router
from app.lessons.manage import manage_lesson_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    redis = aioredis.from_url(
        f"{settings.APP_CACHE_URL}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # on shutdown


app = FastAPI(
    title="AcademyCloud Управление",
    version="Beta 1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/image", StaticFiles(directory="app/static/images"), name="images")
app.mount("/file", StaticFiles(directory="app/static/files"), name="files")


app.include_router(auth_router.router, prefix=settings.APP_PREFIX)
app.include_router(users_router.router, prefix=settings.APP_PREFIX)
app.include_router(files_router.router, prefix=settings.APP_PREFIX)
app.include_router(manage_lesson_router.router, prefix=settings.APP_PREFIX)
# app.include_router(equation_router.router, prefix=settings.APP_PREFIX)


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        reload=True,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.APP_LOG_LEVEL
    )
