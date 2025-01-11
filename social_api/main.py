import logging
from fastapi import FastAPI, HTTPException
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.exception_handlers import http_exception_handler
from social_api.routers.post import router as post_router
from contextlib import asynccontextmanager
from social_api.database import database
from social_api.logging_conf import configure_logging
from social_api.routers.user import router as user_router
from social_api.routers.upload import router as upload_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(upload_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTP Exception: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
