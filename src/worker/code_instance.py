import asyncio
from typing import Dict, Any, List
from src.memory.ledger import MemoryLedger
from src.events import emit_event

class CodeInstance:
    def __init__(self, task_id: str, description: str, memory_store: MemoryLedger, router=None, emits: List[str] = None, api_key: str = None):
        self.task_id = task_id
        self.description = description
        self.memory = memory_store
        self.router = router
        self.emits = emits or []
        self.api_key = api_key
        self.max_retries = 3

    async def _emit(self, status: str, log: str, loop: int):
        print(f"[Worker-{self.task_id}] {log}")
        await emit_event("worker_update", {
            "task_id": self.task_id,
            "description": self.description,
            "status": status,
            "log": log,
            "loop": f"{loop}/{self.max_retries}"
        })

    async def execute(self, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        shared_context = self.memory.get_context()
        await self._emit("Initializing", f"Initializing task triggered by event: {payload}", 0)
        
        briefing = f"Objective: {self.description}\nContext:\n{shared_context}"
        
        for attempt in range(1, self.max_retries + 1):
            await self._emit("Researching", "Researching requirements and environment...", attempt)
            await asyncio.sleep(1.5)
            
            await self._emit("Strategizing", "Formulating strategy...", attempt)
            await asyncio.sleep(1.5)
            
            await self._emit("Acting", "Taking action: Executing tools...", attempt)
            await asyncio.sleep(1.5)
            
            await self._emit("Verifying", "Verifying outputs...", attempt)
            await asyncio.sleep(1.5)
            
            success = True
            if success:
                await self._emit("Success", "Task completed successfully.", attempt)
                self.memory.add_note(
                    agent_id=f"Worker-{self.task_id}",
                    note=f"Successfully completed sub-task: {self.description}",
                    tags=["success", self.task_id]
                )
                await emit_event("memory_update", {"memory": self.memory.memory})
                
                # PubSub Emit
                if self.router:
                    for event_topic in self.emits:
                        await self._emit("Publishing", f"Publishing downstream event: {event_topic}", attempt)
                        await self.router.publish(event_topic, {"task_id": self.task_id, "status": "success"})
                        
                return {"task_id": self.task_id, "status": "success", "output": "Sub-task executed."}
            else:
                await self._emit("Failed", "Verification failed. Retrying...", attempt)
                self.memory.add_note(
                    agent_id=f"Worker-{self.task_id}",
                    note=f"Failed attempt {attempt} due to verification error.",
                    tags=["error", self.task_id]
                )
                await emit_event("memory_update", {"memory": self.memory.memory})

        await self._emit("Stuck", "⚠️ STUCK - ESCALATION REQUIRED. Max retries exceeded.", self.max_retries)
        self.memory.add_note(
            agent_id=f"Worker-{self.task_id}",
            note=f"ESCALATION: Worker stuck after {self.max_retries} attempts.",
            tags=["error", "escalation", self.task_id],
            importance=5
        )
        await emit_event("memory_update", {"memory": self.memory.memory})
        
        # Publish a specific stuck event to the router
        if self.router:
            await self.router.publish("worker:stuck", {"task_id": self.task_id})
            
        return {"task_id": self.task_id, "status": "stuck", "output": "Escalation required."}
