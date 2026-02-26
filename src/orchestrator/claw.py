import asyncio
from typing import List, Dict, Any
from src.worker.code_instance import CodeInstance
from src.memory.ledger import MemoryLedger
from src.events import emit_event
from src.orchestrator.router import TriageRouter

from src.worker.reviewer_instance import ReviewerInstance

class ClawOrchestrator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.memory = MemoryLedger(filename="claw_memory.json")
        self.memory.clear()
        self.workers: List[CodeInstance] = []
        self.router = TriageRouter()
        self.results: List[Dict[str, Any]] = []

    async def _emit_claw(self, log: str):
        print(f"[Claw] {log}")
        await emit_event("claw_update", {"log": log})

    def decompose_task(self, objective: str) -> List[Dict[str, Any]]:
        """Decomposes tasks with pub/sub event configuration."""
        return [
            {"id": "setup_env", "desc": "Set up the local environment and dependencies.", "triggers_on": "objective:started", "emits": ["env:ready"]},
            {"id": "build_ui", "desc": "Create the basic web UI dashboard scaffolding.", "triggers_on": "objective:started", "emits": ["ui:ready"]},
            {"id": "configure_ssh", "desc": "Set up SSH keys for the local target.", "triggers_on": "env:ready", "emits": ["ssh:ready"]},
            {"id": "setup_service", "desc": "Create and configure the systemd service.", "triggers_on": "ssh:ready", "emits": ["service:ready"]}
        ]

    async def execute_plan(self, objective: str):
        await emit_event("objective_start", {"objective": objective})
        await self._emit_claw(f"Received new objective: '{objective}'")
        self.memory.add_note("Claw", f"Started new objective: {objective}", tags=["objective"])
        await emit_event("memory_update", {"memory": self.memory.memory})

        await self._emit_claw("Decomposing objective into pub/sub task graph...")
        sub_tasks = self.decompose_task(objective)
        await emit_event("task_tree", {"tasks": sub_tasks})

        await self._emit_claw("Initializing TriageRouter and subscribing parallel Code instances...")
        
        for task in sub_tasks:
            # 1. Create the code instance (Worker)
            # It will now emit a 'completed' event for the Reviewer instead of the final target.
            worker = CodeInstance(
                task_id=task["id"], 
                description=task["desc"], 
                memory_store=self.memory, 
                router=self.router, 
                emits=[f"task:completed:{task['id']}"], 
                api_key=self.api_key
            )
            self.workers.append(worker)

            # 2. Create the Reviewer instance (Quality Gate)
            # It will emit the final target 'emits' upon approval.
            reviewer = ReviewerInstance(
                task_id=task["id"],
                memory_store=self.memory,
                router=self.router,
                approved_emits=task["emits"]
            )

            # Handler factories using default argument closure pattern
            async def worker_handler_factory(w: CodeInstance, p: dict):
                await self._emit_claw(f"Trigger received, dispatching worker {w.task_id}...")
                result = await w.execute(p)
                self.results.append(result)

            async def reviewer_handler_factory(r: ReviewerInstance, p: dict):
                await self._emit_claw(f"Review gate triggered for {r.task_id}, dispatching reviewer...")
                await r.execute(p)

            # Subscriptions
            self.router.subscribe(
                task["triggers_on"], 
                lambda payload, w=worker: worker_handler_factory(w, payload)
            )
            self.router.subscribe(
                f"task:rejected:{task['id']}",
                lambda payload, w=worker: worker_handler_factory(w, payload)
            )
            self.router.subscribe(
                f"task:completed:{task['id']}",
                lambda payload, r=reviewer: reviewer_handler_factory(r, payload)
            )

        self.router.start()
        
        await self._emit_claw("Awaiting autonomous resolution driven by event triggers...")
        # Kick off the event stream
        await self.router.publish("objective:started", {"objective": objective})

        # Wait for all events to be processed and all handlers to finish
        await self.router.stop()

        await self._emit_claw("Synthesizing results and performing high-level verification...")
        
        # Collect final statuses for each sub-task ID
        final_statuses = {}
        for res in self.results:
            final_statuses[res["task_id"]] = res["status"]

        all_success = len(final_statuses) == len(sub_tasks) and all(s == "success" for s in final_statuses.values())

        if all_success:
            await self._emit_claw("Verification passed. All sub-tasks succeeded.")
            self.memory.add_note("Claw", "Objective completed successfully.", tags=["success"])
        else:
            await self._emit_claw("Verification failed or stuck. Some workers did not complete their tasks.")
            self.memory.add_note("Claw", "Objective failed during synthesis.", tags=["error"], importance=5)
        
        await emit_event("memory_update", {"memory": self.memory.memory})

        self.generate_report(objective, self.results)
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
