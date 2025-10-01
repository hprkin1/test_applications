"""
Demo endpoints for showcasing the platform
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.db.session import get_db
from app import models
from app.api.auth import get_current_user

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/dashboard", response_class=HTMLResponse)
async def demo_dashboard():
    """Demo dashboard showing platform overview"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SwiftTrade Demo Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2em; font-weight: bold; color: #2563eb; }
            .demo-section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .demo-button { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            .demo-button:hover { background: #1d4ed8; }
            .endpoint { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 5px 0; font-family: monospace; }
            .success { color: #059669; }
            .warning { color: #d97706; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 SwiftTrade Demo Dashboard</h1>
                <p>On-Demand Trades Marketplace - MVP Backend</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div>Demo Users</div>
                    <small>2 customers, 3 providers</small>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div>Active Jobs</div>
                    <small>2 completed, 1 in progress, 2 posted</small>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div>Online Providers</div>
                    <small>Plumbing, Electrical, General</small>
                </div>
                <div class="stat-card">
                    <div class="stat-number">$300</div>
                    <div>Total Processed</div>
                    <small>15% commission model</small>
                </div>
            </div>

            <div class="demo-section">
                <h2>🎯 Quick Demo Scenarios</h2>
                <p>Try these scenarios to see the platform in action:</p>
                
                <h3>1. Customer Experience</h3>
                <button class="demo-button" onclick="window.open('/demo/customer-flow', '_blank')">Customer Journey</button>
                <p>Experience posting a job, finding providers, and completing work</p>
                
                <h3>2. Provider Experience</h3>
                <button class="demo-button" onclick="window.open('/demo/provider-flow', '_blank')">Provider Journey</button>
                <p>See how providers discover jobs, accept work, and get paid</p>
                
                <h3>3. Real-time Chat</h3>
                <button class="demo-button" onclick="window.open('/chat-test?job_id=3&user_id=1', '_blank')">Test Chat</button>
                <p>Try the real-time messaging between customers and providers</p>
            </div>

            <div class="demo-section">
                <h2>📱 Demo Users</h2>
                <p>Use these pre-created accounts for testing:</p>
                <div class="endpoint">
                    <strong>Customers:</strong><br>
                    • John: +15550001001 (OTP: 123456)<br>
                    • Sarah: +15550001002 (OTP: 123456)
                </div>
                <div class="endpoint">
                    <strong>Providers:</strong><br>
                    • Mike (Plumber): +15550002001 (OTP: 123456)<br>
                    • Lisa (Electrician): +15550002002 (OTP: 123456)<br>
                    • David (Handyman): +15550002003 (OTP: 123456)
                </div>
            </div>

            <div class="demo-section">
                <h2>🔗 API Endpoints</h2>
                <p>Key endpoints for testing:</p>
                <div class="endpoint">GET /demo/stats - Platform statistics</div>
                <div class="endpoint">GET /demo/jobs - All demo jobs</div>
                <div class="endpoint">GET /demo/providers - Available providers</div>
                <div class="endpoint">GET /providers/discover?lat=40.7608&lng=-111.8910&max_km=15 - Find nearby providers</div>
                <div class="endpoint">GET /docs - Full API documentation</div>
            </div>

            <div class="demo-section">
                <h2>💡 Demo Features</h2>
                <ul>
                    <li><span class="success">✅</span> Phone/Email OTP authentication</li>
                    <li><span class="success">✅</span> Job posting and management</li>
                    <li><span class="success">✅</span> Provider discovery with location</li>
                    <li><span class="success">✅</span> Real-time WebSocket chat</li>
                    <li><span class="success">✅</span> Review and rating system</li>
                    <li><span class="success">✅</span> Payment processing (mock)</li>
                    <li><span class="success">✅</span> Commission calculation</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """


@router.get("/stats")
async def demo_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics for demo"""
    # Count users by role
    customer_count = await db.scalar(select(func.count(models.User.id)).where(models.User.role == "customer"))
    provider_count = await db.scalar(select(func.count(models.User.id)).where(models.User.role == "provider"))
    
    # Count jobs by status
    posted_jobs = await db.scalar(select(func.count(models.Job.id)).where(models.Job.status == "posted"))
    in_progress_jobs = await db.scalar(select(func.count(models.Job.id)).where(models.Job.status == "in_progress"))
    completed_jobs = await db.scalar(select(func.count(models.Job.id)).where(models.Job.status == "completed"))
    
    # Count online providers
    online_providers = await db.scalar(
        select(func.count(models.ProviderProfile.id)).where(models.ProviderProfile.is_online == True)
    )
    
    # Calculate total revenue
    total_revenue = await db.scalar(
        select(func.sum(models.Job.amount)).where(models.Job.status == "completed")
    ) or 0
    
    # Count reviews
    total_reviews = await db.scalar(select(func.count(models.Review.id)))
    
    return {
        "users": {
            "customers": customer_count,
            "providers": provider_count,
            "total": customer_count + provider_count
        },
        "jobs": {
            "posted": posted_jobs,
            "in_progress": in_progress_jobs,
            "completed": completed_jobs,
            "total": posted_jobs + in_progress_jobs + completed_jobs
        },
        "providers": {
            "online": online_providers,
            "total": provider_count
        },
        "revenue": {
            "total_processed": float(total_revenue),
            "commission_earned": float(total_revenue * 0.15),
            "provider_payouts": float(total_revenue * 0.85)
        },
        "reviews": {
            "total": total_reviews
        }
    }


@router.get("/jobs")
async def demo_jobs(db: AsyncSession = Depends(get_db)):
    """Get all demo jobs with details"""
    result = await db.execute(
        select(models.Job, models.User.email.label("customer_email"))
        .join(models.User, models.Job.customer_id == models.User.id)
        .order_by(models.Job.created_at.desc())
    )
    
    jobs = []
    for job, customer_email in result:
        jobs.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "category": job.category,
            "status": job.status,
            "amount": job.amount,
            "customer_email": customer_email,
            "provider_id": job.provider_id,
            "created_at": job.created_at,
            "updated_at": job.updated_at
        })
    
    return {"jobs": jobs}


@router.get("/providers")
async def demo_providers(db: AsyncSession = Depends(get_db)):
    """Get all demo providers with details"""
    result = await db.execute(
        select(
            models.ProviderProfile,
            models.User.email,
            models.ProviderLocation.lat,
            models.ProviderLocation.lng
        )
        .join(models.User, models.ProviderProfile.user_id == models.User.id)
        .outerjoin(models.ProviderLocation, models.ProviderProfile.id == models.ProviderLocation.provider_profile_id)
    )
    
    providers = []
    for profile, email, lat, lng in result:
        providers.append({
            "user_id": profile.user_id,
            "email": email,
            "trade": profile.trade,
            "bio": profile.bio,
            "years_experience": profile.years_experience,
            "is_verified": profile.is_verified,
            "is_online": profile.is_online,
            "work_radius_km": profile.work_radius_km,
            "location": {"lat": lat, "lng": lng} if lat and lng else None
        })
    
    return {"providers": providers}


@router.get("/customer-flow", response_class=HTMLResponse)
async def customer_flow_demo():
    """Interactive customer flow demo"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Flow Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; }
            .step { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .step-number { background: #2563eb; color: white; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px; }
            .demo-button { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            .demo-button:hover { background: #1d4ed8; }
            .endpoint { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 5px 0; font-family: monospace; }
            .response { background: #e7f3ff; padding: 10px; border-radius: 4px; margin: 10px 0; border-left: 4px solid #2563eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👤 Customer Journey Demo</h1>
            <p>Follow these steps to experience the customer side of SwiftTrade:</p>
            
            <div class="step">
                <h3><span class="step-number">1</span>Authenticate as Customer</h3>
                <p>Use John's account to log in:</p>
                <div class="endpoint">POST /auth/request-otp<br>Body: {"phone": "+15550001001"}</div>
                <div class="endpoint">POST /auth/verify-otp<br>Body: {"phone": "+15550001001", "otp_code": "123456"}</div>
                <button class="demo-button" onclick="authenticateCustomer()">Authenticate</button>
                <div id="auth-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">2</span>Post a New Job</h3>
                <p>Create a plumbing job:</p>
                <div class="endpoint">POST /jobs<br>Body: {"title": "Bathroom Sink Repair", "category": "Plumbing", "customer_id": 1}</div>
                <button class="demo-button" onclick="createJob()">Create Job</button>
                <div id="job-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">3</span>Find Available Providers</h3>
                <p>Discover nearby plumbers:</p>
                <div class="endpoint">GET /providers/discover?lat=40.7608&lng=-111.8910&max_km=15</div>
                <button class="demo-button" onclick="findProviders()">Find Providers</button>
                <div id="providers-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">4</span>Chat with Provider</h3>
                <p>Communicate in real-time:</p>
                <div class="endpoint">WebSocket: /ws/chat?job_id=3&user_id=1</div>
                <button class="demo-button" onclick="window.open('/chat-test?job_id=3&user_id=1', '_blank')">Open Chat</button>
            </div>

            <div class="step">
                <h3><span class="step-number">5</span>Complete and Review</h3>
                <p>Finish the job and leave a review:</p>
                <div class="endpoint">POST /reviews<br>Body: {"job_id": 3, "author_id": 1, "recipient_id": 3, "rating": 5, "comment": "Great work!"}</div>
                <button class="demo-button" onclick="leaveReview()">Leave Review</button>
                <div id="review-response" class="response" style="display:none;"></div>
            </div>
        </div>

        <script>
            let authToken = '';
            
            async function authenticateCustomer() {
                try {
                    const response = await fetch('/auth/request-otp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({phone: '+15550001001'})
                    });
                    const data = await response.json();
                    
                    const verifyResponse = await fetch('/auth/verify-otp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({phone: '+15550001001', otp_code: '123456'})
                    });
                    const verifyData = await verifyResponse.json();
                    authToken = verifyData.access_token;
                    
                    document.getElementById('auth-response').style.display = 'block';
                    document.getElementById('auth-response').innerHTML = '✅ Authenticated! Token: ' + authToken.substring(0, 20) + '...';
                } catch (error) {
                    document.getElementById('auth-response').style.display = 'block';
                    document.getElementById('auth-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function createJob() {
                try {
                    const response = await fetch('/jobs', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({
                            title: 'Bathroom Sink Repair',
                            category: 'Plumbing',
                            customer_id: 1
                        })
                    });
                    const data = await response.json();
                    
                    document.getElementById('job-response').style.display = 'block';
                    document.getElementById('job-response').innerHTML = '✅ Job created! ID: ' + data.id;
                } catch (error) {
                    document.getElementById('job-response').style.display = 'block';
                    document.getElementById('job-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function findProviders() {
                try {
                    const response = await fetch('/providers/discover?lat=40.7608&lng=-111.8910&max_km=15');
                    const data = await response.json();
                    
                    document.getElementById('providers-response').style.display = 'block';
                    document.getElementById('providers-response').innerHTML = '✅ Found ' + data.length + ' providers: ' + 
                        data.map(p => p.trade).join(', ');
                } catch (error) {
                    document.getElementById('providers-response').style.display = 'block';
                    document.getElementById('providers-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function leaveReview() {
                try {
                    const response = await fetch('/reviews', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({
                            job_id: 3,
                            author_id: 1,
                            recipient_id: 3,
                            rating: 5,
                            comment: 'Great work!'
                        })
                    });
                    const data = await response.json();
                    
                    document.getElementById('review-response').style.display = 'block';
                    document.getElementById('review-response').innerHTML = '✅ Review posted! ID: ' + data.id;
                } catch (error) {
                    document.getElementById('review-response').style.display = 'block';
                    document.getElementById('review-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """


@router.get("/provider-flow", response_class=HTMLResponse)
async def provider_flow_demo():
    """Interactive provider flow demo"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Provider Flow Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; }
            .step { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .step-number { background: #059669; color: white; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px; }
            .demo-button { background: #059669; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            .demo-button:hover { background: #047857; }
            .endpoint { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 5px 0; font-family: monospace; }
            .response { background: #ecfdf5; padding: 10px; border-radius: 4px; margin: 10px 0; border-left: 4px solid #059669; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Provider Journey Demo</h1>
            <p>Follow these steps to experience the provider side of SwiftTrade:</p>
            
            <div class="step">
                <h3><span class="step-number">1</span>Authenticate as Provider</h3>
                <p>Use Mike's plumber account:</p>
                <div class="endpoint">POST /auth/request-otp<br>Body: {"phone": "+15550002001"}</div>
                <div class="endpoint">POST /auth/verify-otp<br>Body: {"phone": "+15550002001", "otp_code": "123456"}</div>
                <button class="demo-button" onclick="authenticateProvider()">Authenticate</button>
                <div id="auth-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">2</span>Go Online</h3>
                <p>Set availability to receive jobs:</p>
                <div class="endpoint">PATCH /providers/3/profile<br>Body: {"is_online": true}</div>
                <button class="demo-button" onclick="goOnline()">Go Online</button>
                <div id="online-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">3</span>View Available Jobs</h3>
                <p>See posted jobs in your area:</p>
                <div class="endpoint">GET /jobs?status=posted</div>
                <button class="demo-button" onclick="viewJobs()">View Jobs</button>
                <div id="jobs-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">4</span>Accept a Job</h3>
                <p>Accept a plumbing job:</p>
                <div class="endpoint">POST /jobs/4/accept?provider_id=3</div>
                <button class="demo-button" onclick="acceptJob()">Accept Job</button>
                <div id="accept-response" class="response" style="display:none;"></div>
            </div>

            <div class="step">
                <h3><span class="step-number">5</span>Complete Job & Get Paid</h3>
                <p>Finish the work and process payment:</p>
                <div class="endpoint">POST /jobs/4/complete</div>
                <div class="endpoint">POST /payments/confirm-payment?payment_intent_id=pi_mock_4_1</div>
                <button class="demo-button" onclick="completeJob()">Complete Job</button>
                <div id="complete-response" class="response" style="display:none;"></div>
            </div>
        </div>

        <script>
            let authToken = '';
            
            async function authenticateProvider() {
                try {
                    const response = await fetch('/auth/request-otp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({phone: '+15550002001'})
                    });
                    
                    const verifyResponse = await fetch('/auth/verify-otp', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({phone: '+15550002001', otp_code: '123456'})
                    });
                    const verifyData = await verifyResponse.json();
                    authToken = verifyData.access_token;
                    
                    document.getElementById('auth-response').style.display = 'block';
                    document.getElementById('auth-response').innerHTML = '✅ Authenticated as Mike (Plumber)!';
                } catch (error) {
                    document.getElementById('auth-response').style.display = 'block';
                    document.getElementById('auth-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function goOnline() {
                try {
                    const response = await fetch('/providers/3/profile', {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({is_online: true})
                    });
                    
                    document.getElementById('online-response').style.display = 'block';
                    document.getElementById('online-response').innerHTML = '✅ Now online and available for jobs!';
                } catch (error) {
                    document.getElementById('online-response').style.display = 'block';
                    document.getElementById('online-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function viewJobs() {
                try {
                    const response = await fetch('/jobs?status=posted');
                    const data = await response.json();
                    
                    document.getElementById('jobs-response').style.display = 'block';
                    document.getElementById('jobs-response').innerHTML = '✅ Found ' + data.length + ' posted jobs: ' + 
                        data.map(j => j.title).join(', ');
                } catch (error) {
                    document.getElementById('jobs-response').style.display = 'block';
                    document.getElementById('jobs-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function acceptJob() {
                try {
                    const response = await fetch('/jobs/4/accept?provider_id=3', {method: 'POST'});
                    const data = await response.json();
                    
                    document.getElementById('accept-response').style.display = 'block';
                    document.getElementById('accept-response').innerHTML = '✅ Job accepted! Status: ' + data.status;
                } catch (error) {
                    document.getElementById('accept-response').style.display = 'block';
                    document.getElementById('accept-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            async function completeJob() {
                try {
                    await fetch('/jobs/4/complete', {method: 'POST'});
                    const response = await fetch('/payments/confirm-payment?payment_intent_id=pi_mock_4_1', {method: 'POST'});
                    const data = await response.json();
                    
                    document.getElementById('complete-response').style.display = 'block';
                    document.getElementById('complete-response').innerHTML = '✅ Job completed! Provider payout: $' + data.provider_payout;
                } catch (error) {
                    document.getElementById('complete-response').style.display = 'block';
                    document.getElementById('complete-response').innerHTML = '❌ Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """

