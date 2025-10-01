"""
Seed data for demo purposes
"""
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app import models


async def seed_demo_data():
    """Create realistic demo data for showcasing the platform"""
    async with AsyncSessionLocal() as db:
        # Check if data already exists
        result = await db.execute(select(models.User))
        if result.scalar_one_or_none():
            print("Demo data already exists, skipping seed...")
            return

        print("Creating demo data...")

        # Create demo users
        users_data = [
            {
                "email": "john.homeowner@example.com",
                "phone": "+15550001001",
                "role": "customer",
                "created_at": datetime.utcnow() - timedelta(days=30)
            },
            {
                "email": "sarah.homeowner@example.com", 
                "phone": "+15550001002",
                "role": "customer",
                "created_at": datetime.utcnow() - timedelta(days=25)
            },
            {
                "email": "mike.plumber@example.com",
                "phone": "+15550002001", 
                "role": "provider",
                "created_at": datetime.utcnow() - timedelta(days=45)
            },
            {
                "email": "lisa.electrician@example.com",
                "phone": "+15550002002",
                "role": "provider", 
                "created_at": datetime.utcnow() - timedelta(days=40)
            },
            {
                "email": "david.handyman@example.com",
                "phone": "+15550002003",
                "role": "provider",
                "created_at": datetime.utcnow() - timedelta(days=35)
            }
        ]

        users = []
        for user_data in users_data:
            user = models.User(**user_data)
            db.add(user)
            users.append(user)

        await db.commit()
        await db.refresh_all(users)

        # Create provider profiles
        provider_profiles_data = [
            {
                "user_id": users[2].id,  # Mike the plumber
                "trade": "Plumbing",
                "bio": "Licensed plumber with 15 years experience. Specializing in emergency repairs, leak fixes, and pipe installations.",
                "years_experience": 15,
                "is_verified": True,
                "work_radius_km": 25,
                "is_online": True,
                "created_at": datetime.utcnow() - timedelta(days=45)
            },
            {
                "user_id": users[3].id,  # Lisa the electrician
                "trade": "Electrical", 
                "bio": "Master electrician with 12 years experience. Available for electrical repairs, installations, and safety inspections.",
                "years_experience": 12,
                "is_verified": True,
                "work_radius_km": 30,
                "is_online": True,
                "created_at": datetime.utcnow() - timedelta(days=40)
            },
            {
                "user_id": users[4].id,  # David the handyman
                "trade": "General",
                "bio": "Versatile handyman with 8 years experience. Can handle plumbing, electrical, carpentry, and general home repairs.",
                "years_experience": 8,
                "is_verified": True,
                "work_radius_km": 20,
                "is_online": False,  # Currently offline
                "created_at": datetime.utcnow() - timedelta(days=35)
            }
        ]

        provider_profiles = []
        for profile_data in provider_profiles_data:
            profile = models.ProviderProfile(**profile_data)
            db.add(profile)
            provider_profiles.append(profile)

        await db.commit()
        await db.refresh_all(provider_profiles)

        # Create provider locations (Salt Lake City area)
        locations_data = [
            {
                "provider_profile_id": provider_profiles[0].id,  # Mike
                "lat": 40.7608,
                "lng": -111.8910,
                "updated_at": datetime.utcnow() - timedelta(minutes=15)
            },
            {
                "provider_profile_id": provider_profiles[1].id,  # Lisa
                "lat": 40.7505,
                "lng": -111.8750,
                "updated_at": datetime.utcnow() - timedelta(minutes=5)
            },
            {
                "provider_profile_id": provider_profiles[2].id,  # David
                "lat": 40.7850,
                "lng": -111.9000,
                "updated_at": datetime.utcnow() - timedelta(hours=2)
            }
        ]

        for location_data in locations_data:
            location = models.ProviderLocation(**location_data)
            db.add(location)

        await db.commit()

        # Create demo jobs
        jobs_data = [
            {
                "title": "Kitchen Sink Leak Repair",
                "description": "Kitchen sink has been dripping for 2 days. Water is pooling under the cabinet. Need urgent repair.",
                "category": "Plumbing",
                "status": "completed",
                "amount": 85.00,
                "location_lat": 40.7589,
                "location_lng": -111.8881,
                "customer_id": users[0].id,  # John
                "provider_id": users[2].id,  # Mike
                "created_at": datetime.utcnow() - timedelta(days=3),
                "updated_at": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Outdoor Outlet Installation",
                "description": "Need to install a GFCI outlet on the back patio for outdoor lighting and power tools.",
                "category": "Electrical",
                "status": "completed", 
                "amount": 120.00,
                "location_lat": 40.7620,
                "location_lng": -111.8950,
                "customer_id": users[1].id,  # Sarah
                "provider_id": users[3].id,  # Lisa
                "created_at": datetime.utcnow() - timedelta(days=5),
                "updated_at": datetime.utcnow() - timedelta(days=4)
            },
            {
                "title": "Bathroom Faucet Replacement",
                "description": "Old bathroom faucet is corroded and needs replacement. Also need to fix the shut-off valve.",
                "category": "Plumbing",
                "status": "in_progress",
                "amount": 95.00,
                "location_lat": 40.7550,
                "location_lng": -111.8800,
                "customer_id": users[0].id,  # John
                "provider_id": users[2].id,  # Mike
                "created_at": datetime.utcnow() - timedelta(hours=2),
                "updated_at": datetime.utcnow() - timedelta(minutes=30)
            },
            {
                "title": "Ceiling Fan Installation",
                "description": "Need to install a new ceiling fan in the master bedroom. Electrical box is already in place.",
                "category": "Electrical",
                "status": "posted",
                "location_lat": 40.7700,
                "location_lng": -111.9100,
                "customer_id": users[1].id,  # Sarah
                "created_at": datetime.utcnow() - timedelta(minutes=45)
            },
            {
                "title": "Door Handle Repair",
                "description": "Front door handle is loose and won't latch properly. Need someone to fix or replace it.",
                "category": "General",
                "status": "posted",
                "location_lat": 40.7450,
                "location_lng": -111.8700,
                "customer_id": users[0].id,  # John
                "created_at": datetime.utcnow() - timedelta(minutes=20)
            }
        ]

        jobs = []
        for job_data in jobs_data:
            job = models.Job(**job_data)
            db.add(job)
            jobs.append(job)

        await db.commit()
        await db.refresh_all(jobs)

        # Create reviews for completed jobs
        reviews_data = [
            {
                "job_id": jobs[0].id,  # Kitchen sink repair
                "author_id": users[0].id,  # John
                "recipient_id": users[2].id,  # Mike
                "rating": 5,
                "comment": "Mike was fantastic! Arrived within 30 minutes and fixed the leak quickly. Very professional and clean work.",
                "created_at": datetime.utcnow() - timedelta(days=2)
            },
            {
                "job_id": jobs[1].id,  # Outdoor outlet
                "author_id": users[1].id,  # Sarah
                "recipient_id": users[3].id,  # Lisa
                "rating": 5,
                "comment": "Lisa did an excellent job installing the outdoor outlet. Very knowledgeable and explained everything clearly.",
                "created_at": datetime.utcnow() - timedelta(days=4)
            }
        ]

        for review_data in reviews_data:
            review = models.Review(**review_data)
            db.add(review)

        await db.commit()

        # Create some chat messages for the in-progress job
        chat_messages_data = [
            {
                "sender_id": users[0].id,  # John
                "recipient_id": users[2].id,  # Mike
                "job_id": jobs[2].id,  # Bathroom faucet
                "message_body": "Hi Mike, thanks for accepting the job. When can you come by?",
                "created_at": datetime.utcnow() - timedelta(hours=2, minutes=10)
            },
            {
                "sender_id": users[2].id,  # Mike
                "recipient_id": users[0].id,  # John
                "job_id": jobs[2].id,
                "message_body": "Hi John! I can be there in about 30 minutes. I'll bring a new faucet and the tools needed.",
                "created_at": datetime.utcnow() - timedelta(hours=2, minutes=5)
            },
            {
                "sender_id": users[0].id,  # John
                "recipient_id": users[2].id,  # Mike
                "job_id": jobs[2].id,
                "message_body": "Perfect! I'll be home. The bathroom is on the second floor.",
                "created_at": datetime.utcnow() - timedelta(hours=1, minutes=45)
            },
            {
                "sender_id": users[2].id,  # Mike
                "recipient_id": users[0].id,  # John
                "job_id": jobs[2].id,
                "message_body": "I'm here! Just parked out front. Starting the work now.",
                "created_at": datetime.utcnow() - timedelta(minutes=30)
            }
        ]

        for message_data in chat_messages_data:
            message = models.ChatMessage(**message_data)
            db.add(message)

        await db.commit()

        print("✅ Demo data created successfully!")
        print(f"   - {len(users)} users (2 customers, 3 providers)")
        print(f"   - {len(provider_profiles)} provider profiles")
        print(f"   - {len(jobs)} jobs (2 completed, 1 in progress, 2 posted)")
        print(f"   - {len(reviews_data)} reviews")
        print(f"   - {len(chat_messages_data)} chat messages")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())

