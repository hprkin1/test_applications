from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routes import api_router
from app.db.models import Base
from app.db.session import engine
import os

app = FastAPI(
    title="QuantFlow API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS (expand origins in non-dev as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    # Ensure storage directories exist
    for path in [
        settings.UPLOAD_DIR,
        settings.STRATEGY_DIR,
        settings.DATASET_DIR,
        settings.RESULTS_DIR,
    ]:
        os.makedirs(path, exist_ok=True)

    # Create DB tables (replace with Alembic in later iterations)
    Base.metadata.create_all(bind=engine)
    
    # Create default user if not exists
    from app.db.session import SessionLocal
    from app.db.models import User
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            user = User(id=1, email="demo@quantflow.com", hashed_password="demo", is_active=True)
            db.add(user)
            db.commit()
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "quantflow-api"}

app.include_router(api_router, prefix="/api/v1")
