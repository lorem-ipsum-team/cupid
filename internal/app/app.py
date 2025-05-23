from contextlib import asynccontextmanager
import cProfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.router import api_router, health
from internal.config.settings import settings


@asynccontextmanager
async def lifespan(_app):
    profiling = settings.PROFILING
    profiler = None
    print("Starting up...")

    if profiling:
        profiler = cProfile.Profile(builtins=False)
        profiler.enable()
        print("Profiler enabled")

    yield
    print("Shutting down...")

    if profiling:
        profiler.disable()
        print("Profiler disabled, dumping stats...")
        profiler.dump_stats("./profiles/profiling_results.prof")


def create_app():
    app = FastAPI(title="Cupid", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.include_router(api_router, prefix=settings.API_PREFIX)
    app.include_router(health.router, prefix=settings.HEALTH_PREFIX)

    return app
