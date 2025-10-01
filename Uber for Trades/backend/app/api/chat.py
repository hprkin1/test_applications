from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, AsyncSessionLocal
from app import models, schemas

router = APIRouter(prefix="", tags=["chat"])


class ConnectionManager:
	def __init__(self) -> None:
		self.job_id_to_connections: Dict[int, Set[WebSocket]] = {}

	async def connect(self, job_id: int, websocket: WebSocket) -> None:
		await websocket.accept()
		self.job_id_to_connections.setdefault(job_id, set()).add(websocket)

	def disconnect(self, job_id: int, websocket: WebSocket) -> None:
		conns = self.job_id_to_connections.get(job_id)
		if conns and websocket in conns:
			conns.remove(websocket)
			if not conns:
				self.job_id_to_connections.pop(job_id, None)

	async def broadcast(self, job_id: int, message: dict) -> None:
		for ws in list(self.job_id_to_connections.get(job_id, set())):
			try:
				await ws.send_json(message)
			except RuntimeError:
				# connection likely closed
				self.disconnect(job_id, ws)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket, job_id: int, user_id: int):
	# Keep a DB session open for the connection lifetime
	async with AsyncSessionLocal() as db:
		try:
			# Validate job and participant
			res = await db.execute(select(models.Job).where(models.Job.id == job_id))
			job = res.scalar_one_or_none()
			if job is None or job.provider_id is None:
				print(f"WebSocket: Job {job_id} not found or not assigned")
				await websocket.close(code=1008)
				return
			if user_id not in (job.customer_id, job.provider_id):
				print(f"WebSocket: User {user_id} not part of job {job_id}")
				await websocket.close(code=1008)
				return

			customer_id = job.customer_id
			provider_id = job.provider_id
			print(f"WebSocket: User {user_id} connected to job {job_id}")

			await manager.connect(job_id, websocket)
			try:
				await manager.broadcast(job_id, {"system": True, "event": "joined", "user_id": user_id})
				while True:
					data = await websocket.receive_json()
					print(f"WebSocket: Received data: {data}")
					text = data.get("message")
					if not text:
						print("WebSocket: No message text")
						continue
					recipient_id = provider_id if user_id == customer_id else customer_id
					msg = models.ChatMessage(
						sender_id=user_id,
						recipient_id=recipient_id,
						job_id=job_id,
						message_body=text,
					)
					db.add(msg)
					await db.commit()
					await db.refresh(msg)
					print(f"WebSocket: Saved message from {user_id} to {recipient_id}")
					await manager.broadcast(job_id, {
						"system": False,
						"job_id": job_id,
						"sender_id": user_id,
						"recipient_id": recipient_id,
						"message_body": text,
						"created_at": msg.created_at.isoformat(),
					})
					print(f"WebSocket: Broadcasted message to job {job_id}")
			except WebSocketDisconnect:
				print(f"WebSocket: User {user_id} disconnected from job {job_id}")
			except Exception as e:
				print(f"WebSocket: Error in message loop: {e}")
			finally:
				manager.disconnect(job_id, websocket)
				try:
					await manager.broadcast(job_id, {"system": True, "event": "left", "user_id": user_id})
				except Exception:
					pass
		except Exception as e:
			print(f"WebSocket: Error in connection setup: {e}")
			await websocket.close(code=1011)


@router.get("/chat/{job_id}", response_model=list[schemas.ChatMessageRead])
async def get_chat_history(job_id: int, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.ChatMessage).where(models.ChatMessage.job_id == job_id).order_by(models.ChatMessage.created_at.asc()))
	return res.scalars().all()


@router.post("/chat/message", response_model=schemas.ChatMessageRead)
async def send_chat_message(job_id: int, sender_id: int, message: str, db: AsyncSession = Depends(get_db)):
	res = await db.execute(select(models.Job).where(models.Job.id == job_id))
	job = res.scalar_one_or_none()
	if job is None or job.provider_id is None:
		raise HTTPException(status_code=404, detail="Job not found or not assigned")
	if sender_id not in (job.customer_id, job.provider_id):
		raise HTTPException(status_code=403, detail="Sender not part of the job")
	recipient_id = job.provider_id if sender_id == job.customer_id else job.customer_id
	msg = models.ChatMessage(
		sender_id=sender_id,
		recipient_id=recipient_id,
		job_id=job_id,
		message_body=message,
	)
	db.add(msg)
	await db.commit()
	await db.refresh(msg)
	# best-effort broadcast if sockets connected
	await manager.broadcast(job_id, {
		"system": False,
		"job_id": job_id,
		"sender_id": sender_id,
		"recipient_id": recipient_id,
		"message_body": message,
		"created_at": msg.created_at.isoformat(),
	})
	return msg


@router.get("/chat-test", response_class=HTMLResponse)
async def chat_test(job_id: int, user_id: int):
	# Minimal client for local testing
	return f"""
	<!doctype html>
	<html>
	<head><meta charset="utf-8"><title>Chat Test</title></head>
	<body>
	<h3>Chat Test - Job {job_id}, User {user_id}</h3>
	<div id="log" style="white-space:pre-wrap;border:1px solid #ccc;padding:8px;height:240px;overflow:auto;"></div>
	<input id="msg" placeholder="type message..." style="width:80%" />
	<button id="send">Send</button>
	<script>
	  const jobId = {job_id};
	  const userId = {user_id};
	  const log = (m) => {{ 
	    const d = document.getElementById('log'); 
	    d.textContent += new Date().toLocaleTimeString() + ': ' + m + "\\n"; 
	    d.scrollTop = d.scrollHeight; 
	  }};
	  log('Starting chat test...');
	  log('Job ID: ' + jobId + ', User ID: ' + userId);
	  const wsUrl = `ws://${{location.host}}/ws/chat?job_id=${{jobId}}&user_id=${{userId}}`;
	  log('WebSocket URL: ' + wsUrl);
	  const ws = new WebSocket(wsUrl);
	  ws.onopen = () => log('✅ WebSocket connected!');
	  ws.onmessage = (ev) => log('📨 Received: ' + ev.data);
	  ws.onclose = (ev) => log('❌ WebSocket closed: ' + ev.code + ' - ' + ev.reason);
	  ws.onerror = (ev) => log('🚨 WebSocket error: ' + ev);
	  document.getElementById('send').onclick = () => {{
	    const v = document.getElementById('msg').value; 
	    if(!v) return;
	    log('📤 Sending: ' + v);
	    try {{ 
	      ws.send(JSON.stringify({{message: v}})); 
	      log('✅ Message sent successfully');
	    }} catch (e) {{ 
	      log('❌ Send error: ' + e); 
	    }}
	    document.getElementById('msg').value='';
	  }};
	  // Test connection immediately
	  setTimeout(() => {{
	    if (ws.readyState === WebSocket.CONNECTING) {{
	      log('⏳ Still connecting...');
	    }} else if (ws.readyState === WebSocket.OPEN) {{
	      log('✅ Connection is open');
	    }} else {{
	      log('❌ Connection failed, state: ' + ws.readyState);
	    }}
	  }}, 1000);
	</script>
	</body>
	</html>
	"""
