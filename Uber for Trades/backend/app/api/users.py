from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app import models
from app import schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserRead, status_code=201)
async def create_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
	user = models.User(email=payload.email, phone=payload.phone, role=payload.role)
	db.add(user)
	await db.commit()
	await db.refresh(user)
	return user


@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.User).where(models.User.id == user_id))
	user = res.scalar_one_or_none()
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user

