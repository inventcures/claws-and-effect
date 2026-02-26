from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
import json
from pydantic import BaseModel
from src.orchestrator.claw import ClawOrchestrator
from src.events import bus

app = FastAPI(title="Claws & Code Perceptive UI")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ObjectiveRequest(BaseModel):
    objective: str

@app.get("/")
async def get_index():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await bus.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        bus.disconnect(websocket)

@app.post("/api/orchestrate")
async def start_orchestration(req: ObjectiveRequest, x_byok_config: str = Header(None)):
    if not x_byok_config:
        raise HTTPException(status_code=401, detail="X-BYOK-Config header required")

    try:
        byok_config = json.loads(x_byok_config)
        if not isinstance(byok_config, list) or len(byok_config) == 0:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid BYOK configuration")

    # Pass the entire config down for fallback support
    claw = ClawOrchestrator(byok_config=byok_config)
    # Fire and forget the orchestration
    asyncio.create_task(claw.execute_plan(req.objective))
    return {"status": "started", "objective": req.objective}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
