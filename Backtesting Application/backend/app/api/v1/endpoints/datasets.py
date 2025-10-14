from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os
import pandas as pd
import yfinance as yf
from datetime import datetime

from app.db.session import get_db
from app.db.models import Dataset
from app.core.config import settings

router = APIRouter()

class YFinanceRequest(BaseModel):
    ticker: str
    name: str | None = None
    start_date: str
    end_date: str
    interval: str = "1d"  # 1d, 1h, 5m, etc.

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    db: Session = Depends(get_db)
):
    """Upload a CSV dataset with OHLCV data"""
    
    # Validate file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed")
    
    # Read and validate CSV
    content = await file.read()
    try:
        df = pd.read_csv(pd.io.common.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(e)}")
    
    # Validate required columns (flexible column names)
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    df_cols_lower = [col.lower() for col in df.columns]
    
    missing_cols = [col for col in required_cols if col not in df_cols_lower]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain OHLCV columns. Missing: {missing_cols}. Found: {list(df.columns)}"
        )
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = name or file.filename.replace('.csv', '')
    filename = f"{safe_name}_{timestamp}.csv"
    file_path = os.path.join(settings.DATASET_DIR, filename)
    
    # Save file
    os.makedirs(settings.DATASET_DIR, exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Extract date range if date column exists
    start_date = None
    end_date = None
    for col in df.columns:
        if col.lower() in ['date', 'datetime', 'timestamp']:
            try:
                df[col] = pd.to_datetime(df[col])
                start_date = df[col].min()
                end_date = df[col].max()
            except:
                pass
            break
    
    # Save to database
    dataset = Dataset(
        user_id=1,  # Will add auth later
        name=name or file.filename,
        type="uploaded",
        file_path=file_path,
        start_date=start_date,
        end_date=end_date
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    return {
        "id": dataset.id,
        "name": dataset.name,
        "type": dataset.type,
        "rows": len(df),
        "columns": list(df.columns),
        "start_date": start_date,
        "end_date": end_date,
        "created_at": dataset.created_at
    }

@router.post("/yfinance")
def fetch_yfinance_data(req: YFinanceRequest, db: Session = Depends(get_db)):
    """
    Fetch historical data from Yahoo Finance.
    
    Note: Yahoo Finance can be unreliable and may block requests.
    If this fails, please use CSV upload instead.
    """
    
    try:
        import warnings
        import time
        warnings.filterwarnings('ignore')
        
        # Set user agent to avoid blocking
        import requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        print(f"Fetching {req.ticker} from {req.start_date} to {req.end_date}, interval={req.interval}")
        
        # Try with custom session
        ticker_obj = yf.Ticker(req.ticker, session=session)
        
        # Retry logic
        max_retries = 3
        df = pd.DataFrame()
        
        for attempt in range(max_retries):
            try:
                df = ticker_obj.history(
                    start=req.start_date,
                    end=req.end_date,
                    interval=req.interval,
                    auto_adjust=True,
                    prepost=False,
                    actions=False
                )
                if not df.empty:
                    break
                time.sleep(1)  # Wait before retry
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    raise
        
        print(f"Downloaded data shape: {df.shape}")
        print(f"Empty: {df.empty}")
        
        if df.empty:
            raise HTTPException(
                status_code=503,
                detail=f"Yahoo Finance is currently unavailable or blocking requests for {req.ticker}. Please try: (1) Using CSV upload instead, (2) Trying again in a few minutes, (3) Using a different ticker symbol."
            )
        
        # Reset index to make Date a column
        df.reset_index(inplace=True)
        
        # Save to CSV
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_name = req.name or req.ticker
        filename = f"{safe_name}_{timestamp}.csv"
        file_path = os.path.join(settings.DATASET_DIR, filename)
        
        os.makedirs(settings.DATASET_DIR, exist_ok=True)
        df.to_csv(file_path, index=False)
        
        # Save to database
        dataset = Dataset(
            user_id=1,
            name=req.name or f"{req.ticker} ({req.start_date} to {req.end_date})",
            type="yfinance",
            ticker=req.ticker,
            file_path=file_path,
            interval=req.interval,
            start_date=pd.to_datetime(req.start_date),
            end_date=pd.to_datetime(req.end_date)
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        return {
            "id": dataset.id,
            "name": dataset.name,
            "ticker": dataset.ticker,
            "type": dataset.type,
            "rows": len(df),
            "columns": list(df.columns),
            "start_date": dataset.start_date,
            "end_date": dataset.end_date,
            "created_at": dataset.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Failed to fetch data from YFinance: {str(e)}"
        print(f"YFinance error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)

@router.get("")
def list_datasets(db: Session = Depends(get_db)):
    """List all datasets"""
    datasets = db.query(Dataset).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "type": d.type,
            "ticker": d.ticker,
            "start_date": d.start_date,
            "end_date": d.end_date,
            "created_at": d.created_at
        }
        for d in datasets
    ]

@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get dataset details"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Load preview
    try:
        df = pd.read_csv(dataset.file_path, nrows=10)
        preview = df.to_dict(orient='records')
    except:
        preview = []
    
    return {
        "id": dataset.id,
        "name": dataset.name,
        "type": dataset.type,
        "ticker": dataset.ticker,
        "file_path": dataset.file_path,
        "start_date": dataset.start_date,
        "end_date": dataset.end_date,
        "created_at": dataset.created_at,
        "preview": preview
    }

@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Delete a dataset"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Delete file
    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    
    db.delete(dataset)
    db.commit()
    
    return {"message": "Dataset deleted successfully"}
