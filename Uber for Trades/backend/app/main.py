from fastapi import FastAPI
from app.db.session import engine, Base
# Ensure models are imported so SQLAlchemy registers tables on Base.metadata
from app import models  # noqa: F401
from app.api import users as users_router
from app.api import jobs as jobs_router
from app.api import providers as providers_router
from app.api import reviews as reviews_router
from app.api import chat as chat_router
from app.api import auth as auth_router
from app.api import payments as payments_router
from app.api import demo as demo_router
from app.db.seed_data import seed_demo_data

app = FastAPI(title="SwiftTrade API", version="1.0")


@app.on_event("startup")
async def on_startup() -> None:
    # Create tables on startup for MVP convenience
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed demo data
    await seed_demo_data()

app.include_router(users_router.router)
app.include_router(jobs_router.router)
app.include_router(providers_router.router)
app.include_router(reviews_router.router)
app.include_router(chat_router.router)
app.include_router(auth_router.router)
app.include_router(payments_router.router)
app.include_router(demo_router.router)


@app.get("/health")
async def health() -> dict:
	return {"status": "ok"}
