import asyncio
from typing import Dict, Any, List
from src.memory.ledger import MemoryLedger
from src.events import emit_event

class ReviewerInstance:
    def __init__(self, task_id: str, memory_store: MemoryLedger, router=None, approved_emits: List[str] = None):
        self.task_id = task_id
        self.memory = memory_store
        self.router = router
        self.approved_emits = approved_emits or []

    async def _emit(self, status: str, log: str):
        print(f"[Reviewer-{self.task_id}] {log}")
        await emit_event("worker_update", {
            "task_id": f"Reviewer-{self.task_id}",
            "description": f"Adversarial review for: {self.task_id}",
            "status": status,
            "log": log,
            "loop": "1/1"
        })

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        await self._emit("Reviewing", f"Critically analyzing outputs for task {self.task_id}...")
        await asyncio.sleep(2) # Simulate deep analysis time
        
        # In a real scenario, this would use a higher-tier LLM to evaluate the worker's work.
        # We mock an approval for the protocol flow.
        approved = True 
        
        if approved:
            await self._emit("Success", f"Review passed for {self.task_id}. Emitting downstream events.")
            self.memory.add_note(
                agent_id=f"Reviewer-{self.task_id}",
                note=f"QUALITY GATE PASSED: {self.task_id} successfully passed adversarial review.",
                tags=["success", "review", self.task_id],
                importance=3
            )
            await emit_event("memory_update", {"memory": self.memory.memory})

            if self.router:
                for event in self.approved_emits:
                    await self.router.publish(event, {"task_id": self.task_id, "status": "approved"})
            
            return {"task_id": self.task_id, "status": "approved"}
        else:
            await self._emit("Failed", f"Review failed for {self.task_id}. Sending back to worker.")
            self.memory.add_note(
                agent_id=f"Reviewer-{self.task_id}",
                note=f"QUALITY GATE REJECTED: {self.task_id} failed review. Requesting revision.",
                tags=["error", "review", self.task_id],
                importance=4
            )
            if self.router:
                await self.router.publish(f"task:rejected:{self.task_id}", {"task_id": self.task_id})
            
            return {"task_id": self.task_id, "status": "rejected"}
