from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_db
from app import models
from app.api.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

# Commission rate (15% as specified in requirements)
COMMISSION_RATE = Decimal("0.15")


class PaymentIntentCreate(BaseModel):
	job_id: int
	amount: Decimal  # Total amount customer will pay


class PaymentIntentResponse(BaseModel):
	payment_intent_id: str
	client_secret: str
	amount: Decimal
	commission: Decimal
	provider_payout: Decimal


class PayoutRequest(BaseModel):
	provider_id: int
	amount: Decimal


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
	payload: PaymentIntentCreate,
	current_user: models.User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db)
):
	"""Create Stripe payment intent for a job"""
	# Verify job exists and belongs to current user
	res = await db.execute(select(models.Job).where(models.Job.id == payload.job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.customer_id != current_user.id:
		raise HTTPException(status_code=403, detail="Not authorized for this job")
	if job.status != "completed":
		raise HTTPException(status_code=400, detail="Job must be completed before payment")
	
	# Calculate commission and payout
	commission = payload.amount * COMMISSION_RATE
	provider_payout = payload.amount - commission
	
	# In production, create actual Stripe PaymentIntent
	# For now, return mock data
	payment_intent_id = f"pi_mock_{payload.job_id}_{current_user.id}"
	client_secret = f"pi_mock_{payload.job_id}_{current_user.id}_secret"
	
	return PaymentIntentResponse(
		payment_intent_id=payment_intent_id,
		client_secret=client_secret,
		amount=payload.amount,
		commission=commission,
		provider_payout=provider_payout
	)


@router.post("/confirm-payment")
async def confirm_payment(
	payment_intent_id: str,
	current_user: models.User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db)
):
	"""Confirm payment and trigger provider payout"""
	# In production, verify payment with Stripe
	# For now, simulate successful payment
	
	# Extract job_id from mock payment_intent_id
	try:
		job_id = int(payment_intent_id.split("_")[2])
	except (IndexError, ValueError):
		raise HTTPException(status_code=400, detail="Invalid payment intent")
	
	# Verify job
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job or job.customer_id != current_user.id:
		raise HTTPException(status_code=404, detail="Job not found")
	
	# Get the payment amount from the payment intent (in production, from Stripe)
	# For now, we'll use a default amount since we don't store it in the payment intent
	payment_amount = Decimal("100.00")  # This should come from the actual payment intent
	
	# Update job status and amount
	job.status = "paid"
	job.amount = float(payment_amount)
	await db.commit()
	
	# In production, trigger Stripe Connect payout to provider
	# For now, just log the payout
	provider_payout = payment_amount * (1 - COMMISSION_RATE)
	print(f"Payout to provider {job.provider_id}: ${provider_payout}")
	
	return {
		"message": "Payment confirmed",
		"job_id": job_id,
		"status": "paid",
		"commission": float(payment_amount * COMMISSION_RATE),
		"provider_payout": float(provider_payout)
	}


@router.get("/provider-balance/{provider_id}")
async def get_provider_balance(
	provider_id: int,
	current_user: models.User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db)
):
	"""Get provider's current balance and payout history"""
	# Verify provider exists and user has access
	if current_user.role != "provider" and current_user.id != provider_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	
	# Calculate balance from completed paid jobs
	res = await db.execute(
		select(models.Job)
		.where(models.Job.provider_id == provider_id)
		.where(models.Job.status == "paid")
	)
	paid_jobs = res.scalars().all()
	
	total_earnings = sum(job.amount for job in paid_jobs)
	total_commission = sum(job.amount * COMMISSION_RATE for job in paid_jobs)
	available_balance = total_earnings - total_commission
	
	return {
		"provider_id": provider_id,
		"total_earnings": total_earnings,
		"total_commission": total_commission,
		"available_balance": available_balance,
		"paid_jobs_count": len(paid_jobs)
	}


@router.post("/request-payout")
async def request_payout(
	payload: PayoutRequest,
	current_user: models.User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db)
):
	"""Request payout to provider's bank account"""
	if current_user.role != "provider" or current_user.id != payload.provider_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	
	# In production, create Stripe Connect payout
	# For now, simulate payout request
	payout_id = f"po_mock_{payload.provider_id}_{current_user.id}"
	
	return {
		"message": "Payout requested",
		"payout_id": payout_id,
		"amount": payload.amount,
		"status": "pending",
		"estimated_arrival": "2-3 business days"
	}


@router.get("/commission-structure")
async def get_commission_structure():
	"""Get current commission structure"""
	return {
		"commission_rate": float(COMMISSION_RATE),
		"commission_percentage": f"{COMMISSION_RATE * 100}%",
		"description": "15% commission deducted from job payment before provider payout"
	}
