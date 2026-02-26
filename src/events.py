import asyncio
import json
from typing import Set

class EventBus:
    def __init__(self):
        self.clients: Set = set()
    
    async def connect(self, websocket):
        await websocket.accept()
        self.clients.add(websocket)
        
    def disconnect(self, websocket):
        self.clients.remove(websocket)
        
    async def broadcast(self, event_type: str, data: dict):
        if not self.clients:
            return
        message = json.dumps({"type": event_type, "data": data})
        for client in list(self.clients):
            try:
                await client.send_text(message)
            except Exception:
                self.disconnect(client)

bus = EventBus()

async def emit_event(event_type: str, data: dict):
    await bus.broadcast(event_type, data)
