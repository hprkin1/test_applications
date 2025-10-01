from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app import models
from app import schemas

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=schemas.ReviewRead, status_code=201)
async def create_review(payload: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
	# Validate job exists and is completed or cancelled
	res_job = await db.execute(select(models.Job).where(models.Job.id == payload.job_id))
	job = res_job.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.status not in ("completed", "cancelled"):
		raise HTTPException(status_code=400, detail="Can only review completed or cancelled jobs")
	# Validate participants
	if payload.author_id not in (job.customer_id, job.provider_id):
		raise HTTPException(status_code=400, detail="Author not part of the job")
	if payload.recipient_id not in (job.customer_id, job.provider_id) or payload.recipient_id == payload.author_id:
		raise HTTPException(status_code=400, detail="Invalid recipient")
	if not (1 <= payload.rating <= 5):
		raise HTTPException(status_code=400, detail="Rating must be 1-5")
	review = models.Review(
		job_id=payload.job_id,
		author_id=payload.author_id,
		recipient_id=payload.recipient_id,
		rating=payload.rating,
		comment=payload.comment,
	)
	db.add(review)
	await db.commit()
	await db.refresh(review)
	return review


@router.get("", response_model=List[schemas.ReviewRead])
async def list_reviews(recipient_id: int = Query(...), db: AsyncSession = Depends(get_db)):
	res = await db.execute(
		select(models.Review).where(models.Review.recipient_id == recipient_id).order_by(models.Review.created_at.desc())
	)
	return res.scalars().all()


@router.get("/summary/{user_id}")
async def rating_summary(user_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(
		select(func.count(models.Review.id), func.avg(models.Review.rating)).where(models.Review.recipient_id == user_id)
	)
	count, avg_rating = res.one()
	return {"recipient_id": user_id, "count": int(count), "average_rating": float(avg_rating) if avg_rating is not None else None}

