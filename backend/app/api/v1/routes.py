from fastapi import APIRouter

from app.api.v1.endpoints import health, backtests, strategies, datasets

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"]) 
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"]) 
