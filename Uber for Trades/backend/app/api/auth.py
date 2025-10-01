import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_db
from app import models
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# In-memory storage for OTP codes (in production, use Redis)
otp_storage = {}

# Demo OTP codes for easy testing
DEMO_OTP_CODES = {
    "+15550001001": "123456",  # John (customer)
    "+15550001002": "123456",  # Sarah (customer) 
    "+15550002001": "123456",  # Mike (plumber)
    "+15550002002": "123456",  # Lisa (electrician)
    "+15550002003": "123456",  # David (handyman)
}


class OTPRequest(BaseModel):
	phone: Optional[str] = None
	email: Optional[str] = None


class OTPVerify(BaseModel):
	phone: Optional[str] = None
	email: Optional[str] = None
	otp_code: str


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
	user_id: int


@router.post("/request-otp")
async def request_otp(payload: OTPRequest, db: AsyncSession = Depends(get_db)):
	"""Request OTP for phone or email verification"""
	if not payload.phone and not payload.email:
		raise HTTPException(status_code=400, detail="Phone or email required")
	
	# Use demo OTP for known numbers, otherwise generate random
	key = payload.phone or payload.email
	otp_code = DEMO_OTP_CODES.get(key, f"{secrets.randbelow(900000) + 100000:06d}")
	
	# Store OTP with expiration (5 minutes)
	otp_storage[key] = {
		"code": otp_code,
		"expires_at": datetime.utcnow() + timedelta(minutes=5),
		"attempts": 0
	}
	
	# In production, send via SMS/email service
	print(f"OTP for {key}: {otp_code}")
	
	return {"message": "OTP sent", "otp_code": otp_code}  # Remove otp_code in production


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(payload: OTPVerify, db: AsyncSession = Depends(get_db)):
	"""Verify OTP and return JWT token"""
	if not payload.phone and not payload.email:
		raise HTTPException(status_code=400, detail="Phone or email required")
	
	key = payload.phone or payload.email
	
	# Check if OTP exists and is valid
	if key not in otp_storage:
		raise HTTPException(status_code=400, detail="OTP not found or expired")
	
	otp_data = otp_storage[key]
	
	# Check expiration
	if datetime.utcnow() > otp_data["expires_at"]:
		del otp_storage[key]
		raise HTTPException(status_code=400, detail="OTP expired")
	
	# Check attempts
	if otp_data["attempts"] >= 3:
		del otp_storage[key]
		raise HTTPException(status_code=400, detail="Too many attempts")
	
	# Verify code
	if otp_data["code"] != payload.otp_code:
		otp_data["attempts"] += 1
		raise HTTPException(status_code=400, detail="Invalid OTP")
	
	# OTP verified - find or create user
	user = None
	if payload.phone:
		res = await db.execute(select(models.User).where(models.User.phone == payload.phone))
		user = res.scalar_one_or_none()
	elif payload.email:
		res = await db.execute(select(models.User).where(models.User.email == payload.email))
		user = res.scalar_one_or_none()
	
	if not user:
		# Create new user (role will be set during profile creation)
		user = models.User(
			phone=payload.phone,
			email=payload.email,
			role="customer"  # Default role
		)
		db.add(user)
		await db.commit()
		await db.refresh(user)
	
	# Clean up OTP
	del otp_storage[key]
	
	# Generate JWT token (simplified)
	import jwt
	token = jwt.encode(
		{"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=30)},
		settings.jwt_secret,
		algorithm=settings.jwt_algorithm
	)
	
	return TokenResponse(access_token=token, user_id=user.id)


@router.post("/create-provider-profile")
async def create_provider_profile(
	user_id: int,
	trade: str,
	bio: Optional[str] = None,
	years_experience: Optional[int] = None,
	db: AsyncSession = Depends(get_db)
):
	"""Create provider profile for authenticated user"""
	# Check if user exists and update role
	res = await db.execute(select(models.User).where(models.User.id == user_id))
	user = res.scalar_one_or_none()
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	
	# Update user role to provider
	user.role = "provider"
	
	# Create provider profile
	profile = models.ProviderProfile(
		user_id=user_id,
		trade=trade,
		bio=bio,
		years_experience=years_experience,
		is_verified=False,  # Requires admin verification
		work_radius_km=5.0,
		is_online=False
	)
	db.add(profile)
	await db.commit()
	await db.refresh(profile)
	
	return {"message": "Provider profile created", "profile_id": profile.id}


async def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(security),
	db: AsyncSession = Depends(get_db)
) -> models.User:
	"""Get current authenticated user from JWT token"""
	try:
		import jwt
		payload = jwt.decode(
			credentials.credentials,
			settings.jwt_secret,
			algorithms=[settings.jwt_algorithm]
		)
		user_id = payload.get("user_id")
		if not user_id:
			raise HTTPException(status_code=401, detail="Invalid token")
		
		res = await db.execute(select(models.User).where(models.User.id == user_id))
		user = res.scalar_one_or_none()
		if not user:
			raise HTTPException(status_code=401, detail="User not found")
		
		return user
	except jwt.PyJWTError:
		raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me")
async def get_me(current_user: models.User = Depends(get_current_user)):
	"""Get current user profile"""
	return {
		"id": current_user.id,
		"email": current_user.email,
		"phone": current_user.phone,
		"role": current_user.role,
		"created_at": current_user.created_at
	}
