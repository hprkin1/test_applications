from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


# User
class UserBase(BaseModel):
	email: Optional[EmailStr] = None
	phone: Optional[str] = Field(default=None, max_length=32)
	role: str


class UserCreate(UserBase):
	pass


class UserRead(UserBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True


# ProviderProfile
class ProviderProfileBase(BaseModel):
	trade: str
	bio: Optional[str] = None
	is_verified: bool = False
	work_radius_km: float = 5.0
	is_online: bool = False
	years_experience: Optional[int] = None


class ProviderProfileCreate(ProviderProfileBase):
	user_id: int


class ProviderProfileUpdate(BaseModel):
	is_online: Optional[bool] = None
	work_radius_km: Optional[float] = None
	trade: Optional[str] = None
	bio: Optional[str] = None
	years_experience: Optional[int] = None


class ProviderProfileRead(ProviderProfileBase):
	id: int
	user_id: int
	created_at: datetime

	class Config:
		from_attributes = True


# ProviderLocation
class ProviderLocationUpsert(BaseModel):
	lat: float
	lng: float


class ProviderLocationRead(ProviderLocationUpsert):
	updated_at: datetime

	class Config:
		from_attributes = True


# Job
class JobBase(BaseModel):
	title: str
	description: Optional[str] = None
	category: str
	status: str = "posted"
	location_lat: Optional[float] = None
	location_lng: Optional[float] = None
	customer_id: int
	provider_id: Optional[int] = None


class JobCreate(JobBase):
	pass


class JobRead(JobBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True


# JobMedia
class JobMediaBase(BaseModel):
	job_id: int
	media_url: str


class JobMediaCreate(JobMediaBase):
	pass


class JobMediaRead(JobMediaBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True


# Review
class ReviewBase(BaseModel):
	job_id: int
	author_id: int
	recipient_id: int
	rating: int
	comment: Optional[str] = None


class ReviewCreate(ReviewBase):
	pass


class ReviewRead(ReviewBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True


# ChatMessage
class ChatMessageBase(BaseModel):
	sender_id: int
	recipient_id: int
	job_id: int
	message_body: str


class ChatMessageCreate(ChatMessageBase):
	pass


class ChatMessageRead(ChatMessageBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True


# Discovery
class NearbyProvider(BaseModel):
	provider_user_id: int
	provider_profile_id: int
	trade: str
	is_online: bool
	work_radius_km: float
	distance_km: float
	lat: float
	lng: float
