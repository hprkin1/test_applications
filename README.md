# QuantFlow - Backtesting Platform

A modern web-based platform for backtesting Python trading strategies with historical market data.

## Features

✅ **Strategy Management**
- Upload Python strategy files with automatic validation
- Support for class-based and function-based strategies
- Secure file storage and database persistence

✅ **Dataset Management**
- Upload CSV files with OHLCV data
- Fetch historical data from Yahoo Finance
- Automatic date range detection

✅ **Backtest Execution**
- Asynchronous backtest processing via Celery
- Real-time status tracking
- Comprehensive performance metrics (Sharpe, Sortino, Max Drawdown, Calmar)

✅ **Modern UI**
- React frontend with TailwindCSS
- Interactive charts with Recharts
- User-friendly interface for all operations

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Celery + Redis (async task queue)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Pandas, NumPy (data processing)
- vectorbt (backtesting engine)
- yfinance (market data)

**Frontend:**
- React 18 + Vite
- TailwindCSS (styling)
- Recharts (charts)
- Axios (API calls)

**Infrastructure:**
- Docker + Docker Compose
- Nginx (reverse proxy, production)

## Quick Start

### 1. Start Backend Services

```bash
# Copy environment file
cp .env.example .env

# Start all services (API, Worker, Redis, PostgreSQL)
docker compose up --build
```

Backend will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Start Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

## Strategy Format

Your Python strategy must contain **either**:

### Option 1: Class with Method
```python
class Strategy:
    def run(self, data):
        # Your trading logic
        return signals  # pandas Series with 1, -1, 0
```

### Option 2: Standalone Function
```python
def strategy(data):
    # Your trading logic
    return signals  # pandas Series with 1, -1, 0
```

**Accepted names:**
- Methods: `run()`, `execute()`, `backtest()`
- Functions: `strategy()`, `run_strategy()`, `backtest()`

See `STRATEGY_FORMAT.md` for detailed documentation and `example_strategies/` for examples.

## API Endpoints

### Strategies
- `POST /api/v1/strategies` - Upload strategy
- `GET /api/v1/strategies` - List strategies
- `GET /api/v1/strategies/{id}` - Get strategy details
- `DELETE /api/v1/strategies/{id}` - Delete strategy

### Datasets
- `POST /api/v1/datasets/upload` - Upload CSV
- `POST /api/v1/datasets/yfinance` - Fetch from Yahoo Finance
- `GET /api/v1/datasets` - List datasets
- `GET /api/v1/datasets/{id}` - Get dataset details
- `DELETE /api/v1/datasets/{id}` - Delete dataset

### Backtests
- `POST /api/v1/backtests` - Create backtest
- `GET /api/v1/backtests` - List backtests
- `GET /api/v1/backtests/{id}` - Get backtest results
- `DELETE /api/v1/backtests/{id}` - Delete backtest

## Project Structure

```
quantflow/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API routes
│   │   ├── core/              # Configuration
│   │   ├── db/                # Database models
│   │   └── tasks/             # Celery tasks
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/             # React pages
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── example_strategies/         # Example strategy files
├── docker-compose.yml
├── STRATEGY_FORMAT.md         # Strategy documentation
└── QUICK_START.md            # Quick reference
```

## Example Strategies

Check the `example_strategies/` folder for ready-to-use strategies:
- **SMA Crossover** - Moving average crossover
- **RSI Strategy** - RSI mean reversion
- **Bollinger Bands** - Bollinger Bands mean reversion
- **MACD Crossover** - MACD signal crossover
- **Momentum** - Momentum-based trading

## Development

### Backend Development

```bash
# Rebuild after code changes
docker compose up --build -d

# View logs
docker compose logs -f api
docker compose logs -f worker

# Run tests (coming soon)
docker compose exec api pytest
```

### Frontend Development

```bash
cd frontend
npm run dev  # Hot reload enabled
```

## Roadmap

### Current (MVP)
- ✅ Strategy upload and validation
- ✅ Dataset management (CSV + YFinance)
- ✅ Async backtest execution
- ✅ Performance metrics calculation
- ✅ Modern React UI

### Next Steps
- 🔲 Execute uploaded strategy code (currently runs buy-and-hold)
- 🔲 Sandboxed strategy execution (Docker-in-Docker)
- 🔲 User authentication (JWT)
- 🔲 WebSocket for real-time updates
- 🔲 Advanced charting (candlesticks, indicators)
- 🔲 Strategy optimization
- 🔲 Walk-forward analysis
- 🔲 Portfolio backtesting

## Documentation

- `STRATEGY_FORMAT.md` - Detailed strategy format guide
- `QUICK_START.md` - Quick reference for strategy format
- `frontend/README.md` - Frontend documentation
- API Docs: http://localhost:8000/docs (when running)

## License

MIT
