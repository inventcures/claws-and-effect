import asyncio
from typing import Dict, Any
from src.memory.ledger import MemoryLedger
from src.events import emit_event

class CodeInstance:
    def __init__(self, task_id: str, description: str, memory_store: MemoryLedger):
        self.task_id = task_id
        self.description = description
        self.memory = memory_store
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

    async def execute(self, shared_context: str) -> Dict[str, Any]:
        await self._emit("Initializing", f"Initializing task: {self.description}", 0)
        
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
                return {"task_id": self.task_id, "status": "success", "output": "Sub-task executed."}
            else:
                await self._emit("Failed", "Verification failed. Retrying...", attempt)
                self.memory.add_note(
                    agent_id=f"Worker-{self.task_id}",
                    note=f"Failed attempt {attempt} due to verification error.",
                    tags=["error", self.task_id]
                )
                await emit_event("memory_update", {"memory": self.memory.memory})

        await self._emit("Failed", "Max retries exceeded.", self.max_retries)
        return {"task_id": self.task_id, "status": "failed", "output": "Max retries exceeded."}
