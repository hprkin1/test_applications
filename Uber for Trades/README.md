# SwiftTrade - On-Demand Trades Marketplace (MVP)

An "Uber for trades" backend API that connects customers needing urgent home repairs with immediately available, vetted trade service providers.

## Features

✅ **Complete MVP Backend:**
- User authentication with phone/email OTP
- Customer and provider profiles
- Job posting, assignment, and status management
- Real-time WebSocket chat between job participants
- Provider availability and location-based discovery
- Review system with ratings
- Payment processing with 15% commission
- PostgreSQL with PostGIS for geospatial queries

## Quick Start

1. **Prerequisites:**
   - Docker Desktop
   - PowerShell (Windows) or Terminal (Mac/Linux)

2. **Start the application:**
   ```bash
   docker compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /auth/request-otp` - Request OTP for phone/email
- `POST /auth/verify-otp` - Verify OTP and get JWT token
- `POST /auth/create-provider-profile` - Create provider profile
- `GET /auth/me` - Get current user profile

### Jobs
- `POST /jobs` - Create new job
- `GET /jobs/{id}` - Get job details
- `GET /jobs` - List jobs (with filters)
- `POST /jobs/{id}/accept` - Provider accepts job
- `POST /jobs/{id}/start` - Start job
- `POST /jobs/{id}/complete` - Complete job
- `POST /jobs/{id}/cancel` - Cancel job

### Providers
- `PATCH /providers/{user_id}/profile` - Update provider profile
- `PUT /providers/{user_id}/location` - Update provider location
- `GET /providers/discover` - Find nearby available providers

### Chat
- `WebSocket /ws/chat` - Real-time messaging
- `GET /chat/{job_id}` - Get chat history
- `POST /chat/message` - Send message (HTTP fallback)

### Reviews
- `POST /reviews` - Create review
- `GET /reviews` - List reviews for user
- `GET /reviews/summary/{user_id}` - Get rating summary

### Payments
- `POST /payments/create-payment-intent` - Create payment
- `POST /payments/confirm-payment` - Confirm payment
- `GET /payments/provider-balance/{id}` - Get provider balance
- `POST /payments/request-payout` - Request payout
- `GET /payments/commission-structure` - Get commission info

## 🎯 Demo Mode

The backend comes pre-loaded with realistic demo data and easy-to-use demo interfaces:

### Demo Dashboard
Visit: **http://localhost:8000/demo/dashboard**

### Demo Users (All use OTP: `123456`)
- **John (Customer)**: +15550001001
- **Sarah (Customer)**: +15550001002  
- **Mike (Plumber)**: +15550002001
- **Lisa (Electrician)**: +15550002002
- **David (Handyman)**: +15550002003

### Interactive Demos
- **Customer Journey**: http://localhost:8000/demo/customer-flow
- **Provider Journey**: http://localhost:8000/demo/provider-flow
- **Real-time Chat**: http://localhost:8000/chat-test?job_id=3&user_id=1

### Demo Data Includes
- 5 users (2 customers, 3 providers)
- 5 jobs (2 completed, 1 in progress, 2 posted)
- 2 reviews and ratings
- 4 chat messages
- Provider locations in Salt Lake City area

## Quick Testing

### 1. Authenticate (Demo OTP: 123456)
```bash
# Request OTP
curl -X POST "http://localhost:8000/auth/request-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone":"+15550001001"}'

# Verify OTP
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone":"+15550001001","otp_code":"123456"}'
```

### 2. Find Nearby Providers
```bash
curl "http://localhost:8000/providers/discover?lat=40.7608&lng=-111.8910&max_km=15"
```

### 3. View Demo Stats
```bash
curl "http://localhost:8000/demo/stats"
```

## Architecture

- **Backend:** FastAPI (Python 3.11)
- **Database:** PostgreSQL with PostGIS
- **Real-time:** WebSockets
- **Authentication:** JWT tokens
- **Payments:** Stripe Connect (stubbed)
- **Deployment:** Docker containers

## Environment Variables

Create `.env` file:
```env
ENV=dev
POSTGRES_DB=swifttrade
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/swifttrade
JWT_SECRET=change-me
JWT_ALG=HS256
```

## Development

- Code lives in `backend/app/`
- Database auto-creates tables on startup
- Live reload disabled for stability
- All endpoints documented at `/docs`

## Production Notes

- Replace OTP stubs with real SMS/email services
- Implement actual Stripe Connect integration
- Add database migrations (Alembic)
- Enable proper logging and monitoring
- Add rate limiting and security headers
