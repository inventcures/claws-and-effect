from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
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
async def start_orchestration(req: ObjectiveRequest):
    claw = ClawOrchestrator()
    # Fire and forget the orchestration
    asyncio.create_task(claw.execute_plan(req.objective))
    return {"status": "started", "objective": req.objective}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
