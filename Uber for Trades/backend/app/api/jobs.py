from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app import models
from app import schemas

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=schemas.JobRead, status_code=201)
async def create_job(payload: schemas.JobCreate, db: AsyncSession = Depends(get_db)):
	job = models.Job(
		title=payload.title,
		description=payload.description,
		category=payload.category,
		status=payload.status,
		location_lat=payload.location_lat,
		location_lng=payload.location_lng,
		customer_id=payload.customer_id,
		provider_id=payload.provider_id,
	)
	db.add(job)
	await db.commit()
	await db.refresh(job)
	return job


@router.get("/{job_id}", response_model=schemas.JobRead)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	return job


@router.get("", response_model=List[schemas.JobRead])
async def list_jobs(
	customer_id: Optional[int] = Query(default=None),
	provider_id: Optional[int] = Query(default=None),
	status: Optional[str] = Query(default=None),
	db: AsyncSession = Depends(get_db),
):
	query = select(models.Job)
	if customer_id is not None:
		query = query.where(models.Job.customer_id == customer_id)
	if provider_id is not None:
		query = query.where(models.Job.provider_id == provider_id)
	if status is not None:
		query = query.where(models.Job.status == status)
	res = await db.execute(query.order_by(models.Job.created_at.desc()))
	return res.scalars().all()


@router.post("/{job_id}/accept", response_model=schemas.JobRead)
async def accept_job(job_id: int, provider_id: int = Query(...), db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.status not in ("posted",):
		raise HTTPException(status_code=400, detail="Job cannot be accepted in its current status")
	if job.provider_id is not None and job.provider_id != provider_id:
		raise HTTPException(status_code=409, detail="Job already assigned to another provider")
	job.provider_id = provider_id
	job.status = "accepted"
	await db.commit()
	await db.refresh(job)
	return job


@router.post("/{job_id}/start", response_model=schemas.JobRead)
async def start_job(job_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.status != "accepted":
		raise HTTPException(status_code=400, detail="Only accepted jobs can be started")
	job.status = "in_progress"
	await db.commit()
	await db.refresh(job)
	return job


@router.post("/{job_id}/complete", response_model=schemas.JobRead)
async def complete_job(job_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.status not in ("in_progress", "accepted"):
		raise HTTPException(status_code=400, detail="Only in-progress or accepted jobs can be completed")
	job.status = "completed"
	await db.commit()
	await db.refresh(job)
	return job


@router.post("/{job_id}/cancel", response_model=schemas.JobRead)
async def cancel_job(job_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	if job.status in ("completed", "cancelled"):
		raise HTTPException(status_code=400, detail="Job already finalized")
	job.status = "cancelled"
	await db.commit()
	await db.refresh(job)
	return job
