from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.db.session import get_db
from app import models
from app import schemas

router = APIRouter(prefix="/providers", tags=["providers"])


@router.patch("/{user_id}/profile", response_model=schemas.ProviderProfileRead)
async def update_provider_profile(user_id: int, payload: schemas.ProviderProfileUpdate, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.ProviderProfile).where(models.ProviderProfile.user_id == user_id))
	profile = res.scalar_one_or_none()
	if not profile:
		raise HTTPException(status_code=404, detail="Provider profile not found")
	if payload.is_online is not None:
		profile.is_online = payload.is_online
	if payload.work_radius_km is not None:
		profile.work_radius_km = payload.work_radius_km
	if payload.trade is not None:
		profile.trade = payload.trade
	if payload.bio is not None:
		profile.bio = payload.bio
	if payload.years_experience is not None:
		profile.years_experience = payload.years_experience
	await db.commit()
	await db.refresh(profile)
	return profile


@router.put("/{user_id}/location", response_model=schemas.ProviderLocationRead)
async def upsert_provider_location(user_id: int, payload: schemas.ProviderLocationUpsert, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.ProviderProfile).where(models.ProviderProfile.user_id == user_id))
	profile = res.scalar_one_or_none()
	if not profile:
		raise HTTPException(status_code=404, detail="Provider profile not found")
	# upsert location
	res_loc = await db.execute(select(models.ProviderLocation).where(models.ProviderLocation.provider_profile_id == profile.id))
	loc = res_loc.scalar_one_or_none()
	if loc is None:
		loc = models.ProviderLocation(provider_profile_id=profile.id, lat=payload.lat, lng=payload.lng)
		db.add(loc)
	else:
		loc.lat = payload.lat
		loc.lng = payload.lng
	await db.commit()
	await db.refresh(loc)
	return loc


@router.get("/discover", response_model=List[schemas.NearbyProvider])
async def discover_providers(
	lat: float = Query(...),
	lng: float = Query(...),
	max_km: float = Query(10.0),
	db: AsyncSession = Depends(get_db),
):
	# Compute distance in a subquery, then filter in outer WHERE
	sql = text(
		"""
		SELECT * FROM (
			SELECT
				pp.user_id AS provider_user_id,
				pp.id AS provider_profile_id,
				pp.trade,
				pp.is_online,
				pp.work_radius_km,
				pl.lat,
				pl.lng,
				(
					2 * 6371 * ASIN(
						SQRT(
							POWER(SIN(RADIANS(:lat - pl.lat) / 2), 2) +
							COS(RADIANS(:lat)) * COS(RADIANS(pl.lat)) * POWER(SIN(RADIANS(:lng - pl.lng) / 2), 2)
						)
					)
				) AS distance_km
			FROM provider_profiles pp
			JOIN provider_locations pl ON pl.provider_profile_id = pp.id
			WHERE pp.is_online = TRUE
		) AS s
		WHERE s.distance_km <= LEAST(s.work_radius_km, :max_km)
		ORDER BY s.distance_km ASC
		LIMIT 100
		"""
	)
	res = await db.execute(sql.bindparams(lat=lat, lng=lng, max_km=max_km))
	rows = res.mappings().all()
	return [
		schemas.NearbyProvider(
			provider_user_id=row["provider_user_id"],
			provider_profile_id=row["provider_profile_id"],
			trade=row["trade"],
			is_online=row["is_online"],
			work_radius_km=row["work_radius_km"],
			lat=row["lat"],
			lng=row["lng"],
			distance_km=float(row["distance_km"]),
		)
		for row in rows
	]
