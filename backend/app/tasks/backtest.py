from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.db.models import Backtest
import pandas as pd
import numpy as np
from datetime import datetime
import traceback

@celery_app.task(name="tasks.backtest.run_backtest")
def run_backtest(backtest_id: int, strategy_path: str, dataset_path: str, config: dict):
    db = SessionLocal()
    
    try:
        # Update status to running
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
        if not backtest:
            return {"error": "Backtest not found"}
        
        backtest.status = "running"
        backtest.started_at = datetime.utcnow()
        db.commit()
        
        # Load dataset
        df = pd.read_csv(dataset_path)
        
        # Normalize column names
        df.columns = [col.lower() for col in df.columns]
        
        # Basic vectorized backtest simulation (placeholder for real strategy execution)
        initial_capital = config.get("initial_capital", 10000.0)
        commission = config.get("commission", 0.001)
        
        # Simple buy-and-hold strategy as demo
        df['returns'] = df['close'].pct_change()
        df['strategy_returns'] = df['returns'] - commission
        df['equity'] = initial_capital * (1 + df['strategy_returns']).cumprod()
        df['equity'].fillna(initial_capital, inplace=True)
        
        # Calculate metrics
        total_return = (df['equity'].iloc[-1] - initial_capital) / initial_capital
        
        returns = df['strategy_returns'].dropna()
        sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        downside_returns = returns[returns < 0]
        sortino = returns.mean() / downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0
        
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        calmar = total_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        results = {
            "metrics": {
                "total_return": float(total_return),
                "sharpe_ratio": float(sharpe),
                "sortino_ratio": float(sortino),
                "max_drawdown": float(max_drawdown),
                "calmar_ratio": float(calmar),
                "total_trades": 0,  # Placeholder
            },
            "equity_curve": df['equity'].tolist()[-100:],  # Last 100 points
            "trades": [],  # Placeholder
        }
        
        # Update backtest with results
        backtest.status = "completed"
        backtest.results = results
        backtest.completed_at = datetime.utcnow()
        db.commit()
        
        return results
        
    except Exception as e:
        # Update status to failed
        backtest.status = "failed"
        backtest.results = {"error": str(e), "traceback": traceback.format_exc()}
        backtest.completed_at = datetime.utcnow()
        db.commit()
        raise
        
    finally:
        db.close()
