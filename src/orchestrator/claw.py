import asyncio
from typing import List, Dict, Any
from src.worker.code_instance import CodeInstance
from src.memory.ledger import MemoryLedger
from src.events import emit_event

class ClawOrchestrator:
    def __init__(self):
        self.memory = MemoryLedger(filename="claw_memory.json")
        self.memory.clear()
        self.workers: List[CodeInstance] = []

    async def _emit_claw(self, log: str):
        print(f"[Claw] {log}")
        await emit_event("claw_update", {"log": log})

    def decompose_task(self, objective: str) -> List[Dict[str, str]]:
        return [
            {"id": "setup_env", "desc": "Set up the local environment and dependencies."},
            {"id": "build_ui", "desc": "Create the basic web UI dashboard scaffolding."},
            {"id": "configure_ssh", "desc": "Set up SSH keys for the local target."},
            {"id": "setup_service", "desc": "Create and configure the systemd service."}
        ]

    async def execute_plan(self, objective: str):
        await emit_event("objective_start", {"objective": objective})
        await self._emit_claw(f"Received new objective: '{objective}'")
        self.memory.add_note("Claw", f"Started new objective: {objective}", tags=["objective"])
        await emit_event("memory_update", {"memory": self.memory.memory})

        await self._emit_claw("Decomposing objective into sub-tasks...")
        sub_tasks = self.decompose_task(objective)
        await emit_event("task_tree", {"tasks": sub_tasks})

        await self._emit_claw("Initializing parallel Code instances...")
        self.workers = [CodeInstance(task["id"], task["desc"], self.memory) for task in sub_tasks]

        shared_context = self.memory.get_context()
        
        await self._emit_claw("Awaiting autonomous resolution from workers...")
        tasks = [worker.execute(shared_context) for worker in self.workers]
        results = await asyncio.gather(*tasks)

        await self._emit_claw("Synthesizing results and performing high-level verification...")
        all_success = all(res["status"] == "success" for res in results)

        if all_success:
            await self._emit_claw("Verification passed. All sub-tasks succeeded.")
            self.memory.add_note("Claw", "Objective completed successfully.", tags=["success"])
        else:
            await self._emit_claw("Verification failed. Some workers did not complete their tasks.")
            self.memory.add_note("Claw", "Objective failed during synthesis.", tags=["error"])
        
        await emit_event("memory_update", {"memory": self.memory.memory})

        self.generate_report(objective, results)
        await emit_event("orchestration_complete", {"status": "success" if all_success else "failed"})

    def generate_report(self, objective: str, results: List[Dict[str, Any]]):
        report = f"# Post-Execution Report\n\n**Objective:** {objective}\n\n## Sub-Task Results\n"
        for res in results:
            status = "✅" if res["status"] == "success" else "❌"
            report += f"* {status} {res['task_id']}: {res['output']}\n"
        report += "\n## Memory Ledger (Notes for Self)\n"
        report += self.memory.get_context()

        with open("final_report.md", "w") as f:
            f.write(report)
        asyncio.create_task(self._emit_claw("Wrote final execution report to final_report.md. Hand-off to Human Architect complete."))
