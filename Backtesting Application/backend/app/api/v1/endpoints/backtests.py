from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from datetime import datetime

from app.tasks.celery_app import celery_app
from app.db.session import get_db
from app.db.models import Backtest, Strategy, Dataset

router = APIRouter()

class BacktestRequest(BaseModel):
    name: str
    strategy_id: int
    dataset_id: int
    start_date: str | None = None
    end_date: str | None = None
    initial_capital: float = 10000.0
    commission: float = 0.001

@router.post("")
def create_backtest(req: BacktestRequest, db: Session = Depends(get_db)):
    # Validate strategy exists
    strategy = db.query(Strategy).filter(Strategy.id == req.strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    # Validate dataset exists
    dataset = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create backtest record
    backtest = Backtest(
        user_id=1,
        strategy_id=req.strategy_id,
        dataset_id=req.dataset_id,
        name=req.name,
        status="pending",
        parameters=req.model_dump()
    )
    db.add(backtest)
    db.commit()
    db.refresh(backtest)
    
    # Queue task with backtest ID
    task = celery_app.send_task(
        "tasks.backtest.run_backtest",
        args=[backtest.id, strategy.file_path, dataset.file_path, req.model_dump()]
    )
    
    return {
        "backtest_id": backtest.id,
        "task_id": task.id,
        "status": "queued"
    }

@router.get("")
def list_backtests(db: Session = Depends(get_db)):
    """List all backtests"""
    backtests = db.query(Backtest).order_by(Backtest.created_at.desc()).all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "status": b.status,
            "strategy_id": b.strategy_id,
            "dataset_id": b.dataset_id,
            "created_at": b.created_at,
            "completed_at": b.completed_at
        }
        for b in backtests
    ]

@router.get("/{backtest_id}")
def get_backtest(backtest_id: int, db: Session = Depends(get_db)):
    """Get backtest status and details"""
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    return {
        "id": backtest.id,
        "name": backtest.name,
        "status": backtest.status,
        "strategy_id": backtest.strategy_id,
        "dataset_id": backtest.dataset_id,
        "parameters": backtest.parameters,
        "results": backtest.results,
        "created_at": backtest.created_at,
        "started_at": backtest.started_at,
        "completed_at": backtest.completed_at
    }

@router.delete("/{backtest_id}")
def delete_backtest(backtest_id: int, db: Session = Depends(get_db)):
    """Delete a backtest"""
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    db.delete(backtest)
    db.commit()
    
    return {"message": "Backtest deleted successfully"}
