from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
	Boolean,
	DateTime,
	Float,
	ForeignKey,
	Integer,
	String,
	Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
	phone: Mapped[Optional[str]] = mapped_column(String(32), unique=True, nullable=True, index=True)
	role: Mapped[str] = mapped_column(String(32), nullable=False)  # "customer" | "provider"
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	provider_profile: Mapped[Optional["ProviderProfile"]] = relationship(back_populates="user", uselist=False)

	jobs_as_customer: Mapped[list["Job"]] = relationship(back_populates="customer", foreign_keys="Job.customer_id")
	jobs_as_provider: Mapped[list["Job"]] = relationship(back_populates="provider", foreign_keys="Job.provider_id")


class ProviderProfile(Base):
	__tablename__ = "provider_profiles"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
	trade: Mapped[str] = mapped_column(String(64), nullable=False)
	bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	work_radius_km: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
	is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	years_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	user: Mapped["User"] = relationship(back_populates="provider_profile")
	location: Mapped[Optional["ProviderLocation"]] = relationship(back_populates="provider_profile", uselist=False, cascade="all, delete-orphan")


class ProviderLocation(Base):
	__tablename__ = "provider_locations"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	provider_profile_id: Mapped[int] = mapped_column(ForeignKey("provider_profiles.id", ondelete="CASCADE"), unique=True, index=True)
	lat: Mapped[float] = mapped_column(Float, nullable=False)
	lng: Mapped[float] = mapped_column(Float, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	provider_profile: Mapped["ProviderProfile"] = relationship(back_populates="location")


class Job(Base):
	__tablename__ = "jobs"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	title: Mapped[str] = mapped_column(String(120), nullable=False)
	description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	category: Mapped[str] = mapped_column(String(64), nullable=False)
	status: Mapped[str] = mapped_column(String(32), default="posted", nullable=False)  # posted/accepted/in_progress/completed/cancelled/paid
	amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Job payment amount
	location_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
	location_lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
	customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
	provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	customer: Mapped["User"] = relationship(back_populates="jobs_as_customer", foreign_keys=[customer_id])
	provider: Mapped[Optional["User"]] = relationship(back_populates="jobs_as_provider", foreign_keys=[provider_id])
	media: Mapped[list["JobMedia"]] = relationship(back_populates="job", cascade="all, delete-orphan")
	reviews: Mapped[list["Review"]] = relationship(back_populates="job", cascade="all, delete-orphan")
	messages: Mapped[list["ChatMessage"]] = relationship(back_populates="job", cascade="all, delete-orphan")


class JobMedia(Base):
	__tablename__ = "job_media"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
	media_url: Mapped[str] = mapped_column(String(2048), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	job: Mapped["Job"] = relationship(back_populates="media")


class Review(Base):
	__tablename__ = "reviews"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
	author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
	recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
	rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
	comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	job: Mapped["Job"] = relationship(back_populates="reviews")
	author: Mapped["User"] = relationship(foreign_keys=[author_id])
	recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id])


class ChatMessage(Base):
	__tablename__ = "chat_messages"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
	recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
	job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
	message_body: Mapped[str] = mapped_column(Text, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	sender: Mapped["User"] = relationship(foreign_keys=[sender_id])
	recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id])
	job: Mapped["Job"] = relationship(back_populates="messages")
