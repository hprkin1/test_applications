from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import ast
from datetime import datetime

from app.db.session import get_db
from app.db.models import Strategy
from app.core.config import settings

router = APIRouter()

def validate_strategy_file(content: str) -> dict:
    """
    Validate that the Python file contains required strategy components.
    Expected: A class with run() or execute() method, or a function named strategy().
    """
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Python syntax: {str(e)}")
    
    has_strategy_class = False
    has_strategy_function = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if class has run() or execute() method
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name in ["run", "execute", "backtest"]:
                    has_strategy_class = True
                    break
        elif isinstance(node, ast.FunctionDef) and node.name in ["strategy", "run_strategy", "backtest"]:
            has_strategy_function = True
    
    if not (has_strategy_class or has_strategy_function):
        raise HTTPException(
            status_code=400,
            detail="Strategy file must contain either a class with run()/execute()/backtest() method or a function named strategy()/run_strategy()/backtest()"
        )
    
    return {
        "valid": True,
        "has_class": has_strategy_class,
        "has_function": has_strategy_function
    }

@router.post("")
async def upload_strategy(
    file: UploadFile = File(...),
    name: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Upload and validate a Python strategy file"""
    
    # Validate file extension
    if not file.filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Only .py files are allowed")
    
    # Read file content
    content = await file.read()
    try:
        content_str = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 encoded text")
    
    # Validate strategy structure
    validation = validate_strategy_file(content_str)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = name or file.filename.replace('.py', '')
    filename = f"{safe_name}_{timestamp}.py"
    file_path = os.path.join(settings.STRATEGY_DIR, filename)
    
    # Save file
    os.makedirs(settings.STRATEGY_DIR, exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content_str)
    
    # Save to database (user_id=1 for now, will add auth later)
    strategy = Strategy(
        user_id=1,
        name=name or file.filename,
        file_path=file_path,
        description=description or ""
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    
    return {
        "id": strategy.id,
        "name": strategy.name,
        "file_path": strategy.file_path,
        "validation": validation,
        "created_at": strategy.created_at
    }

@router.get("")
def list_strategies(db: Session = Depends(get_db)):
    """List all strategies"""
    strategies = db.query(Strategy).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "created_at": s.created_at
        }
        for s in strategies
    ]

@router.get("/{strategy_id}")
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    """Get strategy details"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    return {
        "id": strategy.id,
        "name": strategy.name,
        "description": strategy.description,
        "file_path": strategy.file_path,
        "created_at": strategy.created_at
    }

@router.delete("/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    """Delete a strategy"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    # Delete file
    if os.path.exists(strategy.file_path):
        os.remove(strategy.file_path)
    
    db.delete(strategy)
    db.commit()
    
    return {"message": "Strategy deleted successfully"}
