from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.router import api_router, health
from internal.config.settings import settings


def create_app():
    app = FastAPI(title="Cupid")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.include_router(api_router, prefix=settings.API_PREFIX)
    app.include_router(health.router, prefix=settings.HEALTH_PREFIX)

    return app
